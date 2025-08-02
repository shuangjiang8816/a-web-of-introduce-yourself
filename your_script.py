import json
import os.path
from datetime import datetime
import time
from json import JSONDecodeError
import sys

class Pat:
    def __init__(self, name, physical=50, mood=20,hungry=100,data=None,introduce=None,times=None,last_save_time=None):
        self.name = name
        self.physical = min(max(physical, 0), 100)
        self.mood = min(max(mood, 0), 150)
        self.last_interaction_time = datetime.now()
        self.hungry_interaction_time = datetime.now()
        self.last_save_time = last_save_time or datetime.now()
        self.introduce = introduce
        self.times = times
        self.hungry = hungry
        self.start = time.perf_counter()  # 更精确的计时方式
        self.data = data

    def _check_values(self):
        """确保数值在合理范围内"""
        self.hungry = min(max(self.hungry,0),200)
        self.physical = min(max(self.physical, 0), 100)
        self.mood = min(max(self.mood, 0), 150)

    def update_mood_by_time(self):
        """根据时间差更新心情"""
        now = datetime.now()

        # 在线时的心情衰减（每5秒-1心情）
        online_mood_seconds = (now - self.last_interaction_time).total_seconds()
        if online_mood_seconds >= 20:
            mood_loss = int(online_mood_seconds / 20)
            self.mood -= mood_loss
            self.mood = max(self.mood, 0)
            if mood_loss > 0:
                print(f"\n{self.name}感到无聊，心情-{mood_loss}")
            self.last_interaction_time = now
        """饥饿值计算"""
        online_hungry_seconds = (now - self.hungry_interaction_time).total_seconds()
        if online_hungry_seconds >= 60:
            hungry_loss = int(online_hungry_seconds / 60)
            self.hungry -= hungry_loss
            self.hungry = max(self.hungry, 0)
            if hungry_loss > 0:
                print(f"\n{self.name}饥饿值-{hungry_loss}")
            self.hungry_interaction_time = now

        self._check_values()

    def eat(self, food):
        if food == "apple" and self.physical < 100:
            self.physical += 10
            self.hungry += 10
            print(f"{self.name}吃了个苹果，体力+10，饥饿值+10")
        elif food == "bread" and self.physical < 100:
            self.physical += 15
            self.hungry += 15
            print(f"{self.name}吃了面包，体力+15,饥饿值+15")

        if self.physical >= 100:
            self.physical = 100
        if self.hungry >=200:
            self.hungry = 200
            print(f"{self.name}吃饱了")
        self.last_interaction_time = datetime.now()
        self._check_values()

    def play(self):
        if self.physical >= 25:
            self.physical -= 10
            self.mood += 5
            print(f"{self.name}玩得很开心！体力-10，心情+5")
        else:
            print(f"{self.name}太累了，需要休息。")
        self.last_interaction_time = datetime.now()
        self._check_values()

    def sleep(self):
        print(f"{self.name}正在睡觉，请不要打扰它~")
        time.sleep(5)  # 测试时缩短等待时间
        self.physical += 50
        self.mood += 2
        self.last_interaction_time = datetime.now()
        self._check_values()
        print(f"{self.name}睡醒了！体力恢复50，心情+2")

    def clear_screen(self):
        """清屏函数（跨平台）"""
        os.system('cls' if os.name == 'nt' else 'clear')

    # 打印宠物状态
    def status(self,mode=None):
        if not mode:
            print(f"\n[{self.name}状态] 体力:{self.physical}/100 心情:{self.mood}/150 饥饿值:{self.hungry}/200")
        elif mode == "introduce":
            print(f"{self.name}的介绍：{self.name}{self.introduce}")
        time.sleep(1)

    def settings(self):
        """内部方法，设置"""
        msg = input("1.修改介绍 2.查看介绍 3.修改名称 4.查看数据")
        if msg in ["1", "修改介绍"]:
            a = input(f"请输入需要修改的内容，如需退出请输入quit或退出:\n{self.name}的介绍：")
            if a not in ["quit", "退出"]:
                print(self.introduce)
        elif msg in ["2.查看介绍"]:
            print(f"{self.name}的介绍：{self.name}{self.introduce}")
        elif msg in ["3", "修改名称"]:
            a = input(f"请输入需要修改的名称，如需退出请输入quit或退出:\n新名称：")
            if a not in ["quit", "退出"]:
                self.data["name"], self.name = a, a
                pet = Pat(a)
                print("修改成功!")
        elif msg in ["4", "查看数据"]:
            print(f"已陪伴{self.name}:{self.times}s")

    def save(self):
        if self.times is not None:
            elapsed = (time.perf_counter() - self.start) + self.times
        else:
            elapsed = time.perf_counter() - self.start
        self.data = {
            "name": self.name,
            "physical": self.physical,
            "mood": self.mood,
            "last_save_time": datetime.now().isoformat(),
            "introduce":self.introduce,
            "hungry":self.hungry,
            "time":elapsed
        }
        try:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"保存失败: {e}")


# 创建字典
data = {
    "name": None,
    "physical": None,
    "mood": None,
    "last_save_time": None,
    "introduce": None,
    "hungry": None,
    "time": None
}
# 加载或创建宠物
try:
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            now = datetime.now()
            last_save_time = datetime.fromisoformat(data.get("last_save_time", datetime.now().isoformat()))
            # 离线时的心情衰减（每分钟-1心情）
            name = data["name"]
            if last_save_time:
                offline_minutes = (now - last_save_time).total_seconds() / 60
                if offline_minutes > 5:
                    data["mood"] = max(data["mood"], 0)
                    mood_loss = int(offline_minutes)
                    if mood_loss > 60:
                        mood_loss = 60
                        print(f"{name}在你离开时心情下降了{mood_loss}点！")
                    if 60 > mood_loss > 0:
                        print(f"{name}在你离开时心情下降了{mood_loss}点！")
                    data["mood"] -= mood_loss
                if offline_minutes > 10:
                    name = data["name"]
                    hungry_loss = int(offline_minutes / 60)
                    if hungry_loss >= 1:
                        print(f"{name}在你离开时饥饿值下降了{hungry_loss}点！")
                        data["hungry"] -= hungry_loss
                        if data["hungry"] < 0:
                            data["hungry"] = 0

            if data["hungry"] > 0:
                pet = Pat(
                    data=data,
                    name=data["name"],
                    physical=data["physical"],
                    mood=data["mood"],
                    introduce=data["introduce"],
                    last_save_time=last_save_time,
                    hungry=data["hungry"],
                    times=data["time"]
                )
                pet.update_mood_by_time()  # 加载后立即计算离线心情变化
            else:
                print(f"你离开的时间太长了，{name}饿死了")
                pet = Pat(input("创建新宠物：\n请输入宠物名："),data=data)
    else:
        pet = Pat(input("请输入宠物名："))
except (FileNotFoundError, JSONDecodeError, KeyError) as e:
    with open("error.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now().isoformat()}: {str(e)}\n")
    print("加载存档失败，创建新宠物")
    pet = Pat(input("请输入宠物名："),data=data)

# 主游戏循环
pet.status()
while True:
    pet.update_mood_by_time()  # 每次循环都检查心情变化

    print("\n" + "=" * 30)
    msg = input("请选择行为：\n1.吃东西 2.玩耍 3.睡觉 4.设置 5.保存 6.退出 \n> ")

    if msg in ["1", "吃东西"]:
        things = input("请选择食物：\n1.苹果 2.面包\n> ").strip()
        if things in ["1", "苹果"]:
            pet.eat("apple")
        elif things in ["2", "面包"]:
            pet.eat("bread")
        else:
            print("输入错误，请重新选择")
    elif msg in ["2", "玩耍"]:
        pet.play()
    elif msg in ["3", "睡觉"]:
        pet.sleep()
    elif msg in ["4", "设置"]:
        pet.settings()
        pet.status("introduce")
    elif msg in ["5", "保存"]:
        pet.save()
        print("已保存")
    elif msg in ["6", "退出"]:
        pet.save()
        break
    else:
        print("输入错误，请重新选择")

    pet.status()