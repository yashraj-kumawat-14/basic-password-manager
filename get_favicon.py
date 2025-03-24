import requests

def get_favicon(site_name, save_as):
    # Construct the favicon URL
    favicon_url = f"https://www.google.com/s2/favicons?sz=64&domain={site_name}"

    # Fetch the favicon
    response = requests.get(favicon_url)

    if response.status_code == 200:
        save_path = f"./images/icons/{save_as}.png"
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Favicon saved as {save_path}")
        return save_path
    else:
        print("Failed to fetch favicon.")
        return None