# -------------------------------------------------------------------------
#developer: ubaid ahmed
# email: ubaidahmedmeo@gmail.com
# -------------------------------------------------------------------------- 

from sys import warnoptions
from sys import exit
import sys
import os
import time
import datetime
import pandas as pd  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

date = datetime.datetime.now().strftime("%Y-%m-%d")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
#WordPress Login Page
URL = "http://fullandroidapp.com/wp-admin/admin.php?page=appyn_importar_contenido_gp"

# chrome browser headless
HEADLESS = False
# WordPress Login 
USERNAME = "" #WordPress Useername
PASSWORD = "" #Wordpress Password
# wait for element loading
WAIT = 10
# input file path
INPUTFILE = "input-file.txt"


options = webdriver.ChromeOptions()
options.headless = HEADLESS
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--windows-size=1920,1080")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
print("run............")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

def run():
    driver.maximize_window()
    driver.get(URL)
    time.sleep(3)
    username = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, "user_login")))
    username.send_keys(USERNAME)
    password = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, "user_pass")))
    password.send_keys(PASSWORD)
    time.sleep(1)
    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, "wp-submit"))).click()
    time.sleep(2)

    CSV = []
    count=0
    with open(INPUTFILE) as file:
        for index, link in enumerate(file):
            try:
                print(f"link ({link})")
                googleplay_url = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, "url_googleplay")))
                googleplay_url.clear()
                googleplay_url.send_keys(link)
                time.sleep(2)
                x=True
                w=1
                while x:
                    try:
                        spiner = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
                        if not spiner:
                            print("App Installed Successfully\n")
                            x=False
                        else:
                            print(f"Installing {index} App..")
                            loading_time()
                            time.sleep(1)
                            w+=1
                    except:
                        installing_status = {
                            "App Link":link, 
                            "App Status":"Apparently the URL does not exist. Check again"
                            }
                        CSV.append(installing_status)
                        print("The app you want to import already exists.\n")     
                        x=False
                count+=1
            except KeyboardInterrupt:
                print(f""" 
                -----------------------------------------------------------------------------------------
                    Total {count} Apps Installed 
                -----------------------------------------------------------------------------------------
                """)
                df = pd.DataFrame(CSV)
                df.to_csv(f"{date}-{count} app installed.csv")
                exit()
    driver.quit()

def loading_time():
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")

if __name__ == "__main__":
    run()
