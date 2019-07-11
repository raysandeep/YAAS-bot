import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json


class Insta_Info_Scraper:

    def getinfo(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        text = data[0].get('content').split()
        print(text)
        self.user = ""
        for i in text:
            if i == "from":
                for k in range(1,len(text) - text.index(i)):
                    self.user =self.user + " "+ text[text.index(i)+k]
        followers = text[0]
        following = text[2]
        self.posts = text[4]
        print ('User:', self.user)
        print ('Followers:', followers)
        print ('Following:', following)
        #print ('Posts:', posts)
        print ('---------------------------')

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        url1 ='https://www.instagram.com/vit_bot/'
        self.getinfo(url1)
        return self.posts

if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()
