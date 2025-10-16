import tkinter as tk
import random
import config
import utils
from tkinter import messagebox
from utils import sleep_time, stop_program
from logger import logger


def choose_item(slot_region, empty_region, description):
    """
    通用的选择装备操作（引线、钩子、饵料）
    :param slot_region: 装备槽位置 (left, top, width, height)
    :param empty_region: 判断是否为空的区域
    :param description: 装备名称（仅用于日志）
    """
    try:
        sleep_time(random.uniform(1.42, 1.52))
        utils.move_mouse_random_in_region(slot_region)
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse(0.1)
        sleep_time(random.uniform(1.22, 1.32))

        if utils.check_template_in_region(empty_region, 'empty.png', threshold=0.95):
            logger.warning(f"{description} 为空，跳过")
            utils.press_key('Esc', 0.1)
            sleep_time(random.uniform(0.22, 0.32))
        else:
            logger.info(f"选择 {description}")
            utils.move_mouse_random_in_region((285, 203, 166, 200))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(0.1)
            utils.click_left_mouse()
    except Exception as e:
        logger.error(f"选择 {description} 时出错: {e}")


def check_assembly(on_sea=False):
    """
    检查钓竿是否组装完成
    若检测到线组被咬断，则自动打开装备界面重新配置
    否则弹窗提醒玩家并停止程序
    """
    try:
        sleep_time(random.uniform(0.01, 0.02))

        # 检查是否有“组装”提示
        if utils.check_template_in_region(region=config.region_check_assembly_area, template_path="assembly.png"):

            # 条件：水底飞竿模式 或 海钓模式
            if (
                (config.auto_mode == 3 and config.is_fly_ticket and config.is_fly_rod and on_sea)
                or (config.mode_type == 2 and (config.auto_mode == 1 or config.auto_mode == 4))
            ):
                logger.warning("检测到线组被咬断，自动重新配置钓组中...")
                sleep_time(random.uniform(1, 1.1))

                # 打开钓组界面
                utils.press_key('v')

                # 通用检测区域
                empty_region = {"left": 859, "top": 606, "width": 190, "height": 23}

                # 选择各部件
                choose_item((1001, 511, 64, 64), empty_region, "引线")
                choose_item((1001, 603, 64, 64), empty_region, "钩子")
                choose_item((1001, 695, 64, 64), empty_region, "饵料")

                # 关闭界面
                sleep_time(random.uniform(0.42, 0.52))
                utils.press_key('v', 0.1)
                sleep_time(random.uniform(0.52, 0.62))

                # 修复：检测抛竿按钮并点击
                if config.is_cast_rod and utils.check_template_in_region(config.region_cast_rod, 'cast_rod.png'):
                    utils.click_left_mouse(random.uniform(0.08, 0.11))

                logger.info("钓组自动修复完成")
                return

            # 若装备缺失或未满足条件，提示用户手动组装
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            messagebox.showwarning("警告", "请配置好鱼竿！", parent=root)
            root.destroy()

            logger.error("钓组未配置，程序停止")
            stop_program()

    except Exception as e:
        logger.error(f"检查钓组时发生错误: {e}")
        stop_program()
