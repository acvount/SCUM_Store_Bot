import time

import pyautogui
import psutil
import pyperclip
import keyboard
import sys
import os
import socks
import socket
import codecs
import re
import threading
import win32gui
import win32con
from ftplib import FTP
from flask import Flask
import pygetwindow as gw
from flask import request
from datetime import datetime, timedelta
from pyautogui import FailSafeException


os.system("title SCUM 商城后端 私人定制QQ:2339510255")

app = Flask(__name__)

KEYS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'enter', 'space', 'backspace', 'delete', 'insert', 'home', 'end', 'page up', 'page down',
    'left', 'right', 'up', 'down', 'shift', 'ctrl', 'alt', 'caps lock', 'num lock', 'scroll lock',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
    # 你还可以添加其他的键
]

# 设定socket使用socks代理
socks.set_default_proxy(socks.SOCKS5, "localhost", 8889)  # 这里设置你的socks代理服务器地址和端口
socket.socket = socks.socksocket

ftp = FTP()
ftp.connect('127.0.0.1', '1234')  # 修改为你提供的IP地址和端口
ftp.login(user='admin', passwd='admin')  # 使用你提供的用户名和密码进行登录

def get_last_login_file(directory):
    files = ftp.nlst(directory)  # 获取FTP服务器上指定目录的文件列表
    login_files = [file for file in files if file.startswith('login')]  # 找到以'login'开头的文件
    if login_files:  # 如果找到了符合条件的文件
        last_login_file = sorted(login_files)[-1]  # 取最后一个文件
        return last_login_file
    else:
        return None

def get_scum_pid():
    for proc in psutil.process_iter():
        if proc.name() == 'SCUM.exe':
            return proc.pid
    return None

def paste(foo):
    pyperclip.copy(foo)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    return "成功"

def minimize_all_windows():
    pyautogui.hotkey('win', 'd')  # 使用快捷键Win + D来最小化所有窗口

def activate_scum_window(retries=5):
    for _ in range(retries):
        try:
            hwnd = win32gui.FindWindow(None, 'SCUM  ')
            if hwnd != 0:
                if hwnd != win32gui.GetForegroundWindow():
                    minimize_all_windows()  # 如果SCUM窗口不在前台，则最小化所有窗口
                    time.sleep(1)  # 等待一会以确保所有窗口已经最小化
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 恢复窗口
                win32gui.SetForegroundWindow(hwnd)  # 将窗口置于前台
                return
        except Exception:
            # 窗口激活失败，等待一会再重试
            time.sleep(1)
    raise RuntimeError("无法激活SCUM窗口")


def activate_and_lock_keyboard():
    windows = gw.getWindowsWithTitle('SCUM  ')
    if len(windows) > 0:
        windows[0].activate()
        for key in KEYS:
            keyboard.block_key(key)
    else:
        return "没有这个窗口"

def unlock_keyboard():
    for key in KEYS:
        keyboard.unblock_key(key)

PID = get_scum_pid()
if PID is None:
    print("没有找到SCUM.exe进程")

@app.route('/tp_service/',methods=['GET'])
def tp_service():
    activate_scum_window()
    activate_and_lock_keyboard()
    steamid = request.args.get('SteamID')
    tp_type = request.args.get('safe_area')
    location = u''
    if tp_type == "A0":
        location = u'#teleport -613404.188 -556331.750 2435.560 "'+steamid+'"'
    elif tp_type == "Z3":
        location = u'#Teleport 27467.420 -677666.313 347.970 "'+steamid+'"'
    elif tp_type == "B4":
        location = u'#Teleport 577438.125 -228798.031 365.020 "'+steamid+'"'
    elif tp_type == "C2":
        location = u'#Teleport -147688.609 292396.125 69688.172 "'+steamid+'"'
    p = psutil.Process(PID)
    if p.name() == "SCUM.exe":
        windows = gw.getWindowsWithTitle('SCUM  ')
        if len(windows) > 0:
            # 打开聊天框
            pyautogui.write("t")
            time.sleep(0.1)
            paste(location)
            time.sleep(0.1)
            pyautogui.press('enter')
        else:
            return "没有这个窗口"
        unlock_keyboard()
        return "成功"
    else:
        return "没有这个pid和这个窗口"

@app.route('/new_tp/',methods=['GET'])
def new_tp():
    activate_scum_window()
    activate_and_lock_keyboard()
    SteamIDA = request.args.get('SteamIDA')
    SteamIDB = request.args.get('SteamIDB')
    location = u'#teleportto "'+SteamIDA+'"  "'+SteamIDB+'"'
    p = psutil.Process(PID)
    if p.name() == "SCUM.exe":
        windows = gw.getWindowsWithTitle('SCUM  ')
        if len(windows) > 0:
            # 打开聊天框
            pyautogui.write("t")
            paste(location)
            pyautogui.press('enter')
        else:
            return "没有这个窗口"
        unlock_keyboard()
        return "成功"
    else:
        return "没有这个pid和这个窗口"

@app.route('/new_people/',methods=['GET'])
def hello_world():
    activate_scum_window()
    activate_and_lock_keyboard()
    steamid = request.args.get('SteamID')
    p = psutil.Process(PID)
    if p.name() == "SCUM.exe":
        windows = gw.getWindowsWithTitle('SCUM  ')
        if len(windows) > 0:
            # 打开聊天框
            pyautogui.write("t")
            foo1 = u'新手礼包正在发放，请待在原地不要走动,1-2分钟之内发放完毕！！！'
            paste(foo1)
            time.sleep(0.1)
            # 以下是刷取物品的代码
            foo2 = u'#spawnItem Military_Backpack_02_02 1 Location '+steamid
            paste(foo2)
            time.sleep(0.1)
            foo3 = u'#spawnitem Bulletproof_Vest_01 1 Location '+steamid
            paste(foo3)
            time.sleep(0.1)
            foo4 = u'#spawnitem Military_Helmet_01_07 1 Location '+steamid
            paste(foo4)
            time.sleep(0.1)
            foo5 = u'#spawnitem Military_Quiver_07 1 Location '+steamid
            paste(foo5)
            time.sleep(0.1)
            foo6 = u'#spawnitem Christmas_Present_UMP_02 1 Location '+steamid
            paste(foo6)
            time.sleep(0.1)
            foo7 = u'#spawnItem MRE_Stew 2 Location '+steamid
            paste(foo7)
            time.sleep(0.1)
            foo8 = u'#spawnitem Water_05l 2 Location '+steamid
            paste(foo8)
            time.sleep(0.1)
            foo9 = u'#spawnitem Rice 1 Location '+steamid
            paste(foo9)
            time.sleep(0.1)
            # foo10 = u'#spawnitem 2H_Tang_Dao 1 Location '+steamid
            # paste(foo10)
            time.sleep(0.1)
            foo11 = u'#spawnitem Cal_45_Ammobox 5 Location '+steamid
            paste(foo11)
            time.sleep(0.1)
            foo12 = u'#spawnitem Cash 1 CashValue 6000 Location '+steamid
            paste(foo12)
            foo13 = u'#spawnvehicle Mine_01 1 Location ' + steamid
            paste(foo13)
            foo14 = u'#spawnitem Mine_01 2 Location ' + steamid
            paste(foo14)
            foo14 = u'#spawnitem 2H_Shovel_01 1 Location ' + steamid
            paste(foo14)
            foo15 = u'#spawnitem Magazine_UMP45 2 Location ' + steamid
            paste(foo15)
            time.sleep(0.1)
            foo16 = u'新手礼包发放完毕，请管理留意此条消息！！！'
            paste(foo16)
            time.sleep(0.1)
            pyautogui.press('enter')
        else:
            return "没有这个窗口"
        unlock_keyboard()
        return "成功发放新手礼包"
    else:
        return "没有这个pid和这个窗口"

@app.route('/add_blance/',methods=['GET'])
def add_blance():
    activate_scum_window()
    activate_and_lock_keyboard()
    steamid = request.args.get('SteamID')
    blance = request.args.get('num')
    p = psutil.Process(PID)
    if p.name() == "SCUM.exe":
        windows = gw.getWindowsWithTitle('SCUM  ')
        if len(windows) > 0:
            pyautogui.write("t")
            time.sleep(0.1)
            foo1 = u'#ChangeCurrencyBalance Normal '+blance+' '+steamid
            paste(foo1)
            time.sleep(0.1)
            pyautogui.press('enter')
        else:
            return "没有这个窗口"
        unlock_keyboard()
        return "成功"
    else:
        return "没有这个pid和这个窗口"


def add_blance(msg):
    activate_scum_window()
    activate_and_lock_keyboard()
    p = psutil.Process(PID)
    if p.name() == "SCUM.exe":
        windows = gw.getWindowsWithTitle('SCUM  ')
        if len(windows) > 0:
            pyautogui.write("t")
            time.sleep(0.1)
            foo1 = msg
            paste(foo1)
            time.sleep(0.1)
            pyautogui.press('enter')
        else:
            return "没有这个窗口"
        unlock_keyboard()
        return "成功"
    else:
        return "没有这个pid和这个窗口"
def run_flask():
    app.run()

def ftp_read_login():
    last_line = None
    first_run = True
    pattern = re.compile(
        r"(\d{4}.\d{2}.\d{2}-\d{2}.\d{2}.\d{2}): '(?:\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3} |0.0.0.0 )\d{17}:(.*?)(?:\(\d+\))' logged (.*?) at")

    while True:
        last_login_file = get_last_login_file('156.146.56.42_7120')
        if last_login_file is not None:

            # 创建一个空的字节数组对象，用于存储从FTP服务器读取的文件内容
            buffer = bytearray()

            # 使用FTP的retrbinary方法读取文件内容
            ftp.retrbinary(f'RETR 156.146.56.42_7120/{last_login_file}', lambda data: buffer.extend(data))

            # 使用codecs模块将文件内容解码为utf-16-le
            content = codecs.decode(buffer, 'utf-16-le')

            # 检查是否有新的登录信息
            lines = content.split('\n')
            new_lines = lines[lines.index(last_line) + 1:] if last_line in lines else lines
            for line in new_lines:
                match = pattern.match(line)
                if match:
                    date_time, player_name, action = match.groups()
                    action = '上线了' if action == 'in' else '下线了'

                    # 转换并调整时间
                    date_time = datetime.strptime(date_time, '%Y.%m.%d-%H.%M.%S')
                    date_time += timedelta(hours=9)
                    date_time = date_time.strftime('%Y.%m.%d %H.%M.%S')

                    # 如果不是第一次运行，就处理这条消息
                    if not first_run:
                        add_blance(f'【{date_time}】尊敬的玩家：【{player_name}】{action}！！！')

                    last_line = line  # 更新last_line为最新处理过的消息

            first_run = False

        else:
            print('没有找到以"login"开头的文件')

        time.sleep(5)  # 每隔5秒进行一次操作

flask_thread = threading.Thread(target=run_flask)
read_login = threading.Thread(target=ftp_read_login)
flask_thread.start()
read_login.start()

