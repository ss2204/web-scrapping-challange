#Import dependencies
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 

#Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)


#NASA Mars News
def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #Scrape the website and find the latest news title and paragraph text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        news_title = soup.find('div', class_='content_title').get_text()
        news_para = soup.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None
    return news_title, news_para


#JPL Mars Space Images - Featured Image
def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #Scrape the website and find the featured image url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        image_source = soup.find('img', class_='headerimage fade-in')['src']
        featured_image_url = f'https://spaceimages-mars.com/{image_source}'
    except AttributeError:
        return None 
    return featured_image_url


#Mars Facts
def mars_facts():
    #Scrape the website table using pandas
    try:
        mars_facts_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
        mars_facts_df.columns=['Description', 'Mars', 'Earth']
        mars_facts_df.set_index('Description', inplace=True)
    except BaseException:
        return None
    return mars_facts_df.to_html(classes="table table-striped")



# Mars Hemispheres
def hemisphere(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    #Initialize an empty list
    hemisphere_image_urls = []

    # Retrieve a list of all hemispheres
    links = browser.links.find_by_partial_text('Enhanced')

    for item in range(len(links)):
        #Initialize an empty dict
        hemisphere = {}
        
        #Find the element on each loop 
        browser.links.find_by_partial_text('Enhanced')[item].click()
        
        #Scrape the image data and add to dict
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        sample_text = browser.links.find_by_partial_text("Sample")
        hemisphere["img_url"] = sample_text["href"]
        
        #Append the dict to the list
        hemisphere_image_urls.append(hemisphere)
        
        #Navigate Backwards
        browser.back()
    return hemisphere_image_urls


#Main scraper
def scrape_all():
    news_title, news_para = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_para,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls
    }

    browser.quit()
    
    return data 