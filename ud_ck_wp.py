from bs4 import BeautifulSoup as bs4
import requests
import schedule
import time

cv_url='https://coursekingdom.xyz'

def getCVLinks():
    cv_links_data = []
    cv_divs = []
    cv_page = requests.get(cv_url+'/courses')
    soup = bs4(cv_page.text, 'html.parser')
    #print(soup.prettify())
    courses = soup.find_all('div', class_='single_courses')
    #print(courses)
    for course in courses:
        cv_div_soup = course.find('div', class_='thumb')
        cv_divs.append(cv_div_soup)
    for cv_div in cv_divs:
        # cv_link = cv_div.find('a').text.strip() # gets all the text inside the a tag, acts like innerHtml
        cv_link = cv_div.find('a')['href']
        cv_links_data.append(cv_link)

    #print(cv_links_data)
    return cv_links_data
    # print(cv_page.status_code)

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

def getUdemyCourse(ck_course_url):
    udemy_course = requests.get(cv_url+ck_course_url)
    soup_udemy_course = bs4(udemy_course.text, 'html.parser')
    #print(soup_udemy_course)
    respon = ""
    try:
        ck_coupon_a_tag = soup_udemy_course.find('i', class_='fas fa-sign-in-alt').parent;
        ck_url = ck_coupon_a_tag['href'].split('?ulp=');
        ud_coupon_url = ck_url[1].split('&source=')[0]
        ud_course_img_div = soup_udemy_course.find('div', class_='video_thumb')
        imgElem = ud_course_img_div.find('img')['src']
        titleElem = soup_udemy_course.find("h1", class_='display1')
        descElem = soup_udemy_course.find("div", class_='single_courses')
        isCourseFound = get_coupon(titleElem.getText())

        if isCourseFound:
            print(isCourseFound)
        else:
            print("new course")
            respon = create_coupon_wp(titleElem.getText(), descElem.getText(), imgElem, ud_coupon_url)
            print(respon)
    except:
        print("Some error occurred")
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
    for clink in cv_links:
        getUdemyCourse(clink)

def job():
    scrapper()

# schedule.every(3).minutes.do(job)
# #schedule.every(6).hours.do(job)
# while True:
#    schedule.run_pending()
#    time.sleep(1)

job()