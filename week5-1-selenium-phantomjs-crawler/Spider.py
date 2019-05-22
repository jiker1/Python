import json, time
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains

results = []

def parse(response):    
    for comment in response.css('div.comment-item'):
        result = dict(
            name=comment.xpath(
                './/a[@class="name"]/text()').extract_first().strip(),
            content=comment.xpath(
                './/div[contains(@class, "content")]/text()'
            ).extract_first()
        )
        print("comment: {}".format(result))
        results.append(result)


def spider():
    driver = webdriver.Chrome()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    while True:
        driver.implicitly_wait(3)   # 隐式等待 3 秒，等待页面加载
        html = driver.page_source   # 获取页面源码
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        parse(response)
        # 如果第二个 li 标签的 class 属性中有 disabled 字样
        # 即表示没有下一页了
        if 'disabled' in response.css(
            'ul.pagination li::attr(class)').extract()[-1]:
            break
        # 点击下一页，因为 driver 无法定位到未显示在屏幕中的元素
        # 所以需要先定位到下一页按钮，再 click 
        ac = driver.find_element_by_xpath(
             '(//li[contains(@class, "page-item")])[2]')
        ActionChains(driver).move_to_element(ac).perform()
        time.sleep(1)
        ac.click()
    driver.quit()
    with open('comments.json', 'w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()
