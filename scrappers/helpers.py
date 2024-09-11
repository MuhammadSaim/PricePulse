import os
import requests
from urllib.parse import urlparse

# get the base path of the app
def get_base_path() -> str:
    return os.path.abspath(os.path.dirname(__file__))

# download the image from the url
def download_image_from_url(url: str, dir: str):
    file_name = get_the_filename(url)

    # ignore the error if there is dir otherwise create for us
    os.makedirs(os.path.join(get_base_path(), 'images/'+dir), exist_ok=True)

    if not os.path.isfile(os.path.join(get_base_path(), 'images/'+dir, file_name)):
        response = requests.get(url)
        with open(os.path.join(get_base_path(), 'images/'+dir, file_name), 'wb') as file:
            file.write(response.content)

# get the fil_name from the url
def get_the_filename(path:  str) -> str:
    a = urlparse(path)
    return os.path.basename(a.path)