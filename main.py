#!/usr/bin/env python3
# coding:utf-8

import tkinter as tk
from View import  MainGUI
'''
这是一个基于tkinter库的图像标注工具，目前支持标注矩形区域和散点区域，标注文件支持XML和JSON格式
'''

IMAGE_FILE_TYPE = ['jpg','JPG','PNG','png','bmp','BMP']




def set_mainUI(root):
    root.title('EasyLabel')
    root.option_add("*Font", "宋体")
    center_window(root, 1640, 900)
    #root.maxsize(960, 640)
    root.resizable(0, 0)
    root.iconbitmap('./icon/icon.ico')
    root.config(background='SteelBlue')
    app = MainGUI(root)
    root.mainloop()

#获取屏幕大小
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()

#获取串口大小
def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()

#设置串口居中
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

if (__name__ == '__main__'):
    root = tk.Tk()
    set_mainUI(root)