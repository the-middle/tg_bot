import re
import requests
from tg_token import token

wiki_url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
get_url = requests.get(wiki_url)

def getText():
    if get_url.text.find("<p><b>") != -1:                                                       # Find if paragraph pattern present in string
        stripped_string = re.findall(r'<p><b>.*[.</p>]', get_url.text)                          # Get this string
        x = str(stripped_string)                                                                # Transform into string from an object
        x = re.sub(r'<.*?>', '', x)                                                             # Delete all HTML tags
        x = re.sub(r'&#\d*;', '', x)                                                            # Delete encoded special symbols
        x = re.sub(r"[\[''\]]", '', x)                                                          # Delete [] and '' that was added while transforming to string
        x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)     
        return x
    elif get_url.text.find("<p><i>") != -1:
        stripped_string = re.findall(r'<p><i>.*[.</p>]', get_url.text)
        x = str(stripped_string)
        x = re.sub(r'<.*?>', '', x)
        x = re.sub(r'&#\d*;', '', x)
        x = re.sub(r"[\[''\]]", '', x)  
        x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)     
        return x
    else: 
        #TODO: catch the <p>[symbol]<b> and <p> Text.
        return "Попалась неинтересная статья, повезет в следующий раз."

def getURL():
    link_str = str(re.findall(r'<link rel="canonical".*[.\/>]', get_url.text))                  # Get the needed part of a string
    link_str = str(re.findall(r'\bhttps?://[^\s]+[^"/>]', link_str))                            # Get just url
    link_str = re.sub(r"\['", '', link_str)                                                     # Delete brackets from str()
    link_str = re.sub(r"\"/>\\'\]'\]", '', link_str)
    return link_str

def getImg():
    if re.search(r'class="infobox-image"', get_url.text) != None:
        link_img = str(re.findall(r'<table class="infobox.*<\/', get_url.text))
        link_img = str(re.findall(r'<img.* />', link_img))
        link_img = str(re.findall(r'src=".*"', link_img))
        link_img = re.findall(r'upload.[^\s]*"', link_img)
        if re.search(r'pictogram', link_img[0]) == None:
            link_img = re.sub(r'"', '', link_img[0])
            link_img = 'https://' + link_img
            print(link_img)
            return link_img
        elif re.search(r'pictogram', link_img[1]) == None:
            link_img = re.sub(r'"', '', link_img[1])
            link_img = 'https://' + link_img
            return link_img
        elif re.search(r'pictogram', link_img[2]) == None:
            link_img = re.sub(r'"', '', link_img[2])
            link_img = 'https://' + link_img
            return link_img
        elif re.search(r'pictogram', link_img[3]) == None:
            link_img = re.sub(r'"', '', link_img[3])
            link_img = 'https://' + link_img
            return link_img
        else:
            return ('Нет фото.')
    else:
        return('Нет фото.')

def botRequest():
    tg_url = "https://api.telegram.org/bot"
    method = "/sendMessage?"
    if getImg() != 'Нет фото.':
        tg_request = requests.post(
            url = tg_url + token + method,
            json = {
                "chat_id": "@wiki_shit",
                "parse_mode": "HTML",
                "text": getText() + F"<a href=\"{getImg()}\">&#8205;</a>" + F"<a href=\"{getURL()}\">\nСсылка</a>",
                "disable_web_page_preview": False
            }
        )
    else:
        tg_request = requests.post(
            url = tg_url + token + method,
            json = {
                "chat_id": "@wiki_shit",
                "parse_mode": "HTML",
                "text": getText() + F"<a href=\"{getURL()}\">\nСсылка</a>",
                "disable_web_page_preview": True
            }
        )
    print(tg_request.text)

if __name__ == "__main__":
    botRequest()