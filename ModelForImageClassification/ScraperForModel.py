import requests
import os
import time


def download_pexels_images(api_key, query, num_images, directory):
    # Base URL for Pexels API
    url = "https://api.pexels.com/v1/search"

    # Set headers with the API key
    headers = {
        "Authorization": api_key
    }

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    images_downloaded = 0
    page = 1  # Start at the first page

    while images_downloaded < num_images:
        # Define parameters for the API request
        params = {
            "query": query,
            "per_page": min(num_images - images_downloaded, 80),  # Request up to 80 images per page
            "orientation": "landscape",
            "page": page
        }

        # Make the API request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('error', 'Failed to fetch images')}")
            return

        # Parse JSON response
        data = response.json()
        images = data.get('photos', [])

        # Break the loop if no more images are returned
        if not images:
            print("No more images available to fetch.")
            break

        # Download each image
        for image in images:
            image_url = image['src']['original']
            image_name = f"{query}_{images_downloaded + 1}.jpg"
            image_path = os.path.join(directory, image_name)

            # Download image
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {image_name}")

            images_downloaded += 1
            if images_downloaded >= num_images:
                break  # Exit the loop once the desired number of images is reached

        # Move to the next page
        page += 1
        time.sleep(2)  # Add delay to avoid rate-limiting

    print(f"Downloaded a total of {images_downloaded} images.")


# Parameters
api_key = "V7lUXgnoYsxalugWvIZGrmklokqncGwNP9WeQ7k7Cbgv7cr0HgHqQZsL"  # Replace with your actual Pexels API key
query = "sightseeing buildings"  # Search term for images
directory = "./data/NightLife"  # Destination directory

for query, num_images in [('festivals', 200), ('nightlife',200)]:
    # Run the function
    download_pexels_images(api_key, query, num_images, directory)
