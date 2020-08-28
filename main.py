import requests, vk_api, json, random, re
from bs4 import BeautifulSoup

f = open("account_info.json", "r")
login_info = json.loads(f.read())
f.close()
it = 1

for sessions in range(0, 1000):
    vk_session = vk_api.VkApi(login=login_info.get("login"), password=login_info.get("password"), token=login_info.get("token"))
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()

    unixTime = 1599224400
    oneHour = 3600

    url = "http://scpfoundation.net/scp-"

    for itera in range(1, 1000):
        # try:
            pageid = random.randint(1, 5000)
            urlReal = url + str(pageid)

            r = requests.get(urlReal)
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

            messageFin = str(titleArt) + '\n' + "Ссылка на статью: " + str(urlReal) + "\n"

            for i in pAr:
                messageFin = messageFin + str(i)

            vk.wall.post(owner_id=login_info.get("owner_id"), message=messageFin, publish_date=unixTime+oneHour*it)
            print("Posted: " + urlReal)
            print("Posts number: " + str(it) + "\n")
            it = it+1
            if it%60==0:
                print("relog in session")
                break
        # except Exception:
        #     print("Exception: " + urlReal)