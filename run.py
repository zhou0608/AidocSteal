import time,re,os,sys
import inifile
from appium import webdriver
class Aidoc(object):
    def Android_Run(self):      #安卓模拟器运行
        desired_caps = {}
        desired_caps['platformName'] = 'Android'   #android的apk还是IOS的ipa
        desired_caps['platformVersion'] = '5.1.1'  #android系统的版本号
        desired_caps['deviceName'] = inifile.And_ip    #手机设备名称，通过adb devices  查看
        desired_caps['appPackage'] = 'me.aidoc.client'  #apk的包名
        desired_caps['appActivity'] = 'me.aidoc.client.mvp.v2.activity.v2_splash.SplashActivity'  #apk的launcherActivity
        desired_caps['unicodeKeyboard'] = True  # 使用unicodeKeyboard的编码方式来发送字符串
        desired_caps['resetKeyboard'] = True     # # 将键盘给隐藏起来
        driver = webdriver.Remote(inifile.Appium_ip, desired_caps)  ##启动服务器地址，后面跟的是手机信息
        return  driver

    def Mining_Name(self,driver):  #进入偷矿的名单列表
        driver.find_element_by_id('animation_view').click()
        client = self.Re(driver)
        print('初始剩余次数:',client)
        while client > 0:
            for i in range(1,11):
                self.swipeUp(driver)
                driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='me.aidoc.client:id/recyclerView']/android.widget.RelativeLayout[" + str(i) + "]").click()
                energy=self.Pull_energy(driver)
                print('第%d次循环的结果'%i,energy)
                self.Click_Mining(driver,energy)
                del energy[:]
            self.Update(driver)
            client = self.Re(driver)
            print('当前剩余次数:', client)

    def Pull_energy(self,driver):  #获取页面有矿可点的
        energy=[]
        result = driver.find_elements_by_id('me.aidoc.client:id/tv_water_amount')
        a = 0
        while True:
            if type(a) == str:
                break
            else:
                try:
                    b = result[a].text
                    energy.append(b)
                    a = a + 1
                except Exception as s:
                    a = str(s)
        return energy

    def Click_Mining(self,driver,list):     #针对偷矿点击事件
        driver = driver
        if len(list)>2:
            num=max(list)
            print('要点击的是:',num)
            driver.find_element_by_name(num).click()
        else:
            print('不支持点击')

    def Update(self,driver):       #偷满十个以后换十个
        driver = driver
        self.swipeUp(driver)
        driver.find_element_by_name('换一批').click()

    def swipeUp(self,driver):   #页面下滑
        size = driver.get_window_size()
        width = size['width']   # 获取屏幕宽度 width
        height = size['height'] # 获取屏幕高度 height
        x1 = width * 0.5
        y1 = height * 0.9
        y2 = height * 0.25
        time.sleep(3)
        driver.swipe(x1, y1, x1, y2)


    def Click_me(self,driver):        #点击自己的能量
        value = self.Pull_energy(driver)
        for i in value:
            driver.find_element_by_name(''+str(i)+'').click()

    def Run(self):
        self.startAndServer()
        time.sleep(30)
        while True:
            self.startAppiumServer()
            time.sleep(10)
            try:
                driver = self.Android_Run()
                self.Login(driver)
                time.sleep(5)
                # driver.save_screenshot('login.png')
                self.Click_me(driver)
                self.Mining_Name(driver)
                driver.quit()
                print('捕捉异常内关闭')
                self.stupAppiumServer()
                break
            except Exception as s:
                print(s)
                print('捕捉异常外关闭')
            self.stupAppiumServer()
        self.stupAndServer()
    def Login(self,driver):
        driver = driver
        try:
            driver.find_element_by_name('我的钱包')
            return  True
        except Exception as s:
            driver.find_element_by_name('请输入手机号').send_keys(inifile.name)
            driver.find_element_by_id('me.aidoc.client:id/etPwd').send_keys(inifile.password)
            driver.find_element_by_id('me.aidoc.client:id/btnLogin').click()
            return  False

    def Re(self,driver):    # 获取剩余使用次数
        self.swipeUp(driver)
        text = driver.find_element_by_id('me.aidoc.client:id/tv_desc').text
        new_client = re.search('\d+', text).group()
        client = int(new_client)
        return  client

    def startAppiumServer(self):
        print('--------------启动Appium服务')
        os.system('start /b startAppium.bat')
    def stupAppiumServer(self):
        print('--------------关闭Appium服务')
        os.system('chcp 65001')
        os.system('taskkill /F /IM node.exe /t')

    def startAndServer(self):
        print('--------------启动安卓模拟器')
        os.system('start /b Run_And.bat')

    def stupAndServer(self):
        print('--------------关闭安卓模拟器')
        os.system('start /b Close_And.bat')


if __name__=='__main__':
    Aidoc().Run()