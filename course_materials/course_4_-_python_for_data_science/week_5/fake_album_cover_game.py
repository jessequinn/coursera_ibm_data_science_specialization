from IPython.display import Image as IPythonImage
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from lxml.html import fromstring

'''Helper Function to superimpose text on image'''


def display_cover(top, bottom):
    name = 'album_art_raw.png'
    # Now let's make get an album cover.
    # https://picsum.photos/ is a free service that offers random images.
    # Let's get a random image:
    album_art_raw = requests.get('https://picsum.photos/500/500/?random')
    # and save it as 'album_art_raw.png'
    with open(name, 'wb') as album_art_raw_file:
        album_art_raw_file.write(album_art_raw.content)
    # Now that we have our raw image, let's open it
    # and write our band and album name on it
    img = Image.open("album_art_raw.png")
    draw = ImageDraw.Draw(img)

    # We'll choose a font for our band and album title,
    # run "% ls /usr/share/fonts/truetype/dejavu" in a cell to see what else is available,
    # or download your own .ttf fonts!
    band_name_font = ImageFont.truetype(
        "dejavu-sans/DejaVuSans-Bold.ttf", 25)  # 25pt font
    album_name_font = ImageFont.truetype(
        "dejavu-sans/DejaVuSans-Bold.ttf", 20)  # 20pt font

    # the x,y coordinates for where our album name and band name text will start
    # counted from the top left of the picture (in pixels)
    band_x, band_y = 50, 50
    album_x, album_y = 50, 400

    # Our text should be visible on any image. A good way
    # of accomplishing that is to use white text with a
    # black border. We'll use the technique shown here to draw the border:
    # https://mail.python.org/pipermail/image-sig/2009-May/005681.html
    outline_color = "black"

    draw.text((band_x-1, band_y-1), top,
              font=band_name_font, fill=outline_color)
    draw.text((band_x+1, band_y-1), top,
              font=band_name_font, fill=outline_color)
    draw.text((band_x-1, band_y+1), top,
              font=band_name_font, fill=outline_color)
    draw.text((band_x+1, band_y+1), top,
              font=band_name_font, fill=outline_color)

    draw.text((album_x-1, album_y-1), bottom,
              font=album_name_font, fill=outline_color)
    draw.text((album_x+1, album_y-1), bottom,
              font=album_name_font, fill=outline_color)
    draw.text((album_x-1, album_y+1), bottom,
              font=album_name_font, fill=outline_color)
    draw.text((album_x+1, album_y+1), bottom,
              font=album_name_font, fill=outline_color)

    draw.text((band_x, band_y), top, (255, 255, 255), font=band_name_font)
    draw.text((album_x, album_y), bottom,
              (255, 255, 255), font=album_name_font)

    return img


'''Wikipedia random select'''


def get_band_album_titles():
    wikipedia_link = 'https://en.wikipedia.org/wiki/Special:Random'

    raw_random_wikipedia_page = requests.get(wikipedia_link)

    tree = fromstring(raw_random_wikipedia_page.content)
    raw_title = tree.findtext('.//title')
    band_title = raw_title.split('-')
    raw_random_wikipedia_page = requests.get(wikipedia_link)

    tree = fromstring(raw_random_wikipedia_page.content)
    raw_title = tree.findtext('.//title')
    album_title = raw_title.split('-')

    return (band_title[0].rstrip() + '-' + album_title[0].rstrip())

# first part use data science and python as bottom and top
img = display_cover(top='Python', bottom='Data Science')
img.save('sample-out.png')

IPythonImage(filename='sample-out.png')

# second part capture two random titles and make them top and bottom text
band_title, album_title = get_band_album_titles().split('-')

album_cover = display_cover(top=band_title, bottom=album_title)
album_cover.save('album-cover.png')

IPythonImage(filename='album-cover.png')
