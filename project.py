from bs4 import BeautifulSoup
import requests
import re
import random


def remove_h2_tags(text):
    return re.sub(r'<h2>|</h2>', '', text)


def find_torrent_links_in_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            torrent_links = []
            for link in soup.find_all('a', href=True):
                if link['href'].endswith('.torrent'):
                    torrent_links.append(link['href'])
            return torrent_links
    except Exception as e:
        print("Error fetching torrent links:", e)
    return []


def find_genre_in_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            count = 0
            for link in soup.find_all('h2'):
                if count == 1:

                    print("Genre -->", link.get_text())
                    return ""
                count += 1
                if count > 1:
                    exit
    except Exception as e:
        print("Error fetching genre links:", e)
    return []


def get_random_movie_from_yts():
    yts_url = "https://en.yts-official.mx/"
    response = requests.get(yts_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        movie_titles = soup.select(".browse-movie-title")
        movie_links = soup.select(".browse-movie-link")
        random_index = random.randint(0, len(movie_titles) - 1)
        random_movie_title = movie_titles[random_index].text.strip()
        random_movie_link = yts_url + movie_links[random_index].get("href")
        return random_movie_title, random_movie_link
    else:
        print("Error: Unable to fetch data from YTS site.")
        return None, None


def display_movie_details(movie_url):
    try:
        movie_request = requests.get(movie_url)
        movie_request.raise_for_status()
        movie_soup = BeautifulSoup(movie_request.text, "html.parser")
        info = movie_soup.select_one(".bottom-info")
        likes = info.select_one("#movie-likes").text.strip() if info else None
        imdb_link = info.select_one("a[title='IMDb Rating']")[
            "href"] if info else None

        print("YTS Link -->", movie_url)
        print("IMDb Links -->", imdb_link)

        print("Likes -->", likes)

        torrent_links = find_torrent_links_in_webpage(movie_url)
        base_url = "https://en.yts-official.mx"

        genre_name = find_genre_in_webpage(movie_url)

        print(genre_name)

        if torrent_links:
            print("Torrent Links:")
            count = 0
            for link in torrent_links:
                link = link.replace(" ", "%20")
                print(f"{base_url}{link}")
                if count == 1:
                    break
                count += 1
        else:
            print("Torrent Links: Not available")
        print("-----------------------------------------------------------------------------------------------")

        print("")
    except Exception as e:
        print(f"Error fetching details for '{movie_url}':", e)


choice = input(
    "Choose an option:\n1. Search for a movie\n2. Get a random movie from YTS\nEnter your choice (1 or 2): ")

if choice == '1':
    name = input("Enter Movie Name: ")
    print("")
    base_url = "https://en.yts-official.mx/"
    search_url = f"https://en.yts-official.mx/browse-movies?keyword={name}&quality=all&genre=all&rating=0&year=0&order_by=featured"

    try:
        r = requests.get(search_url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        movie_count = 0
        for movie in soup.select(".browse-movie-wrap"):
            if movie_count > 9:
                break

            mov_name = movie.select_one(".browse-movie-bottom a").text
            mov_name = mov_name.replace(" ", "-")
            mov_name = mov_name.replace(":", "")
            movie_year = movie.select_one(".browse-movie-bottom div").text
            movie_year = movie_year.replace(" ", "-")
            movie_name = f"{mov_name}-{movie_year}"
            rating = movie.select_one(".rating")
            rating = rating.text if rating else "0.0"

            movie_url = f"https://en.yts-official.mx/movies/{movie_name}/"
            print("\nFetching movie details from:", movie_url)
            display_movie_details(movie_url)
            movie_count += 1

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)

elif choice == '2':
    random_movie_title, random_movie_link = get_random_movie_from_yts()

    print("\nFetching random movie details...")
    display_movie_details(random_movie_link)

else:
    print("Invalid choice. Please enter either 1 or 2.")

print("Done!")

import sys 
user_input = input("Enter 'q' to quit: ") 
if user_input == 'q': sys. exit("You chose to quit the program. ")