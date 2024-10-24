import instaloader

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Ask user to input the Instagram username
username = input("Enter the Instagram username: ")

try:
    # Download profile using the entered username
    print(f"Downloading profile data for {username}...")
    L.download_profile(username, profile_pic_only=False)
    print("Download completed!")
except instaloader.exceptions.ProfileNotExistsException:
    print("Error: The profile does not exist.")
except instaloader.exceptions.InstaloaderException as e:
    print(f"An error occurred: {e}")
