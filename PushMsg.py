#coding:utf-8
from  selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import PIL
from PIL import Image
import time


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
        print("Position:",x1, y1, x2, y2)
        image = self.getScreenShot(x1, y1, x2, y2)

        return image


    def getScreenShot(self,x1, y1, x2, y2):
        """
        根据左上、右下左边获取网页截图中控件
        :return:控件图片对象
        """
        self.browser.save_screenshot('image\ScreenShot.png')
        image = Image.open('image\ScreenShot.png')
        image = image.crop(box=(x1, y1, x2, y2))
        image.save('image\ScreenShot.png')
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

        threshold = 10
        #每个像素的三个值进行对比，最大误差不超过threshold
        if abs(pixel1[0] - pixel2[0] < threshold) and abs(pixel1[0] - pixel2[0] < threshold) and abs(pixel1[0] - pixel2[0] < threshold):
            return True
        else:
            return False

    def getGap(self,image1,iamge2):

        left = 60
        bottom = 20
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1],image1.size[1] - bottom):
                if not self.isPixelEqual(image1,iamge2,i,j):
                    left = i
        return left


if __name__ == '__main__':
    crack = CrackPush()
    crack.browser.get(crack.url)
    #点击按钮
    crack.getBotton().click()
    time.sleep(2)
    before = crack.getImgage()
    #点击滑块
    crack.getSlider().click()
    after = crack.getImgage()

    print crack.getGap(before,after)
