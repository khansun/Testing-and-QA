import re, json, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def _login(email, password):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option('excludeSwitches', ['enable-logging']) 
    browser = webdriver.Chrome("chromedriver.exe", options=option)
    browser.get("http://facebook.com")
    time.sleep(5)
    browser.maximize_window()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))).send_keys(email)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']"))).send_keys(password)
    #target the login button and click it
    button = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(5)
    return browser


def _extract_comments(bs_data, export_html=False):
    if(export_html):
        with open('./bs.html',"w", encoding="utf-8") as file:
            file.write(str(bs_data.prettify()))

    k = bs_data.find_all("div", {"class": "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"})

    with open('comments.txt', 'w', encoding='utf-8') as f:
        for item in k:
            try:
                comment = re.search('start;">(.+?)<', str(item)).group(1)
                f.write(str(comment)+"\n")
            except AttributeError:
                pass
    print("Exported ./comments.txt")



def _count_needed_scrolls(browser, infinite_scroll, numOfPost):
    if infinite_scroll:
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        )
    else:
        # roughly 8 posts per page scroll
        lenOfPage = int(numOfPost / 8)
    print("Number Of Scrolls Needed " + str(lenOfPage))
    return lenOfPage


def _scroll(browser, infinite_scroll, lenOfPage):
    lastCount = -1
    match = False

    while not match:
        if infinite_scroll:
            lastCount = lenOfPage
        else:
            lastCount += 1

        time.sleep(8)

        if infinite_scroll:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")

        if lastCount == lenOfPage:
            match = True

def openComment(browser):    
    moreComment = browser.find_elements(By.XPATH, "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v lrazzd5p m9osqain') and starts-with(text(), 'View') and contains(text(), 'more comments')]")
    
    print("Found", len(moreComment), "more comments")
    if len(moreComment) > 0:
        count = 0
        for i in moreComment:
            action=ActionChains(browser)
            try:
                action.move_to_element(i).click().perform()
                count += 1
            except:
                try:
                    browser.execute_script("arguments[0].click();", i)
                    count += 1
                except:
                    continue
        if len(moreComment) - count > 0:
            print('moreComment issue:', len(moreComment) - count)
        time.sleep(1)
    else:
        pass
    
def extractComments(browser, page, numOfPost, infinite_scroll=False):
    browser.get(page)
    lenOfPage = _count_needed_scrolls(browser, infinite_scroll, numOfPost)
    _scroll(browser, infinite_scroll, lenOfPage)
    print("Opening comments...")
    openComment(browser)
    source_data = browser.page_source
    bs_data = bs(source_data, 'html.parser')

    _extract_comments(bs_data)
    browser.close()


if __name__ == "__main__":
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    fb_page = "https://www.facebook.com/DailyProthomAlo"
    browser = _login(email, password)
    extractComments(browser=browser, page=fb_page, numOfPost=100, infinite_scroll=False)
    