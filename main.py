import requests, vk_api, json, random, re, datetime, time
from bs4 import BeautifulSoup
import urllib.request

f = open("account_info.json", "r")
login_info = json.loads(f.read())
f.close()
it = 1
exceptionCount = 0
session = 0

unix_time = 1633190400
oneHour = 3600

while True:
    session += 1
    print("Current session: " + str(session))
    vk_session = vk_api.VkApi(login=login_info.get("login"), password=login_info.get("password"), token=login_info.get("token"))
    print(vk_session.auth(token_only=True))
    vk = vk_session.get_api()

    post_img = "photo-198135266_457239019"

    for itera in range(1, 1000):
        try:
            response = urllib.request.urlopen('https://scpdb.org/random') #https://scpdb.org/random
        except Exception:
            print("Caught HTTP Error \n")
            break

        try:
            # check if link contains "wikidot" word
            if response.geturl().find("wiki") == -1:
                next

            responseScpId = str(response.geturl()).split('/')
            responseScpId = responseScpId[len(responseScpId)-1]

            url = "https://scpfoundation.net/" + responseScpId

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            
            titleArt = soup.find("div", id="page-title").string.strip()

            pAr = []
            for p in soup.find("div", id="page-content"):
                t = str(p)
                # Get rid of html tags
                t = re.sub(r'\<[^>]*\>', '', t)
                if t != '':
                    pAr.append(t)

            for i in range(1,3):
                pAr.pop(0)

            messageFin = str(titleArt) + '\n' + "Ссылка на статью: " + url + "\n\n\n"

            for i in pAr:
                messageFin = messageFin + str(i)
            unix_time += oneHour
            vk.wall.post(owner_id=login_info.get("owner_id"), message=messageFin, publish_date=unix_time, attachments=post_img)
            print("Posted: " + response.geturl())
            print("Posts number: " + str(it) + "\n")
            it = it+1
            exceptionCount = 0
            time.sleep(3600)
            if it%60==0:
                print("relog in session")
                break
        except Exception:
            print("Exception: " + response.geturl())
            exceptionCount += 1
            print("Exception number: " + str(exceptionCount))
            if(exceptionCount == 15):
                print("Reached max number of exceptions: 15")
                exit()
