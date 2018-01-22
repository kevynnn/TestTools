#coding:utf-8
from  selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import time
import sys


USER = 'xxx'
PASSWORD = 'xxx'
CHROME = r'D:\ToolsFiles\chromedriver.exe'

class CrackPush():
    def __init__(self):
        self.url = 'https://login.flyme.cn/sso?appuri=&useruri=http%3A%2F%2Fpush.meizu.com%2F&sid=unionlogin&service=garcia&autodirct=true'
        self.browser = webdriver.Chrome(executable_path=CHROME)
        self.username = USER
        self.pwd = PASSWORD

    def getBotton(self):
        """
        获取验证码按钮
        :return:按钮对象
        """
        botton = WebDriverWait(self.browser,20,0.5).until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')),message='没有找到验证码按钮')
        return botton

    def getSlider(self):
        """
        获取滑块
        :return:滑块对象
        """
        slider = WebDriverWait(self.browser,20,0.5).until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_slider_button')),message='slider not found')
        return slider

    def getPosition(self):
        """
        获取验证码位置
        :return:左上右下坐标
        """
        image = WebDriverWait(self.browser,20,0.5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/canvas')),message='没有找到图像')
        x1,y1,x2,y2 = image.location['x'],image.location['y'],image.location['x'] + image.size['width'],image.location['y'] + image.size['height']
        return x1,y1,x2,y2

    def getImgage(self):
        """
        获取验证码图像
        """
        x1, y1, x2, y2 = self.getPosition()
        #print("Position:",x1, y1, x2, y2)
        image = self.getScreenShot(x1, y1, x2, y2)

        return image

    def getScreenShot(self,x1, y1, x2, y2):
        """
        根据左上、右下左边获取网页截图中控件
        :return:控件图片对象
        """
        self.browser.save_screenshot(sys.path[0] + '\image\ScreenShot.png')
        image = Image.open(sys.path[0] + '\image\ScreenShot.png')
        image = image.crop(box=(x1, y1, x2, y2))
        image.save(sys.path[0] + '\image\ScreenShot.png')
        #调试显示
        #image.show()
        return image

    def isPixelEqual(self,image1,image2,x,y):
        """
        比较像素
        """
        #获取SRGB值
        pixel1 = image1.load()[x,y]
        pixel2 = image2.load()[x, y]

        threshold = 50
        #每个像素的三个值进行对比，最大误差不超过threshold
        if abs(pixel1[0] - pixel2[0] < threshold) and abs(pixel1[0] - pixel2[0] < threshold) and abs(pixel1[0] - pixel2[0] < threshold):
            return True
        else:
            return False

    def getGap(self,image1,image2):
        """
        通过像素对比获取移动距离
        :param image1:第一张图
        :param image2:第二张图
        :return:移动距离
        """
        left = 60
        bottom = 23
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1] - bottom):
                if not self.isPixelEqual(image1,image2,i,j):
                    left = i
                    print("Distance :",left)
                    return left
        return left

    def getTrack(self,distance):
        """
        获取运动轨迹
        :param disatance:距离
        :return:轨迹
        """
        #实际校准
        distance -= 5
        #轨迹
        track = []
        #当前位移
        current = 0
        #减速位置
        mid = distance * 3 / 4
        #间隔
        t = 0.2
        #当前速度，初速度=0
        v = 0

        while current < distance :
            if current < mid :
                a = 2
            else:
                a = -3
            #初速度为v0
            v0 = v
            #当前速度
            v = v0 + a * t
            #移动距离
            move = v0 * t + 1/2 * a * t * t
            #当前位移
            current += move
            #加入轨迹
            track.append(round(move))
        print 'Track:',track
        return track

    def moveToGap(self,track):
        """
        拖动滑动条至缺口处
        :param slider:滑块
        :param track:轨迹
        """
        for x in track:
            ActionChains(self.browser).move_by_offset(x,0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crackSlider(self):
        self.browser.get(crack.url)
        # 点击打开验证码按钮
        self.getBotton().click()
        time.sleep(2)

        x = len(self.browser.find_elements_by_link_text('http://www.geetest.com/first_page'))
        print 'x:', x
        i = 1
        while len(self.browser.find_elements_by_link_text('http://www.geetest.com/first_page')) == 0 and i <6:
            print 'Crack times :' , i

            # 获取验证码完整图片
            before = self.getImgage()
            # 点击滑块
            slider = self.getSlider()
            ActionChains(self.browser).click_and_hold(slider).perform()
            # 获取有缺口验证码图片
            after = self.getImgage()
            #ActionChains(self.browser).release().perform()
            time.sleep(2)
            # 移动距离
            distance = self.getGap(before, after)
            # 获取移动轨迹
            track = self.getTrack(distance)
            time.sleep(2)
            # 滑动滑块
            self.moveToGap(track)
            time.sleep(3)
            i += 1

            if len(self.browser.find_elements_by_link_text('http://www.geetest.com/first_page')) == 0 :
                print 'Crack Fail'
            else:
                print 'Crack Success'
                break


if __name__ == '__main__':
    crack = CrackPush()
    crack.crackSlider()

