import requests
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import ssl
import json
from pprint import pprint
from random import choice
import os
from lxml import html
from InstagramAPI import InstagramAPI
import pandas as pd 
import csv
import time
import subprocess
_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]
def run_again(cmd):
    subprocess.call(["bash", "-c", "source ~/.profile; " + cmd]) 

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
        url1 = "https://www.instagram.com/"+ username.split("@")[1].split(")")[0] + "/"
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

    

InstagramAPI2 = InstagramAPI("yaas_bot", "yaas123")
InstagramAPI2.login()    
dnj=[]
pos = []
with open(r"/Users/akshatvg/Desktop/insta-bot/works/final.csv") as csv_file:  
    csv_reader = csv.reader(csv_file, delimiter=',') 
    df = pd.DataFrame([csv_reader], index=None) 
    df.head() 
c=0
f=0
while(True and f==0):
    c=0
    while(True):
        print(c)
        c+=1
        for x in range(1,43):
            for val in df[x]:
                #print(val[1])
                us,po = Insta_Info_Scraper().main(val[1])
                print(us,po,int(val[2]))
                time.sleep(2)
                if int(po)>int(val[2]):
                    k = InstagramScraper()
                    namee = us.split("@")[1].split(")")[0]
                    u = 'https://www.instagram.com/' + namee  +'/?hl=en'
                    results = k.profile_page_recent_posts(u)
                    for i in range(int(po)-int(val[2])):
                        print(i)
                        url = results[0]['display_url']
                        has = "#yaas #teamyaas #vitbot #vit #technology "
                        if results[0]['edge_media_to_caption']['edges']==[]:
                            cap = "Repost from : " + us + " "
                            cap += has
                        else:
                            cap = "Repost from : " + us + " "+ results[0]['edge_media_to_caption']['edges'][0]['node']['text']
                            cap += has

                        urllib.request.urlretrieve(url,"test.jpg")
                    # login
                        photo_path = 'test.jpg'
                        InstagramAPI2.uploadPhoto(photo_path, caption=cap)
                        os.remove("test.jpg")
                        print(i)
                        df[val[2]] = int(df[val[2]])
                        df[val[2]] += 1
                        print(int(val[2]))
                        break
                elif int(po)< int(val[2]) :
                    print(int(val[2]))
                    df[val[2]] = po
                    po = int(po)
