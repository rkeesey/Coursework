""" art.py module used to edit historical photos/artifacts
from an external API"""

import random
import logging
import requests
from simpleimage import SimpleImage

def get_inputs() -> tuple:
    """gets user inputs and returns them as a tuple"""
    #start = '1400'
    #end = '1800'
    #query = 'flower'
    while True:

        start = input("Start year: ")
        end = input("End year: ")
        query = input("Query: ")

        return (start, end, query)

def build_url(start_date: str, end_date: str, search_query: str) -> str:
    """builds url from user inputs to be used for the external API"""
    url = (f'https://collectionapi.metmuseum.org/public/collection/v1/search'
           f'?q={search_query}&hasImages=true&dateBegin={start_date}&dateEnd={end_date}'
           )
    return url

def get_result(url: str) -> list:
    """requests API search IDs based off of the user formatted url"""
    try:
        result = requests.get(url, timeout=5)
        data = result.json()
        object_ids = data.get("objectIDs", [])  # extracts list of IDs
    except requests.exceptions.Timeout:
        logging.error("The request timed out after 5 seconds.")
    return object_ids

def search_description(search_result: list, max_: int) -> str:
    """ get image urls that match the user specified data"""
    if not search_result:
        return []
    select = search_result[:max_]
    img_urls = []

    for img_id in select:
        img_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{img_id}"
        try:
            data = requests.get(img_url, timeout=5).json()
        except requests.exceptions.Timeout:
            logging.error("The request timed out after 5 seconds.")
        primary_image = data.get("primaryImage", "")
        if primary_image:                # Only add if image exists
            img_urls.append(primary_image)

    return img_urls

def get_images(img_list: list) -> None:
    """ get images from the saved urls from search_description """
    filenames = ["image1.jpg", "image2.jpg"]

    for i, url in enumerate(img_list):

        try:
            img = requests.get(url, timeout=5)
            img.raise_for_status()

            with open(filenames[i], 'wb') as f:
                f.write(img.content)

        except requests.exceptions.Timeout:
            logging.error("The request timed out after 5 seconds.")

        except requests.RequestException:
            print("Failed to download image.")

def get_transforms(file1: str, file2: str) -> list:
    """image manipulation function that uses the
    simpleimage module classes/methods"""
    img1 = SimpleImage.file(file1)
    img2 = SimpleImage.file(file2)

    img1 = img1.shrink(5)
    img2 = img2.shrink(5)

    grey1 = img1.grayscale()
    #grey1.show()

    sepia1 = img1.sepia()
    #sepia1.show()

    blur1 = img1.blur()
    #blur1.show()

    filter_r = img1.filter('red', 100)
    #filterR.show()
    filter_g = img1.filter('green', 100)
    #filterG.show()
    filter_b = img1.filter('blue', 100)
    #filterB.show()

    fliph = img1.flip(0)
    flipv = img1.flip(1)
    #fliph.show()
    #flipv.show()

    grsc1 = img1.greenscreen('red', 100, img2)
    grsc2 = img1.greenscreen('green', 100, img2)
    grsc3 = img1.greenscreen('blue', 100, img2)
    #grsc1.show()
    #grsc2.show()
    #grsc3.show()


    return [img1,grey1,sepia1,blur1,filter_r,filter_g,filter_b,fliph,flipv,grsc1,grsc2,grsc3]

def compose(img_list: list) -> SimpleImage:
    """composes images into a randomly ordered 5 by 5 collage"""
    rows = 5
    cols = 5

    img1 = img_list[0]
    w, h = img1.width, img1.height

    grid_w = w * cols
    grid_h = h * rows

    collage = SimpleImage.blank(grid_w, grid_h)

    for row in range(rows):
        for col in range(cols):
            tile = random.choice(img_list)
            for x in range(w):
                for y in range(h):
                    pixel = tile.get_pixel(x, y)
                    collage.set_pixel(col*w + x, row*h + y, pixel)

    collage.write("pop.jpg")
    return collage


def main():
    """ main function that facilitates the function of this module"""
    start, end, query = get_inputs()
    url = build_url(start, end, query)
    result = get_result(url)
    top = search_description(result, 2)
    get_images(top)

    images = get_transforms("image1.jpg", "image2.jpg")

    collage = compose(images)
    collage.show()

if __name__=='__main__':
    main()
