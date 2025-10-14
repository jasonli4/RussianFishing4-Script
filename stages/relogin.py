import tkinter as tk
from tkinter import messagebox
import time
import random
import datetime
import config
import utils
from utils import sleep_time, stop_program
from ocr.ocr_global import ocr
from stages import navigator
from logger import logger  # ✅ 添加日志模块

def init_rest_schedule():
    """初始化下次休息时间"""
    now = time.time()
    config.rest_interval_hours = getattr(config, "rest_interval_hours", 3)  # 每3小时休息一次
    config.rest_duration_minutes = getattr(config, "rest_duration_minutes", 10)  # 默认休息10分钟
    config.next_rest_time = now + config.rest_interval_hours * 3600
    logger.info(
        f"🕒 已设定 {config.rest_interval_hours} 小时休息一次，每次休息 {config.rest_duration_minutes} 分钟"
    )
    show_next_rest_time()


def show_next_rest_time():
    """打印下次休息时间"""
    next_rest = datetime.datetime.fromtimestamp(config.next_rest_time)
    remain = config.next_rest_time - time.time()
    h, m = divmod(int(remain // 60), 60)
    logger.info(f"⌛ 下次休息时间: {next_rest.strftime('%Y-%m-%d %H:%M:%S')}（约 {h} 小时 {m} 分钟后）")


def check_and_rest():
    """检查是否到达休息时间，并执行休息"""
    now = time.time()

    # 若尚未设定，则初始化
    if getattr(config, "next_rest_time", None) is None:
        init_rest_schedule()

    # 到达休息时间
    if now >= config.next_rest_time:
        duration = config.rest_duration_minutes * 60
        logger.info(f"💤 到达定时休息点，脚本暂停 {config.rest_duration_minutes} 分钟")

        elapsed = 0
        interval = 30  # 每30秒检查一次中断
        start_time = time.time()

        while elapsed < duration:
            if hasattr(config, "stop_event") and config.stop_event.is_set():
                logger.info("⚠️ 休息被中断，提前恢复脚本运行")
                break
            sleep_time(min(interval, duration - elapsed))
            elapsed = time.time() - start_time

        logger.info("✅ 休息结束，恢复脚本运行")

        # 安排下次休息
        config.next_rest_time = time.time() + config.rest_interval_hours * 3600
        show_next_rest_time()

    else:
        # 每小时提示剩余时间
        remain = config.next_rest_time - now
        if remain > 0 and int(remain) % 3600 < 60:
            h, m = divmod(int(remain // 60), 60)
            logger.info(f"⌛ 距离下次休息还有 {h} 小时 {m} 分钟")

# ========== 小退操作 ==========
def relogin():
    """
    重新登录游戏，并在检测到登录界面时，可能触发每日随机休息 3~4 小时（每天一次）
    """
    while not config.stop_event.is_set():
        # 是否在菜单界面
        quit_button1 = utils.find_template_in_regions(config.QuitGameButtonRegionScreenshot, template_filename="quit1.png")
        quit_button2 = utils.find_template_in_regions(config.QuitGameButtonRegionScreenshot, template_filename="quit2.png")
        quit_button = quit_button1 or quit_button2
        if quit_button:
            logger.info("检测到菜单界面。")
            break
        # 是否在游戏界面
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
            logger.info("已在游戏界面。")
            sleep_time(random.uniform(0.23, 0.24))
            utils.press_key('esc')
            sleep_time(random.uniform(0.25, 0.26))
            # 是否在菜单界面
            quit_button1 = utils.find_template_in_regions(config.QuitGameButtonRegionScreenshot, template_filename="quit1.png")
            quit_button2 = utils.find_template_in_regions(config.QuitGameButtonRegionScreenshot, template_filename="quit2.png")
            quit_button = quit_button1 or quit_button2
            if quit_button:
                logger.info("检测到菜单界面。")
                break
        
        sleep_time(random.uniform(0.4, 0.5))
    
    if not config.stop_event.is_set():
        # 把鼠标移动到退出游戏按钮区域
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region((quit_button[0]["left"], quit_button[0]["top"], quit_button[0]["width"], quit_button[0]["height"]))
        sleep_time(random.uniform(0.53, 0.54))
        utils.key_down('Left Shift')
        sleep_time(random.uniform(0.53, 0.54))
        utils.click_left_mouse(0.02)
        sleep_time(random.uniform(0.53, 0.54))
        utils.key_up('Left Shift')

    if not config.stop_event.is_set():
        # 把鼠标移动到确定按钮区域
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(region=config.QuitConfirmButtonRegionClick)
        sleep_time(random.uniform(0.23, 0.24))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.23, 0.24))

    # 等待出现重新登录界面
    steam_match = standalone_match = False
    while not config.stop_event.is_set():
        steam_match = utils.check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
        standalone_match = utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
        if steam_match or standalone_match:
            logger.info("检测到%s登录界面。" % ("Steam" if steam_match else "独立"))

            # ✅ 每日随机休息逻辑
            check_and_rest()

            # 继续登录操作
            if steam_match:
                logger.info("准备重新登录Steam端。")
                sleep_time(random.uniform(0.23, 0.235))
                utils.move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                sleep_time(random.uniform(0.23, 0.235))
                utils.click_left_mouse()
                break
            if standalone_match:
                logger.info("准备重新登录独立端。")
                sleep_time(random.uniform(0.23, 0.235))
                utils.move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                sleep_time(random.uniform(0.23, 0.24))
                utils.click_left_mouse()
                break
        sleep_time(random.uniform(0.04, 0.06))

    while not config.stop_event.is_set():
        fish_match = utils.check_template_in_region(config.FishRegionScreenshot, "fish.png")
        login_error_match = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
        if fish_match:
            logger.info("重新登录成功")
            break
        if login_error_match:
            # 如果Steam端登录失败，重启游戏
            if steam_match:
                utils.restart_game()
                continue
            # 如果独立端登陆失败，退出游戏
            if standalone_match:
                logger.warning("登录错误！独立端填写密码和勾选记住密码。")
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                root.attributes("-topmost", True)  # 设置最前
                messagebox.showwarning("警告", f"登录错误！独立端检测密码和勾选记住密码！", parent=root)
                root.destroy()
                stop_program()
                return  # ✅ 直接退出 relogin

        sleep_time(random.uniform(0.04, 0.06))
