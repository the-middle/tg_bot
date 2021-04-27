import re
import requests
from tg_token import token

wiki_url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
get_url = requests.get(wiki_url)


class goto(Exception):
    pass


def getText():
    if get_url.text.find("<p><b>") != -1:
        x = re.findall(r'<p>.*[.</p>]', get_url.text)
        x = re.sub(r'<.*?>', '', x[0])
        x = re.sub(r'&#\d*;', '', x)
        x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)
        return x
    elif get_url.text.find("<p>") != -1:
        x = re.findall(r'<p>.*[.</p>]', get_url.text)
        if x[0] != '':
            x = re.sub(r'<.*?>', '', x[0])
            x = re.sub(r'&#\d*;', '', x)
            x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)
            return x
        elif x[1] != '':
            x = re.sub(r'<.*?>', '', x[1])
            x = re.sub(r'&#\d*;', '', x)
            x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)
            return x
        elif x[2] != '':
            x = re.sub(r'<.*?>', '', x[2])
            x = re.sub(r'&#\d*;', '', x)
            x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)
            return x
        else:
            x = re.sub(r'<.*?>', '', x[3])
            x = re.sub(r'&#\d*;', '', x)
            x = re.sub(r"(([А-я])(\d{1,3}))", r"\g<2>", x)
            return x
    else:
        return "Попалась неинтересная статья, повезет в следующий раз."


def getURL():
    link_str = re.findall(r'<link rel="canonical".*[.\/>]', get_url.text)
    link_str = re.findall(r'\bhttps?://[^\s]+[^"/>]', link_str[0])
    link_str = link_str[0]
    return link_str


def getImg():
    if re.search(r'class="infobox-image"', get_url.text) != None:
        link_img = re.findall(r'class="infobox-image.*<\/', get_url.text)
        link_img = re.findall(r'<img.* />', link_img[0])
        link_img = re.findall(r'src=".*"', link_img[0])
        try:
            if re.search(r'upload.[^\s]+ 2x', link_img[0]) != None:
                link_img = re.findall(r'upload.[^\s]+ 2x', link_img[0])
                if re.search(r'pictogram|mark|Ice_hockey_puck', link_img[0]) == None:
                    link_img = re.sub(r' 2x', '', link_img[0])
                    link_img = 'https://' + link_img
                    return link_img
                else:
                    raise goto()
            else:
                raise goto()
        except goto():
            # Drop the icons on some pages in infobox table. Unfortunately, python don't have switch().
            if re.search(r'pictogram|mark|Ice_hockey_puck', link_img[0]) == None:
                link_img = re.sub(r'"', '', link_img[0])
                link_img = 'https://' + link_img
                print(link_img)
                return link_img
            elif re.search(r'pictogram|mark|Ice_hockey_puck', link_img[1]) == None:
                link_img = re.sub(r'"', '', link_img[1])
                link_img = 'https://' + link_img
                return link_img
            elif re.search(r'pictogram|mark|Ice_hockey_puck', link_img[2]) == None:
                link_img = re.sub(r'"', '', link_img[2])
                link_img = 'https://' + link_img
                return link_img
            elif re.search(r'pictogram|mark|Ice_hockey_puck', link_img[3]) == None:
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
            url=tg_url + token + method,
            json={
                "chat_id": "@wiki_shit",
                "parse_mode": "HTML",
                "text": getText() + F"<a href=\"{getImg()}\">&#8205;</a>" + F"<a href=\"{getURL()}\">\nСсылка</a>",
                "disable_web_page_preview": False
            }
        )
    else:
        tg_request = requests.post(
            url=tg_url + token + method,
            json={
                "chat_id": "@wiki_shit",
                "parse_mode": "HTML",
                "text": getText() + F"<a href=\"{getURL()}\">\nСсылка</a>",
                "disable_web_page_preview": True
            }
        )
    print(tg_request.text)


if __name__ == "__main__":
    botRequest()
