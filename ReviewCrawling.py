
def ReviewCrawler(URL):
    from selenium import webdriver
    import time
    import pandas as pd
    url = URL

    driver = webdriver.Chrome("/Users/hansuho/PycharmProjects/chrome_driver/chromedriver")
    driver.get(url)
    # driver.maximize_window()
    time.sleep(5)


    review_dict = {}
    try:
        total_review_window = driver.find_element_by_class_name("lNyfxzGc")
        total_rating = total_review_window.find_element_by_css_selector(".DrjyGw-P._1SRa-qNz._3t0zrF_f._1QGef_ZJ").text
        total_review_cnt = total_review_window.find_element_by_css_selector(".DrjyGw-P._26S7gyB4._14_buatE._2nPM5Opx").text

        satisfactions = total_review_window.find_elements_by_css_selector("._1P_xnQHX")
        satisfactions_list = []
        for satisfaction in satisfactions:
            each_cnt = satisfaction.find_element_by_css_selector(".DrjyGw-P._26S7gyB4._1dimhEoy").text
            satisfactions_list.append(each_cnt)
        review_dict[0] = {'total_rating': total_rating, "total_review_cnt": total_review_cnt,
                          'very satisfied': satisfactions_list[0], 'satisfied': satisfactions_list[1],
                          'neither satisfied nor dissatisfied': satisfactions_list[2],
                          'dissatisfied': satisfactions_list[3], 'very dissatisfied': satisfactions_list[4]}
    except:
        pass


    review_num = 1
    for i in range(2):
        time.sleep(5)
        # contents = driver.find_element_by_class_name("_1c8_1ITO")
        # reviews = contents.find_elements_by_css_selector("div")
        reviews = driver.find_elements_by_css_selector("#tab-data-qa-reviews-0 > div > div._1c8_1ITO > div")

        for review in reviews[:-1]:  # reviews 는 한 페이지에 있는 리뷰 10개
            try:
                writer = review.find_element_by_css_selector("._7c6GgQ6n._22upaSQN._37QDe3gr.WullykOU._3WoyIIcL").text
                review_title = review.find_element_by_class_name("_2tsgCuqy").text
                review_date = review.find_element_by_class_name("_3JxPDYSx").text
                content = review.find_elements_by_class_name("_2tsgCuqy")[1].text
                rating = review.find_element_by_class_name("zWXXYhVR").get_attribute("title")
                rating = rating[-3:]
                review_dict[review_num] = {"writer": writer, "review_title": review_title, "review_date": review_date,
                                           "content": content, "rating": rating}
            except:
                continue

            review_num += 1
        if i < 1:    # 마지막 페이지에서는 다음 페이지로 넘어가지 않도록
            try:    # 페이지 다음 버튼 클릭
                next_button = driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a')
                driver.execute_script("arguments[0].click();", next_button)
            except:
                print("다음 페이지 리뷰가 없습니다.")
                break
        time.sleep(3)
    driver.close()
    return review_dict



## test
# a = ReviewCrawler('https://www.tripadvisor.co.kr/Attraction_Review-g1074321-d3805449-Reviews-Bongjeongsa_Temple-Andong_Gyeongsangbuk_do.html')
# print(a)


'''
pageNumbers Class 는 span -a -a -a  혹은 2페이지라면 a -span -a -a 의 형태로 이루어져있기 때문에
span.text (번호 출력) 번째의  a를 click해주면 됨
'''
'''
review = reviews[0].find_element_by_class_name("IRsGHoPm")
rating = reviews[0].find_element_by_css_selector(".ui_bubble_rating").get_attribute("class")
    # class="ui_bubble_rating bubble_50" 클래스 중간 공백은 클래스가 두 개로 분리돼있다는 것으로 이해하고 get_attribute로 class 가져옴
    # class끝이 평점에 따라서 숫자가 바뀌므로 공백으로 분리된 클래스 앞의 것을 잡아와서 전체 클래스명을 불러오는 과정
'''

