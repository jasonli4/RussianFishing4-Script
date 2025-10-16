from datetime import datetime
import os
import json
import tkinter as tk
from tkinter import ttk,filedialog, messagebox
import config
from logger import logger  # logger 是 get_logger() 返回的 logging.Logger 实例
import logging


CONFIG_FILE = "config.json"
GEOMETRY_FILE = "window_geometry.json"


class GuiLogger(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self._write, msg)

    def _write(self, msg):
        self.text_widget.config(state="normal")         # 打开写入权限
        self.text_widget.insert(tk.END, msg + "\n")     # 写入日志
        self.text_widget.see(tk.END)                    # 滚动到底部
        self.text_widget.config(state="disabled")       # 重新设为只读


def save_config_to_file():
    config_dict = {
        "destination": config.destination,
        "dist": config.dist,
        "START_HOTKEY": config.START_HOTKEY,
        "STOP_HOTKEY": config.STOP_HOTKEY,
        # "EXIT_HOTKEY": config.EXIT_HOTKEY,
        "status_type": config.status_type,
        "reel_type": config.reel_type,
        "fishing_rod_btn": config.fishing_rod_btn,
        "stamina_btn": config.stamina_btn,
        "hunger_btn": config.hunger_btn,
        "cast_line_meters": config.cast_line_meters,
        "max_cast_line_meters": config.max_cast_line_meters,
        "is_cut_fish": config.is_cut_fish,
        "is_cut_low_quality_fish": config.is_cut_low_quality_fish,
        "fish_block_types1": config.fish_block_types1,
        "fish_block_types2": config.fish_block_types2,
        "is_fly_ticket": config.is_fly_ticket,
        "is_fly_rod": config.is_fly_rod,
        "is_MN": config.is_MN,
        "is_trolling_mode": config.is_trolling_mode,
        "direction": config.direction,
        "trolling_status_type": config.trolling_status_type,
        "trolling_reeling_speed": config.trolling_reeling_speed,
        "trolling_unlock_meters": config.trolling_unlock_meters,
        "status_sleep": config.status_sleep,
        "status_click": config.status_click,
        "is_open_lock_unlock": config.is_open_lock_unlock,
        "open_lock_unlock_alone": config.open_lock_unlock_alone,
        "min_lock_unlock_value": config.min_lock_unlock_value,
        "max_lock_unlock_value": config.max_lock_unlock_value,
        "is_open_gear_ratio": config.is_open_gear_ratio,
        "gear_ratio": config.gear_ratio,
        "sleep_when_on_status": config.sleep_when_on_status,
        "reeling_time_after_status_detected": config.reeling_time_after_status_detected,
        "change_leader_line_max_value":config.change_leader_line_max_value,
        "auto_change_pit":config.auto_change_pit,
        "auto_pits":config.auto_pits,
        "ticket_target_count":config.ticket_target_count,
        "is_shift": config.is_shift,
        # 新增字段
        "lure_mode": config.lure_mode,
        "lure_rod_power": config.lure_rod_power,
        "lure_rod_reeling_duration": config.lure_rod_reeling_duration,
        "lure_rod_stop_duration": config.lure_rod_stop_duration,
        "bottom_map": config.bottom_map,
        "lure_map": config.lure_map,
        "bottom_reel_speed": config.bottom_reel_speed,
        "bottom_reel_friction": config.bottom_reel_friction,
        "lure_reel_speed": config.lure_reel_speed,
        "lure_reel_friction": config.lure_reel_friction,
        "sink_time": config.sink_time,
        "put_down_rod_key": config.put_down_rod_key,
        "lure_rod_name": config.lure_rod_name,
        "auto_mode": config.auto_mode,
        "only_bottom_meters": config.only_bottom_meters,
        "bottom_wait_time": config.bottom_wait_time,
        "dig_bait_tool_name": config.dig_bait_tool_name,
        "game_mode": config.game_mode,
        "steam_path": config.steam_path,
        "standalone_path": config.standalone_path,
        "mode_type": config.mode_type,
        "rest_interval_hours": config.rest_interval_hours,
        "rest_duration_minutes": config.rest_duration_minutes,
        #手竿
        "hand_rod_fishing_mode": config.hand_rod_fishing_mode,
        "hand_rod_fishing_map": config.hand_rod_fishing_map,
        "water_status": config.water_status,
        "hand_rod_power": config.hand_rod_power,
        "drifting_total_duration": config.drifting_total_duration,
        "hand_rod_main_line_name": config.hand_rod_main_line_name,
        "hand_rod_float_name": config.hand_rod_float_name,
        "hand_rod_sink_name": config.hand_rod_sink_name,
        "hand_rod_leader_line_name": config.hand_rod_leader_line_name,
        "hand_rod_hook_name": config.hand_rod_hook_name,
        "hand_rod_bait_name1": config.hand_rod_bait_name1,
        "hand_rod_bait_name2": config.hand_rod_bait_name2,

        "laoao_points": config.laoao_points,
        "hupo_points": config.hupo_points,
        "ahetubahe_points": config.ahetubahe_points,
        "tonghu_points": config.tonghu_points,
        "weiyounuoke_mhl_points": config.weiyounuoke_mhl_points,
        "baihe_lure_points": config.baihe_lure_points,
        "aier_lure_points": config.aier_lure_points,
        "weiyounuoke_hand_points": config.weiyounuoke_hand_points,
        "beidun_hand_points": config.beidun_hand_points,
        #其他
        "is_rainbow_line": config.is_rainbow_line,
        "keep_underperforming_fish": config.keep_underperforming_fish,
        # "chum_the_water": config.chum_the_water
        "is_dig_bait": config.is_dig_bait
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)


def load_config_from_file():
    if not os.path.exists(CONFIG_FILE):
        return
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        config.destination = tuple(data.get("destination", config.destination))
        config.dist = data.get("dist", config.dist)
        config.START_HOTKEY = data.get("START_HOTKEY", config.START_HOTKEY)
        config.STOP_HOTKEY = data.get("STOP_HOTKEY", config.STOP_HOTKEY)
        # config.EXIT_HOTKEY = data.get("EXIT_HOTKEY", config.EXIT_HOTKEY)
        config.status_type = data.get("status_type", config.status_type)
        config.reel_type = data.get("reel_type", config.reel_type)
        config.fishing_rod_btn = data.get("fishing_rod_btn", config.fishing_rod_btn)
        config.stamina_btn = data.get("stamina_btn", config.stamina_btn)
        config.hunger_btn = data.get("hunger_btn", config.hunger_btn)
        config.cast_line_meters = data.get("cast_line_meters", config.cast_line_meters)
        config.max_cast_line_meters = data.get("max_cast_line_meters", config.max_cast_line_meters)
        config.is_cut_fish = data.get("is_cut_fish", config.is_cut_fish)
        config.is_cut_low_quality_fish = data.get("is_cut_low_quality_fish", config.is_cut_low_quality_fish)
        config.fish_block_types1 = data.get("fish_block_types1", config.fish_block_types1)
        config.fish_block_types2 = data.get("fish_block_types2", config.fish_block_types2)
        config.is_fly_ticket = data.get("is_fly_ticket", config.is_fly_ticket)
        config.is_fly_rod = data.get("is_fly_rod", config.is_fly_rod)
        config.is_MN = data.get("is_MN", config.is_MN)
        config.is_trolling_mode = data.get("is_trolling_mode", config.is_trolling_mode)
        config.direction = data.get("direction", config.direction)
        config.trolling_status_type = data.get("trolling_status_type", config.trolling_status_type)
        config.trolling_reeling_speed = data.get("trolling_reeling_speed", config.trolling_reeling_speed)
        config.trolling_unlock_meters = data.get("trolling_unlock_meters", config.trolling_unlock_meters)
        config.status_sleep = data.get("status_sleep", config.status_sleep)
        config.status_click = data.get("status_click", config.status_click)
        config.is_open_lock_unlock = data.get("is_open_lock_unlock", config.is_open_lock_unlock)
        config.min_lock_unlock_value = data.get("min_lock_unlock_value", config.min_lock_unlock_value)
        config.max_lock_unlock_value = data.get("max_lock_unlock_value", config.max_lock_unlock_value)
        config.is_open_gear_ratio = data.get("is_open_gear_ratio", config.is_open_gear_ratio)
        config.gear_ratio = data.get("gear_ratio", config.gear_ratio)
        config.sleep_when_on_status = data.get("sleep_when_on_status", config.sleep_when_on_status)
        config.reeling_time_after_status_detected = data.get("reeling_time_after_status_detected", config.reeling_time_after_status_detected)
        config.change_leader_line_max_value = data.get("change_leader_line_max_value", config.change_leader_line_max_value)
        config.auto_change_pit = data.get("auto_change_pit", config.auto_change_pit)
        config.auto_pits = data.get("auto_pits", config.auto_pits)
        config.ticket_target_count = data.get("ticket_target_count", config.ticket_target_count)
        config.is_shift = data.get("is_shift", getattr(config, "is_shift", False))
        # 新增字段
        config.lure_mode = data.get("lure_mode", getattr(config, "lure_mode", 1))
        config.lure_rod_power = data.get("lure_rod_power", getattr(config, "lure_rod_power", 70))
        config.lure_rod_reeling_duration = data.get("lure_rod_reeling_duration", getattr(config, "lure_rod_reeling_duration", 1.1))
        config.lure_rod_stop_duration = data.get("lure_rod_stop_duration", getattr(config, "lure_rod_stop_duration", 0.5))
        config.bottom_map = data.get("bottom_map", getattr(config, "bottom_map", 0))
        config.lure_map = data.get("lure_map", getattr(config, "lure_map", 1))
        config.bottom_reel_speed = data.get("bottom_reel_speed", getattr(config, "bottom_reel_speed", 50))
        config.bottom_reel_friction = data.get("bottom_reel_friction", getattr(config, "bottom_reel_friction", 25))
        config.lure_reel_speed = data.get("lure_reel_speed", getattr(config, "lure_reel_speed", 25))
        config.lure_reel_friction = data.get("lure_reel_friction", getattr(config, "lure_reel_friction", 23))
        config.sink_time = data.get("sink_time", getattr(config, "sink_time", 12))
        config.put_down_rod_key = data.get("put_down_rod_key", getattr(config, "put_down_rod_key", 'x'))
        config.lure_rod_name = data.get("lure_rod_name", getattr(config, "lure_rod_name", 'S68ML'))
        config.auto_mode = data.get("auto_mode", getattr(config, "auto_mode", 3))
        config.only_bottom_meters = data.get("only_bottom_meters", getattr(config, "only_bottom_meters", 10))
        config.bottom_wait_time = data.get("bottom_wait_time", getattr(config, "bottom_wait_time", 0))
        config.dig_bait_tool_name = data.get("dig_bait_tool_name", getattr(config, "dig_bait_tool_name", '铲'))
        config.game_mode = data.get("game_mode", getattr(config, "game_mode", 1))
        config.steam_path = data.get("steam_path", getattr(config, "steam_path", r'C:\Program Files (x86)\Steam\steam.exe'))
        config.standalone_path = data.get("standalone_path", getattr(config, "standalone_path", r'C:\Games\RF4_CN\RF4Launcher.exe'))
        config.mode_type = data.get("mode_type", getattr(config, "mode_type", 1))
        config.rest_interval_hours = data.get("rest_interval_hours", getattr(config, "rest_interval_hours", 3))
        config.rest_duration_minutes = data.get("rest_duration_minutes", getattr(config, "rest_duration_minutes", 15))
        #手竿
        config.hand_rod_fishing_mode = data.get("hand_rod_fishing_mode", getattr(config, "hand_rod_fishing_mode", 1))
        config.hand_rod_fishing_map = data.get("hand_rod_fishing_map", getattr(config, "hand_rod_fishing_map", 1))
        config.water_status = data.get("water_status", getattr(config, "water_status", 0))
        config.hand_rod_power = data.get("hand_rod_power", getattr(config, "hand_rod_power", 70))
        config.drifting_total_duration = data.get("drifting_total_duration", getattr(config, "drifting_total_duration", 60))
        config.hand_rod_main_line_name = data.get("hand_rod_main_line_name", getattr(config, "hand_rod_main_line_name", ''))
        config.hand_rod_float_name = data.get("hand_rod_float_name", getattr(config, "hand_rod_float_name", ''))
        config.hand_rod_sink_name = data.get("hand_rod_sink_name", getattr(config, "hand_rod_sink_name", ''))
        config.hand_rod_leader_line_name = data.get("hand_rod_leader_line_name", getattr(config, "hand_rod_leader_line_name", ''))
        config.hand_rod_hook_name = data.get("hand_rod_hook_name", getattr(config, "hand_rod_hook_name", ''))
        config.hand_rod_bait_name1 = data.get("hand_rod_bait_name1", getattr(config, "hand_rod_bait_name1", ''))
        config.hand_rod_bait_name2 = data.get("hand_rod_bait_name2", getattr(config, "hand_rod_bait_name2", ''))


        config.is_rainbow_line = data.get("is_rainbow_line", getattr(config, "is_rainbow_line", False))
        config.keep_underperforming_fish = data.get("keep_underperforming_fish", getattr(config, "keep_underperforming_fish", False))
        # config.chum_the_water = data.get("chum_the_water", getattr(config, "chum_the_water", False))
        config.is_dig_bait = data.get("is_dig_bait", getattr(config, "is_dig_bait", False)) 

        # 加载老奥点位，限制最多四个
        laoao_loaded_points = data.get("laoao_points", config.laoao_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.laoao_points = [
            {
                "name": p.get("name", ""),
                "point_id": p.get("point_id", f"point_{i+1}"),
                "meters": p.get("meters", "")
                } for i, p in enumerate(laoao_loaded_points)
        ]
         # 加载琥珀湖点位，限制最多四个
        hupo_loaded_points = data.get("hupo_points", config.hupo_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.hupo_points = [
            {
                "name": p.get("name", ""),
                "point_id": p.get("point_id", f"point_{i+1}"),
                "baits": p.get("baits", ["", "", "",""]),
                "meters": p.get("meters", "")

            } for i, p in enumerate(hupo_loaded_points)
        ]
         # 加载28图点位，限制最多四个
        ahetubahe_loaded_points = data.get("ahetubahe_points", config.ahetubahe_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.ahetubahe_points = [
            {
                "name": p.get("name", ""),
                "point_id": p.get("point_id", f"point_{i+1}"),
                "baits": p.get("baits", ["", "", "",""]),
                "meters": p.get("meters", "")

            } for i, p in enumerate(ahetubahe_loaded_points)
        ]
         # 加载铜湖点位，限制最多四个
        loaded_points = data.get("tonghu_points", config.tonghu_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.tonghu_points = [
            {
                "name": p.get("name", ""),
                "point_id": p.get("point_id", f"point_{i+1}"),
                "baits": p.get("baits", ["", "", "",""]),
                "meters": p.get("meters", "")

            } for i, p in enumerate(loaded_points)
        ]
        # 加载惟有诺克河-梅花鲈点位，限制最多三个
        weiyounuoke_mhl_loaded_points = data.get("weiyounuoke_mhl_points", config.weiyounuoke_mhl_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.weiyounuoke_mhl_points = [
            {
                "name": p.get("name", ""),
                "point_id": p.get("point_id", f"point_{i+1}"),
                "meters": p.get("meters", "")
                } for i, p in enumerate(weiyounuoke_mhl_loaded_points)
        ]        
        # 加载白河点位，限制最多三个
        baihe_lure_loaded_points = data.get("baihe_lure_points", config.baihe_lure_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.baihe_lure_points = [
            {
                "point_id": p.get("point_id", f"point_{i+1}"),
                # "meters": p.get("meters", "")
                } for i, p in enumerate(baihe_lure_loaded_points)
        ]
        # 加载埃尔克湖点位，限制最多三个
        aier_lure_loaded_points = data.get("aier_lure_points", config.aier_lure_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.aier_lure_points = [
            {
                "point_id": p.get("point_id", f"point_{i+1}"),
                # "meters": p.get("meters", "")
                } for i, p in enumerate(aier_lure_loaded_points)
        ]
        #手竿
        # 加载唯有诺克河手竿点位，限制最多三个
        weiyounuoke_hand_loaded_points = data.get("weiyounuoke_hand_points", config.weiyounuoke_hand_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.weiyounuoke_hand_points = [
            {
                "point_id": p.get("point_id", f"point_{i+1}"),
                # "meters": p.get("meters", "")
                } for i, p in enumerate(weiyounuoke_hand_loaded_points)
        ]
        # 加载北顿点位，限制最多三个
        beidun_hand_loaded_points = data.get("beidun_hand_points", config.beidun_hand_points)[:3]
        # 确保每个点位有 name, point_id, baits
        config.beidun_hand_points = [
            {
                "point_id": p.get("point_id", f"point_{i+1}"),
                # "meters": p.get("meters", "")
                } for i, p in enumerate(beidun_hand_loaded_points)
        ]


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 20
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text,
            justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("Microsoft YaHei", 9)
        )
        label.pack(ipadx=5, ipady=2)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

    


def save_window_geometry(geometry: str):
    with open(GEOMETRY_FILE, "w") as f:
        json.dump({"geometry": geometry}, f)

def load_window_geometry():
    if os.path.exists(GEOMETRY_FILE):
        try:
            with open(GEOMETRY_FILE, "r") as f:
                data = json.load(f)
                return data.get("geometry")
        except:
            pass
    return None

def launch_config_window():
    load_config_from_file()

    root = tk.Tk()
    root.title("钓鱼脚本v1.0.4")
    root.configure(bg="#f0f0f0")  # 设置窗口背景色为浅灰

    geometry = load_window_geometry()
    if geometry:
        root.geometry(geometry)
    else:
        root.geometry("646x931")  # 略微增加宽度以改善布局

    def on_close():
        save_config_to_file()
        save_window_geometry(root.geometry())
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    style = ttk.Style()
    style.theme_use('vista')  # 使用 'clam' 主题，更现代美观
    style.configure("Small.TButton", font=("Microsoft YaHei", 8), padding=2)
    style.configure("TLabel", font=("Microsoft YaHei", 8), foreground="#333")
    style.configure("TButton", font=("Microsoft YaHei", 8), padding=2)
    style.configure("TCheckbutton", font=("Microsoft YaHei", 8))
    style.configure("TEntry", font=("Microsoft YaHei", 8))
    style.configure("TCombobox", font=("Microsoft YaHei", 8))
    style.configure("TLabelframe", font=("Microsoft YaHei", 8, "bold"), foreground="#007bff")  # 蓝色标题
    style.configure("TLabelframe.Label", font=("Microsoft YaHei", 8, "bold"), foreground="#007bff")

    # 使用 Notebook 来组织不同部分，提高美观性和可导航性
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    
    def create_labeled_entry(parent, label, default, update_func, row, tooltip_text=None):
        label=ttk.Label(parent, text=label)
        label.grid(row=row, column=0, sticky="w", pady=2, padx=2)
        var = tk.StringVar(value=str(default))
        entry = ttk.Entry(parent, textvariable=var, width=22,font=("Microsoft YaHei", 8))
        entry.grid(row=row, column=1, sticky="w", padx=2)
        def trace_func(*args):
            update_func(var.get())
            save_config_to_file()
        var.trace_add("write", trace_func)
        
        # 🔹 添加悬浮提示
        if tooltip_text:
            ToolTip(label, tooltip_text)

        return var, entry, row + 1

    def create_labeled_combobox(parent, label, values, default, update_func, row, tooltip_text=None):
        label=ttk.Label(parent, text=label)
        label.grid(row=row, column=0, sticky="w", pady=2, padx=2)
        var = tk.StringVar(value=str(default))
        combo = ttk.Combobox(parent, values=values, textvariable=var, width=19, state="readonly",font=("Microsoft YaHei", 8) )
        combo.grid(row=row, column=1, sticky="w", padx=2)
        def trace_func(*args):
            update_func(var.get())
            save_config_to_file()
        var.trace_add("write", trace_func)

        # 🔹 添加悬浮提示
        if tooltip_text:
            ToolTip(label, tooltip_text)

        return var, combo, row + 1

    def create_checkbox(parent, label, default, update_func, row):
        var = tk.BooleanVar(value=default)
        cb = ttk.Checkbutton(parent, text=label, variable=var)
        cb.grid(row=row, column=0, columnspan=2, sticky="w", pady=2, padx=2)
        def trace_func(*args):
            update_func(var.get())
            save_config_to_file()
        var.trace_add("write", trace_func)
        return var, row + 1
    

    def refresh_ui():
        """根据 config.json 的值刷新 UI 控件"""
        # 重新加载 config.json
        load_config_from_file()

        # 更新首页配置
        selected_mode_type.set(get_mode_type_text(config.mode_type))
        selected_game_mode.set(get_game_mode_text(config.game_mode))
        steam_var.set(config.steam_path)
        standalone_var.set(config.standalone_path)
        start_hotkey_var.set(config.START_HOTKEY)
        stop_hotkey_var.set(config.STOP_HOTKEY)
        stamina_var.set(str(config.stamina_btn))
        hunger_var.set(str(config.hunger_btn))
        max_cast_line_meters_var.set(str(config.max_cast_line_meters))
        rest_interval_hours_var.set(str(config.rest_interval_hours))
        rest_duration_minutes_var.set(str(config.rest_duration_minutes))

        # 更新手竿
        hand_rod_fishing_mode_var.set(get_hand_rod_fishing_mode_text(config.hand_rod_fishing_mode))
        hand_rod_fishing_map_var.set(get_hand_rod_fishing_map_text(config.hand_rod_fishing_map))
        water_status_var.set(get_water_status_text(config.water_status))
        hand_rod_power_var.set(str(config.hand_rod_power))
        drifting_total_duration_var.set(str(config.drifting_total_duration))
        hand_rod_main_line_name_var.set(config.hand_rod_main_line_name)
        hand_rod_float_name_var.set(config.hand_rod_float_name)
        hand_rod_sink_name_var.set(config.hand_rod_sink_name)
        hand_rod_leader_line_name_var.set(config.hand_rod_leader_line_name)
        hand_rod_hook_name_var.set(config.hand_rod_hook_name)
        hand_rod_bait_name1_var.set(config.hand_rod_bait_name1)
        hand_rod_bait_name2_var.set(config.hand_rod_bait_name2)

        # 更新水底和路亚配置
        auto_mode_var.set(get_auto_mode_text(config.auto_mode))
        is_rainbow_line_var.set(config.is_rainbow_line)
        keep_underperforming_fish_var.set(config.keep_underperforming_fish)
        # chum_the_water_var.set(config.chum_the_water)
        is_dig_bait_var.set(config.is_dig_bait)
        is_cut_fish_var.set(config.is_cut_fish)
        bottom_reel_speed_var.set(str(config.bottom_reel_speed))
        bottom_reel_friction_var.set(str(config.bottom_reel_friction))
        put_down_rod_key_var.set(config.put_down_rod_key)
        only_bottom_meters_var.set(str(config.only_bottom_meters))
        bottom_wait_time_var.set(str(config.bottom_wait_time))
        dig_bait_tool_name_var.set(config.dig_bait_tool_name)
        bottom_map_var.set(get_bottom_map_text(config.bottom_map))

        # 刷新点位（铜湖、旧奥、琥珀湖、28图、白河）
        render_tonghu_points()
        render_laoao_points()
        render_hupo_points()
        render_ahetubahe_points()
        render_weiyounuoke_mhl_points()
        render_baihe_points()
        render_aier_points()
        render_weiyounuoke_hand_points()
        render_beidun_hand_points()

        update_add_button_state()
        update_laoao_add_button_state()
        update_hupo_add_button_state()
        update_ahetubahe_add_button_state()
        update_weiyounuoke_mhl_add_button_state()
        update_baihe_add_button_state()
        update_aier_add_button_state()
        update_weiyounuoke_hand_add_button_state()
        update_beidun_hand_add_button_state()

        # 更新路亚参数
        lure_mode_var.set(get_lure_mode_text(config.lure_mode))
        lure_rod_name_var.set(config.lure_rod_name)
        lure_rod_power_var.set(str(config.lure_rod_power))
        lure_rod_reeling_duration_var.set(str(config.lure_rod_reeling_duration))
        lure_rod_stop_duration_var.set(str(config.lure_rod_stop_duration))
        lure_reel_speed_var.set(str(config.lure_reel_speed))
        lure_reel_friction_var.set(str(config.lure_reel_friction))
        lure_sink_time_var.set(str(config.sink_time))
        lure_map_var.set(get_lure_map_text(config.lure_map))

        # 更新海图搬砖配置
        selected_pit.set("自定义")
        for k, v in predefined_pits.items():
            if not config.auto_change_pit and config.destination == (v[0], v[1]) and config.dist == v[2]:
                selected_pit.set(k)
                break
        x_var.set(str(config.destination[0]))
        y_var.set(str(config.destination[1]))
        dist_var.set(str(config.dist))
        cast_line_meters_var.set(str(config.cast_line_meters))
        auto_var.set(config.auto_change_pit)
        for i in range(5):
            auto_x_vars[i].set(str(config.auto_pits[i][0]) if i < len(config.auto_pits) else "0")
            auto_y_vars[i].set(str(config.auto_pits[i][1]) if i < len(config.auto_pits) else "0")
            auto_dist_vars[i].set(str(config.auto_pits[i][2]) if i < len(config.auto_pits) else "0")
            auto_cast_vars[i].set(str(config.auto_pits[i][3]) if i < len(config.auto_pits) else "0")

        # 更新海图参数
        reel_type_var.set(get_reel_type_text(config.reel_type))
        fishing_rod_btn_var.set(str(config.fishing_rod_btn))
        change_leader_line_max_value_var.set(str(config.change_leader_line_max_value))
        ticket_target_count_var.set(str(config.ticket_target_count))
        status_type_var.set(get_status_type_text(config.status_type))
        is_shift_var.set(config.is_shift)
        status_sleep_var.set(str(config.status_sleep))
        status_click_var.set(str(config.status_click))
        reeling_time_after_status_detected_var.set(str(config.reeling_time_after_status_detected))
        sleep_when_on_status_var.set(str(config.sleep_when_on_status))
        # cast_line_meters_var.set(str(config.cast_line_meters))
        is_cut_fish_var.set(config.is_cut_fish)
        is_cut_low_quality_fish_var.set(config.is_cut_low_quality_fish)
        fish_block_types1_var.set(get_fish_block_types1_text(config.fish_block_types1))
        fish_block_types2_var.set(get_fish_block_types2_text(config.fish_block_types2))
        is_fly_ticket_var.set(config.is_fly_ticket)
        is_fly_rod_var.set(config.is_fly_rod)

        # 更新拖钓设置
        is_trolling_var.set(config.is_trolling_mode)
        direction_var.set(get_direction_text(config.direction))
        troll_status_var.set(get_troll_status_text(config.trolling_status_type))
        trolling_reeling_speed_var.set(str(config.trolling_reeling_speed))
        trolling_unlock_meters_var.set(str(config.trolling_unlock_meters))

        # 更新点锁/传动比设置
        open_lock_unlock_alone_var.set(config.open_lock_unlock_alone)
        is_open_lock_unlock_var.set(config.is_open_lock_unlock)
        # min_lock_unlock_value_var.set(str(config.min_lock_unlock_value))
        max_lock_unlock_value_var.set(str(config.max_lock_unlock_value))
        is_open_gear_ratio_var.set(config.is_open_gear_ratio)
        gear_ratio_var.set(str(config.gear_ratio))

        # 更新界面状态（例如禁用/启用控件）
        update_fields_state()
        update_ui_state()
        on_is_cut_fish_change(config.is_cut_fish)

        # logger.info("UI 已根据 config.json 刷新")


    CONFIG_FILE = "config.json"  # 默认文件名，全局变量可被更新

    def save_config():
        global CONFIG_FILE
        file_path = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json")],
            initialfile=os.path.basename(CONFIG_FILE)
        )
        if not file_path:
            return
        try:
            CONFIG_FILE = file_path
            save_config_to_file()
            CONFIG_FILE = "config.json" 
            messagebox.showinfo("提示", f"配置已保存到 {file_path}")
            config_file_label.config(text=f"当前配置文件: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")

    LAST_PATH_FILE = "last_config_path.txt"

    def get_last_open_file():
        """获取上一次打开的配置文件完整路径，默认空"""
        if os.path.exists(LAST_PATH_FILE):
            with open(LAST_PATH_FILE, "r", encoding="utf-8") as f:
                path = f.read().strip()
                if os.path.isfile(path):
                    return path
        return ""  # 没有记录则为空

    def save_last_open_file(file_path):
        """保存最后一次打开配置文件的完整路径"""
        with open(LAST_PATH_FILE, "w", encoding="utf-8") as f:
            f.write(file_path)

    def load_config():
        global CONFIG_FILE

        # 获取上一次选择的文件路径
        last_file = get_last_open_file()
        initial_dir = os.path.dirname(last_file) if last_file else os.getcwd()
        initial_file = os.path.basename(last_file) if last_file else ""

        file_path = filedialog.askopenfilename(
            title="读取配置文件",
            filetypes=[("JSON 文件", "*.json")],
            initialdir=initial_dir,
            initialfile=initial_file
        )
        if not file_path:
            return

        try:
            # 保存完整文件路径供下次使用
            save_last_open_file(file_path)

            # 读取用户选择文件
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()

            # 覆盖写到根目录 config.json
            root_config_path = os.path.join(os.getcwd(), "config.json")
            with open(root_config_path, "w", encoding="utf-8") as f:
                f.write(data)

            # 重新加载根目录的 config.json
            # load_config_from_file()
            refresh_ui()

            # 更新 UI
            messagebox.showinfo("提示", f"已经读取配置 {file_path} ")
            config_file_label.config(text=f"当前配置文件: {file_path}")

        except Exception as e:
            messagebox.showerror("错误", f"读取配置失败: {e}")



    # 新增 Tab 1: 首页配置
    tab_home = ttk.Frame(notebook)
    notebook.add(tab_home, text="首页")

    frame_home = ttk.LabelFrame(tab_home, text="基础设置", padding=10)
    frame_home.pack(fill="x", padx=5, pady=5)

    row = 0

    mode_type_map = {"手竿": 1, "水底和路亚": 2, "海图": 3, "自动连点": 4}
    def get_mode_type_text(val):
        for k, v in mode_type_map.items():
            if v == val:
                return k
        return "手竿"

    selected_mode_type, selected_mode_type_combo, row = create_labeled_combobox(
        frame_home,
        "模式类型",
        list(mode_type_map.keys()),
        get_mode_type_text(config.mode_type),
        lambda v: setattr(config, "mode_type", mode_type_map.get(v, 1)),
        row
    )

    start_hotkey_var, start_hotkey_entry, row = create_labeled_entry(frame_home, "启动热键", config.START_HOTKEY, lambda v: setattr(config, "START_HOTKEY", v), row)
    stop_hotkey_var, stop_hotkey_entry, row = create_labeled_entry(frame_home, "停止热键", config.STOP_HOTKEY, lambda v: setattr(config, "STOP_HOTKEY", v), row)
    stamina_var, stamina_entry, row = create_labeled_entry(frame_home, "体力键", config.stamina_btn, lambda v: setattr(config, "stamina_btn", int(v) if v.isdigit() else config.stamina_btn), row)
    hunger_var, hunger_entry, row = create_labeled_entry(frame_home, "饥饿键", config.hunger_btn, lambda v: setattr(config, "hunger_btn", int(v) if v.isdigit() else config.hunger_btn), row)
    max_cast_line_meters_var, max_cast_line_meters_entry, row = create_labeled_entry(frame_home, "出线米数小退", config.max_cast_line_meters, lambda v: setattr(config, "max_cast_line_meters", int(v) if v.isdigit() else config.max_cast_line_meters), row)
    rest_interval_hours_var, rest_interval_hours_entry, row = create_labeled_entry(
    frame_home,
    "多久休息一次(h)",
    config.rest_interval_hours,
    lambda v: setattr(config, "rest_interval_hours", float(v) if v.replace('.', '', 1).isdigit() else config.rest_interval_hours),
    row
    )
    rest_duration_minutes_var, rest_duration_minutes_entry, row = create_labeled_entry(
    frame_home,
    "一次休息多久(min)",
    config.rest_duration_minutes,
    lambda v: setattr(config, "rest_duration_minutes", float(v) if v.replace('.', '', 1).isdigit() else config.rest_duration_minutes),
    row
    )
    
    frame_fishing_other = ttk.LabelFrame(tab_home, text="其他设置", padding=10)
    frame_fishing_other.pack(fill="x", padx=5, pady=5)

    game_mode_map = {"Steam端": 1, "独立端": 2}
    def get_game_mode_text(val):
        for k, v in game_mode_map.items():
            if v == val:
                return k
        return "Steam端"

    selected_game_mode, selected_game_mode_combo, row = create_labeled_combobox(
        frame_fishing_other,
        "游戏平台",
        list(game_mode_map.keys()),
        get_game_mode_text(config.game_mode),
        lambda v: setattr(config, "game_mode", game_mode_map.get(v, 1)),
        row
    )

    # Steam 路径（禁用输入）
    steam_var = tk.StringVar(value=config.steam_path)
    ttk.Label(frame_fishing_other, text="Steam路径").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    steam_entry = ttk.Entry(frame_fishing_other, textvariable=steam_var, width=40, state="readonly")
    steam_entry.grid(row=row, column=1, sticky="w", padx=2)
    def select_steam_path():
        path = filedialog.askopenfilename(
            title="选择 Steam 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if path:
            normalized_path = os.path.normpath(path)  # 转换为 Windows 风格路径
            steam_var.set(normalized_path)
            config.steam_path = normalized_path
            save_config_to_file()
    ttk.Button(frame_fishing_other, text="选择文件", command=select_steam_path, style="Small.TButton").grid(row=row, column=2, sticky="w", padx=2)
    row += 1

    # 独立端路径（禁用输入）
    standalone_var = tk.StringVar(value=config.standalone_path)
    ttk.Label(frame_fishing_other, text="独立端路径").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    standalone_entry = ttk.Entry(frame_fishing_other, textvariable=standalone_var, width=40, state="readonly")
    standalone_entry.grid(row=row, column=1, sticky="w", padx=2)
    def select_standalone_path():
        path = filedialog.askopenfilename(
            title="选择独立端可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if path:
            normalized_path = os.path.normpath(path)  # 转换为 Windows 风格路径
            standalone_var.set(normalized_path)
            config.standalone_path = normalized_path
            save_config_to_file()
    ttk.Button(frame_fishing_other, text="选择文件", command=select_standalone_path, style="Small.TButton").grid(row=row, column=2, sticky="w", padx=2)
    row += 1

    # 保存/读取按钮行
    btn_frame = ttk.Frame(frame_fishing_other)
    btn_frame.grid(row=row, column=0, columnspan=2, pady=5, sticky="w")

    btn_save = ttk.Button(btn_frame, text="保存配置", command=save_config)
    btn_save.pack(side="left", padx=5)

    btn_load = ttk.Button(btn_frame, text="读取配置", command=load_config)
    btn_load.pack(side="left", padx=5)

    row += 1

    # 文件名标签
    config_file_label = ttk.Label(
        frame_fishing_other,
        text=f"当前配置文件: {get_last_open_file() or os.path.abspath(CONFIG_FILE)}",
    )
    config_file_label.grid(row=row, column=0, columnspan=2, pady=5, sticky="w")

    row += 1


    #点位变量
    #水底
    laoao_available_points = ["48,28", "23,67", "25,41", "42,32", "36,28", "35,29","20,34","35,58","23,45","09,50","27,27", "67,59_laoao","27,54"]  # 老奥点位
    tonghu_available_points = ["66,55", "56,50", "67,59", "37,32", "44,34", "67,58", "66,59"]  # 铜湖点位
    hupo_available_points = []  # 琥珀湖点位
    ahetubahe_available_points = []  # 阿赫图巴赫点位
    weiyounuoke_mhl_available_points = ["99,121"] # 惟有诺克河-梅花鲈点位
    #路亚
    baihe_available_points = ["71,37", "66,28", "65,26", "73,45", "73,59"]  # 白河点位
    aier_available_points = ["65,93"]  # 艾尔克湖点位
    #手竿
    weiyounuoke_hand_available_points = ["72,85","87,103"]  #惟有诺克河-手竿点位
    beidun_hand_available_points = ["96,137","99,133","72,160"]  #北顿-手竿点位
    

    tab_hand = ttk.Frame(notebook)
    notebook.add(tab_hand, text="手竿")

    frame_fishing_hand = ttk.LabelFrame(tab_hand, text="手竿参数", padding=10)
    frame_fishing_hand.pack(fill="both", padx=5, pady=5)

    row = 0

    hand_rod_fishing_mode_map = {
        "全天手竿-自动卖鱼-换点": 1,
        "仅手竿": 2,
    }
    def get_hand_rod_fishing_mode_text(val):
        for k, v in hand_rod_fishing_mode_map.items():
            if v == val:
                return k
        return "仅手竿"

    hand_rod_fishing_mode_var, hand_rod_fishing_mode_combo, row = create_labeled_combobox(
        frame_fishing_hand,
        "手竿的钓鱼模式",
        list(hand_rod_fishing_mode_map.keys()),
        get_hand_rod_fishing_mode_text(config.hand_rod_fishing_mode),
        lambda v: [setattr(config, "hand_rod_fishing_mode", hand_rod_fishing_mode_map.get(v, 0)), save_config_to_file()],
        row,
        tooltip_text="全天手竿-自动卖鱼-换点：全天使用手竿钓鱼，自动卖鱼并换点\n仅手竿：只有手竿钓鱼功能"
    )

    water_status_map = {
        "静水": 1,
        "流水": 2,
    }
    def get_water_status_text(val):
        for k, v in water_status_map.items():
            if v == val:
                return k
        return "静水"

    water_status_var, water_status_combo, row = create_labeled_combobox(
        frame_fishing_hand,
        "水面状态",
        list(water_status_map.keys()),
        get_water_status_text(config.water_status),
        lambda v: [setattr(config, "water_status", water_status_map.get(v, 0)), save_config_to_file()],
        row,
        tooltip_text="静水：视角不会转动\n流水：视角会从左往右转动"
    )

    # 手竿参数
    hand_rod_power_var, hand_rod_power_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿力度",
        config.hand_rod_power,
        lambda v: setattr(config, "hand_rod_power", int(v) if v.isdigit() else config.hand_rod_power),
        row,
        tooltip_text="手竿抛竿力度，大于等于100为全力抛竿"
    )
    drifting_total_duration_var, drifting_total_duration_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "转动视角时间(s)",
        config.drifting_total_duration,
        lambda v: setattr(config, "drifting_total_duration", int(v) if v.isdigit() else config.drifting_total_duration),
        row,
        tooltip_text="漂流状态下多久转动一次视角"
    )
    hand_rod_main_line_name_var, hand_rod_main_line_name_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿主线名称",
        config.hand_rod_main_line_name,
        lambda v: setattr(config, "hand_rod_main_line_name", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_float_name_var, hand_rod_float_name_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿浮漂名称",
        config.hand_rod_float_name,
        lambda v: setattr(config, "hand_rod_float_name", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_sink_name_var, hand_rod_sink_name_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿沉子名称",
        config.hand_rod_sink_name,
        lambda v: setattr(config, "hand_rod_sink_name", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_leader_line_name_var, hand_rod_leader_line_name_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿引线名称",
        config.hand_rod_leader_line_name,
        lambda v: setattr(config, "hand_rod_leader_line_name", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_hook_name_var, hand_rod_hook_name_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿钩子名称",
        config.hand_rod_hook_name,
        lambda v: setattr(config, "hand_rod_hook_name", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_bait_name1_var, hand_rod_bait_name1_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿饵料名称1",
        config.hand_rod_bait_name1,
        lambda v: setattr(config, "hand_rod_bait_name1", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    hand_rod_bait_name2_var, hand_rod_bait_name2_entry, row = create_labeled_entry(
        frame_fishing_hand,
        "手竿饵料名称2",
        config.hand_rod_bait_name2,
        lambda v: setattr(config, "hand_rod_bait_name2", v),
        row,
        tooltip_text="断线后自动更换，留空则不更换"
    )
    
    hand_rod_fishing_map_map = {
        "惟有诺克河钓雅罗鱼": 1,
        "北顿钓黑海": 2,
    }
    def get_hand_rod_fishing_map_text(val):
        for k, v in hand_rod_fishing_map_map.items():
            if v == val:
                return k
        return "北顿钓黑海"

    hand_rod_fishing_map_var, hand_rod_fishing_map_combo, row = create_labeled_combobox(
        frame_fishing_hand,
        "全天手竿的地图",
        list(hand_rod_fishing_map_map.keys()),
        get_hand_rod_fishing_map_text(config.hand_rod_fishing_map),
        lambda v: [setattr(config, "hand_rod_fishing_map", hand_rod_fishing_map_map.get(v, 0)), save_config_to_file(), update_fields_state()],
        row
    )
    
    # 为 weiyounuoke_hand_entries 添加 UI，类似于 tonghu
    weiyounuoke_hand_entries = []
    weiyounuoke_hand_bait_entries = []
    weiyounuoke_hand_meters_entries = []
    weiyounuoke_hand_id_selectors = []

    weiyounuoke_hand_container_row = row
    weiyounuoke_hand_container = ttk.Frame(frame_fishing_hand)
    weiyounuoke_hand_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_weiyounuoke_hand_meters(key, value):
        config.weiyounuoke_hand_points[key]["meters"] = value
        save_config_to_file()

    def refresh_weiyounuoke_hand_point_options():
        used = {var.get() for _, var, _ in weiyounuoke_hand_id_selectors if var.get()}
        for combo, var, idx in weiyounuoke_hand_id_selectors:
            current = var.get()
            values = [p for p in weiyounuoke_hand_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.weiyounuoke_hand_points:
            for combo, _, _ in weiyounuoke_hand_id_selectors:
                combo['values'] = []

    def render_weiyounuoke_hand_points():
        for widget in weiyounuoke_hand_container.winfo_children():
            widget.destroy()
        weiyounuoke_hand_entries.clear()
        weiyounuoke_hand_bait_entries.clear()
        weiyounuoke_hand_meters_entries.clear()
        weiyounuoke_hand_id_selectors.clear()

        if not config.weiyounuoke_hand_points:
            ttk.Label(weiyounuoke_hand_container, text="暂无唯有诺克河点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.weiyounuoke_hand_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(weiyounuoke_hand_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in weiyounuoke_hand_available_points if p not in [pt['point_id'] for pt in config.weiyounuoke_hand_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.weiyounuoke_hand_points[i].update({'point_id': v.get()}), refresh_weiyounuoke_hand_point_options(), save_config_to_file()])
            weiyounuoke_hand_id_selectors.append((point_selector, point_var, idx))

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.weiyounuoke_hand_points.pop(i), save_config_to_file(), render_weiyounuoke_hand_points(), update_weiyounuoke_hand_add_button_state()]
            ).grid(row=1, column=0, columnspan=2, pady=2)

    def add_weiyounuoke_hand_point():
        if len(config.weiyounuoke_hand_points) < 3:
            used_points = [p["point_id"] for p in config.weiyounuoke_hand_points]
            available_points = weiyounuoke_hand_available_points
            for point_id in available_points:
                if point_id not in used_points:
                    config.weiyounuoke_hand_points.append({"point_id": point_id})
                    save_config_to_file()
                    render_weiyounuoke_hand_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    weiyounuoke_hand_add_button = ttk.Button(
        frame_fishing_hand,
        text="添加唯有诺克河点位",
        style="Small.TButton",
        command=lambda: [add_weiyounuoke_hand_point(), update_weiyounuoke_hand_add_button_state()]
    )
    weiyounuoke_hand_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_weiyounuoke_hand_add_button_state():
        if len(config.weiyounuoke_hand_points) >= 3:
            weiyounuoke_hand_add_button.config(state="disabled")
        else:
            weiyounuoke_hand_add_button.config(state="normal")

    # 刷新唯有诺克河点位下拉框
    render_weiyounuoke_hand_points()
    update_weiyounuoke_hand_add_button_state()


    # 为 beidun_hand_entries 添加 UI，类似于 tonghu
    beidun_hand_entries = []
    beidun_hand_bait_entries = []
    beidun_hand_meters_entries = []
    beidun_hand_id_selectors = []

    beidun_hand_container_row = row
    beidun_hand_container = ttk.Frame(frame_fishing_hand)
    beidun_hand_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_beidun_hand_meters(key, value):
        config.beidun_hand_points[key]["meters"] = value
        save_config_to_file()

    def refresh_beidun_hand_point_options():
        used = {var.get() for _, var, _ in beidun_hand_id_selectors if var.get()}
        for combo, var, idx in beidun_hand_id_selectors:
            current = var.get()
            values = [p for p in beidun_hand_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.beidun_hand_points:
            for combo, _, _ in beidun_hand_id_selectors:
                combo['values'] = []

    def render_beidun_hand_points():
        for widget in beidun_hand_container.winfo_children():
            widget.destroy()
        beidun_hand_entries.clear()
        beidun_hand_bait_entries.clear()
        beidun_hand_meters_entries.clear()
        beidun_hand_id_selectors.clear()

        if not config.beidun_hand_points:
            ttk.Label(beidun_hand_container, text="暂无北顿点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.beidun_hand_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(beidun_hand_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in beidun_hand_available_points if p not in [pt['point_id'] for pt in config.beidun_hand_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.beidun_hand_points[i].update({'point_id': v.get()}), refresh_beidun_hand_point_options(), save_config_to_file()])
            beidun_hand_id_selectors.append((point_selector, point_var, idx))

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.beidun_hand_points.pop(i), save_config_to_file(), render_beidun_hand_points(), update_beidun_hand_add_button_state()]
            ).grid(row=1, column=0, columnspan=2, pady=2)

    def add_beidun_hand_point():
        if len(config.beidun_hand_points) < 3:
            used_points = [p["point_id"] for p in config.beidun_hand_points]
            for point_id in beidun_hand_available_points:
                if point_id not in used_points:
                    config.beidun_hand_points.append({"point_id": point_id})
                    save_config_to_file()
                    render_beidun_hand_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    beidun_hand_add_button = ttk.Button(
        frame_fishing_hand,
        text="添加北顿手点位",
        style="Small.TButton",
        command=lambda: [add_beidun_hand_point(), update_beidun_hand_add_button_state()]
    )
    beidun_hand_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_beidun_hand_add_button_state():
        if len(config.beidun_hand_points) >= 3:
            beidun_hand_add_button.config(state="disabled")
        else:
            beidun_hand_add_button.config(state="normal")

    # 刷新北顿手点位下拉框
    render_beidun_hand_points()
    update_beidun_hand_add_button_state()





    # Tab 2: 水底和路亚钓鱼参数
    tab_fishing_params = ttk.Frame(notebook)
    notebook.add(tab_fishing_params, text="水底和路亚")

    frame_fishing_params = ttk.LabelFrame(tab_fishing_params, text="模式", padding=5)
    frame_fishing_params.pack(fill="x", padx=5, pady=5)

    row = 0

    auto_mode_map = {
        "全天水底-换点-卖鱼": 0,
        "全天路亚-换点-卖鱼": 1,
        "白天路亚，晚上水底-换点-卖鱼": 2,
        "仅水底": 3,
        "仅路亚": 4
    }
    def get_auto_mode_text(val):
        for k, v in auto_mode_map.items():
            if v == val:
                return k
        return "仅水底"

    auto_mode_var, auto_mode_combo, row = create_labeled_combobox(
        frame_fishing_params,
        "自动模式",
        list(auto_mode_map.keys()),
        get_auto_mode_text(config.auto_mode),
        lambda v: [setattr(config, "auto_mode", auto_mode_map.get(v, 3)), save_config_to_file(), update_fields_state()],
        row
    )

    # 放在一行里的容器
    checkbox_container = ttk.Frame(frame_fishing_params)
    checkbox_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=2)

    is_rainbow_line_var = tk.BooleanVar(value=getattr(config, "is_rainbow_line", False))
    cb1 = ttk.Checkbutton(checkbox_container, text="是否为彩虹线", variable=is_rainbow_line_var)
    cb1.pack(side="left", padx=2)
    def trace_func1(*args):
        setattr(config, "is_rainbow_line", bool(is_rainbow_line_var.get()))
        save_config_to_file()
    is_rainbow_line_var.trace_add("write", trace_func1)

    keep_underperforming_fish_var = tk.BooleanVar(value=getattr(config, "keep_underperforming_fish", False))
    cb2 = ttk.Checkbutton(checkbox_container, text="是否保留不达标的鱼", variable=keep_underperforming_fish_var)
    cb2.pack(side="left", padx=2)
    def trace_func2(*args):
        setattr(config, "keep_underperforming_fish", bool(keep_underperforming_fish_var.get()))
        save_config_to_file()
    keep_underperforming_fish_var.trace_add("write", trace_func2)


    # chum_the_water_var = tk.BooleanVar(value=getattr(config, "chum_the_water", False))
    # cb2 = ttk.Checkbutton(checkbox_container, text="是否打窝（手抛）", variable=chum_the_water_var)
    # cb2.pack(side="left", padx=2)
    # def trace_func4(*args):
    #     setattr(config, "chum_the_water", bool(chum_the_water_var.get()))
    #     save_config_to_file()
    # chum_the_water_var.trace_add("write", trace_func4)

    is_dig_bait_var = tk.BooleanVar(value=getattr(config, "is_dig_bait", False))
    cb2 = ttk.Checkbutton(checkbox_container, text="是否挖饵", variable=is_dig_bait_var)
    cb2.pack(side="left", padx=2)
    def trace_func4(*args):
        setattr(config, "is_dig_bait", bool(is_dig_bait_var.get()))
        save_config_to_file()
    is_dig_bait_var.trace_add("write", trace_func4)
    
    is_cut_fish_bottom_lure_var = tk.BooleanVar(value=getattr(config, "is_cut_fish_bottom_lure", False))
    cb3 = ttk.Checkbutton(checkbox_container, text="是否切鱼肉", variable=is_cut_fish_bottom_lure_var)
    cb3.pack(side="left", padx=2)
    def trace_func3(*args):
        setattr(config, "is_cut_fish_bottom_lure", bool(is_cut_fish_bottom_lure_var.get()))
        save_config_to_file()
    is_cut_fish_bottom_lure_var.trace_add("write", trace_func3)

    row += 1

    frame_fishing_params_bottom = ttk.LabelFrame(tab_fishing_params, text="水底", padding=5)
    frame_fishing_params_bottom.pack(fill="x", padx=5, pady=5)

    row = 0

    bottom_reel_speed_var, bottom_reel_speed_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "水底轮子收线速度",
        config.bottom_reel_speed,
        lambda v: setattr(config, "bottom_reel_speed", int(v) if v.isdigit() else config.bottom_reel_speed),
        row
    )

    bottom_reel_friction_var, bottom_reel_friction_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "水底轮子摩擦力",
        config.bottom_reel_friction,
        lambda v: setattr(config, "bottom_reel_friction", int(v) if v.isdigit() else config.bottom_reel_friction),
        row
    )

    put_down_rod_key_var, put_down_rod_key_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "放下竿子按键",
        config.put_down_rod_key,
        lambda v: setattr(config, "put_down_rod_key", v),
        row
    )

    only_bottom_meters_var, only_bottom_meters_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "仅水底模式卡米数",
        config.only_bottom_meters,
        lambda v: setattr(config, "only_bottom_meters", int(v) if v.isdigit() else config.only_bottom_meters),
        row,
        tooltip_text="会影响仅水底模式的抛竿力度"
    )

    bottom_wait_time_var, bottom_wait_time_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "每轮拿竿间隔(s)",
        config.bottom_wait_time,
        lambda v: setattr(config, "bottom_wait_time", int(v) if v.isdigit() else config.bottom_wait_time),
        row,
        tooltip_text="依次拿起三根杆子后为一轮，每轮间隔的时间"
    )

    dig_bait_tool_name_var, dig_bait_tool_name_entry, row = create_labeled_entry(
        frame_fishing_params_bottom,
        "挖饵的工具名称",
        config.dig_bait_tool_name,
        lambda v: setattr(config, "dig_bait_tool_name", v),
        row,
        tooltip_text="挖饵的铲子名称"
    )


      # bottom_map_options = {"旧奥斯特罗格湖": 0, "琥珀湖": 1, "铜湖": 2}
    bottom_map_options = {"旧奥斯特罗格湖": 0,"琥珀湖": 1,"阿赫图巴河": 2,"铜湖":3,"惟有诺克河-梅花鲈":4}

    def get_bottom_map_text(val):
        for k, v in bottom_map_options.items():
            if v == val:
                return k
        return "旧奥斯特罗格湖"

    bottom_map_var, bottom_map_combo, row = create_labeled_combobox(
        frame_fishing_params_bottom,
        "水底地图",
        list(bottom_map_options.keys()),
        get_bottom_map_text(config.bottom_map),
        lambda v: [setattr(config, "bottom_map", bottom_map_options.get(v, 0)), save_config_to_file(), update_fields_state()],
        row
    )

    tonghu_entries = []
    tonghu_bait_entries = []
    tonghu_meters_entries=[]
    tonghu_id_selectors = []  # 保存 (Combobox, StringVar, index)

    # 创建用于动态点位的容器框架
    global tonghu_container_row  # 在 launch_config_window 顶部定义
    tonghu_container_row = row
    tonghu_container = ttk.Frame(frame_fishing_params_bottom)
    tonghu_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    # 保存 config 到文件的辅助函数（假设你已经有）
    def save_bait(key, index, value):
        config.tonghu_points[key]["baits"][index] = value
        save_config_to_file()

    def save_name(key, value):
        config.tonghu_points[key]["name"] = value
        save_config_to_file()

    def save_meters(key, value):
        config.tonghu_points[key]["meters"] = value
        save_config_to_file()    

    # 刷新所有点位下拉框选项，防止重复
    def refresh_point_options():
        used = {var.get() for _, var, _ in tonghu_id_selectors if var.get()}
        for combo, var, idx in tonghu_id_selectors:
            current = var.get()
            values = [p for p in tonghu_available_points if p not in used or p == current]
            combo['values'] = values
        # 如果没有点位，确保下拉框为空
        if not config.tonghu_points:
            for combo, _, _ in tonghu_id_selectors:
                combo['values'] = []

    # 渲染点位函数
    def render_tonghu_points():
        # 清空容器中的所有控件
        for widget in tonghu_container.winfo_children():
            widget.destroy()
        tonghu_entries.clear()
        tonghu_bait_entries.clear()
        tonghu_id_selectors.clear()
        tonghu_meters_entries.clear()


        # 如果没有点位，显示提示信息
        if not config.tonghu_points:
            ttk.Label(tonghu_container, text="暂无铜湖点位配置").grid(row=0, column=0, sticky="w")
            return

        # 渲染现有点位
        row_frame = None
        for idx, point in enumerate(config.tonghu_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(tonghu_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", pady=0, padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in tonghu_available_points if p not in [pt['point_id'] for pt in config.tonghu_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.tonghu_points[i].update({'point_id': v.get()}), refresh_point_options(), save_config_to_file()])
            tonghu_id_selectors.append((point_selector, point_var, idx))

            # 窝子名称
            _, entry, _ = create_labeled_entry(
                group_frame,
                f"窝子名称",
                point["name"],
                lambda v, i=idx: [save_name(i, v), save_config_to_file()],
                1
            )
            entry.config(width=15,font=("Microsoft YaHei", 8))
            tonghu_entries.append(entry)

            # 三个饵料
            for j in range(4):
                _, bait_entry, _ = create_labeled_entry(
                    group_frame,
                    f"饵料 {j+1}" if j!=3 else "PVA",
                    point["baits"][j],
                    lambda v, i=idx, j=j: [save_bait(i, j, v), save_config_to_file()],
                    j + 2
                )
                bait_entry.config(width=15, font=("Microsoft YaHei", 8))
                tonghu_bait_entries.append(bait_entry)

            # 卡米数
            _, meters_entry, _ = create_labeled_entry(
                group_frame,
                f"卡米数",
                point["meters"],
                lambda v, i=idx: [save_meters(i, v), save_config_to_file()],
                6
            )
            meters_entry.config(width=15, font=("Microsoft YaHei", 8))
            tonghu_meters_entries.append(meters_entry)

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",  
                command=lambda i=idx: [config.tonghu_points.pop(i), save_config_to_file(), render_tonghu_points(),update_add_button_state()]
            ).grid(row=7, column=0, columnspan=2, pady=2)


    # 添加点位按钮
    def add_tonghu_point():
        if len(config.tonghu_points) < 3:
            used_points = [p["point_id"] for p in config.tonghu_points]
            for point_id in tonghu_available_points:
                if point_id not in used_points:
                    config.tonghu_points.append({"name": "", "point_id": point_id, "baits": ["", "", "",""],"meters":""})
                    save_config_to_file()
                    render_tonghu_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（4个）")

    
    tonghu_add_button = ttk.Button(
        frame_fishing_params_bottom,
        text="添加铜壶点位",
        style="Small.TButton",
        command=lambda: [add_tonghu_point(), update_add_button_state()]
    )
    tonghu_add_button.grid(row=row, column=0, columnspan=1, pady=0, sticky="w")
    row += 1

    def update_add_button_state():
        if len(config.tonghu_points) >= 3:
            tonghu_add_button.config(state="disabled")
        else:
            tonghu_add_button.config(state="normal")

    # 初始渲染
    render_tonghu_points()
    update_add_button_state()


    # 为 laoao_points 添加 UI，类似于 tonghu，但无 baits，只有 name, point_id, meters
    laoao_entries = []
    laoao_meters_entries = []
    laoao_id_selectors = []  # 保存 (Combobox, StringVar, index)

    # 创建用于动态点位的容器框架
    laoao_container_row = row
    laoao_container = ttk.Frame(frame_fishing_params_bottom)
    laoao_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    # 保存 config 到文件的辅助函数
    def save_laoao_name(key, value):
        config.laoao_points[key]["name"] = value
        save_config_to_file()

    def save_laoao_meters(key, value):
        config.laoao_points[key]["meters"] = value
        save_config_to_file()

    # 刷新所有点位下拉框选项，防止重复
    def refresh_laoao_point_options():
        used = {var.get() for _, var, _ in laoao_id_selectors if var.get()}
        for combo, var, idx in laoao_id_selectors:
            current = var.get()
            values = [p for p in laoao_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.laoao_points:
            for combo, _, _ in laoao_id_selectors:
                combo['values'] = []

    # 渲染点位函数
    def render_laoao_points():
        for widget in laoao_container.winfo_children():
            widget.destroy()
        laoao_entries.clear()
        laoao_meters_entries.clear()
        laoao_id_selectors.clear()

        if not config.laoao_points:
            ttk.Label(laoao_container, text="暂无旧奥斯特罗格湖点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.laoao_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(laoao_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in laoao_available_points if p not in [pt['point_id'] for pt in config.laoao_points if pt != point]],  # 调整可用点位
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.laoao_points[i].update({'point_id': v.get()}), refresh_laoao_point_options(), save_config_to_file()])
            laoao_id_selectors.append((point_selector, point_var, idx))

            # 窝子名称
            _,entry, _ = create_labeled_entry(
                group_frame,
                f"窝子名称",
                point["name"],
                lambda v, i=idx: [save_laoao_name(i, v), save_config_to_file()],
                1
            )
            entry.config(width=15,font=("Microsoft YaHei", 8))
            laoao_entries.append(entry)

            # 卡米数
            _,meters_entry, _ = create_labeled_entry(
                group_frame,
                f"卡米数",
                point["meters"],
                lambda v, i=idx: [save_laoao_meters(i, v), save_config_to_file()],
                2
            )
            meters_entry.config(width=15,font=("Microsoft YaHei", 8))
            laoao_meters_entries.append(meters_entry)

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.laoao_points.pop(i), save_config_to_file(), render_laoao_points(), update_laoao_add_button_state()]
            ).grid(row=3, column=0, columnspan=2, pady=2)

    # 添加点位按钮
    def add_laoao_point():
        if len(config.laoao_points) < 3:
            used_points = [p["point_id"] for p in config.laoao_points]
            for point_id in laoao_available_points:
                if point_id not in used_points:
                    config.laoao_points.append({"name": "", "point_id": point_id, "meters": ""})
                    save_config_to_file()
                    render_laoao_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    laoao_add_button = ttk.Button(
        frame_fishing_params_bottom,
        text="添加旧奥点位",
        style="Small.TButton",
        command=lambda: [add_laoao_point(), update_laoao_add_button_state()]
    )
    laoao_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_laoao_add_button_state():
        if len(config.laoao_points) >= 3:
            laoao_add_button.config(state="disabled")
        else:
            laoao_add_button.config(state="normal")

    # 初始渲染
    render_laoao_points()
    update_laoao_add_button_state()

    # 为 hupo_points 添加 UI，类似于 tonghu
    hupo_entries = []
    hupo_bait_entries = []
    hupo_meters_entries = []
    hupo_id_selectors = []

    hupo_container_row = row
    hupo_container = ttk.Frame(frame_fishing_params_bottom)
    hupo_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_hupo_bait(key, index, value):
        config.hupo_points[key]["baits"][index] = value
        save_config_to_file()

    def save_hupo_name(key, value):
        config.hupo_points[key]["name"] = value
        save_config_to_file()

    def save_hupo_meters(key, value):
        config.hupo_points[key]["meters"] = value
        save_config_to_file()

    def refresh_hupo_point_options():
        used = {var.get() for _, var, _ in hupo_id_selectors if var.get()}
        for combo, var, idx in hupo_id_selectors:
            current = var.get()
            values = [p for p in hupo_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.hupo_points:
            for combo, _, _ in hupo_id_selectors:
                combo['values'] = []

    def render_hupo_points():
        for widget in hupo_container.winfo_children():
            widget.destroy()
        hupo_entries.clear()
        hupo_bait_entries.clear()
        hupo_meters_entries.clear()
        hupo_id_selectors.clear()

        if not config.hupo_points:
            ttk.Label(hupo_container, text="暂无琥珀湖点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.hupo_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(hupo_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in hupo_available_points if p not in [pt['point_id'] for pt in config.hupo_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.hupo_points[i].update({'point_id': v.get()}), refresh_hupo_point_options(), save_config_to_file()])
            hupo_id_selectors.append((point_selector, point_var, idx))

            # 窝子名称
            _,entry, _ = create_labeled_entry(
                group_frame,
                f"窝子名称",
                point["name"],
                lambda v, i=idx: [save_hupo_name(i, v), save_config_to_file()],
                1
            )
            entry.config(width=15, font=("Microsoft YaHei", 8))
            hupo_entries.append(entry)

            # 四个饵料
            for j in range(4):
                _,bait_entry, _ = create_labeled_entry(
                    group_frame,
                    f"饵料 {j+1}" if j != 3 else "PVA",
                    point["baits"][j],
                    lambda v, i=idx, j=j: [save_hupo_bait(i, j, v), save_config_to_file()],
                    j + 2
                )
                bait_entry.config(width=15, font=("Microsoft YaHei", 8))
                hupo_bait_entries.append(bait_entry)

            # 卡米数
            _,meters_entry, _ = create_labeled_entry(
                group_frame,
                f"卡米数",
                point["meters"],
                lambda v, i=idx: [save_hupo_meters(i, v), save_config_to_file()],
                6
            )
            meters_entry.config(width=15, font=("Microsoft YaHei", 8))
            hupo_meters_entries.append(meters_entry)

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.hupo_points.pop(i), save_config_to_file(), render_hupo_points(), update_hupo_add_button_state()]
            ).grid(row=7, column=0, columnspan=2, pady=2)

    def add_hupo_point():
        if len(config.hupo_points) < 3:
            used_points = [p["point_id"] for p in config.hupo_points]
            for point_id in hupo_available_points:
                if point_id not in used_points:
                    config.hupo_points.append({"name": "", "point_id": point_id, "baits": ["", "", "", ""], "meters": ""})
                    save_config_to_file()
                    render_hupo_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    hupo_add_button = ttk.Button(
        frame_fishing_params_bottom,
        text="添加琥珀湖点位",
        style="Small.TButton",
        command=lambda: [add_hupo_point(), update_hupo_add_button_state()]
    )
    hupo_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_hupo_add_button_state():
        if len(config.hupo_points) >= 3:
            hupo_add_button.config(state="disabled")
        else:
            hupo_add_button.config(state="normal")

    # 初始渲染
    render_hupo_points()
    update_hupo_add_button_state()

    # 为ahetubahe_points 添加 UI，类似于 tonghu
    ahetubahe_entries = []
    ahetubahe_bait_entries = []
    ahetubahe_meters_entries = []
    ahetubahe_id_selectors = []

    ahetubahe_container_row = row
    ahetubahe_container = ttk.Frame(frame_fishing_params_bottom)
    ahetubahe_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_ahetubahe_bait(key, index, value):
        config.ahetubahe_points[key]["baits"][index] = value
        save_config_to_file()

    def save_ahetubahe_name(key, value):
        config.ahetubahe_points[key]["name"] = value
        save_config_to_file()

    def save_ahetubahe_meters(key, value):
        config.ahetubahe_points[key]["meters"] = value
        save_config_to_file()

    def refresh_ahetubahe_point_options():
        used = {var.get() for _, var, _ in ahetubahe_id_selectors if var.get()}
        for combo, var, idx in ahetubahe_id_selectors:
            current = var.get()
            values = [p for p in ahetubahe_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.ahetubahe_points:
            for combo, _, _ in ahetubahe_id_selectors:
                combo['values'] = []

    def render_ahetubahe_points():
        for widget in ahetubahe_container.winfo_children():
            widget.destroy()
        ahetubahe_entries.clear()
        ahetubahe_bait_entries.clear()
        ahetubahe_meters_entries.clear()
        ahetubahe_id_selectors.clear()

        if not config.ahetubahe_points:
            ttk.Label(ahetubahe_container, text="暂无阿赫图巴河点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.ahetubahe_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(ahetubahe_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in ahetubahe_available_points if p not in [pt['point_id'] for pt in config.ahetubahe_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.ahetubahe_points[i].update({'point_id': v.get()}), refresh_ahetubahe_point_options(), save_config_to_file()])
            ahetubahe_id_selectors.append((point_selector, point_var, idx))

            # 窝子名称
            _,entry, _ = create_labeled_entry(
                group_frame,
                f"窝子名称",
                point["name"],
                lambda v, i=idx: [save_ahetubahe_name(i, v), save_config_to_file()],
                1
            )
            entry.config(width=15, font=("Microsoft YaHei", 8))
            ahetubahe_entries.append(entry)

            # 四个饵料
            for j in range(4):
                _,bait_entry, _ = create_labeled_entry(
                    group_frame,
                    f"饵料 {j+1}" if j != 3 else "PVA",
                    point["baits"][j],
                    lambda v, i=idx, j=j: [save_ahetubahe_bait(i, j, v), save_config_to_file()],
                    j + 2
                )
                bait_entry.config(width=15, font=("Microsoft YaHei", 8))
                ahetubahe_bait_entries.append(bait_entry)

            # 卡米数
            _,meters_entry, _ = create_labeled_entry(
                group_frame,
                f"卡米数",
                point["meters"],
                lambda v, i=idx: [save_ahetubahe_meters(i, v), save_config_to_file()],
                6
            )
            meters_entry.config(width=15, font=("Microsoft YaHei", 8))
            ahetubahe_meters_entries.append(meters_entry)

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.ahetubahe_points.pop(i), save_config_to_file(), render_ahetubahe_points(), update_ahetubahe_add_button_state()]
            ).grid(row=7, column=0, columnspan=2, pady=2)

    def add_ahetubahe_point():
        if len(config.ahetubahe_points) < 3:
            used_points = [p["point_id"] for p in config.ahetubahe_points]
            for point_id in ahetubahe_available_points:
                if point_id not in used_points:
                    config.ahetubahe_points.append({"name": "", "point_id": point_id, "baits": ["", "", "", ""], "meters": ""})
                    save_config_to_file()
                    render_ahetubahe_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大数量（3个）")

    ahetubahe_add_button = ttk.Button(
        frame_fishing_params_bottom,
        text="添加28图点位",
        style="Small.TButton",
        command=lambda: [add_ahetubahe_point(), update_ahetubahe_add_button_state()]
    )
    ahetubahe_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_ahetubahe_add_button_state():
        if len(config.ahetubahe_points) >= 3:
            ahetubahe_add_button.config(state="disabled")
        else:
            ahetubahe_add_button.config(state="normal")

    # 初始渲染
    render_ahetubahe_points()
    update_ahetubahe_add_button_state()

    # 为 weiyounuoke_mhl_points 添加 UI，类似于 tonghu，但无 baits，只有 name, point_id, meters
    weiyounuoke_mhl_entries = []
    weiyounuoke_mhl_meters_entries = []
    weiyounuoke_mhl_id_selectors = []  # 保存 (Combobox, StringVar, index)

    # 创建用于动态点位的容器框架
    weiyounuoke_mhl_container_row = row
    weiyounuoke_mhl_container = ttk.Frame(frame_fishing_params_bottom)
    weiyounuoke_mhl_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    # 保存 config 到文件的辅助函数
    def save_weiyounuoke_mhl_name(key, value):
        config.weiyounuoke_mhl_points[key]["name"] = value
        save_config_to_file()

    def save_weiyounuoke_mhl_meters(key, value):
        config.weiyounuoke_mhl_points[key]["meters"] = value
        save_config_to_file()


    # 刷新所有点位下拉框选项，防止重复
    def refresh_weiyounuoke_mhl_point_options():
        used = {var.get() for _, var, _ in weiyounuoke_mhl_id_selectors if var.get()}
        for combo, var, idx in weiyounuoke_mhl_id_selectors:
            current = var.get()
            values = [p for p in weiyounuoke_mhl_available_points if p not in used or p == current]
            combo['values'] = values
            
        if not config.weiyounuoke_mhl_points:
            for combo, _, _ in weiyounuoke_mhl_id_selectors:
                combo['values'] = []



    # 渲染点位函数
    def render_weiyounuoke_mhl_points():
        for widget in weiyounuoke_mhl_container.winfo_children():
            widget.destroy()
        weiyounuoke_mhl_entries.clear()
        weiyounuoke_mhl_meters_entries.clear()
        weiyounuoke_mhl_id_selectors.clear()

        if not config.weiyounuoke_mhl_points:
            ttk.Label(weiyounuoke_mhl_container, text="暂无惟有诺克河点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.weiyounuoke_mhl_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(weiyounuoke_mhl_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in weiyounuoke_mhl_available_points if p not in [pt['point_id'] for pt in config.weiyounuoke_mhl_points if pt != point]],  # 调整可用点位
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.weiyounuoke_mhl_points[i].update({'point_id': v.get()}), refresh_weiyounuoke_mhl_point_options(), save_config_to_file()])
            weiyounuoke_mhl_id_selectors.append((point_selector, point_var, idx))


            # 窝子名称
            _,entry, _ = create_labeled_entry(
                group_frame,
                f"窝子名称",
                point["name"],
                lambda v, i=idx: [save_weiyounuoke_mhl_name(i, v), save_config_to_file()],
                1
            )
            entry.config(width=15,font=("Microsoft YaHei", 8))
            weiyounuoke_mhl_entries.append(entry)


            # 卡米数
            _,meters_entry, _ = create_labeled_entry(
                group_frame,
                f"卡米数",
                point["meters"],
                lambda v, i=idx: [save_weiyounuoke_mhl_meters(i, v), save_config_to_file()],
                2
            )
            meters_entry.config(width=15,font=("Microsoft YaHei", 8))
            weiyounuoke_mhl_meters_entries.append(meters_entry)

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.weiyounuoke_mhl_points.pop(i), save_config_to_file(), render_weiyounuoke_mhl_points(), update_weiyounuoke_mhl_add_button_state()]
            ).grid(row=3, column=0, columnspan=2, pady=2)

    # 添加点位按钮
    def add_weiyounuoke_mhl_point():
        if len(config.weiyounuoke_mhl_points) < 3:
            used_points = [p["point_id"] for p in config.weiyounuoke_mhl_points]
            for point_id in weiyounuoke_mhl_available_points:
                if point_id not in used_points:
                    config.weiyounuoke_mhl_points.append({"name": "", "point_id": point_id, "meters": ""})
                    save_config_to_file()
                    render_weiyounuoke_mhl_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")


    weiyounuoke_mhl_add_button = ttk.Button(
        frame_fishing_params_bottom,
        text="添加惟有诺克河点位",
        style="Small.TButton",
        command=lambda: [add_weiyounuoke_mhl_point(), update_weiyounuoke_mhl_add_button_state()]
    )
    weiyounuoke_mhl_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1


    def update_weiyounuoke_mhl_add_button_state():
        if len(config.weiyounuoke_mhl_points) >= 3:
            weiyounuoke_mhl_add_button.config(state="disabled")
        else:
            weiyounuoke_mhl_add_button.config(state="normal")


    # 初始渲染
    render_weiyounuoke_mhl_points()
    update_weiyounuoke_mhl_add_button_state()

    # 更新 update_fields_state 以控制新容器可见性
    def update_fields_state(*args):
        is_bottom_mode = config.auto_mode in [0, 2]
        is_lure_mode = config.auto_mode in [1, 2]

        # 工具函数：更新输入框/选择器状态
        def set_state(entries, bait_entries, meters_entries, selectors, add_button, state):
            for entry in entries:
                entry.config(state=state)
            for entry in bait_entries:
                entry.config(state=state)
            for entry in meters_entries:
                entry.config(state=state)
            for combo, _, _ in selectors:
                combo.config(state=state)
            add_button.config(state=state)

        # 工具函数：显示 / 隐藏容器
        def show_container(container, add_button, row):
            container.grid(row=row, column=0, columnspan=2, sticky="w", pady=10, padx=10)
            add_button.grid(row=row+1, column=0, columnspan=2, pady=0, sticky="w")

        def hide_all_containers():
            for c in [laoao_container, hupo_container, tonghu_container, ahetubahe_container,weiyounuoke_mhl_container, baihe_container, aier_container,weiyounuoke_hand_container, beidun_hand_container]:
                c.grid_remove()
            for b in [laoao_add_button, hupo_add_button, tonghu_add_button, ahetubahe_add_button,weiyounuoke_mhl_add_button, baihe_add_button, aier_add_button, weiyounuoke_hand_add_button, beidun_hand_add_button]:
                b.grid_remove()

        # ------------------ 更新控件状态 ------------------
        set_state(laoao_entries, [], laoao_meters_entries, laoao_id_selectors, laoao_add_button,
                "normal" if is_bottom_mode and config.bottom_map == 0 else "disabled")
        set_state(hupo_entries, hupo_bait_entries, hupo_meters_entries, hupo_id_selectors, hupo_add_button,
                "normal" if is_bottom_mode and config.bottom_map == 1 else "disabled")
        set_state(ahetubahe_entries, ahetubahe_bait_entries, ahetubahe_meters_entries, ahetubahe_id_selectors, ahetubahe_add_button,
                "normal" if is_bottom_mode and config.bottom_map == 2 else "disabled")
        set_state(tonghu_entries, tonghu_bait_entries, tonghu_meters_entries, tonghu_id_selectors, tonghu_add_button,
                "normal" if is_bottom_mode and config.bottom_map == 3 else "disabled")
        set_state(weiyounuoke_mhl_entries, [], weiyounuoke_mhl_meters_entries, weiyounuoke_mhl_id_selectors, weiyounuoke_mhl_add_button,
                "normal" if is_bottom_mode and config.bottom_map == 4 else "disabled")        
        set_state([], [], [], [], baihe_add_button,
                "normal" if is_lure_mode and config.lure_map == 1 else "disabled")
        set_state([], [], [], [], aier_add_button,
                "normal" if is_lure_mode and config.lure_map == 2 else "disabled")
        
        set_state([], [], [], [], weiyounuoke_hand_add_button,
                "normal" if config.hand_rod_fishing_map == 1 else "disabled")
        set_state([], [], [], [], beidun_hand_add_button,
                "normal" if config.hand_rod_fishing_map == 2 else "disabled")

        # ------------------ 更新容器可见性 ------------------
        hide_all_containers()

        if is_bottom_mode:
            if config.bottom_map == 0:
                show_container(laoao_container, laoao_add_button, laoao_container_row)
            elif config.bottom_map == 1:
                show_container(hupo_container, hupo_add_button, hupo_container_row)
            elif config.bottom_map == 2:
                show_container(ahetubahe_container, ahetubahe_add_button, ahetubahe_container_row)
            elif config.bottom_map == 3:
                show_container(tonghu_container, tonghu_add_button, tonghu_container_row)
            elif config.bottom_map == 4:
                show_container(weiyounuoke_mhl_container, weiyounuoke_mhl_add_button, weiyounuoke_mhl_container_row)

        if is_lure_mode and config.lure_map == 1:
            show_container(baihe_container, baihe_add_button, baihe_container_row)
        elif is_lure_mode and config.lure_map == 2:
            show_container(aier_container, aier_add_button, aier_container_row)

        if config.hand_rod_fishing_map == 1:
            show_container(weiyounuoke_hand_container, weiyounuoke_hand_add_button, weiyounuoke_hand_container_row)
        elif config.hand_rod_fishing_map == 2:
            show_container(beidun_hand_container, beidun_hand_add_button, beidun_hand_container_row)

    #----------------------------路亚--------------------------------
    frame_fishing_params_lure = ttk.LabelFrame(tab_fishing_params, text="路亚", padding=5)
    frame_fishing_params_lure.pack(fill="x", padx=5, pady=5)

    row = 0

    lure_mode_map = {"匀速收线": 1, "抽停": 2}
    def get_lure_mode_text(val):
        for k, v in lure_mode_map.items():
            if v == val:
                return k
        return "匀速收线"

    lure_mode_var, lure_mode_combo, row = create_labeled_combobox(
        frame_fishing_params_lure,
        "路亚模式",
        list(lure_mode_map.keys()),
        get_lure_mode_text(config.lure_mode),
        lambda v: setattr(config, "lure_mode", lure_mode_map.get(v, 1)),
        row
    )

    lure_rod_name_var, lure_rod_name_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "路亚鱼竿名称",
        config.lure_rod_name,
        lambda v: setattr(config, "lure_rod_name", v),
        row
    )

    lure_rod_power_var, lure_rod_power_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "抛竿力度",
        config.lure_rod_power,
        lambda v: setattr(config, "lure_rod_power", int(v) if v.isdigit() else config.lure_rod_power),
        row
    )
    lure_rod_reeling_duration_var, lure_rod_reeling_duration_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "抽停收线时长(s)",
        config.lure_rod_reeling_duration,
        lambda v: setattr(config, "lure_rod_reeling_duration", float(v) if v.replace('.', '', 1).isdigit() else config.lure_rod_reeling_duration),
        row
    )
    lure_rod_stop_duration_var, lure_rod_stop_duration_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "抽停停止时长(s)",
        config.lure_rod_stop_duration,
        lambda v: setattr(config, "lure_rod_stop_duration", float(v) if v.replace('.', '', 1).isdigit() else config.lure_rod_stop_duration),
        row
    )    


    lure_reel_speed_var, lure_reel_speed_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "路亚轮子收线速度",
        config.lure_reel_speed,
        lambda v: setattr(config, "lure_reel_speed", int(v) if v.isdigit() else config.lure_reel_speed),
        row
    )

    lure_reel_friction_var, lure_reel_friction_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "路亚轮子摩擦力",
        config.lure_reel_friction,
        lambda v: setattr(config, "lure_reel_friction", int(v) if v.isdigit() else config.lure_reel_friction),
        row
    )

    lure_sink_time_var, lure_sink_time_entry, row = create_labeled_entry(
        frame_fishing_params_lure,
        "沉底的时间(s)",
        config.sink_time,
        lambda v: setattr(config, "sink_time", int(v) if v.isdigit() else config.sink_time),
        row
    )

    # lure_map_options = {"旧奥斯特罗格湖": 0, "白河": 1}
    lure_map_options = {"白河": 1,"埃尔克湖": 2}
    def get_lure_map_text(val):
        for k, v in lure_map_options.items():
            if v == val:
                return k
        return "白河"

    lure_map_var,lure_map_combo, row = create_labeled_combobox(
        frame_fishing_params_lure,
        "路亚地图",
        list(lure_map_options.keys()),
        get_lure_map_text(config.lure_map),
        lambda v: [setattr(config, "lure_map", lure_map_options.get(v, 1)), save_config_to_file(), update_fields_state()],
        row
    )

    # 为 baihe_entries 添加 UI，类似于 tonghu
    baihe_entries = []
    baihe_bait_entries = []
    baihe_meters_entries = []
    baihe_id_selectors = []

    baihe_container_row = row
    baihe_container = ttk.Frame(frame_fishing_params_lure)
    baihe_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_baihe_meters(key, value):
        config.baihe_lure_points[key]["meters"] = value
        save_config_to_file()

    def refresh_baihe_point_options():
        used = {var.get() for _, var, _ in baihe_id_selectors if var.get()}
        for combo, var, idx in baihe_id_selectors:
            current = var.get()
            values = [p for p in baihe_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.baihe_lure_points:
            for combo, _, _ in baihe_id_selectors:
                combo['values'] = []

    def render_baihe_points():
        for widget in baihe_container.winfo_children():
            widget.destroy()
        baihe_entries.clear()
        baihe_bait_entries.clear()
        baihe_meters_entries.clear()
        baihe_id_selectors.clear()

        if not config.baihe_lure_points:
            ttk.Label(baihe_container, text="暂无白河点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.baihe_lure_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(baihe_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in baihe_available_points if p not in [pt['point_id'] for pt in config.baihe_lure_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.baihe_lure_points[i].update({'point_id': v.get()}), refresh_baihe_point_options(), save_config_to_file()])
            baihe_id_selectors.append((point_selector, point_var, idx))

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.baihe_lure_points.pop(i), save_config_to_file(), render_baihe_points(), update_baihe_add_button_state()]
            ).grid(row=1, column=0, columnspan=2, pady=2)

    def add_baihe_point():
        if len(config.baihe_lure_points) < 3:
            used_points = [p["point_id"] for p in config.baihe_lure_points]
            available_points = baihe_available_points
            for point_id in available_points:
                if point_id not in used_points:
                    config.baihe_lure_points.append({"point_id": point_id})
                    save_config_to_file()
                    render_baihe_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    baihe_add_button = ttk.Button(
        frame_fishing_params_lure,
        text="添加白河点位",
        style="Small.TButton",
        command=lambda: [add_baihe_point(), update_baihe_add_button_state()]
    )
    baihe_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_baihe_add_button_state():
        if len(config.baihe_lure_points) >= 3:
            baihe_add_button.config(state="disabled")
        else:
            baihe_add_button.config(state="normal")

    # 刷新白河点位下拉框
    render_baihe_points()
    update_baihe_add_button_state()


    # 为 aier_entries 添加 UI，类似于 tonghu
    aier_entries = []
    aier_bait_entries = []
    aier_meters_entries = []
    aier_id_selectors = []

    aier_container_row = row
    aier_container = ttk.Frame(frame_fishing_params_lure)
    aier_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=0, padx=0)
    row += 1

    def save_aier_meters(key, value):
        config.aier_lure_points[key]["meters"] = value
        save_config_to_file()

    def refresh_aier_point_options():
        used = {var.get() for _, var, _ in aier_id_selectors if var.get()}
        for combo, var, idx in aier_id_selectors:
            current = var.get()
            values = [p for p in aier_available_points if p not in used or p == current]
            combo['values'] = values
        if not config.aier_lure_points:
            for combo, _, _ in aier_id_selectors:
                combo['values'] = []

    def render_aier_points():
        for widget in aier_container.winfo_children():
            widget.destroy()
        aier_entries.clear()
        aier_bait_entries.clear()
        aier_meters_entries.clear()
        aier_id_selectors.clear()

        if not config.aier_lure_points:
            ttk.Label(aier_container, text="暂无白河点位配置").grid(row=0, column=0, sticky="w")
            return

        row_frame = None
        for idx, point in enumerate(config.aier_lure_points):
            if idx % 3 == 0:
                row_frame = ttk.Frame(aier_container)
                row_frame.grid(row=idx // 3, column=0, sticky="w", pady=0, padx=0)

            group_frame = ttk.Frame(row_frame)
            group_frame.grid(column=idx % 3, row=0, sticky="w", padx=0)

            # 点位编号下拉框
            ttk.Label(group_frame, text="点位编号").grid(row=0, column=0, sticky="w", pady=2, padx=2)
            point_var = tk.StringVar(value=point['point_id'])
            point_selector = ttk.Combobox(
                group_frame,
                textvariable=point_var,
                values=[p for p in aier_available_points if p not in [pt['point_id'] for pt in config.aier_lure_points if pt != point]],
                state="readonly",
                width=12,
                font=("Microsoft YaHei", 8)
            )
            point_selector.grid(row=0, column=1, sticky="w", pady=2, padx=2)
            point_var.trace_add("write", lambda *a, v=point_var, i=idx: [config.aier_lure_points[i].update({'point_id': v.get()}), refresh_aier_point_options(), save_config_to_file()])
            aier_id_selectors.append((point_selector, point_var, idx))

            # 删除按钮
            ttk.Button(
                group_frame,
                text="删除",
                style="Small.TButton",
                command=lambda i=idx: [config.aier_lure_points.pop(i), save_config_to_file(), render_aier_points(), update_aier_add_button_state()]
            ).grid(row=1, column=0, columnspan=2, pady=2)

    def add_aier_point():
        if len(config.aier_lure_points) < 3:
            used_points = [p["point_id"] for p in config.aier_lure_points]
            for point_id in aier_available_points:
                if point_id not in used_points:
                    config.aier_lure_points.append({"point_id": point_id})
                    save_config_to_file()
                    render_aier_points()
                    break
            else:
                logger.warning("无可用点位可添加")
        else:
            logger.warning("已达到最大点位数量（3个）")

    aier_add_button = ttk.Button(
        frame_fishing_params_lure,
        text="添加埃尔客湖点位",
        style="Small.TButton",
        command=lambda: [add_aier_point(), update_aier_add_button_state()]
    )
    aier_add_button.grid(row=row, column=0, columnspan=2, pady=2, sticky="w")
    row += 1

    def update_aier_add_button_state():
        if len(config.aier_lure_points) >= 3:
            aier_add_button.config(state="disabled")
        else:
            aier_add_button.config(state="normal")

    # 刷新埃尔克湖点位下拉框
    render_aier_points()
    update_aier_add_button_state()

    # 初始化输入框状态
    update_fields_state()


    #----------------------------海图搬砖--------------------------------
    # Tab 1: 目的地设置
    tab_destination = ttk.Frame(notebook)
    notebook.add(tab_destination, text="海图")

    # frame_dest = ttk.LabelFrame(tab_destination, text="目的地坑位设置", padding=10)
    # frame_dest.pack(fill="both", expand=True, padx=5, pady=5)

    # 选择目的坑位区域
    frame_select_pit = ttk.LabelFrame(tab_destination, text="目的地坑位设置", padding=10)
    frame_select_pit.pack(fill="x", padx=5, pady=5)

    row = 0

    predefined_pits = {
        "34坑": (469, 337, 32, 0),
        "30坑": (367, 454, 18, 0),
        "41坑": (307, 173, 45, 0),
        "55坑": (742, 385, 30, 0),
        "75坑": (784, 627, 40, 0),
        "80坑": (656, 209, 30, 0),
        "120坑": (426, 218, 40, 0),
    }

    # Assume config has these new attributes
    # config.auto_change_pit = False  # Boolean to toggle mode
    # config.auto_pits = []  # List of up to 5 tuples (x, y, dist)

    # Initialize default selected pit
    selected_pit_default = "自定义"
    for k, v in predefined_pits.items():
        if not config.auto_change_pit and config.destination == (v[0], v[1]) and config.dist == v[2]:
            selected_pit_default = k
            break

    selected_pit = tk.StringVar(value=selected_pit_default)

    # Auto change pit toggle
    auto_var = tk.BooleanVar(value=config.auto_change_pit if hasattr(config, 'auto_change_pit') else False)

    def on_auto_toggle():
        config.auto_change_pit = auto_var.get()
        update_ui_state()
        save_config_to_file()

    def update_ui_state():
        state = "disabled" if auto_var.get() else "normal"
        pit_combo.config(state=state)
        x_entry.config(state=state)
        y_entry.config(state=state)
        dist_entry.config(state=state)
        cast_line_meters_entry.config(state=state)
        
        auto_state = "normal" if auto_var.get() else "disabled"
        for i in range(5):
            auto_x_entries[i].config(state=auto_state)
            auto_y_entries[i].config(state=auto_state)
            auto_dist_entries[i].config(state=auto_state)
            auto_cast_entries[i].config(state=auto_state)

    # Original single pit settings
    def on_pit_select(value):
        if value in predefined_pits:
            x, y, d, c = predefined_pits[value]
            config.destination = (x, y)
            config.dist = d
            config.cast_line_meters = c
            x_var.set(str(x))
            y_var.set(str(y))
            dist_var.set(str(d))
            cast_line_meters_var.set(str(config.cast_line_meters))
        save_config_to_file()

    def on_x_change(v):
        try:
            x = int(v)
            config.destination = (x, config.destination[1])
        except:
            pass
        save_config_to_file()

    def on_y_change(v):
        try:
            y = int(v)
            config.destination = (config.destination[0], y)
        except:
            pass
        save_config_to_file()

    def on_dist_change(v):
        try:
            d = int(v)
            config.dist = d
        except:
            pass
        save_config_to_file()

    def on_cast_line_meters_change(v):
        try:
            d = int(v)
            config.cast_line_meters = d
        except:
            pass
        save_config_to_file()

    ttk.Label(frame_select_pit, text="选择目的地坑位").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    pit_combo = ttk.Combobox(frame_select_pit,
                            values=list(predefined_pits.keys()) + ["自定义"],
                            textvariable=selected_pit,
                            state="readonly",
                            width=19,font=("Microsoft YaHei", 8))
    pit_combo.grid(row=row, column=1, sticky="w", padx=2)
    pit_combo.bind("<<ComboboxSelected>>", lambda e: on_pit_select(selected_pit.get()))
    row += 1

    x_var = tk.StringVar(value=str(config.destination[0]))
    ttk.Label(frame_select_pit, text="目标 X 坐标").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    x_entry = ttk.Entry(frame_select_pit, textvariable=x_var, width=22,font=("Microsoft YaHei", 8))
    x_entry.grid(row=row, column=1, sticky="w", padx=2)
    x_var.trace_add("write", lambda *_, v=x_var: on_x_change(v.get()))
    row += 1

    y_var = tk.StringVar(value=str(config.destination[1]))
    ttk.Label(frame_select_pit, text="目标 Y 坐标").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    y_entry = ttk.Entry(frame_select_pit, textvariable=y_var, width=22,font=("Microsoft YaHei", 8))
    y_entry.grid(row=row, column=1, sticky="w", padx=2)
    y_var.trace_add("write", lambda *_, v=y_var: on_y_change(v.get()))
    row += 1

    dist_var = tk.StringVar(value=str(config.dist))
    ttk.Label(frame_select_pit, text="回坑距离").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    dist_entry = ttk.Entry(frame_select_pit, textvariable=dist_var, width=22,font=("Microsoft YaHei", 8))
    dist_entry.grid(row=row, column=1, sticky="w", padx=2)
    dist_var.trace_add("write", lambda *_, v=dist_var: on_dist_change(v.get()))
    row += 1

    cast_line_meters_var = tk.StringVar(value=str(config.cast_line_meters))
    ttk.Label(frame_select_pit, text="卡米数").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    cast_line_meters_entry = ttk.Entry(frame_select_pit, textvariable=cast_line_meters_var, width=22,font=("Microsoft YaHei", 8))
    cast_line_meters_entry.grid(row=row, column=1, sticky="w", padx=2)
    cast_line_meters_var.trace_add("write", lambda *_, v=cast_line_meters_var: on_cast_line_meters_change(v.get()))
    row += 1


    # 自动换坑设置区域
    frame_auto_pits = ttk.LabelFrame(tab_destination, text="自动换坑设置", padding=10)
    frame_auto_pits.pack(fill="x", padx=5, pady=5)

    ttk.Checkbutton(frame_auto_pits, text="启用卖鱼后自动换坑（最多5个坑位）", variable=auto_var, command=on_auto_toggle).grid(row=row, column=0, columnspan=2, sticky="w", pady=5, padx=5)
    row += 1

    # # Auto change pits section
    # ttk.Label(frame_auto_pits, text="自动换坑设置（最多5个）").grid(row=row, column=0, columnspan=2, sticky="w", pady=10, padx=5)
    # row += 1

    # Initialize auto_pits list, pad to 5 with (0,0,0,0) if needed
    auto_pits = config.auto_pits if hasattr(config, 'auto_pits') else []
    while len(auto_pits) < 5:
        auto_pits.append((0, 0, 0, 0))

    auto_x_vars = [tk.StringVar(value=str(auto_pits[i][0])) for i in range(5)]
    auto_y_vars = [tk.StringVar(value=str(auto_pits[i][1])) for i in range(5)]
    auto_dist_vars = [tk.StringVar(value=str(auto_pits[i][2])) for i in range(5)]
    auto_cast_vars = [tk.StringVar(value=str(auto_pits[i][3])) for i in range(5)]

    auto_x_entries, auto_y_entries, auto_dist_entries, auto_cast_entries = [], [], [], []

    def save_auto_pits():
        config.auto_pits = [pit for pit in auto_pits if pit != (0, 0, 0, 0)]
        save_config_to_file()

    def on_auto_change(idx, key, value):
        try:
            val = int(value)
            x, y, d, cast = auto_pits[idx]
            if key == "x":
                auto_pits[idx] = (val, y, d, cast)
            elif key == "y":
                auto_pits[idx] = (x, val, d, cast)
            elif key == "dist":
                auto_pits[idx] = (x, y, val, cast)
            elif key == "cast":
                auto_pits[idx] = (x, y, d, val)
            save_auto_pits()
        except:
            pass

    frame_auto_pits.columnconfigure(0, weight=1)

    for i in range(5):
        row_frame = ttk.Frame(frame_auto_pits)
        row_frame.grid(row=row, column=0, sticky="w", padx=5, pady=2)

        pit_x_frame = ttk.Frame(row_frame)
        pit_x_frame.pack(side="left", padx=(0, 15))
        ttk.Label(pit_x_frame, text=f"坑位 {i+1}").pack(side="left")
        ttk.Label(pit_x_frame, text=" X:").pack(side="left")
        entry_x = ttk.Entry(pit_x_frame, textvariable=auto_x_vars[i], width=8)
        entry_x.pack(side="left")
        auto_x_entries.append(entry_x)
        auto_x_vars[i].trace_add("write", lambda *_, idx=i, v=auto_x_vars[i]: on_auto_change(idx, "x", v.get()))

        y_frame = ttk.Frame(row_frame)
        y_frame.pack(side="left", padx=(0, 15))
        ttk.Label(y_frame, text="Y:").pack(side="left")
        entry_y = ttk.Entry(y_frame, textvariable=auto_y_vars[i], width=8)
        entry_y.pack(side="left")
        auto_y_entries.append(entry_y)
        auto_y_vars[i].trace_add("write", lambda *_, idx=i, v=auto_y_vars[i]: on_auto_change(idx, "y", v.get()))

        dist_frame = ttk.Frame(row_frame)
        dist_frame.pack(side="left", padx=(0, 15))
        ttk.Label(dist_frame, text="回坑距离:").pack(side="left")
        entry_dist = ttk.Entry(dist_frame, textvariable=auto_dist_vars[i], width=8)
        entry_dist.pack(side="left")
        auto_dist_entries.append(entry_dist)
        auto_dist_vars[i].trace_add("write", lambda *_, idx=i, v=auto_dist_vars[i]: on_auto_change(idx, "dist", v.get()))

        cast_frame = ttk.Frame(row_frame)
        cast_frame.pack(side="left")
        ttk.Label(cast_frame, text="卡米数:").pack(side="left")
        entry_cast = ttk.Entry(cast_frame, textvariable=auto_cast_vars[i], width=8)
        entry_cast.pack(side="left")
        auto_cast_entries.append(entry_cast)
        auto_cast_vars[i].trace_add("write", lambda *_, idx=i, v=auto_cast_vars[i]: on_auto_change(idx, "cast", v.get()))

        row += 1

    # Initial UI state update
    update_ui_state()

    # Tab 2: 海图设置
    # tab_params = ttk.Frame(notebook)
    # notebook.add(tab_params, text="海图设置")

    frame_params = ttk.LabelFrame(tab_destination, text="海图参数", padding=10)
    frame_params.pack(fill="x", padx=5, pady=5)

    row = 0


    status_type_map = {
        "轻微": 1,
        "强烈": 2,
        "jig": 3,
        "随机": 4,
        "摆烂": 5,
        "自定义": 6,
    }

    def get_status_type_text(num):
        for k, v in status_type_map.items():
            if v == num:
                return k
        return "轻微"

    def update_status_sleep(v):
        try:
            config.status_sleep = float(v)
        except:
            pass
        save_config_to_file()

    def update_status_click(v):
        try:
            config.status_click = float(v)
        except:
            pass
        save_config_to_file()

    def on_status_type_change(v):
        config.status_type = status_type_map.get(v, 1)
        if config.status_type == 6:  # 自定义
            entry_sleep.config(state="normal")
            entry_click.config(state="normal")
        else:
            entry_sleep.config(state="disabled")
            entry_click.config(state="disabled")
        save_config_to_file()

    def on_reel_type_change(v):
        try:
            config.reel_type = reel_type_map.get(v, 1)
        except:
            pass
        save_config_to_file()    

    reel_type_map = {
        "纺车轮": 1,
        "鼓轮": 2,
        "电轮": 3,
    }

    def get_reel_type_text(num):
        for k, v in reel_type_map.items():
            if v == num:
                return k
        return "纺车轮"

    reel_type_var, reel_type_combo, row = create_labeled_combobox(
        frame_params,
        "轮子类型",
        list(reel_type_map.keys()),
        get_reel_type_text(config.reel_type),
        on_reel_type_change,
        row
    )    

    fishing_rod_btn_var, fishing_rod_btn_entry, row = create_labeled_entry(frame_params, "海图鱼竿按键", config.fishing_rod_btn, lambda v: setattr(config, "fishing_rod_btn", int(v) if v.isdigit() else config.fishing_rod_btn), row)

    change_leader_line_max_value_var, change_leader_line_max_value_entry, row = create_labeled_entry(
    frame_params,
    "损耗多少更换引线",
    config.change_leader_line_max_value,
    lambda v: setattr(config, "change_leader_line_max_value", float(v) if v.replace('.', '', 1).isdigit() else config.change_leader_line_max_value),
    row
    )
    ticket_target_count_var, ticket_target_count_entry, row = create_labeled_entry(frame_params, "保持船票的数量", config.ticket_target_count, lambda v: setattr(config, "ticket_target_count", int(v) if v.isdigit() else config.ticket_target_count), row)

    status_type_var, status_type_combo, row = create_labeled_combobox(
        frame_params,
        "状态类型",
        list(status_type_map.keys()),
        get_status_type_text(config.status_type),
        on_status_type_change,
        row
    )

    status_sleep_var = tk.StringVar(value=str(getattr(config, "status_sleep", 2)))
    status_click_var = tk.StringVar(value=str(getattr(config, "status_click", 2)))

    is_shift_var, row = create_checkbox(frame_params,"是否按 Shift 抬竿",getattr(config, "is_shift", False),lambda v: setattr(config, "is_shift", bool(v)),row)

    ttk.Label(frame_params, text="抬竿间隔(s)").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    entry_sleep = ttk.Entry(frame_params, textvariable=status_sleep_var, width=22,font=("Microsoft YaHei", 8))
    entry_sleep.grid(row=row, column=1, sticky="w", padx=2)
    status_sleep_var.trace_add("write", lambda *_, v=status_sleep_var: update_status_sleep(v.get()))
    row += 1

    ttk.Label(frame_params, text="右键按住时间(s)").grid(row=row, column=0, sticky="w", pady=2, padx=2)
    entry_click = ttk.Entry(frame_params, textvariable=status_click_var, width=22,font=("Microsoft YaHei", 8))
    entry_click.grid(row=row, column=1, sticky="w", padx=2)
    status_click_var.trace_add("write", lambda *_, v=status_click_var: update_status_click(v.get()))
    row += 1

    reeling_time_after_status_detected_var, reeling_time_after_status_detected_entry, row = create_labeled_entry(
    frame_params,
    "沉底后收线时间 (s)",
    config.reeling_time_after_status_detected,
    lambda v: setattr(config, "reeling_time_after_status_detected", float(v) if v.replace('.', '', 1).isdigit() else config.reeling_time_after_status_detected),
    row,
    tooltip_text="第一次出现底部的运动后会收线，该值为收线的时长"
    )

    sleep_when_on_status_var, sleep_when_on_status_entry, row = create_labeled_entry(
    frame_params,
    "沉底后延迟 (s)",
    config.sleep_when_on_status,
    lambda v: setattr(config, "sleep_when_on_status", float(v) if v.replace('.', '', 1).isdigit() else config.sleep_when_on_status),
    row,
    tooltip_text="出现底部的运动后延迟多久锁轮"
    )

    # 根据初始类型设置禁用状态
    if config.status_type == 6:
        entry_sleep.config(state="normal")
        entry_click.config(state="normal")
    else:
        entry_sleep.config(state="disabled")
        entry_click.config(state="disabled")

    # cast_line_meters_var, cast_line_meters_entry, row = create_labeled_entry(frame_params, "卡米距离", config.cast_line_meters, lambda v: setattr(config, "cast_line_meters", int(v) if v.isdigit() else config.cast_line_meters), row)
    # max_cast_line_meters_var, row = create_labeled_entry(frame_params, "出线米数小退", config.max_cast_line_meters, lambda v: setattr(config, "max_cast_line_meters", int(v) if v.isdigit() else config.max_cast_line_meters), row)

    fish_block_types_map = {
        "小块": 1,
        "鱼柳": 2,
        "大块": 3,
        "巨大": 4,
    }

    def get_fish_block_types1_text(num):
        for k, v in fish_block_types_map.items():
            if v == num:
                return k
        return "鱼柳"

    def get_fish_block_types2_text(num):
        for k, v in fish_block_types_map.items():
            if v == num:
                return k
        return "鱼柳"

    def on_is_cut_fish_change(val):
        config.is_cut_fish = bool(val)
        state = "readonly" if config.is_cut_fish else "disabled"
        fish_block_types1_combo.config(state=state)
        fish_block_types2_combo.config(state=state)
        cb2.config(state=state)


    # is_cut_fish_var, row = create_checkbox(frame_params, "是否切鱼块", config.is_cut_fish, on_is_cut_fish_change, row)

    # 放在一行里的容器
    checkbox_frame_params_container = ttk.Frame(frame_params)
    checkbox_frame_params_container.grid(row=row, column=0, columnspan=2, sticky="w", pady=2)

    is_cut_fish_var = tk.BooleanVar(value=getattr(config, "is_cut_fish", False))
    cb1 = ttk.Checkbutton(checkbox_frame_params_container, text="是否切鱼块", variable=is_cut_fish_var)
    cb1.pack(side="left", padx=2)
    def trace_func1(*args):
        setattr(config, "is_cut_fish", bool(is_cut_fish_var.get()))
        on_is_cut_fish_change(is_cut_fish_var.get())
        save_config_to_file()
    is_cut_fish_var.trace_add("write", trace_func1)

    is_cut_low_quality_fish_var = tk.BooleanVar(value=getattr(config, "is_cut_low_quality_fish", False))
    cb2 = ttk.Checkbutton(checkbox_frame_params_container, text="是否切3k以下的绿青鳕鱼块", variable=is_cut_low_quality_fish_var)
    cb2.pack(side="left", padx=2)
    def trace_func2(*args):
        setattr(config, "is_cut_low_quality_fish", bool(is_cut_low_quality_fish_var.get()))
        save_config_to_file()
    is_cut_low_quality_fish_var.trace_add("write", trace_func2)

    row += 1

    fish_block_types1_var, fish_block_types1_combo, row = create_labeled_combobox(
        frame_params,
        "绿青鳕鱼块",
        list(fish_block_types_map.keys()),
        get_fish_block_types1_text(config.fish_block_types1),
        lambda v: setattr(config, "fish_block_types1", fish_block_types_map.get(v, 2)),
        row
    )
    fish_block_types2_var, fish_block_types2_combo, row = create_labeled_combobox(
        frame_params,
        "鲭鱼块",
        list(fish_block_types_map.keys()),
        get_fish_block_types2_text(config.fish_block_types2),
        lambda v: setattr(config, "fish_block_types2", fish_block_types_map.get(v, 2)),
        row
    )

    # 创建一个横向的容器
    fly_frame = ttk.Frame(frame_params)
    fly_frame.grid(row=row, column=0, columnspan=2, sticky="w", pady=2)

    # 是否为飞机票
    is_fly_ticket_var = tk.BooleanVar(value=getattr(config, "is_fly_ticket", False))
    cb_fly_ticket = ttk.Checkbutton(fly_frame, text="是否为飞机票", variable=is_fly_ticket_var)
    cb_fly_ticket.pack(side="left", padx=4)
    def trace_fly_ticket(*args):
        setattr(config, "is_fly_ticket", bool(is_fly_ticket_var.get()))
        # 同步控制是否使用飞机竿的可用状态
        state = "normal" if is_fly_ticket_var.get() else "disabled"
        cb_fly_rod.config(state=state)
        save_config_to_file()
    is_fly_ticket_var.trace_add("write", trace_fly_ticket)

    # 是否使用飞机竿
    is_fly_rod_var = tk.BooleanVar(value=getattr(config, "is_fly_rod", False))
    cb_fly_rod = ttk.Checkbutton(fly_frame, text="是否使用飞机竿", variable=is_fly_rod_var)
    cb_fly_rod.pack(side="left", padx=4)
    def trace_fly_rod(*args):
        setattr(config, "is_fly_rod", bool(is_fly_rod_var.get()))
        save_config_to_file()
    is_fly_rod_var.trace_add("write", trace_fly_rod)



    # Tab 3: 拖钓设置
    tab_trolling = ttk.Frame(notebook)
    notebook.add(tab_trolling, text="拖钓设置")

    frame_trolling = ttk.LabelFrame(tab_trolling, text="拖钓参数", padding=10)
    frame_trolling.pack(fill="both", expand=True, padx=5, pady=5)

    row = 0

    is_trolling_var, row = create_checkbox(frame_trolling, "是否开启拖钓模式（需要手动配合）", config.is_trolling_mode, lambda v: setattr(config, "is_trolling_mode", bool(v)), row)

    direction_map = {
        "右转圈": 1,
        "左转圈": 2,
        "直线": 3,
    }
    def get_direction_text(val):
        for k, v in direction_map.items():
            if v == val:
                return k
        return "直线"
    direction_var, direction_combo, row = create_labeled_combobox(
        frame_trolling,
        "拖钓转圈方向",
        list(direction_map.keys()),
        get_direction_text(config.direction),
        lambda v: setattr(config, "direction", direction_map.get(v, 3)),
        row
    )

    troll_status_map = {
        "卡米强抽": 1,
        "打电梯": 2,
    }
    def get_troll_status_text(val):
        for k, v in troll_status_map.items():
            if v == val:
                return k
        return "打电梯"
    troll_status_var, troll_status_combo, row = create_labeled_combobox(
        frame_trolling,
        "拖钓打状态方式",
        list(troll_status_map.keys()),
        get_troll_status_text(config.trolling_status_type),
        lambda v: setattr(config, "trolling_status_type", troll_status_map.get(v, 2)),
        row
    )

    trolling_reeling_speed_var, trolling_reeling_speed_entry, row = create_labeled_entry(frame_trolling, "打电梯收线速度", config.trolling_reeling_speed, lambda v: setattr(config, "trolling_reeling_speed", int(v) if v.isdigit() else config.trolling_reeling_speed), row)
    trolling_unlock_meters_var, trolling_unlock_meters_entry, row = create_labeled_entry(frame_trolling, "打电梯放线米数", config.trolling_unlock_meters, lambda v: setattr(config, "trolling_unlock_meters", int(v) if v.isdigit() else config.trolling_unlock_meters), row)

    # Tab 4: 点锁设置
    tab_lock = ttk.Frame(notebook)
    notebook.add(tab_lock, text="点锁/传动比设置")

    frame_lock = ttk.LabelFrame(tab_lock, text="点锁参数", padding=10)
    frame_lock.pack(fill="x", padx=5, pady=5)

    row = 0

    # 是否只开启点锁功能
    def on_open_lock_toggle(val):
        config.open_lock_unlock_alone = bool(val)
        save_config_to_file()

    open_lock_unlock_alone_var, row = create_checkbox(frame_lock, "是否只开启点锁功能", config.open_lock_unlock_alone, on_open_lock_toggle, row)


    # 是否开启点锁功能
    def is_open_lock_unlock_toggle(val):
        config.is_open_lock_unlock = bool(val)
        save_config_to_file()

    is_open_lock_unlock_var, row = create_checkbox(frame_lock, "是否开启点锁功能", config.is_open_lock_unlock, is_open_lock_unlock_toggle, row)


    # # 升摩擦的值
    # def on_lock_value_change_min(v):
    #     try:
    #         config.min_lock_unlock_value = float(v)
    #     except:
    #         pass
    #     save_config_to_file()

    # min_lock_unlock_value_var, min_lock_unlock_value_entry, row = create_labeled_entry(
    #     frame_lock,
    #     "升摩擦的值(0.0 ~ 1.0)",
    #     config.min_lock_unlock_value,
    #     on_lock_value_change_min,
    #     row
    # )

    # 降摩擦的值
    def on_lock_value_change_max(v):
        try:
            config.max_lock_unlock_value = float(v)
        except:
            pass
        save_config_to_file()

    max_lock_unlock_value_var, max_lock_unlock_value_entry, row = create_labeled_entry(
        frame_lock,
        "降摩擦的值(0.0 ~ 1.0)",
        config.max_lock_unlock_value,
        on_lock_value_change_max,
        row
    )


    frame_gear_ratio = ttk.LabelFrame(tab_lock, text="鼓轮切换传动比", padding=10)
    frame_gear_ratio.pack(fill="x", padx=5, pady=5)

    row = 0

    # 是否开启切换传动比
    def is_open_gear_ratio_toggle(val):
        config.is_open_gear_ratio = bool(val)
        save_config_to_file()

    is_open_gear_ratio_var, row = create_checkbox(frame_gear_ratio, "是否开启自动切换传动比", config.is_open_gear_ratio, is_open_gear_ratio_toggle, row)

    gear_ratio_var, gear_ratio_entry, row = create_labeled_entry(
        frame_gear_ratio,
        "切换传动比的值",
        config.gear_ratio,
        lambda v: setattr(config, "gear_ratio", float(v) if v.replace('.', '', 1).isdigit() else config.gear_ratio),
        row
    )


    


    # Tab 5：收益统计页
    tab_income = ttk.Frame(notebook)
    notebook.add(tab_income, text="收益统计")

    frame_income = ttk.LabelFrame(tab_income, text="收益信息", padding=10)
    frame_income.pack(fill="both", expand=True, padx=5, pady=5)

    start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 从 income_log.txt 第一行读取第一次启动时间
    income_log_file = "income_log.txt"
    first_start_time_str = start_time_str  # 默认使用当前时间
    if os.path.exists(income_log_file):
        with open(income_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                try:
                    # 提取第一行时间部分，例如 [2025-08-04 22:42:20]
                    first_line = lines[0].strip()
                    time_part = first_line.split("]")[0].strip("[")
                    # 验证时间格式
                    datetime.strptime(time_part, "%Y-%m-%d %H:%M:%S")
                    first_start_time_str = time_part
                except Exception as e:
                    logger.warning(f"解析第一次启动时间失败: {e}")
    else:
        # 文件不存在，写入当前时间作为第一次启动时间
        with open(income_log_file, "w", encoding="utf-8") as f:
            f.write(f"[{start_time_str}] 收益：0 银币\n")

    lbl_first_start_time = ttk.Label(frame_income, text=f"首次启动时间：{first_start_time_str}")
    lbl_first_start_time.pack(anchor="w", pady=2)        

    lbl_start_time = ttk.Label(frame_income, text=f"启动时间：{start_time_str}")
    lbl_start_time.pack(anchor="w", pady=2)

    lbl_income_last = ttk.Label(frame_income, text="最近一次收益：0 银币")
    lbl_income_last.pack(anchor="w", pady=2)

    lbl_income_total = ttk.Label(frame_income, text="总收益：0 银币")
    lbl_income_total.pack(anchor="w", pady=2)

    tree_income = ttk.Treeview(frame_income, columns=("time", "amount"), show="headings", height=10)
    tree_income.heading("time", text="时间")
    tree_income.heading("amount", text="银币收益")
    tree_income.column("time", width=120, anchor="center")
    tree_income.column("amount", width=100, anchor="center")
    tree_income.pack(fill="both", expand=True, padx=5, pady=5)


    def add_income_to_table(timestamp, amount):
        tree_income.insert("", "end", values=(timestamp, amount))


    def load_income_history():
        if not os.path.exists("income_log.txt"):
            return
        with open("income_log.txt", "r", encoding="utf-8") as f:
            # 跳过第一行（第一次启动时间）
            lines = f.readlines()
            for line in lines[1:]:
                if "收益" in line:
                    try:
                        # 解析格式: [12:34:56] 收益：251.49 银币
                        time_part = line.split("]")[0].strip("[")
                        amount_part = line.split("收益：")[1].split("银币")[0]
                        time_str = time_part.strip()
                        amount = float(amount_part.strip())
                        add_income_to_table(time_str, amount)
                        config.income.append(amount)
                    except Exception as e:
                        logger.warning(f"解析收益日志失败: {e}")

    
    # === 收益监控器函数 ===
    def setup_income_monitor(root, table, lbl_income_last, lbl_income_total):
        income_len = [len(config.income)]  # 记录已显示收益数量

        def monitor():
            current_len = len(config.income)
            if current_len > income_len[0]:
                new_items = config.income[income_len[0]:current_len]
                for amount in new_items:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    table.insert("", "end", values=(timestamp, amount))
                    # 追加写入收益日志文件
                    with open("income_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"[{timestamp}] 收益：{amount} 银币\n")
                income_len[0] = current_len

            # 更新界面标签
            if config.income:
                lbl_income_last.config(text=f"最近一次收益：{config.income[-1]} 银币")
                lbl_income_total.config(text=f"总收益：{round(sum(config.income),2)} 银币")
            else:
                lbl_income_last.config(text="最近一次收益：0 银币")
                lbl_income_total.config(text="总收益：0 银币")

            root.after(1000, monitor)  # 每秒刷新一次

        monitor()

    load_income_history()
    setup_income_monitor(root, tree_income, lbl_income_last, lbl_income_total)


    # Tab 6: 日志
    tab_log = ttk.Frame(notebook)
    notebook.add(tab_log, text="日志输出")

    log_frame = ttk.LabelFrame(tab_log, text="实时日志", padding=10)
    log_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # 添加滚动条到日志文本框
    log_scroll = ttk.Scrollbar(log_frame)
    log_scroll.pack(side="right", fill="y")

    text_log = tk.Text(log_frame, height=20, wrap="word", bg="#2b2b2b", fg="#00ff00", insertbackground="#00ff00", yscrollcommand=log_scroll.set)
    text_log.pack(fill="both", expand=True)
    log_scroll.config(command=text_log.yview)
    text_log.config(state="disabled")  # 设置为只读

    gui_handler = GuiLogger(text_log)
    gui_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S"))
    logger.addHandler(gui_handler)

    # === 状态栏：显示程序运行状态 ===
    status_bar = ttk.Label(root, text="", relief="sunken", anchor="w", padding=5, font=("Microsoft YaHei", 9))
    status_bar.pack(side="bottom", fill="x")

    def update_status_label():
        if config.program_starting:
            status_bar.config(text="⏳ 正在启动程序...")
        elif config._stopping:
            status_bar.config(text="⚠️ 正在停止程序...")
        elif config.stop_event.is_set():
            status_bar.config(text="🛑 程序已停止")
        elif not config.program_stopped:
            status_bar.config(text="✅ 程序运行中")
        else:
            status_bar.config(text="🔲 程序已准备就绪")
        root.after(1000, update_status_label)

    update_status_label()

    # 加载初始配置
    def loading_first_config():
        if not os.path.exists(CONFIG_FILE):
           save_config_to_file()
        file_path=get_last_open_file() or os.path.abspath(CONFIG_FILE)
        # 读取用户选择文件
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()

        # 覆盖写到根目录 config.json
        root_config_path = os.path.join(os.getcwd(), "config.json")
        with open(root_config_path, "w", encoding="utf-8") as f:
            f.write(data)

        # 刷新 UI
        refresh_ui()
    loading_first_config()

    root.mainloop()