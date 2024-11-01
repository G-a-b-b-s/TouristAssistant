import os
import shutil
import instaloader

class InstaScrapper:
    def __init__(self, username):
        self.username = username
        self.L = instaloader.Instaloader()
        self.scrap_insta()
        self.manage_insta_data()

    def scrap_insta(self):
        try:
            # Download profile using the entered username
            print(f"Downloading profile data for {self.username}...")
            self.L.download_profile(self.username, profile_pic_only=False)
            print("Download completed!")
        except instaloader.exceptions.ProfileNotExistsException:
            print("Error: The profile does not exist.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"An error occurred: {e}")

    def manage_insta_data(self):
        dir_path = f"./{self.username}"
        os.makedirs("./dataScrappedFromSocialMedia/Text/", exist_ok=True)
        os.makedirs("./dataScrappedFromSocialMedia/Pictures/", exist_ok=True)
        try:
            text=""
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)

                if not (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".txt")):
                    os.remove(file_path)
                    continue

                if file.endswith(".txt"):
                    with open(file_path, "r", encoding='utf-8') as f:
                        text += f.read()
                        text+="\n"
                else:
                    shutil.move(file_path, f"./dataScrappedFromSocialMedia/Pictures/{file}")

            with open(f"./dataScrappedFromSocialMedia/Text/Instagram.txt", "w", encoding='utf-8') as f:
                f.write(text)
            shutil.rmtree(dir_path)

        except PermissionError:
            print("Error: You do not have permission to delete some files.")
        except Exception as e:
            print(f"An error occurred: {e}")


