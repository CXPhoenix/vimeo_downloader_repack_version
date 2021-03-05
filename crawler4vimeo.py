"""
Request library:
    1. bs4
    2. selenium
    3.1 vimeo_dl (if you don't need to download original film)
    3.2 (optional if vimeo_dl can't use) vimeo_downloader
    4. time
"""

"""
20210305 23:47
    Can't use vimeo_dl in MacOS Catalina, so find a new library to replace old library: vimeo_downloader.
"""

from selenium import webdriver
from bs4 import BeautifulSoup as bs
#import vimeo_dl as vimeo
from vimeo_downloader import Vimeo
import time

def getAllFilmListFromVimeo(url):
    chrome = webdriver.Chrome('./chromedriver')
    chrome.get(url)
    time.sleep(5)
    # wait for js render finish
    cookies = None
    while cookies == None:
        try:
            cookies = chrome.find_element_by_link_text('Cookies')
        except:
            print('not ready')
    time.sleep(1)
    
    chrome.execute_script("window.scrollTo(0,document.getElementsByClassName('SectionGrid__GridItem-avy0mo-2')[9].offsetTop+100)")
    time.sleep(1)
    
    #show "Load more" button
    try:
        chrome.execute_script("document.getElementsByClassName('ifjMTK')[0].classList.replace('ifjMTK','bekpqx')")
    except:
        pass
    time.sleep(2)
    
    #show all films
    while True:
        try:
            loadMore = chrome.find_element_by_class_name('bekpqx')
            loadMore = loadMore.find_element_by_tag_name('button')
            # print(loadMore)
            loadMore.click()
            time.sleep(3)
            chrome.execute_script("window.scrollTo(0,document.getElementsByClassName('SectionGrid__GridItem-avy0mo-2')[document.getElementsByClassName('SectionGrid__GridItem-avy0mo-2').length-1].offsetTop+100)")
            time.sleep(1)
        except:
            print('read end')
            break
            
    # bs4 to select
    soup = bs(chrome.page_source, 'html.parser')
    titles = soup.find_all('a', {'class': 'VideoCard__TitleAnchor-sc-1w6ij7e-15 lcdyMA'})
    urls = []
    for title in titles:
        url = title.get('href')
        urls.append(url)
    return urls

def downloadOriginalFilms(urls: list):
    chrome = webdriver.Chrome()
    website = 'https://vimeo.com/'
    for url in urls:
        url = url.split('/')[-1]
        #chrome = webdriver.Chrome()
        chrome.get(website+url)
        time.sleep(1)
        chrome.execute_script("window.scrollTo(0,document.getElementsByClassName('_2qxn8')[1].offsetHeight + 400)")
        download1 = chrome.find_element_by_class_name('sc-jqCOkK.jivVNl')
        download1.click()
        time.sleep(3)
        download2 = chrome.find_elements_by_link_text('Download')
        download2[-1].click()

#def downloadBestFilms(urls, filePath):
#    website = 'https://vimeo.com/'
#    for url in urls:
#        url = url.split('/')[-1]
#        video = vimeo.new(website+url)
#        best = video.getbest()
#        #print(best.resolution, best.extension, best.url)
#        best.download(filepath=filePath)
        
#20210305 23:55 rewrite 
def downloadSpecifiedQualityFilms(targetQuality, urls, filePath):
    website = 'https://vimeo.com/'
    for url in urls:
        url = website + url.split('/')[-1]
        video = Vimeo(url)
        stream = video.streams
        #replace '/' to '-' is preventing path errors.
        filmTitle = '_'.join(video.metadata.title.split()).replace('/','-')
        for s in stream:
            if s.quality == '1080p':
                s.download(download_directory=filePath, filename=filmTitle)
                break
        else:
            print("Unable to find the specified quality")
                
        

if '__main__' == __name__:
    url = 'https://vimeo.com/howfun'
    allFilms = getAllFilmListFromVimeo(url)
    downloadSpecifiedQualityFilms('1080p', allFilms, "/Users/fhshwork/crawler/films")