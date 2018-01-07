# -*- coding: utf-8 -*-
#原理简单任何事都是人做的
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

#获取屏幕截图（adb
def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')

#计算按压力
def jump(distance):
    press_time = distance * 1.35
    press_time = int(press_time)
    cmd = 'adb shell input swipe 320 410 320 410 ' + str(press_time)
    print(cmd)
    os.system(cmd)


fig = plt.figure()
pull_screenshot()
img = np.array(Image.open('autojump.png'))
im = plt.imshow(img, animated=True)

update = True
click_count = 0
cor = []

#更新plt屏幕
def update_data():
    return np.array(Image.open('autojump.png'))


def updatefig(*args):
    global update
    if update:
        time.sleep(1.5)
        pull_screenshot()
        im.set_array(update_data())
        update = False
    return im,

#计算需要跳跃的距离（通过鼠标点击来），用 Matplotlib 显示截图，用鼠标先点击起始点位置，然后点击目标位置，计算像素距离；
def on_click(event):
    global update
    global ix, iy
    global click_count
    global cor

    ix, iy = event.xdata, event.ydata
    coords = [(ix, iy)]
    print('now = ', coords)
    cor.append(coords)

    click_count += 1
    if click_count > 1:
        click_count = 0
        cor1 = cor.pop()
        cor2 = cor.pop()

        distance = (cor1[0][0] - cor2[0][0])**2 + (cor1[0][1] - cor2[0][1])**2
        distance = distance ** 0.5
        print('distance = ', distance)
        jump(distance)
        update = True


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
