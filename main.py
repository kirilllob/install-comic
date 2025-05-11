import requests
import os
import telegram
import random
from dotenv import load_dotenv


def get_random_number():
    url_last = "https://xkcd.com/info.0.json"
    response_last = requests.get(url_last)
    response_last.raise_for_status()
    url_last_comic = response_last.json()["num"]
    random_number = random.randint(1,url_last_comic)
    return random_number


def get_comic(random_number):
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    url_image = response_json["img"]
    autor_comment = response_json["alt"]
    return url_image, autor_comment


def download_image(url, filename, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def publish_comic(autor_comment, token, chat_id):
    bot = telegram.Bot(token)
    with open("comic.png", "rb") as file:
        bot.send_photo(chat_id, photo=file, caption=autor_comment)


def main():
    load_dotenv()
    chat_id = os.environ["TG_CHAT_ID"]
    token = os.environ["TG_TOKEN"]    
    filename = "comic.png"
    try:
        random_number = get_random_number()
        url_comic,comment = get_comic(random_number)
        download_image(url_comic, filename)
        publish_comic(comment, chat_id, token)
    finally:   
        os.remove(filename)


if __name__ == '__main__':
    main()




