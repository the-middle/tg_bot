import re
import requests
from tg_token import token

wiki_url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
get_url = requests.get(wiki_url)

def getText():
    # Find if paragraph pattern present in string
    if get_url.text.find("<p><b>") != -1:
        # Get this string
        stripped_string = re.findall(r'<p><b>.*[.</p>]', get_url.text)
        # Transform into string from an object
        x = str(stripped_string)
        # Delete all HTML tags
        x = re.sub(r'<.*?>', '', x)
        # Delete encoded special symbols
        x = re.sub(r'&#\d*;', '', x)
        # Delete [] and '' that was added while transforming to string
        x = re.sub(r"[\[''\]]", '', x)  
        x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)     
        return x
    elif get_url.text.find("<p><i>") != 1:
        stripped_string = re.findall(r'<p><i>.*[.</p>]', get_url.text)
        x = str(stripped_string)
        x = re.sub(r'<.*?>', '', x)
        x = re.sub(r'&#\d*;', '', x)
        x = re.sub(r"[\[''\]]", '', x)  
        x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)     
        return x
    else: 
        return "Попалась неинтересная статья, повезет в следующий раз."

def getURL():
    # Get the needed part of a string
    link_str = str(re.findall(r'<link rel="canonical".*[.\/>]', get_url.text))
    # Get just url
    link_str = str(re.findall(r'\bhttps?://[^\s]+[^"/>]', link_str))
    # Delete brackets from str()
    link_str = re.sub(r"\['", '', link_str)
    link_str = re.sub(r"\"/>\\'\]'\]", '', link_str)
    return link_str


def botRequest():
    tg_url = "https://api.telegram.org/bot"
    method = "/sendMessage?"
    tg_request = requests.post(
        url = tg_url + token + method,
        json = {
            "chat_id": "@wiki_shit",
            "text": getText() + F"\n<a href=\"{getURL()}\">Ссылка</a>",
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
    )
    print(tg_request.text)

if __name__ == "__main__":
    botRequest()