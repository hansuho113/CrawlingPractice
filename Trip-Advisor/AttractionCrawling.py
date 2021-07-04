from selenium import webdriver
import time
from ReviewCrawling import ReviewCrawler
import pandas as pd

url = "https://www.tripadvisor.co.kr/Search?q=%EB%AC%B8%ED%99%94%EC%9E%AC&searchSessionId=8EBF88D174A91ADC36646AB58D987C3F1625156723243ssid&searchNearby=false&geo=294196&sid=52B42C988B4F45369A66F8B2D64C5EDE1625156727562&blockRedirect=true"
# url = "https://www.tripadvisor.co.kr/Search?q=%EA%B0%95%EB%A6%89&searchSessionId=740C6C129A0D381066BC8A28C09074F01598103071455ssid&sid=185AFFCDF0EA41D59463255802FCBDE61608620844552&blockRedirect=true&ssrc=A&geo=1"
driver = webdriver.Chrome("/Users/hansuho/PycharmProjects/chrome_driver/chromedriver")
driver.get(url)
time.sleep(3)


# 더보기 버튼
view_more = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[3]/div/div/span[1]")
view_more.click()
time.sleep(2)

url_list = []
row_num = 1
total_dict = {}
title_dict = {}

for page in range(5):    # 다섯 페이지 데이터 수집
    contents = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div")
    # contents = driver.find_element_by_class_name("ui_columns is-multiline is-mobile")

    attractions = contents.find_elements_by_css_selector(".ui_column.is-12.content-column.result-card")
    # attractions = contents.find_elements_by_class_name("ui_column is-12 content-column result-card result-card-default")
    for attraction in attractions:
        try:
            attr_title = attraction.find_element_by_class_name("result-title")
            title = attr_title.text
            driver.execute_script("arguments[0].click();", attr_title)
            title_dict[row_num] = {'Title': title}
            # attr_title.click()
            # click은 안 되는데 execute_script하니깐 됨, 이유는 잘 모르겠음.

            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1]) # 마지막 탭으로 이동

            url = driver.current_url
            if "custome" not in url:
                url_list.append(url)
            row_num += 1

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except: # 중간 광고, NoSuchElementException
            pass
    next_button = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div/div/div/a[2]")
    next_button.click()
    time.sleep(3)


driver.quit()
time.sleep(2)

for i, url in enumerate(url_list):
    print(url)
    time.sleep(3)
    total_dict[i+1] = ReviewCrawler(url)
    time.sleep(3)

title_csv = pd.DataFrame.from_dict(title_dict)
review_csv = pd.DataFrame.from_dict(total_dict)

title_csv.to_csv("/Users/hansuho/PycharmProjects/SNS_Crawling/TripAdvisor_Crawler/TripAdvisor_data/"
                 "heritage_data/heritage_title.csv",
                 sep=',', encoding= 'utf-8-sig')
review_csv.to_csv("/Users/hansuho/PycharmProjects/SNS_Crawling/TripAdvisor_Crawler/TripAdvisor_data/heritage_data"
                  "/heritage_review.csv",
                  sep=',', encoding= 'utf-8-sig')
