# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:08:09 2021
@author: I Kit Cheng

Title: get_youtube_transcript.py

Description: get transcript (auto-generated) from any youtube video.

"""

import pandas as pd
from time import sleep
from selenium import webdriver # for interacting with website

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
    sleep(2)
    try:
        # click 'no thanks' if it pops up
        driver.find_element_by_xpath("//*[@id='dismiss-button']").click()
    except:
        sleep(2)
    
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
        sleep(3)
    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button").click()

        except:
            sleep(3)
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
            sleep(3)
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

def transcript2df(transcript):
    if transcript == None:
        return "None in transcript."
    transcript = transcript.split('\n')
    transcript_timestamps = transcript[::2]
    
    transcript_text = transcript[1::2]
    df = pd.DataFrame({'timestamp':transcript_timestamps, 
                   'text':transcript_text})
    
    return df

if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=5tvmMX8r_OM"
    
    mode = 'headed'
    
    driver = open_url_in_chrome(url, mode)
    
    count = 0
    transcript = get_transcript(driver, mode)
    
    driver.close()
    	
    df = transcript2df(transcript)
    
    print('Saving transcript ')
    df.to_csv('out_transcript_timestamped.csv', index=False) 
    with open("out_transcript_text_only.txt", "w") as text_file:
        print(" ".join(" ".join(df.text.values).split()), file=text_file)
    print('Done')
    