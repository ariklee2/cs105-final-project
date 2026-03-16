import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ACTION_WORDS = set([
    "go", "run", "move", "hurry", "stop",
    "wait", "look", "get", "take", "come",
    "help", "shoot", "kill", "fight", "attack",
    "cover", "down", "now", "fast", "quick",
    "gun", "bomb", "target", "enemy", "mission",
    "escape", "chase", "danger", "secure", "clear" 
])

COMEDY_WORDS = set([
    "funny", "joke", "laugh", "crazy", "weird",
    "silly", "oops", "awkward", "sorry", "what",
    "why", "really", "classic", "wait", "look"
    "dude", "bro", "man", "cousin", "guy",
    "exactly", "literally", "party", "drink", "dance",
    "chill", "stupid", "idiot", "seriously", "relax"
])

FAMILY_WORDS = set ([
    "secret", "believe", "magic", "legend", "discover",
    "hidden", "forever", "imagine", "journey", "wonder",
    "together", "promise", "brave", "listen", "heart",
    "home", "belong", "trust", "change", "remember"
    "hurry", "escape", "trouble", "monster", "finally",
    "impossible", "danger", "team", "mission", "destiny"
])

CORPUS = set()

genre_links = [
    "https://imsdb.com/genre/Action",
    "https://imsdb.com/genre/Comedy",
    "https://imsdb.com/genre/Family"
]

not_read = 0
read = 0

for genre_link in genre_links:
    response = requests.get(genre_link)
    content = response.text

    # Check if request works
    print("Status code:", response.status_code)

    soup = BeautifulSoup(content, "html.parser")

    movie_links = [a["href"] for a in soup.select("p a")]

    for movie_link in movie_links:    
        movie = urljoin(genre_link, movie_link)
        new_response = requests.get(movie)
        new_content = new_response.text

        print("Status code:", movie, new_response.status_code)

        new_soup = BeautifulSoup(new_content, "html.parser")

        for a in new_soup.select("a"):
            if "Read" in a.text:
                script_url = a["href"]
                script_site = urljoin(movie, script_url)

                new_new_response = requests.get(script_site)
                new_new_content = new_new_response.text

                print("Status code:", script_site, new_new_response.status_code)

                if new_new_response.ok:
                    new_new_soup = BeautifulSoup(new_new_content, "html.parser")

                    script = new_new_soup.find("pre")

                    # Check if pre exists
                    if script:
                        words = script.get_text().split()
                        CORPUS.update(words)
                        read += 1
                    else:
                        not_read += 1
                else:
                    not_read += 1

print(len(CORPUS), not_read, read, read / (not_read + read) * 100)