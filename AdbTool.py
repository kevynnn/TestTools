#coding:utf-8
import os
import time
import sys
fileDre = "C:\Users\dongkaiwen\Downloads"

while True:
    i = raw_input("请输入需要数字（1.截图；2.录屏;3.清除数据;4.安装程序;5.云服务重启):")

    if i == '1':
        name = 'Screenshot_' + str(time.strftime("%Y%m%d%H%M%S",time.localtime())) +'.jpg'
        shell_capture = 'adb shell screencap -p /sdcard/' + name
        shell_pull = 'adb pull /sdcard/' + name +' '  + fileDre
        shell_del = 'adb shell rm /sdcard/' + name

        os.system(shell_capture)
        os.system(shell_pull)
        os.system(shell_del)
    elif i == '2':
        time = raw_input('输入录屏时间(s):')
        shell_capture = 'adb shell screenrecord --time-limit ' +  time  +' /sdcard/video.mp4'
        shell_pull = 'adb pull /sdcard/video.mp4 ' + fileDre
        shell_del = 'adb shell rm /sdcard/video.mp4'

        os.system(shell_capture)
        os.system(shell_pull)
        os.system(shell_del)
    elif i == '3':
        shell_clear = 'adb shell pm clear com.meizu.flyme.gamecenter'
        os.system(shell_clear)
    elif i == '4':
        shell_install = 'adb install -r ' + r'E:\\Tool\\monkey\\'
        shell_uninstall = 'adb uninstall com.meizu.flyme.gamecenter'
        os.system(shell_uninstall)

        apks = {'GameCenter.apk':'com.meizu.flyme.gamecenter','AlphaTravel.apk':'com.meizu.flyme.alphatravel',
                }#'scriptkeeper.apk':'com.meizu.flyme.xtemui','GameDemo-online-debug.apk':'com.meizu.gamedemo.online'

        for apk in apks:
            #查询是否存在包名
            content = os.popen('adb shell pm list packages ' + apks[apk])
            if content.readline() == '':
                #安装apk
                os.system(shell_install + apk)
                time.sleep(2)

    elif i == '5':
        shell_clear = 'adb shell pm clear com.meizu.cloud'
        shell_reboot = 'adb shell reboot'
        os.system(shell_clear)
        time.sleep(2)
        os.system(shell_reboot)

    elif i == '6':
        getIMEI = 'adb shell getprop ril.gsm.imei'
        getSN = 'adb shell getprop ro.serialno'
        IMEIS =  os.popen(getIMEI).readline()
        SN =  os.popen(getSN).readline()
        print "IMEI :"
        print IMEIS
        print "SN :"
        print SN






