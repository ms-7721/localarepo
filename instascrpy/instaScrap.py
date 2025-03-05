import sys
from bs4 import BeautifulSoup as soup
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import requests
import getpass
from pynput.keyboard import Key,Controller
import urllib
import time
from webdriver_manager.chrome import ChromeDriverManager
def instagram_login(web):
    user= WebDriverWait(web,10).until(ec.visibility_of_element_located((By.NAME,"username")))
    password=WebDriverWait(web,10).until(ec.visibility_of_element_located((By.NAME,"password")))
    user.clear()
    password.clear()
    instagram_user= getpass.getpass("enter your usremane:")
    user.send_keys(instagram_user)
    instagram_password=getpass.getpass("enter your password:")
    password.send_keys(instagram_password)
    time.sleep(5)
    submit=web.find_element(By.XPATH,"//button[@type='submit']")
    submit.click()
    #web.get("ttps://www.instagram.com/"+instagram_user+'/')
    time.sleep(5)
    return
#create one folder or multiple folders
def makeMainDirectory(directory):
    make_maindirectory = directory
    if not os.path.isdir(make_maindirectory):
        os.mkdir(make_maindirectory)
        os.chdir(make_maindirectory)
def getInstagramAccount(instagramUsername,web):
    instagram_holder=instagramUsername
    time.sleep(5)
    web.get("https://www.instagram.com/"+instagram_holder+"/")
    getinspector()
    #scraping photos 
    scraping_images(instagram_holder,web)
    hrfactions=  getinstagramaction(instagram_holder,web)
    #SCRAPING FOLLOWING
    following=getinstagramfollowing(hrfactions,web)
    hrfactions=  getinstagramaction(instagram_holder,web)
    print(following)
    #SCRPING FOLLOWERS
    followeres=getinstagramfollowers(hrfactions,web)
    print(followeres)

def scraping_images(instagram_holder,web):
    lenofpage=web.execute_script("window.scrollTo(0,document.body.scrollHeight); var lenofpage=document.body.scrollHeight;return lenofpage")
    match=False
    x=100
    while(match==False):
        #directory of instagram account
        directory = instagram_holder
        lastcount= lenofpage
        time.sleep(30)
        instagram_urls=[]
        instagram_capture= web.find_elements(By.XPATH,"//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'] ")
        #image source
        for i in instagram_capture:
            instagram_urls.append(i.get_attribute('src'))
            
        #create directory    
        if not os.path.isdir(directory):
            os.mkdir(directory)    
        for i, link in enumerate(instagram_urls):

            path = os.path.join(instagram_holder, f"{i + x}.jpg")  # सही फ़ाइल नाम
            try:
                urllib.request.urlretrieve(link, path)
                print(f"Downloaded: {path}")
            except Exception as e:
                print(f"Unable to download {link}: {e}")

        x+=100

        lenofpage = web.execute_script("window.scrollTo(0,document.body.scrollHeight); var lenofpage=document.body.scrollHeight; return lenofpage")
        if (lastcount==lenofpage):
            match = True                
    
#actions for getting follwers and following
def getinstagramaction(instagram_holder,web):
     web.get("https://www.instagram.com/"+instagram_holder+"/")
     time.sleep(5)
     href_temp= web.find_elements(By.XPATH,"")
     return href_temp
def getinstagramfollowing(action,web):
    following_names=[]
    following = action[2]
    following.click()
    time.sleep(20)
    following_temp= web.page_source
    following_data = soup(following_temp,"html-parser")
    following_name= following_data.find_all("a")
    for i in following_name:
        following_names.append(i.get('title'))
    clean_following_name=[x for x in following_names if x != None]  
    return clean_following_name  
def getinstagramfollowers(action,web):
    followers_names=[]
    followere = action[2]
    followere.click()
    time.sleep(20)
    followere_temp= web.page_source
    followere_data = soup(followere_temp,"html-parser")
    followere_name= followere_data.find_all("a")
    for i in followere_name:
        followers_names.append(i.get('title'))
    clean_followere_name=[x for x in followers_names if x != None]  
    return clean_followere_name  

def getinspector():
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press("i")
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release("i")
    time.sleep(5)



def main():
    
    web = webdriver.Chrome()
    web.get("https://www.instagram.com/accounts/login/?hl=en")
    web.maximize_window()
    time.sleep(5)
    instagram_login(web)
    make_mainAccount=input(str("please type name to store youre  instagram account into:"))
    makeMainDirectory(make_mainAccount)
    while(True):
        instagram_Account=input(str("please type instagram account to me for find or 'quit' to end program :€"))
        if (instagram_Account=='quit'):
            return False
        else:
           getInstagramAccount(instagram_Account,web)    

    

    
if __name__=="__main__":
    main()
