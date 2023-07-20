# author: @mtcnbzks

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    print(f'\033[92mWelcome to Dictionary\033[0m')
    print(f'\033[92mPress "q" to quit\033[0m\n')

    url = 'https://tureng.com/en/turkish-english/'
    while True:
        word = str(input("Word/Kelime?: "))

        # check if word is empty
        if not word:
            print(f'\033[91mPlease enter a word!\033[0m')
            # normalize terminal output color
            print("\033[0m")
            continue

        if word == 'q':
            print(f'\033[92mSee you...\033[0m')
            break

        try:
            page = requests.get(url + word, headers=headers)
            soup = BeautifulSoup(page.content, 'lxml')

            is_word_eng = soup.find("th", {"class": "c2"}).text == "English"

            meaning_table = soup.find("table", {"class": "searchResultsTable"})
            rows = meaning_table.find_all("tr")

            for row in rows:
                no = row.find("td", {"class": "rc0"})
                if no is not None:  # check if row stands for a word
                    if is_word_eng:
                        no = no.text
                        tr = row.find("td", {"class": "tr"}).text.strip()
                        eng = row.find("td", {"class": "en"}
                                       ).text.strip().split(" ")[1]
                        eng = eng[:-1]  # remove last character (.)
                        print(f"{no}. {tr} ({eng})")
                    elif not is_word_eng:
                        no = no.text
                        tr = row.find("td", {"class": "tr"}).text.strip()
                        eng = row.find("td", {"class": "en"}
                                       ).text.strip().split(" ")[0]
                        print(f"{no}. {eng}")

        except ConnectionError:
            print("\033[91mConnection error!")
        except AttributeError:
            print("\033[91mWord not found!")
        except IndexError:
            print("\n")
            continue

        # normalize terminal output color
        print("\033[0m")
