from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import urllib3
from tkinter import messagebox 
import pandas as pd
import os
import imagesize
import time 
import requests
import socket
import threading
import datetime
import urllib.request
import selenium 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
opener = urllib.request.URLopener()
opener.addheader('User-Agent', user_agent)

# for show message 
def text_box(text):
	log_box.configure(state='normal')
	log_box.insert(1.0, text + '\n')
	log_box.configure(state='disabled')

# for get input from GUI and run program  
def get_input():
    Keyword = input1.get().rstrip()
    No_of_img = input3.get().rstrip()
    No_of_tab = input4.get().rstrip()
    Get_check = check.get()
    if Keyword == "":
        messagebox.showinfo("ALERT","Please Enter A Keyword!")
    elif No_of_img == "":
        messagebox.showinfo("ALERT","Please Enter A Number")
    elif not No_of_img.isdigit():
        messagebox.showinfo("ALERT","In Fild 3 Please Enter A Number Only")
    elif int(No_of_img) >= 200:
        messagebox.showinfo("ALERT","Bing Have Only 200 Images, Please Put Less-than 200!")
    elif No_of_tab == "":
        messagebox.showinfo("ALERT","Please Enter A Number Tab Fild!")
    elif not No_of_tab.isdigit():
        messagebox.showinfo("ALERT","Please Enter Only Number In Tab Fild!")
    elif int(No_of_tab) >= 15:
        messagebox.showinfo("ALERT","Mazimum No is 15")
    else:
        thread1 = threading.Thread(target=main_prograam, args=(Keyword, No_of_img, Get_check, No_of_tab))
        thread1.start()
        start_button["state"] = "disabled"
        check_btn1.config(state=DISABLED)

# our main program 
def main_prograam(Keyword, No_of_img, Get_check, No_of_tab):
    try:
        options = webdriver.ChromeOptions()
        if Get_check:
            options.headless = True
        else:
            options.headless = False
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy--bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # driver = webdriver.Chrome(chrome_options=options, executable_path="driver/chromedriver.exe")
        text_box("Browser Opning For Fold Above Images\n")
        driver.maximize_window()
        driver.get(f'https://www.bing.com/images/search?q={Keyword}')
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tags = soup.find_all("a", class_="suggestion-item")

        TITLE = [Keyword,]
        t_title = driver.find_elements_by_class_name('suggestion-title')
        for title in t_title:
            try:
                t1 = title.text
                t2 = t1.replace("\n", " ")
                TITLE.append(t2)
            except Exception:
                pass

        TAB_LINKS = []
        FOR_THUMB_IMG = []
        for i in img_tags:
            if 'href' in i.attrs:
                get_tab_links = str("https://www.bing.com/" + i.attrs['href'] + "&view=detailV2&ccid")
                get_tab_view_links = str("https://www.bing.com/" + i.attrs['href'])
                TAB_LINKS.append(get_tab_links)
                FOR_THUMB_IMG.append(get_tab_view_links)

        text_box(f"{len(TITLE)} Search Related Tabs Found\n")
        # geting all thumbnails links
        TAB_COUNT = 0
        for for_thumb, for_title in zip(FOR_THUMB_IMG, TITLE):
            # making a thumbnail folder
            try:
                os.makedirs("thumbnail/" + for_title)
            except FileExistsError:
                pass

            if int(No_of_img) <= 100:
                t = 2
            else:
                t = 9
            i = 0
            while i < t:  
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                try:
                    driver.find_element_by_xpath('/html/body/div[3]/div[5]/div[2]/div[2]/div[2]/a').click()
                except Exception:
                    pass
                time.sleep(5)
                i+=1
            print(f"**************************{for_title} Page Scrolling Done****************************")
            # thumb_images = soup.find_all("img", class_="mimg")
            tb1 = driver.find_elements_by_class_name("img_cont")
            time.sleep(5)
            text_box(f"{len(tb1)} {for_title} Images Found On This Page\n")
            thumbnail_img_count = 0
            for gtb in tb1:
                try:
                    a2 = gtb.find_element_by_tag_name("img")
                    a3 = a2.get_property("src")
                    print(f"{thumbnail_img_count} {for_title} Thumbnail download")
                    text_box(f"{thumbnail_img_count} {for_title} Thumbnail download")
                    urllib.request.urlretrieve(a3, "thumbnail" + "/" + for_title + "/" + str(thumbnail_img_count)+".jpg")
                    thumbnail_img_count+=1
                except Exception as e:
                    pass
                if int(thumbnail_img_count) >= int(No_of_img):
                    break
            driver.get(for_thumb)
            thumbnail_img_count = 0
            TAB_COUNT+=1
            if TAB_COUNT >= int(No_of_tab):
                break
        print(f"\n\n*******************************All Thumbnil DOWNLOADED***********************************\n\n")
        text_box("\nAll Thumbnil DOWNLOADED\n")
        print(f"\n\n*******************************Geting HQ images***********************************\n\n")
        text_box("Geting HQ images\n")
        COUNT = 0
        WEBPAGE_LINKS = []
        HQ_IMAGES_LINKS = []
        H1 = []
        HQ_Count = 0
        CSV = []
        ERROR = 0
        for GO, title1 in zip(TAB_LINKS, TITLE):
            driver.get(f'https://www.bing.com/images/search?q={title1}&view=detailV2&ccid')
            time.sleep(3)
            try:
                os.makedirs("HQ images/" + title1)
            except FileExistsError:
                pass
            for ab in range(0, int(No_of_img)):
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navr"]/span'))).click()
                    # driver.find_element_by_xpath('//*[@id="navr"]/span').click()
                    time.sleep(2)
                    h1 = driver.find_element_by_class_name("pimc")
                    web_h1 = h1.find_element_by_tag_name("a").text
                    H1.append(web_h1)
                    wbl = driver.find_element_by_class_name("pimc")
                    wbl1 = wbl.find_element_by_tag_name("a")
                    wbl2 = wbl1.get_property("href")
                    WEBPAGE_LINKS.append(wbl2)
                    img1 = driver.find_element_by_class_name('imgContainer')
                    img2 = img1.find_element_by_tag_name('img')
                    img3 = img2.get_property('src')
                    HQ_IMAGES_LINKS.append(img3)
                    socket.setdefaulttimeout(10)
                    filename, headers = opener.retrieve(img3, "HQ images"+ "/" + str(title1) + "/" + str(COUNT) + ".jpg")
                    COUNT+=1
                    print(f"{ab} {title1} Image Download")
                    text_box(f"{ab} {title1} Image Download\n")
                    data_1 = {"Keyword":title1,"Web Page Links":wbl2 ,"HQ Images Links":img3, "Web Page Title":web_h1}
                    CSV.append(data_1)
                except requests.exceptions.ConnectionError:
                    ERROR+=1
                except requests.exceptions.ReadTimeout:
                    ERROR+=1
                except socket.timeout:
                    ERROR+=1
                except urllib.error.HTTPError as e:
                    ERROR+=1
                    print('HTTPError: {}'.format(e.code))
                except urllib.error.URLError as e:
                    ERROR+=1
                    print('URLError: {}'.format(e.reason))
                except OSError:
                    ERROR+=1
                    print("Os Error")
                except NoSuchElementException:
                    print("Error somthing")
                    pass
                except RuntimeError:
                    print("You Close Browser")
                    messagebox.showinfo("ERROR", "You Close Browser, Please Try Agin") 
                except:
                    print("ERROR")
                    pass
            print(f"\n\n***********************{title1} Images Downloading Start****************************\n\n")
            text_box(f"{title1} Images Downloading Start")
            COUNT = 0
            HQ_Count+=1
            if HQ_Count >= int(No_of_tab):
                break
        print(f"\n\n*******************************All HQ Images Downloaded Done************************************\n\n")
        text_box("All HQ Images Downloaded Done")
        try:
            os.makedirs("csv/" + Keyword)
        except FileExistsError:
            pass
        df = pd.DataFrame(CSV)
        df.to_csv("csv" + "/" + Keyword + "/" + Keyword + ".csv")



        print(f"\n\n************************Program Start For Above Images Download*****************************\n\n")
        text_box("Program Start For Above Images Download")
        ABOVE_count = 0
        VISIT_COUNT = 0
        for title2 in TITLE:
            try:
                os.makedirs("Above Fold images/" + title2)
            except FileExistsError:
                pass
            for visit in WEBPAGE_LINKS:
                visit = visit
                try:
                    driver.set_page_load_timeout(10)
                    driver.get(visit)
                    time.sleep(3)
                    driver.save_screenshot("Above Fold images/" + title2 + "/" + str(VISIT_COUNT) + ".png")
                    VISIT_COUNT+=1
                    print(f"{VISIT_COUNT} {title2} Image Download")
                    text_box(f"{VISIT_COUNT} {title2} Image Download\n")
                except TimeoutException as TO:
                    print(str(TO))
                    pass
                except urllib3.exceptions.ReadTimeoutError:
                    pass
                    print("Web Page TimeOut!")
                except WebDriverException:
                    pass
                    print("WebDriverException")
                except requests.exceptions.ConnectionError:
                    pass
                    print("requests.exceptions.ConnectionError")
                except requests.exceptions.ReadTimeout:
                    pass
                    print("requests.exceptions.ReadTimeout")
                except socket.timeout:
                    pass
                    print("socket.timeout")
                except urllib.error.HTTPError as e:
                    pass
                    print("6")
                    print('HTTPError: {}'.format(e.code))
                except urllib.error.URLError as e:
                    pass
                    print("urllib.error.URLError")
                    print('URLError: {}'.format(e.reason))
                except OSError:
                    pass
                    print("Os Error")
                    VISIT_COUNT+=1
                if VISIT_COUNT >= int(No_of_img):
                    break
            VISIT_COUNT = 0
            print(f"************************{title2} Above Fold Images Downloading start*****************************")
            ABOVE_count+=1
            if ABOVE_count >= int(No_of_tab):
                break
        driver.close()
        print(f"************************Above Fold Images Download Successfully*****************************")
        text_box("Above Fold Images Download Successfully")
    except selenium.common.exceptions.WebDriverException:
        print("!!!!!!!!!!!!!!!!!!!! Internet Probleme, Or My Be You Close Browser !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# for windows GUI 
root = Tk()
root.title("Download Bulk Images From Bing")
root.geometry("500x500+500+500")

frame = Frame(root, borderwidth=1, bg="#e5e5e5", pady=10, padx=10)
frame.pack()

frame1 = LabelFrame(frame, text="Enter Search Keyword", bg="#e5e5e5", padx=5, pady=5, width=310)
frame1.pack()

frame7 = LabelFrame(frame, text="How Much Tabs You Need To Scrape", bg="#e5e5e5", padx=5, pady=5, width=310)
frame7.pack()

frame2 = LabelFrame(frame, text="Select Directory", bg="#e5e5e5", padx=8, pady=5, width=310)
frame2.pack()

frame4 = LabelFrame(frame, text="Number Of Images (number only)", padx=8, pady=5, width=310)
frame4.pack()

frame6 = LabelFrame(frame, text="Get Start", padx=8, pady=5, width=310, bg="#e5e5e5")
check_label = Label(frame6, text="Hide Browser", bg="#e5e5e5")
check_label.grid(row=0, column=0, pady=5)

check = IntVar(value=1)
check_btn1 = Checkbutton(frame6, variable=check, bg="#e5e5e5")
check_btn1.grid(row=0, column=1, pady=5)

start_button = Button(frame6, text="START PROGRAM", command=get_input, width=50)
start_button.grid()
frame6.pack(pady=20)

input3 = Entry(frame4, width=300)
input3.pack(padx=6, pady=5)

complete_image = StringVar()
Hq_imgs = StringVar()
tot_found = StringVar()
frame5 = LabelFrame(frame, text='Do Not Close Program Until The Completion Task', bg="#e5e5e5", padx=8, pady=5, width=310)

total_images = Label(frame5, textvariable=tot_found, font = "Calibri 11", bg="#e5e5e5")
total_images.grid(row=0, column=0)
image_found = Label(frame5, text="Images Found Total", font = "Calibri 11", bg="#e5e5e5")
image_found.grid(row=0, column=1, ipady=3)

complete_img = Label(frame5, textvariable=complete_image, font = "Calibri 11", bg="#e5e5e5")
complete_img.grid(row=1, column=2)
fold_img = Label(frame5, text="Get Fold Above Images", font = "Calibri 11", bg="#e5e5e5")
fold_img.grid(row=1, column=1, ipady=3)

cent_lab = Label(frame5, text="HQ Images Download", font = "Calibri 11", bg="#e5e5e5")
cent_lab.grid(row=2, column=1, ipady=3)
get_hq_img= Label(frame5, textvariable=Hq_imgs, font = "Calibri 11", bg="#e5e5e5")
get_hq_img.grid(row=1, column=2)
frame5.pack()

frame5 = LabelFrame(frame, text="Program Log", bg="#e5e5e5", padx=8, pady=5, width=310)
frame5.pack()

input1 = Entry(frame1, width=300)
input1.pack(padx=6, pady=5)

input4 = Entry(frame7, width=300)
input4.pack(padx=6, pady=5)

scrool_y = Scrollbar(frame5)
log_box = Text(frame5, width=300, height=100, wrap="word", state='disabled', yscrollcommand=scrool_y.set, relief='groove')
scrool_y.config(command=log_box.yview)
scrool_y.pack(side=RIGHT, fill=Y)
log_box.pack()

# main loop close
root.mainloop()