# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 09:26:36 2018

@author: William Keilsohn
"""

#Import Packages:
import nltk, re, pprint
import urllib
from urllib import request
from urllib import request
import bs4
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
import re #https://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python


# Define our two urls:
'''
Removed for GitHub
'''

# Assign Reading levels to each Website:

def ARIText(site):
    ARIValue = 0
    response = request.urlopen(site) #Taken from what we did in class but also in textbook.
    raw = response.read().decode('utf8') #Same as Above
    searcher = re.search('<title>(.+?)</title>', raw) #https://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python
    # Does this based on the HTML5 tag for the title of a webpage. 
    if searcher:
        siteTitle = searcher.group(1) #https://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python
    searching = re.search('<h1(.+?)>', raw)
    if searching:
        h1 = searching.group(1)#https://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python
    h1 = "<h1" + h1 + ">(.+?)</h1>" #B/c This is the html tag I am looking for.
    title = re.search(h1, raw)
    if title:
        fullHead = title.group(0) #Foud via counsole.
    raw2 = raw[raw.index(fullHead):] #Trying to cut off a section of code (probably CSS and JavaScript) that is cramed in the top of the webpages.
    #Also want to cut off a section at the bottom that contains similar material, so I just get the text.
    if site == url1:
        bottomCropper = "ITIS Report: Octopoda Leach, 1818" #References have a huge impact on the reading score. Also, how many people actually read the citations on Wikipedia???
    elif site == url2:
        bottomCropper = "Copyright" #Everything after this is either a hyperlink or javaScript. 
        #bottomCropper = "doi:10.1126/science.aav4851" #This is for the other article.
    page = BeautifulSoup(raw2, "html5lib").get_text() #http://www.nltk.org/book/ch03.html
    page2 = page[:page.index(bottomCropper)] #Cut off the last bit.
    #I do still get some Css, but overall a huge improvement. 
    #https://www.crummy.com/software/BeautifulSoup/
    #Turns out an html document is better processed as an html document.
    page3 = page2.replace("\n", " ") #https://www.tutorialspoint.com/How-to-remove-specific-characters-from-a-string-in-Python
    #Don't want a bunch of extra lines. 
    if site == url1:
        page3 = page3.replace("\u202f", " ")#https://www.fileformat.info/info/unicode/char/202f/index.htm
        #Due to a table in the middle of the page there is an extra set of characters.
    page4 = ''.join([i for i in page3 if not i.isdigit()])#https://stackoverflow.com/questions/12851791/removing-numbers-from-string
    page3 = re.sub("[!@#$%'-^&*.,{};:()]", '', page3) #https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
    words = word_tokenize(page3) #http://www.nltk.org/book/ch03.html
    words2 = [i for i in words if i.isalpha()] #Assuming numbers (and special characters) aren't words.
    # Also, we want a reading level. Most people (including kids) use a different skill set for numbers than reading.
    #https://www.ams.org/notices/200102/rev-devlin.pdf
    sents = sent_tokenize(page4)
    if site == url1:
        sents.remove(sents[299]) #Table...
    for i in sents:
        i = re.sub("[!@#$%'-^&*.,{};:()]", '', i)#https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
    wordLen = [len(i) for i in words2]
    sentWords = [word_tokenize(i) for i in sents]
    for x in sentWords:#Remember no numbers or special characters
        x = [y for y in x if y.isalpha()]
    sentLen = [len(x) for x in sentWords]#Need a list after all.            
    charVal = sum(wordLen)/len(wordLen) #https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
    wordVal = sum(sentLen)/len(sentLen) #https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
    ARIValue = (4.71 * (charVal)) + (0.5 * (wordVal)) - 21.43 #Based on excersise 29
    ARILis = [ARIValue, siteTitle]
    #print(page3)
    return ARILis

# Evaluate the reading score: https://en.wikipedia.org/wiki/Automated_readability_index

def ARIValidator(num): #It appares that for the most part the number corresponds to a grade level.
    if num >= 14:
        return "Professor"
    elif num >= 13:
        return "College Student"
    elif num >= 12:
        return "Twelfth Grade Student"
    elif num >= 11:
        return "Eleventh Grade Student"
    elif num >= 10:
        return "Tenth Grade Student"
    elif num >= 9:
        return "Ninth Grade Student"
    elif num >= 8:
        return "Eighth Grade Student"
    elif num >= 7:
        return "Seventh Grade Student"
    elif num >= 6:
        return "Sixth Grade Student"
    elif num >= 5:
        return "Fifth Grade Student"
    elif num >= 4:
        return "Fourth Grade Student"
    elif num >= 3:
        return "Third Grade Student"
    elif num >= 2:
        return "First or Second Grade Student"
    elif num >= 1:
        return "Kindergartener" 
    else:
        return "Youtube comment section"


# Produce results:

def outputer(url):
    print("The wepage: ")
    print(ARIText(url)[1])
    print("\n")
    print("The url of the webpage is: ")
    print(url)
    print("\n")
    print("The website has a reading score of: ")
    print(str(ARIText(url)[0]))
    print("\n")
    print("This corresponds to a: ")
    print(ARIValidator(ARIText(url)[0]))
    print("\n")
    
outputer(url1) #Answers questions for website 1
outputer(url2) #Answers questions for website 2
    
    