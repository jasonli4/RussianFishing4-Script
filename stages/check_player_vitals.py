import random
import config
import utils
from utils import sleep_time

#自动补充体力和能量
def check_player_vitals():
    """
    检查玩家状态,自动补充状态
    """
    while not config.stop_event.is_set():
        # stamina=utils.analyze_region_colors(config.region_stamina)
        # hunger=utils.analyze_region_colors(config.region_hunger)
        stamina = utils.analyze_tension_color_percentage(config.region_stamina)
        hunger = utils.analyze_tension_color_percentage(config.region_hunger)
        if stamina is None or hunger is None:
            continue
        stamina = max(stamina['green'], stamina['yellow'], stamina['red'])*100
        hunger = max(hunger['green'], hunger['yellow'], hunger['red'])*100
        config.current_stamina = stamina

        if stamina<50 and config.is_reeling_line:
            utils.press_key(config.stamina_btn)
        if hunger<50  and config.is_reeling_line:
            utils.press_key(config.hunger_btn)
            
        sleep_time(random.uniform(6.1, 6.2))  
   