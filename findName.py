import time
from lxml import html
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from collections import Counter
import re


def handleText(summaryList, excludeWords):
    wordList = []
    for ele in summaryList:
        for word in ele.split():
            word = word.lower()
            if word not in excludeWords:
                if ',' in word:
                    word = word.replace(",", "")
                if ':' in word:
                    word = word.replace(":", "")
                if '(' in word:
                    word = word.replace("(", "")
                if ')' in word:
                    word = word.replace(")", "")
                if re.search('[a-z]', word):
                    wordList.append(word)
    return wordList


def closePopup(driver):
    time.sleep(3) #Wait for page to catch up
    try:
        driver.find_element_by_id("prime-popover-close-button").click()
    except Exception as e:
        #print("Error: " + str(e))
        pass
    try:
        driver.find_element_by_id("popover-x-button")
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except Exception as e:
        #print("Error: " + str(e))
        pass


def nextPage(driver):
    driver.switch_to_window(driver.window_handles[0])
    driver.find_element_by_class_name("np").click()
    time.sleep(3) #Wait for page to catch up
    closePopup(driver)


def scrape(driver, summaryList):
    counter = 0;
    pageAmt = input("How many pages would you like to scan: ")
    while(counter < int(pageAmt)):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jobtitle')))
            
        jobListings = []
        jobListings = driver.find_elements_by_class_name("jobtitle")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Page #" + str(counter+1) + " has " + str(len(jobListings)) + " job listings.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for i in jobListings:
            try:
                i.click()
            except Exception as e:
                #print("Error: " + str(e))
                pass

            try:
                element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'summary')))
                time.sleep(1) #Wait for page to catch up
                
                driver.switch_to_window(driver.window_handles[1])
                try:
                    jobSummary = driver.find_element_by_class_name("summary")
                    summaryList.append(jobSummary.text)
                    print("Job Added!")
                except Exception as e:
                    #print("Error: " + str(e))
                    pass
            except Exception as e:
                #print("Error: " + str(e))
                continue
            
            driver.close()
            driver.switch_to_window(driver.window_handles[0])

        nextPage(driver)
        counter = counter + 1


def analyzeData(wordList):
    counter = 0
    for word in wordList:
        counter = counter + 1
    print("\nScraped " + str(counter) + " words.")
    cnt = Counter(wordList)
    
    while True:
        userInput = input("\nWhat would you like to do?\n0.)Exit\n1.)Display x amount "
                          "of words found\n2.)Search for specific word\n")
        if userInput == '0':
            break
        
        elif userInput == '1':
            wordAmt = input("How many words would you like to output: ")
            for word in cnt.most_common(int(wordAmt)):
                print(word)
            
        elif userInput == '2':
            userInput = input("What word would you like to search for: ")
            
            for tupl in cnt.most_common(len(wordList)):
                if userInput in tupl:
                    print(tupl)
                    break


def initalize():
    excludeWords = ['and', 'to', 'the', 'of', 'with', 'a', 'in', 'or', 'for', 'work',
                    'as', 'an', 'are', 'is', 'our', 'that', 'on', 'be', 'applications',
                    'skills', 'ability', 'all', 'must', 'understanding', 'strong', 'will',
                    'usingwe', 'knowledge', 'years', 'job', 'we', 'you', 'using', 'user',
                    'required', 'building', 'related', 'such', 'environment', 'requirements',
                    'at', 'technologies', 'responsibilities', 'working' ,'other' ,'from',
                    'systems', 'data', 'application', 'like', 'this', 'level', 'developer',
                    'perform', 'company', 'developers', 'your', 'excellent', 'technical',
                    'maintain', 'new', 'good', 'best', 'technology', 'product', 'help',
                    'including', 'products', 'communication', 'developing', 'not',
                    'information', 'have', 'by', 'tools', 'about', 'build', 'position',
                    'support', 'services', 'production', 'full-time', 'type', 'able',
                    'within', 'well', 'materials', 'duties', 'it', 'field', 'responsible',
                    'process', 'industry', 'through', 'provide', 'and/or', 'may', 'ensure',
                    'include', 'time', 'high', 'up', 'use', 'provides', 'year', 'which',
                    'more', 'their', 'status', 'who', 'can', 'role', 'any', 'preferred', 'into',
                    'disability', 'across', 'opportunity', 'quality', 'one', 'us', 'looking',
                    'people', 'but', 'employment', 'join', 'required', 'etc.', 'familiarity',
                    'both', 'end', 'do', 'minimum', 'apply', 'plus', 'equal', 'status',
                    'based', 'practices', 'part', 'applicants', 'location', 'features',
                    'meet', 'large', 'equivalent', 'if', 'requirements', 'what', 'national',
                    'understand', 'need', 'has', 'how', 'gender', 'required', 'benefits',
                    'requirements', 'delier', 'multiple', 'get', 'every', 'take', 'out',
                    'when', 'some', 'bring', 'while', 'canidate', 'they', 'over', 'most',
                    'tasks', 'standards', 'should', 'big', 'great', 'also', 'closely']
    summaryList = []
    
    driver = webdriver.Firefox()
    page = driver.get('https://www.indeed.com/')
    search_bar = driver.find_element_by_xpath("//*[@id='text-input-what']")
    search_bar_location = driver.find_element_by_xpath("//*[@id='text-input-where']")

    search_bar_location.send_keys(Keys.CONTROL + "a")
    search_bar_location.send_keys(Keys.DELETE)

    jobTitle = input("Please enter a job title: ")
    jobLocation = input("Please enter a location, or press ENTER: ")
    search_bar.send_keys(jobTitle)
    search_bar_location.send_keys(jobLocation)
    search_bar.submit()

    closePopup(driver)
    
    scrape(driver, summaryList)

    
    wordList = handleText(summaryList, excludeWords)

    analyzeData(wordList)
    

initalize()
print("Finished")
