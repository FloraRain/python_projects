import pytest
import yaml
from appium import webdriver
import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestAddContact:
    def setup(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['appPackage'] = 'com.tencent.wework'
        desired_caps['appActivity'] = '.launch.LaunchSplashActivity'
        desired_caps['noReset'] = 'true'
        desired_caps['automationName'] = 'UiAutomator2'
        # desired_caps['dontStopAppOnReset'] = 'true'
        # desired_caps['settings[waitForIdleTimeout'] = 0
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(15)

    def teardown(self):
        self.driver.quit()

    def swip_find(self,text):
        num=3
        for i in range(num):
            try:
                element = self.driver.find_element(MobileBy.XPATH, f"//*[@text='{text}']")
                return element
            except:
                print("没找到元素，滑动一下")
                size = self.driver.get_window_size()
                width = size.get("width")
                height = size.get("height")
                start_x = width/2
                start_y = height*0.8
                end_x = start_x
                end_y = height*0.4
                self.driver.swipe(start_x,start_y,end_x,end_y,2000)
            if i == num -1:
                raise NoSuchElementException("没有找到该元素")



    @pytest.mark.parametrize(["name", "phonenum"], yaml.safe_load(open("./data.yaml")))
    def test_addcontact(self, name, phonenum):
        '''测试用例
        1. 打卡企业微信
        2. 点击通讯录
        3. 点击手动输入添加
        4. 输入姓名手机号码
        5. 点击保存
        6. 验证是否添加成功
        Note: 添加多个通讯录
        '''
        time.sleep(10)
        self.driver.find_element(MobileBy.XPATH, "//*[@text='通讯录']").click()
        self.driver.find_element(MobileBy.XPATH, "//*[@text='通讯录']").click()
        self.driver.update_settings({'waitForIdleTimeout': 0})
        self.swip_find("添加成员").click()
        self.driver.find_element(MobileBy.XPATH, "//*[@text='手动输入添加']").click()
        self.driver.find_element_by_id("com.tencent.wework:id/bf6").send_keys(name)
        self.driver.find_element_by_id("com.tencent.wework:id/ge0").send_keys(phonenum)
        self.driver.find_element(MobileBy.XPATH, '//*[contains(@text,"保存")]').click()
        toast_element = (MobileBy.XPATH, ".//*[@class='android.widget.Toast']")
        el = WebDriverWait(self.driver, 10,0.1).until(expected_conditions.presence_of_element_located(toast_element))
        print(el.get_attribute("text"))
