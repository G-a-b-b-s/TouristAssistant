from playwright.async_api import async_playwright
import asyncio, random, json, logging, time, os, yt_dlp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DOWNLOAD_VIDEOS = True


async def random_sleep(min_seconds, max_seconds):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))


async def scroll_page(page):
    await page.evaluate("""
        window.scrollBy(0, window.innerHeight);
    """)
    await random_sleep(1, 2)


async def handle_captcha(page):
    try:
        # Check for the presence of the CAPTCHA dialog
        captcha_dialog = page.locator('div[role="dialog"]')
        is_captcha_present = await captcha_dialog.count() > 0 and await captcha_dialog.is_visible()

        if is_captcha_present:
            logging.info("CAPTCHA detected. Please solve it manually.")
            # Wait for the CAPTCHA to be solved
            await page.wait_for_selector('div[role="dialog"]', state='detached', timeout=300000)  # 5 minutes timeout
            logging.info("CAPTCHA solved. Resuming script...")
            await asyncio.sleep(0.5)  # Short delay after CAPTCHA is solved
    except Exception as e:
        logging.error(f"Error while handling CAPTCHA: {str(e)}")


async def hover_and_get_views(page, video_element):
    await video_element.hover()
    await random_sleep(0.5, 1)
    views = await video_element.evaluate("""
        (element) => {
            const viewElement = element.querySelector('strong[data-e2e="video-views"]');
            return viewElement ? viewElement.textContent.trim() : 'N/A';
        }
    """)
    return views


async def extract_video_info(page, video_url, views):
    await page.goto(video_url, wait_until="networkidle")
    await random_sleep(2, 4)
    await handle_captcha(page)

    video_info = await page.evaluate("""
        () => {
            const getTextContent = (selectors) => {
                for (let selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    for (let element of elements) {
                        const text = element.textContent.trim();
                        if (text) return text;
                    }
                }
                return 'N/A';
            };

            const getTags = () => {
                const tagElements = document.querySelectorAll('a[data-e2e="search-common-link"]');
                return Array.from(tagElements).map(el => el.textContent.trim());
            };

            return {
                likes: getTextContent(['[data-e2e="like-count"]', '[data-e2e="browse-like-count"]']),
                comments: getTextContent(['[data-e2e="comment-count"]', '[data-e2e="browse-comment-count"]']),
                shares: getTextContent(['[data-e2e="share-count"]']),
                bookmarks: getTextContent(['[data-e2e="undefined-count"]']),
                description: getTextContent(['span.css-j2a19r-SpanText']),
                musicTitle: getTextContent(['.css-pvx3oa-DivMusicText']),
                date: getTextContent(['span[data-e2e="browser-nickname"] span:last-child']),
                tags: getTags()
            };
        }
    """)

    video_info['views'] = views
    video_info['url'] = video_url

    logging.info(f"Extracted info for {video_url}: {video_info}")
    return video_info


def download_tiktok_video(video_url, save_path):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            logging.info(f"Video successfully downloaded: {filename}")
            return filename
    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}")
        return None


async def scrape_tiktok_profile(username, videos=[]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        )

        page = await context.new_page()

        url = f"https://www.tiktok.com/@{username}"
        await page.goto(url, wait_until="networkidle")
        await handle_captcha(page)

        if not videos:
            videos = []
            last_video_count = 0
            no_new_videos_count = 0
            start_time = time.time()
            timeout = 300  # 5 minutes timeout

            while True:
                await scroll_page(page)
                await handle_captcha(page)

                video_elements = await page.query_selector_all('div[data-e2e="user-post-item"]')

                for element in video_elements:
                    video_url = await element.evaluate('(el) => el.querySelector("a").href')
                    if any(video['url'] == video_url for video in videos):
                        continue

                    views = await hover_and_get_views(page, element)
                    videos.append({'url': video_url, 'views': views})

                logging.info(f"Found {len(videos)} unique videos so far")

                if len(videos) == last_video_count:
                    no_new_videos_count += 1
                else:
                    no_new_videos_count = 0

                last_video_count = len(videos)

                if no_new_videos_count >= 3 or time.time() - start_time > timeout:
                    break

        logging.info(f"Found a total of {len(videos)} videos")

        for i, video in enumerate(videos):
            if 'likes' not in video:
                video_info = await extract_video_info(page, video['url'], video['views'])
                videos[i].update(video_info)
                logging.info(f"Processed video {i + 1}/{len(videos)}: {video['url']}")

                if DOWNLOAD_VIDEOS:
                    save_path = os.path.join(os.getcwd(), username)
                    filename = download_tiktok_video(video['url'], save_path)
                    if filename:
                        videos[i]['local_filename'] = filename

                # Save progress every 10 videos
                if (i + 1) % 10 == 0:
                    with open(f"{username}_progress.json", "w") as f:
                        json.dump(videos, f, indent=2)
                    logging.info(f"Progress saved. Processed {i + 1}/{len(videos)} videos.")

                await random_sleep(3, 5)

        await browser.close()
        return videos


async def main():
    username = "fpl_insights"

    # Try to load progress
    try:
        with open(f"{username}_progress.json", "r") as f:
            videos = json.load(f)
        logging.info(
            f"Loaded progress. {len([v for v in videos if 'likes' in v])}/{len(videos)} videos already processed.")
    except FileNotFoundError:
        videos = []

    if DOWNLOAD_VIDEOS:
        os.makedirs(username, exist_ok=True)
        os.chdir(username)

    videos = await scrape_tiktok_profile(username, videos)

    logging.info(f"\nTotal videos scraped: {len(videos)}")

    # Save as JSON
    with open(f"{username}_playwright_video_stats.json", "w") as f:
        json.dump(videos, f, indent=2)
    print(f"Data saved to {username}_playwright_video_stats.json")

    logging.info(f"Data saved to {username}_playwright_video_stats.json")


if __name__ == "__main__":
    asyncio.run(main())