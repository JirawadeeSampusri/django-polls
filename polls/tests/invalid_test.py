from selenium import webdriver
import requests

def get_links(url: str):
    """Find all links on page at the given url.
       Return a list of all link addresses, as strings.
    """
    browser = webdriver.Chrome(executable_path=r"/Users/mac/Desktop/chromedriver")
    browser.get(url)
    linklist = browser.find_elements_by_tag_name('a')
    links =[]
    for i in linklist:
        if i.tag_name == 'a':
            url = i.get_attribute('href')
            links.append(url)
    browser.close()
    return links

x = get_links('https://cpske.github.io/ISP/')
for url in x:
    print(url)

def invalid_urls(u_list):
    inva_list = []
    for url in u_list:
        r = requests.head(url)
        if r.status_code == 404:
            inva_list.append(url)
    return inva_list     


if __name__ == "__main__":
    href_list = get_links("https://cpske.github.io/ISP/")
    for href in href_list:
        print("Valid: "+ href)
    invalid_url = invalid_urls(href_list)        
    for invalid in invalid_url:
        print("Broken: "+ invalid)
