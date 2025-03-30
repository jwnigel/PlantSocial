import requests
from requests.exceptions import RequestException
from PIL import Image
from io import BytesIO


def get_inaturalist_image_urls(genus, species, num_results=10):
    endpoint = "https://api.inaturalist.org/v1/observations"
    params = {
        "taxon_name": f"{genus} {species}",
        "per_page": num_results,
        "photos": True,
        "quality_grade": "research",
        "license": "cc0",
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  

        print(f"Running utils/get_inaturalist_image.py for {genus} {species}.")
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")  # First 200 chars
        data = response.json()
        results = data.get("results", [])
        
        plant_images = results[0].get("photos", [])
        if plant_images:
            urls = []
            for image in plant_images:
                url_of_original_photo = image.get("url").replace("square", "original")
                urls.append(url_of_original_photo)

            print(f"Found {len(urls)} images for {genus} {species}")
            print(f"First image URL: {urls[0]}")
            print(f"Last image URL: {urls[-1]}")
            return urls

        else:
            print(f"No image found for {genus} {species}")
            return None

    except RequestException as e:
        print(f"Error fetching image for {genus} {species}: {str(e)}")
    except ValueError as e:
        print(f"Error parsing JSON for {genus} {species}: {str(e)}")
    return None


def display_images(urls, max_images=None):
    display_count = len(urls) if max_images is None else (min(max_images, len(urls)))
    for i, url in enumerate(urls[:display_count]):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.show()
            print(f"Displaying image {i+1} of {display_count}")
        except Exception as e:
            print(f"Error displaing image {i+1}: {e}")
