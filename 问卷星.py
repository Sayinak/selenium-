from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def smart_fill_simple():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://v.wjx.cn/vm/OxRveN0.aspx")

    while not driver.find_elements(By.XPATH, "//*[@id='countdownHtml']/a"):
        time.sleep(0.5)

    driver.execute_script("refreshWin();")
    time.sleep(0.5)


    # 智能填写映射
    field_rules = {
        '名': 'name',
        '班级': 'class',
        '学号': 'id',
        '手机号': 'phone number',
        '电话':'phone number',
        '学院':'school',
        '输':''
    }
    # 找到所有字段标签
    field_labels = driver.find_elements(By.XPATH, "//div[contains(@class, 'topichtml')]")

    for label_element in field_labels:
        label_text = label_element.text.strip()

        # 匹配字段类型
        for keyword, value in field_rules.items():
            if keyword in label_text:

                # 找到对应的输入框
                field_label_parent = label_element.find_element(By.XPATH, "./ancestor::div[@class='field-label']")
                input_container = field_label_parent.find_element(By.XPATH,"./following-sibling::*[1]")
                input_field = input_container.find_element(By.TAG_NAME, "input")
                if keyword != '输':
                    # 填写内容
                    input_field.clear()
                    input_field.send_keys(value)
                    print(f"✅ 填写 {label_text}: {value}")
                elif keyword=='输':
                    input_field.clear()
                    value=str(label_text[3::])
                    input_field.send_keys(value)
                    print(f"✅ 填写 {label_text}: {value}")
                break
    time.sleep(0.1)

    try:
        sensitive_label = driver.find_element(By.XPATH, "//*[@id='sensitiveInfoWrap']/label")
    except NoSuchElementException:
        print('')
    else:
        sensitive_label.click()



    # 提交
    submit_btn = driver.find_elements(By.XPATH, "//*[@id='ctlNext']")
    if submit_btn:
        submit_btn[0].click()
        print("✅ 已提交！")
    time.sleep(1)
    driver.quit()


if __name__ == "__main__":
    smart_fill_simple()
