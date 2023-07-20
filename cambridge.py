# author: @mtcnbzks

import re
import time

import requests
from bs4 import BeautifulSoup

start_time = time.time()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/103.0.0.0 Safari/537.36",
}

if __name__ == "__main__":
    print(f"\033[92mWelcome to English Dictionary\033[0m")
    print(f'\033[92mPress "q" to quit\033[0m\n')

    while True:
        url = "https://dictionary.cambridge.org/dictionary/english/"
        word = str(input("Word?: ")).strip()

        # check if user wants to quit
        if word == "q":
            print(f"\033[92mSee you...\033[0m")
            break

        # check if word is empty
        if not word:
            print(f"\033[91mPlease enter a word!\033[0m")
            # normalize terminal output color
            print("\033[0m")
            continue

        page = requests.get(url + word, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")

        try:
            general_part = soup.find("div", {"class": "def-block ddef_block"})

            word_level = general_part.find(
                "span", {"class": "def-info ddef-info"}
            ).text.split(" ")[0]
            word_status = soup.find("span", {"class": "pos dpos"}).text.strip()
            word_meaining = general_part.find(
                "div", {"class": "def ddef_d db"}
            ).text.strip()
            sentences = general_part.find("div", {"class": "def-body ddef_b"}).find_all(
                "div", {"class": "examp dexamp"}
            )

            print(f"\033[95m{word} \033[94m({word_status})\033[0m")
            if re.compile("[A-C]").search(word_level):
                print(f"({word_level})")
            print(f"\033[96m{word_meaining}\033[0m")
            if re.compile("[a-zA-Z]").search(str(sentences)):
                print(f"\033[92mExamples:\033[0m\033[4m")
                for sentence in sentences:
                    print(sentence.text.strip())

            # execution_time = time.time() - start_time
            # execution_time = round(execution_time, 2)
            # print(f"--- {execution_time} seconds ---")

        except ConnectionError:
            print("\033[91mConnection error!")
        except AttributeError:
            print("\033[91mWord not found!")

        # normalize terminal output color
        print("\033[0m")
