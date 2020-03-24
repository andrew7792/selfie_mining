from datetime import datetime
import pymysql.cursors
import os, sys, importlib

import requests
import json
from time import sleep
from config import db, app
from config import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD

import wget
import random

importlib.reload(sys)


def grab_posts(posts):
    for post in posts:
        post = post['node']

        if not post["is_video"]:
            likes, mediaid, url, comments, date, post_caption, user_id = post["edge_liked_by"]["count"], post["id"], \
                                                                         post["display_url"], \
                                                                         post["edge_media_to_comment"][
                                                                             "count"], datetime.fromtimestamp(
                post["taken_at_timestamp"]), '', post["owner"]["id"]

            if len(post["edge_media_to_caption"]["edges"]) != 0:
                post_caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]

            directory = "{}/{}".format(app.config['IMAGES_FOLDER'], date.strftime("%d-%b-%Y"))

            if not os.path.exists(directory):
                os.mkdir(directory)

            img_path = "{}/{}.jpg".format(directory, mediaid)
            wget.download(url, img_path)

            with connection.cursor() as cursor:
                print(mediaid, user_id, post["taken_at_timestamp"], likes, comments, post_caption, img_path)
                try:
                    sql = "INSERT INTO `posts_instagram` " \
                          "(`post_id`, `user_id`, `post_time`, `post_likes`, " \
                          "`post_comments`, `post_caption`, `post_image`, `parse_tag`) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                        mediaid, user_id, date, likes, comments, post_caption, img_path, parse_tag))
                except Exception as e:
                    print(e.__repr__())
                    print('adding empty post_caption')
                    sql = "INSERT INTO `posts_instagram` " \
                          "(`post_id`, `user_id`, `post_time`, `post_likes`, " \
                          "`post_comments`, `post_caption`, `post_image`, `parse_tag`) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql,
                                   (mediaid, user_id, date, likes, comments, '', img_path, parse_tag))

            connection.commit()


# max_id = 'QVFETU42dnJ3ZFVhaUI4SDVfM2UybTFnMDJKT2ljaERTOEp4M3hmV2NzTlU3UG5MTmJVd3lxNktmNy1qSGUtZ1NudW9KeDJZUGNGUUtNZ2JrdmI0eGJuSg=='
# max_id = 'QVFDTF84OVExcWVKcjAyZkVTbzJreWRWcjZRMVprQnZhY3hiVXNUM3c5cllzS3Ffc1laai1RUTBSNy0tYUNWeTdKRFdCLWpMekFRVUtvWFA4eEZfVVByVQ=='
max_id = 'QVFEM2N0WEJwQ3RLWmJpZ0xId1hvLWItcFJnUzFCOGZUdnJKQ3E3ZE9PUkJlbUF2QkliemUxN1Jxd3N4WmJ1eXpjOFFBTjNhdS1wekZWa2ZzWl95YW9YTA=='
parse_tag = 'selfietime'
base_url = "https://www.instagram.com/explore/tags/{}/?__a=1".format(parse_tag)

for i in range(0, 10000):
    if (i % 4) == 0:
        posts_sleep = random.randint(5, 10)
    elif (i % 9) == 0:
        posts_sleep = random.randint(10, 20)
    elif (i % 35) == 0:
        posts_sleep = random.randint(20, 35)
    elif (i % 50) == 0:
        posts_sleep = random.randint(35, 60)
    elif (i % 115) == 0:
        posts_sleep = random.randint(150, 300)
    elif (i % 285) == 0:
        posts_sleep = random.randint(400, 700)
    elif (i % 517) == 0:
        posts_sleep = random.randint(600, 1200)
    elif (i % 713) == 0:
        posts_sleep = random.randint(500, 800)
    else:
        posts_sleep = random.randint(2, 6)

    sleep(posts_sleep)  # Be polite.

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', ]

    url = base_url
    try:
        if max_id:
            url = base_url + f"&max_id={max_id}"

    except Exception as e:
        print(e.__repr__())
        posts = None

    print(f"Requesting {url}")
    # response = requests.get(url)
    response = requests.get(url, headers={'User-Agent': USER_AGENTS[0]})
    response = json.loads(response.text)

    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USERNAME,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)

    max_id = response['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    posts = response['graphql']['hashtag']['edge_hashtag_to_media']["edges"]

    print(f"New cursor is {max_id}")

    if i > 0:
        datetime_now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        with open('post_cursor.txt', 'a') as the_file:
            the_file.write(max_id + '\n' + str(i) + '\n' + datetime_now + '\n')

    try:
        grab_posts(posts)
    except BaseException as e:
        print(e.__repr__())
        connection.close()
        exit(1)

    connection.close()
