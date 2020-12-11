import requests
import sys
from bs4 import BeautifulSoup

language_list = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch", "polish",
                 "portuguese", "romanian", "russian", "turkish"]
lang_from = sys.argv[1]
lang_to = sys.argv[2]
word = sys.argv[3]
s = requests.Session()  # for faster fetch
file = open(f"{word}.txt", "w+", encoding="utf-8")

# header is to show the program as a device when requesting
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def translate(lang_to_be):
    if lang_to not in language_list and lang_to != "all":
        print(f"Sorry, the program doesn't support {lang_to}")
        sys.exit()
    elif lang_from not in language_list:
        print(f"Sorry, the program doesn't support {lang_to}")
        sys.exit()
    language = lang_from + "-" + lang_to_be
    r = s.get(f"https://context.reverso.net/translation/{language}/{word}", headers=headers)
    if r.status_code == 404:
        print(f"Sorry, unable to find {word}")
        sys.exit()
    elif r.status_code != 200:
        print("Something wrong with your internet connection", r.status_code)
        sys.exit()
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find("div", {"id": "translations-content"})
    section = soup.find("section", {"id": "examples-content"})
    a_list = div.find_all("a")
    span_list = section.find_all("span", {"class": "text"})
    a_text_list = []
    span_text_list = []
    a_text = ""
    for i in range(5):
        if lang_to_be == "all":
            a_text = a_list[0].text.strip(" \n ")
        a_text_list.append(a_list[i].text.strip(" \n "))
    for j in range(10):
        span_text_list.append(span_list[j].text.strip(" \n "))

    joined_a_texts = "\n".join(a_text_list)
    joined_span_texts = ":\n".join(span_text_list)
    write_txt_list = [f"{lang_to_be.capitalize()} Translations:\n", f"{a_text if lang_to_be == 'all' else joined_a_texts}\n",
                      f"{lang_to_be.capitalize()} Examples:\n", f"{joined_span_texts}\n"]
    file.writelines(write_txt_list)


if lang_to == "all":
    for i in range(len(language_list)):
        if language_list[i] == lang_from:
            continue
        else:
            translate(language_list[i])

else:
    translate(lang_to)

file.seek(0) # move the cursor to the beginning of the file to read.
print(file.read())
file.close()
