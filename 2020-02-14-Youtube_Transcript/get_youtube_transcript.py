# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:08:09 2021
@author: I Kit Cheng

Title: get_youtube_transcript.py

Description: get transcript (auto-generated) from any youtube video.

"""

import pandas as pd
from time import sleep
import os
from selenium import webdriver # for interacting with website

def open_url_in_chrome(url, mode='headed'):
    #print(f'Opening {url}')
    if mode == 'headed':
        driver = webdriver.Chrome()
    elif mode == 'headless':   
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver.exe', options=options)
    
    driver.get(url)
    return driver

def accept_T_and_C(driver):
    # Click 'No thanks'
    driver.find_element_by_xpath("//paper-button[@aria-label='No thanks']").click()
    
    # Click 'I agree' https://stackoverflow.com/questions/64846902/how-to-get-rid-of-the-google-cookie-pop-up-with-my-selenium-automation
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src, 'consent.google.com')]"))
    sleep(1)
    driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
    sleep(3)
    driver.refresh()
    
def get_transcript(driver, mode):
    
    driver.implicitly_wait(10)
    
    if mode=='headed':
        try:
            print('Accepting Terms and Conditions')
            accept_T_and_C(driver)
        except:
            print("No T&Cs to accept.")
        
        print("Opening transcript")
        # Click 'More actions'
        driver.find_element_by_xpath("//button[@aria-label='More actions']").click() 
        
        # Click 'Open transcript'
        driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()
        sleep(3)
    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_elements_by_xpath("//button[@aria-label='More actions']")[1].click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
        
        # Click 'open transcript'
        try:
            driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
    
    # Get all transcript text
    print("Copying transcript ")
    transcript_element = driver.find_element_by_xpath("//*[@id='body']/ytd-transcript-segment-list-renderer")
    transcript = transcript_element.text

    return transcript

def transcript2df(transcript):

    transcript = transcript.split('\n')
    transcript_timestamps = transcript[::2]
    
    transcript_text = transcript[1::2]
    df = pd.DataFrame({'timestamp':transcript_timestamps, 
                   'text':transcript_text})
    
    return df

def main(url, mode='headless'):
    driver = open_url_in_chrome(url, mode)
    
    transcript = get_transcript(driver, mode)
    
    driver.close()
    	
    df = transcript2df(transcript)
    
    # Existing list of unique ingredients
    if not os.path.exists("./output"):
        os.makedirs("./output")

    print('Saving transcript ')
    path_to_transcript = "./output/"
    df.to_csv(f"{path_to_transcript}my_transcript_timestamped.csv", index=False) 
    with open(f"{path_to_transcript}my_transcript_text_only.txt", "w") as text_file:
        print(" ".join(" ".join(df.text.values).split()), file=text_file)
    print(f"Transcript saved to: {path_to_transcript}")

if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=5tvmMX8r_OM"
    mode = 'headed'
    main(url, mode)
    

    