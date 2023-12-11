from bs4 import BeautifulSoup as bs4
import requests
import schedule
import time

cv_url='https://coursevania.com'

def getCVLinks():
    cv_links_data = []
    cv_divs = []
    cv_page = requests.get(cv_url)
    soup = bs4(cv_page.text, 'html.parser')
    # print(soup.prettify())
    courses = soup.find_all('div', class_='stm_lms_courses__single_animation')
    # print(courses)
    for course in courses:
        cv_div_soup = course.find('div', class_='stm_lms_courses__single--info_title')
        cv_divs.append(cv_div_soup)
    for cv_div in cv_divs:
        # cv_link = cv_div.find('a').text.strip() # gets all the text inside the a tag, acts like innerHtml
        cv_link = cv_div.find('a')['href']
        cv_links_data.append(cv_link)

    #print(cv_links_data)
    return cv_links_data
    # print(cv_page.status_code)

def getUDLinks(cv_links):
    ud_links_data = []
    for link in cv_links:
        ud_page = requests.get(link)
        soup = bs4(ud_page.text, 'html.parser')
        ud_course_div = soup.find('div', class_ = 'stm-lms-buy-buttons')
        ud_course_link = ud_course_div.find('a')['href']
        ud_links_data.append(ud_course_link)
    #print(ud_links_data)
    return ud_links_data

def get_coupon(title):
    #getPostUrl = 'http://localhost/cv/wp-json/wp/v2/coupon?_fields=acf.coupon_subtitle'
    getPostUrl = 'https://couponcity.tech/wp-json/wp/v2/coupon?_fields=acf.coupon_subtitle'
    respData = requests.get(getPostUrl)
    jsonList = respData.json()
    for acf in jsonList:
        if acf['acf']['coupon_subtitle'] == title:
            return True

def create_coupon_wp(title, content, image_url, coupon_url):
    curHeaders = {
        # For Local - "Authorization": "Basic YWRtaW46YWRtaW4=",
        "Authorization": "Basic YXBpdXNlcjpxMDRJTU9UWSRoRGpnKXF4RVpIWUc5NXQ=",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    acfDict = {
        "coupon_subtitle": title,
        "image_url": image_url,
        "coupon_url": coupon_url
    }
    postDict = {
        "title": title,
        "content": content,
        "status": "publish",  # 'draft'
        "slug": title,
        "coupontype": [28],
        "acf": acfDict
    }

    #yourHost = 'http://localhost/cv'
    yourHost = 'https://couponcity.tech'
    createPostUrl = yourHost + "/wp-json/wp/v2/coupon"  # 'https://www.crifan.com/wp-json/wp/v2/posts'

    resp = requests.post(
        createPostUrl,
        headers=curHeaders,
        #data=json.dumps(postDict),
        json=postDict,  # internal auto do json.dumps
    )

    return resp

def getUdemyCourse(ud_coupon_url):
    udemy_course = requests.get(ud_coupon_url)
    soup_udemy_course = bs4(udemy_course.text, 'html.parser')
    imgElem = soup_udemy_course.find("meta", {"property": "og:image"})
    titleElem = soup_udemy_course.find("h1", {"data-purpose" : "lead-title"})
    subTitleElem = soup_udemy_course.find("div", {"data-purpose": "lead-headline"})
    reviewElem = soup_udemy_course.find("span", {"data-purpose": "rating-number"})
    descElem = soup_udemy_course.find("div", {"data-purpose": "course-description"})
    isCourseFound = get_coupon(titleElem.getText())
    respon = ""
    if isCourseFound:
        print(isCourseFound)
    else:
        print("new course")
        #respon = create_coupon_wp(titleElem.getText(), descElem.getText(), imgElem['content'], ud_coupon_url)
        #print(respon)
    #mainContentWrapper = soup_udemy_course.find("div", class_="paid-course-landing-page__container")
    #enrollElem = mainContentWrapper.find("span", string="100% off")
    #enrollElem = mainContentWrapper.find("button", {"data-purpose": "buy-this-course-button"})
    return respon

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
        str1 += "\n\n"
    return str1

def scrapper():
    cv_links = getCVLinks()
    ud_links = getUDLinks(cv_links)
    for clink in ud_links:
        getUdemyCourse(clink)

def job():
    scrapper()

schedule.every(3).minutes.do(job)
#schedule.every(6).hours.do(job)
while True:
   schedule.run_pending()
   time.sleep(1)

#job()
