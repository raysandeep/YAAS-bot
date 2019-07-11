import datetime
from selenium import webdriver
import time
from InstagramAPI import InstagramAPI
import numpy as np
import cv2
import textwrap
import random
import praw
import csv


dt=datetime.datetime.today()
print(dt.weekday())


while(True):
    count = 0
    if(count<1):
        InstagramAPI = InstagramAPI("vit_bot", "yaas123")
        InstagramAPI.login()  # login
        photo_path = '/Users/anandsure/Desktop/til-2-insta/post2.jpg'
        caption = "XYZ ABCEDFGGGGGGGGGGGG! \n "
        InstagramAPI.uploadPhoto(photo_path, caption=caption)
        count = count + 1
    else:
        break


