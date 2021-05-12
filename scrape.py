from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd




def scrape_all():

    executable_path = {"executable_path": "C:/Users/XPS9360/Documents/scraping/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)  

    dfs = {

        'hhri' : hhri(browser),
        'sentera' : sentera(browser),
        'gvrnment' : gvrnmt_jobs(browser),
        'nasa' : nasa(browser)
    }

    browser.quit()

    return dfs


def hhri(browser):


    url = 'https://hhri.applicantpro.com/jobs/'
    browser.visit(url)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    posis_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

#        posis = posis_soup.find_all("div", class_="list-group job-listings")
        posis = posis_soup.find_all("h4")

        headers = [h.get_text().replace('\n','') for h in posis]

        df = pd.DataFrame(headers)
        df.columns = ['Title']

    except AttributeError:
        return None

    return df.to_html(classes="table table-striped",index=False)




def sentera(browser):


    url = 'https://sentera-inc.oasisrecruit.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    posis_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        posis = posis_soup.find_all("div", class_="job-title-and-category")
        headers = [h.get_text().replace('\n','') for h in posis]

        df = pd.DataFrame(headers)
        df.columns = ['Title']

    except AttributeError:
        return None

    return df.to_html(classes="table table-striped",index=False)


def gvrnmt_jobs(browser):
    url = 'https://www.governmentjobs.com/jobs?keyword=data+scientist&location=minnesota+'
    browser.visit(url)    

    html = browser.html
    posis_soup = soup(html, 'html.parser')
    
    
    try:
        # Keep ourselves in the list elements
        list_elem = posis_soup.find_all("li", class_= 'job-item')

        #print(list_elem)

        # take all the text from the h3 tags (job titles)
        titles = [h.find('h3').get_text().replace('\n','') for h in list_elem]  

        df = pd.DataFrame(titles)
        df.columns = ['Title']

        
    
    except AttributeError:
        return None
    
    return df.to_html(classes="table table-striped",index=False)

def nasa(browser):
    
    url = 'https://earthobservatory.nasa.gov/topic/image-of-the-day'
    
    browser.visit(url)    

    html = browser.html
    posis_soup = soup(html, 'html.parser')
    
    try:
        # Keep ourselves in the list elements
        list_elem = posis_soup.find_all("div", class_= 'thumbnail-image')
        img_urls = [a.img['src'] for a in list_elem]

      
    
    except AttributeError:
        return None
    
    return img_urls[0]