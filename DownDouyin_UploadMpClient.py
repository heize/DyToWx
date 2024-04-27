
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO


class DownDouyin_UploadMpClient:
    def __init__(self):
        option=webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('start-maximized')
        option.add_argument('window-size=1920x3000')
        # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # option.add_argument("--remote-debugging-port=9222")

        self.driver=webdriver.Chrome(options=option)

    def QgSleep(self,timeleft,title=''):
        if title=='':
            title='等待'
        _time = timeleft
        while _time>0:
            print(f"{title}_{_time}")
            time.sleep(1)
            _time=_time-1

    def Login(self):
        self.driver.get("https://mp.weixin.qq.com/")
        self.QgSleep(3,'等待打开首页')

        imgLi = self.driver.find_elements(By.CLASS_NAME, "login__type__container__scan__qrcode")
        if len(imgLi)>0:
            print('get login qrcode')
            image222 = imgLi[0].screenshot_as_png
            image_data = BytesIO(image222)
            return Image.open(image_data)
        else:
            return None

    def IsChromeOnline(self):
        try:
            self.driver.get("https://mp.weixin.qq.com/")
        except Exception as ex:
            print(ex)
            return False
        
        return True

    def Logout(self):
        self.driver.get("https://mp.weixin.qq.com/cgi-bin/logout?t=wxm-logout")
        self.QgSleep(3,'等待访问网页')

    def GetLogoAndName(self):
        list = self.driver.find_elements(By.XPATH, "//div[@class='weui-desktop-account__info weui-desktop-layout__side-menu__footer-item']//img")
        if len(list)==1:
            logo = list[0].get_attribute("src")
            list = self.driver.find_elements(By.XPATH, "//div[@class='weui-desktop-account__info weui-desktop-layout__side-menu__footer-item']//span[@class='acount_box-nickname']")
            name = list[0].text
            return [logo,name]
      
        return None


    def UploadToMp(self, filepath, filename, title, request):
        try:
            self.driver.get("https://mp.weixin.qq.com/")
            self.QgSleep(3,'等待打开首页')

            while True:
                list = self.driver.find_elements(By.XPATH, "//li[@class='weui-desktop-menu__item weui-desktop-menu_create menu-fold']")
                if len(list)>0:
                    list[0].click()
                    self.QgSleep(1,'展开内容与互动菜单')

                list = self.driver.find_elements(By.XPATH, "//a[@class='weui-desktop-menu__link menu_report']")
                if len(list)>0:
                    for x in list:
                        print(x.get_attribute("title"))
                        if x.get_attribute("title") == "素材库":
                            x.click()
                            break
                    break
                else:
                    self.QgSleep(2,'等待素材库按钮')

            self.QgSleep(2,'点击素材库按钮')

            while True:
                list = self.driver.find_elements(By.XPATH, "//li[@class='weui-desktop-tab__nav']")
                if len(list)>0:
                    for x in list:
                        print(x.get_attribute("title"))
                        if x.text.find("视频") != -1:
                            x.click()
                            break
                    break
                else:
                    self.QgSleep(2,'视频按钮')

            self.QgSleep(2,'点击视频按钮')

            list = self.driver.find_elements(By.TAG_NAME, "button")
            for x in list:
                print(x.text)
                if x.text == "添加":
                    x.click()
                    break

            self.QgSleep(4,'点击完添加，等待加载页面')

            #切换当前标签页
            current_windows = self.driver.window_handles
            self.driver.switch_to.window(current_windows[1])

            item = self.driver.find_elements(By.XPATH , "//dt[@class='weui-desktop-form__dropdowncascade__dt weui-desktop-form__dropdowncascade__dt__inner-button placeholder']")
            item[0].click()
            self.QgSleep(1)

            item = self.driver.find_elements(By.XPATH , "//ul[@class='weui-desktop-dropdown__list__section__list']/li[1]")
            item[0].click()
            self.QgSleep(1)

            item = self.driver.find_elements(By.XPATH , "(//ul[@class='weui-desktop-dropdown__list__section__list'])[2]/li[1]")
            item[0].click()
            self.QgSleep(2,'设置分类完成')

            self.driver.find_element(By.XPATH, "//input[@class='weui-desktop-upload-input']").send_keys(filepath)

            #协议
            self.driver.find_element(By.XPATH, "//label[@class='weui-desktop-form__check-label weui-desktop-form__tool__tips video-setting__footer-link']//i").click()
            #封面
            while True:
                list = self.driver.find_elements(By.XPATH, "//img[@class='cover__options__item__image']")
                if len(list)>0:
                    self.QgSleep(3,'封面待点击')
                    list[1].click()
                    break
                else:
                    self.QgSleep(2,'封面')

            self.QgSleep(7,'选择封面完毕')
            list = self.driver.find_elements(By.XPATH, "//div[@class='weui-desktop-dialog__wrp weui-desktop-dialog_img-picker weui-desktop-dialog_img-picker-with-crop']//button[@class='weui-desktop-btn weui-desktop-btn_primary']")
            if len(list)==5:
                list[4].click()

            self.QgSleep(10,'设置封面完成')

            #保存
            while True:
                list = self.driver.find_elements(By.XPATH, "//div[@class='video-setting__footer-btns-group']//button[@class='weui-desktop-btn weui-desktop-btn_primary']")
                if len(list)>0:
                    list[0].click()
                    break
                else:
                    self.QgSleep(2,'保存按钮')

            self.QgSleep(5,'保存完成等待关闭')
            # self.driver.save_screenshot(r"d:\done1.png")

            self.driver.close()
            #焦点在已关闭的标签上，还得切换回第一个
            self.driver.switch_to.window(current_windows[0])

            # self.driver.save_screenshot(r"d:\done2.png")

            print("完成")
            request.record_upload(filename ,title)
        except Exception as ex:
            print(ex)
            self.driver.save_screenshot(r"d:\error1.png")
            