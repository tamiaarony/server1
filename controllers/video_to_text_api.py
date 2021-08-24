import json
from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask_cors import cross_origin
import pandas as pd
from time import sleep
from selenium import webdriver # for interacting with website
app = Flask(__name__)

def open_url_in_chrome(url, mode='headed'):
    #print(f'Opening {url}')
    if mode == 'headed':
        options = webdriver.ChromeOptions()
        #options.add_argument("start-maximized")
            
    elif mode == 'headless':   
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')    
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    
    driver.get(url)
    return driver

def accept_T_and_C(driver):
    """
    Accept terms and conditions.
    
    ### Old Code ###
    # Click 'No thanks'
    driver.find_element_by_xpath("//paper-button[@aria-label='No thanks']").click() # old
    driver.find_element_by_xpath("//*[@id='dismiss-button']").click() #new
    
    # Click 'I agree' https://stackoverflow.com/questions/64846902/how-to-get-rid-of-the-google-cookie-pop-up-with-my-selenium-automation
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src, 'consent.google.com')]"))
    sleep(1)
    driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
    sleep(3)
    driver.refresh()
    #################
    
    """
    # Click I agree
    driver.find_element_by_xpath("//*[@id='yDmH0d']/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/div[2]").click()
    # sleep(2)
    try:
        # click 'no thanks' if it pops up
        driver.find_element_by_xpath("//*[@id='dismiss-button']").click()
    except:
        # sleep(2)
        pass
#פונקצית תמלול  
def get_transcript(driver, mode):
    
    global count 
    driver.implicitly_wait(10)
    
    if mode=='headed':
        print('Accepting Terms and Conditions')
        accept_T_and_C(driver)
        
        # Click 'More actions' (full xpath)
        #driver.find_elements_by_xpath("//button[@aria-label='More actions']")[1].click()
        driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button").click()
        
        # Click 'Open transcript'
        driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()
        # sleep(3)
    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button").click()

        except:
            # sleep(3)
            count += 1
            if count < 5:
                driver.refresh()
                get_transcript(driver, mode)
            else:
                print("Error loading page.")
                return None
        
        # Click 'open transcript'
        try:
            #driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/paper-item").click()
            driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()

        except:
            # sleep(3)
            count += 1
            if count < 5:
                driver.refresh()
                get_transcript(driver, mode)
            else: 
                print("Error loading page.")
                return None
            
    
    # Get all transcript text
    print("Copying transcript ")
    transcript_element = driver.find_element_by_xpath("//*[@id='body']/ytd-transcript-body-renderer")
    transcript = transcript_element.text
    return transcript
#פונקציה המעצבת את הטקסט
def transcript2df(transcript):
    if transcript == None:
        return "None in transcript."
    transcript = transcript.split('\n')
    transcript_timestamps = transcript[::2]
    transcript_text = transcript[1::2]
    dic={}
    j=0
    for i in transcript_timestamps:
        dic[i]=transcript_text[j]
        j+=1
    print(dic)

    df = pd.DataFrame({'timestamp':transcript_timestamps, 
                   'text':transcript_text})
    
    return df
#פונקציה שמקבלת ניתוב ומנהלת את כל התמלול
def GetTranscript(url):
    
    mode = 'headless'
    #שולח נתיב ומקבל את הדף
    driver = open_url_in_chrome(url, mode)
    #שולח דף ומקבל תמלול
    transcript = get_transcript(driver, mode)
    #סוגר את הדף
    driver.close()
    #עיצוב הטקסט
    df = transcript2df(transcript)
    print('Saving transcript ')
    #שמירה לקובץ
    df.to_csv('out_transcript_timestamped.csv', index=False) 
    with open("out_transcript_text_only.txt", "w") as text_file:
        print(" ".join(" ".join(df.text.values).split()), file=text_file)
    print('Done')
    #החזרת התמלול
    return " ".join(" ".join(df.text.values).split())

@app.route('/Transcrire', methods=['POST'])
@cross_origin()  # מגשר בין הפייתון לריאקט
def upload_file():
    if request.method == 'POST':
      #get the url and convert to string
      url=request.get_data(parse_form_data=True).decode("utf-8") 
      return jsonify(GetTranscript(url))
    else:
      return 'No file'


if __name__ == "__main__":
  count=0
  app.run(debug=True)  # בריענון של הדף נותן שינויים שלא יצטרכו לפתוח שוב
