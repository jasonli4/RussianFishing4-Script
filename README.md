<div align="center">
    
# 俄罗斯钓鱼4自动钓鱼脚本

</div>


一个专为《俄罗斯钓鱼4》设计的自动化钓鱼工具，集成图形化界面（UI），支持 手杆、水底、路亚、海图模式等多种钓鱼方式。
程序可自动完成钓点导航、抛竿、收鱼、切鱼、卖鱼、咖啡厅任务、制作、打窝、体力补给等操作，实现全程无人值守钓鱼体验。

<div align="center">

    
![示例图片](readme.png)

</div>

## 功能介绍

### 手杆、水底、路亚
- **自动寻路**：自动前往目的地，完成咖啡厅任务及卖鱼操作。
- **自动钓鱼**：自动执行抛竿和收鱼。
- **定时换点**：自动更换钓点以提升效率。
- **昼夜切换**：白天使用路亚模式，夜间切换至水底模式。
- **自动打窝**：支持手抛窝子和PVA棒子（暂不支持蜗杆）。
- **自动切鱼肉**：自动完成鱼肉切割。

### 海图
- **支持搬砖、深坑、拖钓**：拖钓需配合部分手动操作。
- **自动寻路**：自动前往目的地，完成咖啡厅任务及卖鱼操作。
- **自动钓鱼**：自动抛竿、打状态、收鱼。
- **自动换坑/回坑**：自动切换坑位或返回钓点。
- **自动续费**：自动续费或补充船票。
- **自动更换引线、鱼饵**：确保持续钓鱼。
- **自动切鱼片**：自动完成鱼片切割。
- **智能切换**：电轮、鼓轮自动切换传动比。

### 其他功能
- **用户界面**：直观易用的UI界面。
- **全程自动点锁**：加速收鱼（需注意线组搭配）。
- **补充体力食物**：自动补充体力食物。
- **自动小退**：肘击后自动小退。
- **连点器**：用于快速制作物品，提升熟练度。
- **上星上蓝自动截图**：记录关键时刻。
- **定时睡眠**：模拟真实操作。
- **随机时间间隔**：操作时间间隔随机化。

## 程序使用说明

为确保脚本正常运行，请严格按照以下说明操作。

### 基本要求
- **分辨率**：仅支持1920x1080分辨率。
- **窗口模式**：仅支持全屏无边框窗口。
- **语言支持**：仅支持简体中文界面及简体中文游戏界面。
- **游戏内鼠标设置**：鼠标灵敏度需为默认值。
- **模式切换**：切换模式后需停止程序并重新启动。
- **后台运行**：建议在高配置环境下使用虚拟机（如VMware）进行后台运行。

### 手杆
- 配置好鱼竿并取出，仅支持**单杆**。
- 在设置中启用浮子相机，设置为“始终显示-中下-小”。
- 流水状态下，视角自动右转以保持顺水漂流；静水状态下视角保持不变。

### 全天水底模式
- 配置**三根鱼竿**，依次绑定到数字按键**1、2、3**。
- 将窝子添加到**喜欢列表**。
- 准备充足的窝子和鱼饵，强烈建议使用**彩虹线**。

### 水底自动挖饵
- 把铲子添加到**喜欢列表**

### 全天路亚模式
- 配置好鱼竿并添加到**喜欢列表**。

### 仅水底和仅路亚模式
- 仅包含自动抛竿、收鱼和水底挖饵功能。当鱼竿在水底点位放置好，或路亚到达目标点后，可随时启动或暂停，适合与手动操作配合使用。
- 仅水底模式卡米数会影响抛竿力度。

### 海图
- 仅支持**彩虹线**，仅支持在X坐标大于230的地方钓鱼，需配置好鱼竿并准备充足的鱼饵和引线。
- 在海上启动时，需回到船中，以从岸上进入船中的视角为基准，将船移动至目的地附近后再启动。
- 海图模式功能最完善。

## 开发环境搭建

### 开发模式
- **CPU环境**：兼容性强（推荐）。
- **GPU环境**：图像识别速度更快。
- **Python版本**：3.13.5。

#### 创建CPU环境
```bash
python -m venv venv_cpu
venv_cpu\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements_cpu.txt
```

#### 创建GPU环境
```bash
python -m venv venv_gpu
venv_gpu\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements_gpu.txt
# 查看CUDA版本
nvidia-smi
# 根据CUDA版本从官网获取下载链接
python -m pip install paddlepaddle-gpu==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu129/
```

> **注意**：请访问[PaddlePaddle官网](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/develop/install/pip/windows-pip.html)获取正确的CUDA版本安装链接。


## 添加水底路亚点位

在相关配置文件和脚本文件中添加水底路亚钓鱼点位。遵循以下步骤，确保正确集成而不产生冲突。

### 步骤 1: 更新配置文件
在 `gui_config.py` 文件中找到以下代码。将所需的点位添加到对应的地图数组中，遵循既定格式。如果点位与其他地图点位冲突，请添加后缀，例如 `67,59_laoao`。

```python
# 点位变量
# 水底
laoao_available_points = ["48,28", "23,67", "25,41", "42,32", "36,28", "35,29","20,34","35,58","23,45","09,50","27,27", "67,59_laoao","27,54"]  # 老奥点位
tonghu_available_points = ["66,55", "56,50", "67,59", "37,32", "44,34", "67,58", "66,59"]  # 铜湖点位
hupo_available_points = []  # 琥珀湖点位
ahetubahe_available_points = []  # 阿赫图巴赫点位
weiyounuoke_mhl_available_points = ["99,121"] # 惟有诺克河-梅花鲈点位
# 路亚
baihe_available_points = ["71,37", "66,28", "65,26", "73,45", "73,59"]  # 白河点位
aier_available_points = ["65,93"]  # 艾尔克湖点位
```

### 步骤 2: 在脚本文件中添加点位函数
在 `corestages_bottom_lure.py` 文件中定义新的点位函数。标准点位使用命名格式 `position_x_y`，带后缀的点位参考 `position_67_59_laoao`。数组元素如 `(-100, 5)` 表示将视角向左转动 100 个单位，并向前移动 5 秒。以人物进入地图时的初始视角和位置为基准。需自行测试，确保人物到达所需点位并能完成抛竿操作。

```python
def position_27_27():
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 2),
        (-500, 4),
        (-70, 3),
        (130, 6),
        (-780, 7.4),
        (-690, 0.4),
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)
```



## 运行与打包

### 运行方式

#### CPU环境
```bash
venv_cpu\Scripts\activate
python main.py
```

#### GPU环境
```bash
venv_gpu\Scripts\activate
python main.py
```

### 打包方式

#### CPU环境
```bash
venv_cpu\Scripts\activate
pyinstaller --clean main_cpu.spec
```

#### GPU环境
```bash
venv_gpu\Scripts\activate
pyinstaller --clean main_gpu.spec
```

## 注意事项
- 首次启动需等待一定时间。
- 脚本运行期间，**请勿随意干扰**脚本操作。
- 避免长时间挂机，建议配合手动操作。
- 本脚本为自动化辅助工具，使用者需自行承担使用风险。

## 语言支持
目前仅支持简体中文，欢迎通过贡献代码支持多语言。

## 社区
[![Discord](https://img.shields.io/badge/Join%20Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/sUTr9Z7dxW)

**QQ群**：1044761397

如果喜欢本项目，请点个Star⭐️！

## 贡献与反馈
通过[GitHub Issues](https://github.com/fyodorrss/RussianFishing4-Script/issues)或[Pull Requests](https://github.com/fyodorrss/RussianFishing4-Script/pulls)提交问题或建议，并提供系统环境、日志和重现步骤。

## 许可证
本项目采用[MIT许可证](LICENSE)。DLL版权归mono所有，遵守其许可协议。
