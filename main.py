from random import choice
import json
from InstagramAPI import InstagramAPI
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import ssl

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

class Insta_Info_Scraper:

    def getinfo(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        
        text = data[0].get('content').split()
        self.user = ""
        for i in text:
            if i == "from":
                for k in range(1,len(text) - text.index(i)):
                    self.user =self.user + " "+ text[text.index(i)+k]
        followers = text[0]
        following = text[2]
        self.posts = text[4]
        '''print ('User:', self.user)
        print ('Followers:', followers)
        print ('Following:', following)
        print ('Posts:', self.posts)
        print ('---------------------------')'''
    def main(self,username):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        #print(username)
        url1 = "https://www.instagram.com/"+ username + "/"
        #print(url1)
        self.getinfo(url1)
        return self.user,self.posts


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results
from pprint import pprint
InstagramAPI = InstagramAPI("yaas_bot", "manboobs")
InstagramAPI.login()
k = InstagramScraper()
chaptername = input("Enter Chapter insta handle by removing @ before :   ")
urlofchap = 'https://www.instagram.com/'+chaptername+'/?hl=en'
results = k.profile_page_recent_posts(urlofchap)
for i in range(0,1):
    url = results[i]['display_url']
    us,po = Insta_Info_Scraper().main(chaptername)
    cap = "Repost from: " + us +" "+results[i]['edge_media_to_caption']['edges'][0]['node']['text']+"#yaas #teamyaas #vitbot #vit #technology"
    urllib.request.urlretrieve(url,"test.jpg")
  # login
    photo_path = 'test.jpg'
    InstagramAPI.uploadPhoto(photo_path, caption=cap)
    os.remove("test.jpg")
    print(cap)
