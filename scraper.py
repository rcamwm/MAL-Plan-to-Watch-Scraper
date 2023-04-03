# %%
from bs4 import BeautifulSoup as bsp
from tqdm import tqdm
import csv
import requests
import sys
import time

def main(args):
    if args[1]:
        write_csv(get_plan_to_watch_list(args[1]))
    else:
        write_csv(input("Enter username: "))

def get_plan_to_watch_list(username):
    soup = get_username_soup(username)
    plan_to_watch = soup.find("div", {"class" : "list-unit plantowatch"})
    table = plan_to_watch.find('table', class_='list-table')
    data_items = table.get("data-items")[1:-1].split('{"status":6,')[1:]

    plan_to_watch_list = []
    
    for i in tqdm(range(len(data_items)), ncols = 100, desc ="Anime scraping progress: "):
        item = data_items[i]
        if '"anime_airing_status":3' not in item: # anime_airing_status 3 is Not Yet Aired
            i = item.split('"anime_title')

            title = i[1][3:-2]
            url = i[2].split('anime_url":"')[1].split('"')[0].replace("\\", "")
            hyperlink = '=HYPERLINK("{}","{}")'.format('https://myanimelist.net' + url, title)
            episodes = int(i[2].split('anime_num_episodes":')[1].split(",")[0])
            rating = get_MAL_rating(url)
            time.sleep(1)
            plan_to_watch_list.append([hyperlink, episodes, rating])

    return plan_to_watch_list

def get_MAL_rating(anime_url):
    soup = get_anime_soup(anime_url)
    try:
        return float(soup.find("span", {"itemprop" : "ratingValue"}).contents[0])
    except:
        return "Read error"

def get_anime_soup(anime_url):
    return get_soup("https://myanimelist.net" + anime_url)

def get_username_soup(MAL_username):
    return get_soup("https://myanimelist.net/animelist/" + MAL_username + "?status=6")

def get_soup(url):
    try:
        return bsp(requests.get(url).text, 'html.parser')
    except:
        print("Invalid MyAnimeList URL: {}".format(url))

def write_csv(rows):
    fields = ['Title', 'Episode Count', "MAL Rating"]
    with open('plan_to_watch.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

# %%
main(sys.argv)