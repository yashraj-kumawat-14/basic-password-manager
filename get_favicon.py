"""
Utility to fetch and save the favicon of a website.
"""

import requests  # Library to make HTTP requests

def get_favicon(site_name, save_as):
    """
    Fetches the favicon of a website and saves it locally.

    Args:
        site_name (str): The domain name of the website (e.g., "example.com").
        save_as (str): The name to save the favicon file as (without extension).

    Returns:
        str: The path to the saved favicon file if successful, otherwise None.
    """
    # Construct the favicon URL using Google's favicon service
    favicon_url = f"https://www.google.com/s2/favicons?sz=64&domain={site_name}"

    # Fetch the favicon from the constructed URL
    response = requests.get(favicon_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the path to save the favicon
        save_path = f"./images/icons/{save_as}.png"
        
        # Save the favicon content to the specified file
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        return save_path  # Return the path to the saved favicon
    else:
        return None  # Return None if the favicon could not be fetched