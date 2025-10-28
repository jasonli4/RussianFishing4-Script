import time
import keyboard
import config
from logger import logger
import utils
from gui_config import launch_config_window  # ✅ GUI 配置窗口（Tkinter）

# =========================
# 🎯 常量定义
# =========================
MONITOR_INTERVAL = (1.0, 1.1)
SHORT_WAIT = (0.23, 0.25)
RELOGIN_WAIT = (2.2, 3.3)


# =========================
# 🧩 通用封装函数
# =========================
def click_random_region(region, label="区域"):
    """在指定区域内随机点击"""
    utils.move_mouse_random_in_region(region)
    time.sleep(utils.human_like_uniform(*SHORT_WAIT))
    utils.click_left_mouse()
    logger.debug(f"👆 点击了 {label}")


def try_relogin(label, check_func, click_region):
    """
    通用重连逻辑：
    - 停止程序
    - 点击对应按钮
    - 检测登录界面
    - 自动进入游戏
    """
    logger.warning(f"🔁 [{label}] 检测到异常，执行重连")
    utils.stop_program()
    time.sleep(utils.human_like_uniform(*SHORT_WAIT))
    click_random_region(click_region, label=f"{label} 点击区域")

    # 等待登录界面或进入游戏
    while not config.stop_event.is_set():
        if check_func():
            logger.debug(f"[{label}] 异常仍存在，继续等待")
            time.sleep(utils.human_like_uniform(0.05, 0.07))
            continue

        # 检测 Steam 登录界面
        if utils.check_template_in_region(config.SteamLoginRegionScreenshot, "steamlogin.png"):
            logger.info(f"[{label}] 检测到 Steam 登录界面，准备登录")
            time.sleep(utils.human_like_uniform(*RELOGIN_WAIT))
            click_random_region(config.SteamLoginRegionClick, "Steam 登录")
            break

        # 检测独立登录界面
        if utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, "standalonelogin.png"):
            logger.info(f"[{label}] 检测到独立登录界面，准备登录")
            time.sleep(utils.human_like_uniform(*RELOGIN_WAIT))
            click_random_region(config.StandaloneLoginRegionClick, "独立登录")
            break

        # 检测是否回到游戏界面
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or utils.get_current_position():
            logger.info(f"[{label}] ✅ 已重新进入游戏界面")
            time.sleep(utils.human_like_uniform(*RELOGIN_WAIT))
            config.need_restart = True
            return

        time.sleep(utils.human_like_uniform(0.05, 0.07))


# =========================
# 👁️ 守护线程：监视异常并重启
# =========================
def monitor_and_restart():
    while not config.stop_event.is_set():
        time.sleep(utils.human_like_uniform(*MONITOR_INTERVAL))

        # 检测各种状态
        lossgameconnect = utils.check_template_in_region(config.LossGameConnectRegionScreenshot, "lossgameconnect.png")
        serverloss = utils.check_template_in_region(config.ServerLossRegionScreenshot, "serverloss.png")
        login_error = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
        gifts = utils.find_template_in_regions(config.GiftRegionScreenshot, "gift.png", confidence=0.8)

        # 登录错误处理
        if login_error:
            try_relogin("登录错误", 
                        lambda: utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png"),
                        config.ServerLossRegionClick)

        # 服务器未响应
        elif serverloss:
            try_relogin("服务器未响应", 
                        lambda: utils.check_template_in_region(config.ServerLossRegionScreenshot, "serverloss.png"),
                        config.ServerLossRegionClick)

        # 游戏失联
        elif lossgameconnect:
            try_relogin("服务器失联",
                        lambda: utils.check_template_in_region(config.LossGameConnectRegionScreenshot, "lossgameconnect.png"),
                        config.LossGameConnectRegionClick)

        # 检测礼物
        elif len(gifts) > 0:
            time.sleep(utils.human_like_uniform(0.43, 0.45))
            logger.info("🎁 检测到礼物，准备领取")
            utils.press_key('Space')

        # 检测是否需要重启
        if config.need_restart:
            logger.warning("🔁 检测到 need_restart=True，立即重启")
            config.need_restart = False
            config.need_restart_sign = True
            utils.stop_program()
            utils.delayed_start()


# =========================
# 🎹 热键监听线程
# =========================
def hotkey_listener():
    try:
        keyboard.add_hotkey(config.START_HOTKEY, utils.delayed_start)
        keyboard.add_hotkey(config.STOP_HOTKEY, utils.stop_program)
        logger.info(f"🎮 按 {config.START_HOTKEY} 启动，{config.STOP_HOTKEY} 停止。")
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("🛑 热键监听中断，退出监听线程。")


# =========================
# 🚀 主程序入口
# =========================
def main():
    # 启动守护线程
    utils.start_daemon_thread(monitor_and_restart)
    utils.start_daemon_thread(hotkey_listener)

    # 启动 GUI
    logger.info("🚀 正在启动配置界面")
    launch_config_window()

    # 退出前清理
    config.stop_event.set()
    utils.cleanup_keys()
    logger.info("👋 GUI 退出，程序结束")


if __name__ == "__main__":
    main()
