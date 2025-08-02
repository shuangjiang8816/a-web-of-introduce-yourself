import os
import sys
import json

# 创建日志字符串
error = ""
# 判断游戏数据文件是否存在
try:
    if os.path.exists(os.path.join("data","information.json")):
        # 游戏数据读取
        with open(os.path.join("data", "information.json"), 'r') as f:
            data = json.load(f)
            information = data['information']
            settings = data['settings']
            achievement = data['achievement']
            # 信息读取
            name = information['name']
            # 设置读取
            WIDTH = settings['WIDTH']
            HEIGHT = settings['HEIGHT']
    else:
        settings = {"WIDTH": 1000, "HEIGHT": 618}
        information = {"name": "player","high_store": 0,"apple": 0,"gold_apple": 0,"emerald": 0,"time": 0}
        data = {"settings":settings,"information":information}
        with open(os.path.join("data", "information.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        with open(os.path.join("data", "information.json"), 'r') as f:
            data = json.load(f)
            information = data['information']
            settings = data['settings']
            # 信息读取
            name = information['name']
            high_store = information['high_store']
            save_apple = information['apple']
            apple = str(save_apple)
            save_gold_apple = information['gold_apple']
            gold_apple = str(save_gold_apple)
            # 设置读取
            WIDTH = settings['WIDTH']
            HEIGHT = settings['HEIGHT']
except KeyError or json.decoder.JSONDecodeError:
    with open("崩溃报告.log",'w') as a:
        a.write("KeyError:文件内数据格式错误！你可以尝试删除游戏数据恢复,路径：./data/information.json")
        sys.exit()
except Exception as e:
    with open("崩溃报告.log",'w')as a:
        a.write(f"未知错误：{e}")
        sys.exit()

# 视频系统初始化
import pygame
import time
from datetime import datetime
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
infoObject = pygame.display.Info()
pygame.display.set_caption("minecraft 抢苹果")
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 2048)  # 设置合适的采样率和缓冲区大小
pygame.mixer.set_num_channels(8)
# 颜色
WHITE = (255, 255, 255)
GREEN = 0,255,0
black = (0, 0, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
yellow = (255, 255, 0)

# 游戏数据处理
game_time = information["time"] / 1000
if game_time < 300:
    game_time = f"{game_time:.2f}s"
elif 3600 > game_time > 300:
    game_time = f"{game_time / 60:.2f}m"
elif 86400 > game_time > 3600:
    game_time = f"{game_time / 3600:.2f}h"
else:
    game_time = f"{game_time / 86400:.2f}d"

# 窗口大小处理,判断是否是全屏
if (WIDTH, HEIGHT) != (0, 0):  # 不是全屏
    width = WIDTH / 2
    height = HEIGHT / 2
    Width = width
    Height = height
    resolution0 = 2
else:  # 是全屏
    # 获取屏幕长宽
    WIDTH = infoObject.current_w
    HEIGHT = infoObject.current_h
    width, height = WIDTH / 2, HEIGHT / 2
    Width, Height = width, height
    resolution0 = 1

# 创建空字典存储资源
resources = {"font":None,"sounds": {},"images": {}}
try:
    # 字体导入
    resources["font"] = os.path.join("data", "minecraft.ttf")
    # 音频预载
    resources["sounds"]["fizz"] = pygame.mixer.Sound(os.path.join("data", "sounds", "fizz.ogg"))
    resources["sounds"]["background"] = pygame.mixer.Sound(os.path.join("data", "sounds", "minecraft.ogg"))
    resources["sounds"]["arrow"] = pygame.mixer.Sound(os.path.join("data", "sounds", "bow.ogg"))
    resources["sounds"]["level_up"] = pygame.mixer.Sound(os.path.join("data", "sounds", "level_up.ogg"))
    resources["sounds"]["die"] = pygame.mixer.Sound(os.path.join("data", "sounds", "death.ogg"))
    resources["sounds"]["eat"] = pygame.mixer.Sound(os.path.join("data", "sounds", "eat1.ogg"))
    resources["sounds"]["transmission"] = pygame.mixer.Sound(os.path.join("data", "sounds", "portal.ogg"))
    resources["sounds"]["boom"] = pygame.mixer.Sound(os.path.join("data", "sounds", "explode1.ogg"))
    # 图片预载
    resources["images"]["player"] = pygame.image.load(os.path.join("data", "textures", "skins", "player.png"))
    resources["images"]["arrow"] = pygame.image.load(os.path.join("data", "textures", "other", "arrow.png"))
    resources["images"]["apple"] = pygame.image.load(os.path.join("data", "textures", "other", "apple.png"))
    resources["images"]["gold_apple"] = pygame.image.load(os.path.join("data", "textures", "other", "gold_apple.png"))
    resources["images"]["blood"] = pygame.image.load(os.path.join("data", "textures", "gui", "blood.png"))
    resources["images"]["gold_blood"] = pygame.image.load(os.path.join("data", "textures", "gui", "gold_blood.png"))
    resources["images"]["chorus_fruit"] = pygame.image.load(os.path.join("data", "textures", "other", "chorus_fruit.png"))
    resources["images"]["widgets_choose"] = pygame.image.load(os.path.join("data", "textures", "gui", "widgets_choose.png"))
    resources["images"]["creeper"] = pygame.image.load(os.path.join("data", "textures", "other", "creeper.png"))
    resources["images"]["boom"] = pygame.image.load(os.path.join("data", "textures", "other", "boom.png"))
    resources["images"]["widgets"] = pygame.image.load(os.path.join("data", "textures", "gui", "widgets.png"))
    resources["images"]["inventory"] = pygame.image.load(os.path.join("data", "textures", "gui", "inventory.png"))
except Exception as e:
    timestamp = datetime.now().timestamp()
    local_time = datetime.fromtimestamp(timestamp)
    time_str = local_time.strftime("%H:%M:%S")
    with open("崩溃报告.log", 'w', encoding='utf-8') as a:
        a.write(f"[{time_str}] Error:{e}")
        sys.exit()
# 播放音乐
print(resources["sounds"]["background"])
resources["sounds"]["background"].play(loops=-1)
resources["sounds"]["background"].set_volume(1)

# 游戏窗口设置
ttf = resources["font"]
windows = pygame.font.Font(ttf, 15)
textImage = windows.render("pygame", True, WHITE)
# 文字格式预载
text = pygame.font.Font(ttf, 25)
# 管理游戏的资源和行为
class Resource:
    def __init__(self):
        # 检测游戏是否在运行
        self.running = True
        """游戏资源"""
        self.apple_photo = resources["images"]["apple"]
        self.gold_apple_photo = resources["images"]["gold_apple"]
        self.chorus_fruit_photo = resources["images"]["chorus_fruit"]
        self.arrow_photo = resources["images"]["arrow"]
        self.creeper_photo = resources["images"]["creeper"]
        self.boom_photo = resources["images"]["boom"]
        self.gold_blood_photo = resources["images"]["gold_blood"]
        self.player_photo = resources["images"]["player"]
        self.blood_photo = resources["images"]["blood"]
        # 保存的数据
        self.save_apple = information['apple']
        self.high_store = information['high_store']
        self.save_gold_apple = information['gold_apple']
        """音频"""
        self.die_sound = resources["sounds"]["die"]
        # 创建不同方向的箭头
        self.arrow_s = self.arrow_photo  # 默认方向（右）
        self.arrow_d = pygame.transform.rotate(self.arrow_photo, 90)  # 上
        self.arrow_w = pygame.transform.rotate(self.arrow_photo, 180)  # 左
        self.arrow_a = pygame.transform.rotate(self.arrow_photo, 270)  # 下
        # 分别创建rect
        self.arrow_s_rect = self.arrow_s.get_rect()
        self.arrow_d_rect = self.arrow_d.get_rect()
        self.arrow_w_rect = self.arrow_w.get_rect()
        self.arrow_a_rect = self.arrow_a.get_rect()

    def save(self,mode=None):
        if mode == "game":
            resource.save_apple = resource.save_apple + thing.apple
            resource.save_gold_apple = resource.save_gold_apple + thing.gold_apple
            information['apple'] = resource.save_apple
            information['gold_apple'] = resource.save_gold_apple
            information['emerald'] = resource.save_apple + resource.save_gold_apple * 5
            new_data = {"information": information}
        else:
            new_data = achievement
        _data = {**data, **new_data}
        with open(os.path.join("data", "information.json"), 'w', encoding='utf-8') as _f:
            json.dump(data, _f, indent=4, ensure_ascii=False)

    @staticmethod
    def quit_game():
        # 将游戏运行状态设为False
        resource.running = False
        try:
            # 1. 先停止所有声音但不关闭mixer
            pygame.mixer.stop()

            # 2. 释放图片资源
            for img_name in list(resources["images"].keys()):
                if isinstance(resources["images"][img_name], pygame.Surface):
                    resources["images"][img_name] = None
                del resources["images"][img_name]

            # 3. 释放声音资源
            for sound_name in list(resources["sounds"].keys()):
                if isinstance(resources["sounds"][sound_name], pygame.mixer.Sound):
                    resources["sounds"][sound_name].stop()
                    resources["sounds"][sound_name] = None
                del resources["sounds"][sound_name]

            # 4. 最后关闭mixer
            pygame.mixer.quit()

            # 5. 确保pygame完全退出
            pygame.quit()
        except Exception as e:
            print(f"资源释放错误: {e}")
        finally:
            sys.exit()
resource = Resource()

# 管理渲染方法
class Render:
    @staticmethod
    def button(color: [int,int,int], buttons, word):
        """按钮渲染"""
        pygame.draw.rect(screen, color, buttons)
        screen.blit(word, (buttons.centerx - word.get_width() / 2,
                                 buttons.centery - word.get_height() / 2))
    @staticmethod
    def text(color: [int,int,int], word: str, size: int, x: [int,float], y: [int,float]):
        """文字渲染"""
        text_a = pygame.font.Font(ttf, size)
        title = text_a.render(word, True, color)
        screen.blit(title, (x, y))
render = Render()

# 将生成窗口不需要使用的库放到窗口生成后加载，加快载入速度
import random
import threading
from pygame import MOUSEBUTTONDOWN, KEYDOWN, MOUSEWHEEL
from pygame.sprite import Sprite

class Thing:
    def __init__(self):
        self.eat = False
        self.things = None
        self.choose = None
        self.things_number = 0
        self.apple = 0
        self.gold_apple = 0
        self.chorus_fruit = 0
        self.things_x,self.things_y = 0,0
        self.things_rect = pygame.Rect(self.things_x, self.things_y, 16, 16)
        self.widgets_choose_photo = resources["images"]["widgets_choose"]
        self.widgets_photo = resources["images"]["widgets"]

    def thing_product(self):
        if self.things is None:
            probability = random.randint(0, 100)
            if probability <= 5:
                thing.things = "gold_apple"
            elif 5 < probability <= 15:
                thing.things = "chorus_fruit"
            elif 15 < probability:
                thing.things = "apple"
            self.things_x = random.randint(50, WIDTH - 50)
            self.things_y = random.randint(50, HEIGHT - 30)
            self.things_rect = pygame.Rect(self.things_x, self.things_y, 16, 16)

    def thing_use(self):
        self.eat = True
        """物品使用"""
        if self.choose == "apple" and self.apple > 0:
            self.apple -= 1
            player.blood += 1
            resources["sounds"]["eat"].play(loops=3)
        elif self.choose == "gold_apple" and self.gold_apple > 0:
            self.gold_apple -= 1
            player.blood += 5
            player.gold_blood += 3
            resources["sounds"]["eat"].play(loops=3)
        elif self.choose == "chorus_fruit" and self.chorus_fruit > 0:
            self.chorus_fruit -= 1
            player.x = random.randint(50, WIDTH - 50)
            player.y = random.randint(50, HEIGHT - 50)
            player.rect = pygame.Rect(player.x, player.y, 16, 16)
            resources["sounds"]["eat"].play(loops=3)
            resources["sounds"]["transmission"].play()
        if player.blood > 10:
            player.blood = 10
        if player.gold_blood > 3:
            player.gold_blood = 3

    def thing_choose(self,event):
        if event.y > 0:  # 向上滚动
            self.things_number += 1
        elif event.y < 0:  # 向下滚动
            self.things_number -= 1
        elif event.key == pygame.K_KP_1:
            self.things_number = 0
        elif event.key == pygame.K_KP_2:
            self.things_number = 1
        elif event.key == pygame.K_KP_3:
            self.things_number = 2
        # 滚动循环
        if self.things_number > 2:
            self.things_number = 0
        elif self.things_number < 0:
            self.things_number = 2
        # 赋值
        if self.things_number == 0:
            self.choose = "apple"
        elif self.things_number == 1:
            self.choose = "gold_apple"
        elif self.things_number == 2:
            self.choose = "chorus_fruit"

    def draw(self):
        # 物品栏绘制
        screen.blit(self.widgets_photo, (Width-40, HEIGHT-33))
        if self.choose =="apple":
            screen.blit(self.widgets_choose_photo,(Width-38, HEIGHT-35))
        elif self.choose =="gold_apple":
            screen.blit(self.widgets_choose_photo,(Width-10, HEIGHT-35))
        elif self.choose =="chorus_fruit":
            screen.blit(self.widgets_choose_photo,(Width+12, HEIGHT-35))
        screen.blit(resource.apple_photo, (Width-37, HEIGHT-23))
        screen.blit(resource.gold_apple_photo, (Width-5, HEIGHT-23))
        screen.blit(resource.chorus_fruit_photo, (Width+25, HEIGHT-23))
        render.text(WHITE, f"{self.apple}", 10, Width - 10, HEIGHT - 10)
        render.text(WHITE, f"{self.gold_apple}", 10, Width + 15, HEIGHT - 10)
        render.text(WHITE, f"{self.chorus_fruit}", 10, Width + 40, HEIGHT - 10)
        # 物品绘制
        if self.things == "gold_apple":
            screen.blit(resource.gold_apple_photo,(self.things_x,self.things_y))
        elif self.things == "apple":
            screen.blit(resource.apple_photo,(self.things_x,self.things_y))
        elif self.things == "chorus_fruit":
            screen.blit(resource.chorus_fruit_photo,(self.things_x,self.things_y))

    @staticmethod
    def run():
        thing.draw()
        thing.thing_product()
thing = Thing()

class Bullet(Sprite):
    """子弹类"""

    def __init__(self, x, y, direction):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.direction = direction

        # 根据方向选择正确的箭头图片和rect
        if direction == "w":  # 上
            self.image = resource.arrow_w
            self.rect = resource.arrow_w_rect.copy()
            self.rect.center = (x + 8, y)
            self.speed_x = 0
            self.speed_y = -10
        elif direction == "a":  # 左
            self.image = resource.arrow_a
            self.rect = resource.arrow_a_rect.copy()
            self.rect.center = (x, y + 8)
            self.speed_x = -10
            self.speed_y = 0
        elif direction == "s":  # 下
            self.image = resource.arrow_s
            self.rect = resource.arrow_s_rect.copy()
            self.rect.center = (x + 8, y + 16)
            self.speed_x = 0
            self.speed_y = 10
        elif direction == "d":  # 右
            self.image = resource.arrow_d
            self.rect = resource.arrow_d_rect.copy()
            self.rect.center = (x + 16, y + 8)
            self.speed_x = 10
            self.speed_y = 0

    def update(self):
        """子弹移动"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 如果子弹超出屏幕，删除它
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

    def draw(self):
        """绘制子弹"""
        self.screen.blit(self.image, self.rect)
bullet = Bullet

# 玩家行为管理
blood_x = Width - 90
blood_y = HEIGHT - 50
gold_blood_y = HEIGHT - 70
class Player:
    def __init__(self):
        """基础数据"""
        self.die_music = 0
        self.blood = 10
        self.gold_blood = 0
        self.gold_blood_list = [1,2,3]
        self.blood_list = [1,2,3,4,5,6,7,8,9,10]
        self.direction = "d"
        self.speed = 2
        self.store = 0
        """渲染数据"""
        self.x,self.y = width,height
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        """子弹相关"""
        self.bullets = pygame.sprite.Group()  # 管理子弹
        self.fire_cooldown = 0  # 发射冷却时间

    def die(self):
        """死亡监测与渲染"""
        if not 0 < self.x < WIDTH or not 0 < self.y < HEIGHT:
            self.blood = 0
            # 抽象的调用，我也忘了怎么弄的，反正不吃性能，千万别动
            if self.die_music != 1:
                resource.die_sound.play()
                # 保存数据
                resource.save("game")
                self.die_music = 1
        if self.blood == 0:
            self.gold_blood = 0
            self.direction = ""
            render.text(red,"你死了",25,Width-50,Height-100)
            # 按钮渲染
            render.button(gray, game.button_quit, game.button_quit_text)
            # 重置
            render.button(gray, game.button_again, game.button_again_text)

    def move(self):
        """移动计算"""
        if self.direction =="w" and self.blood > 0:
            self.y -= self.speed
        elif self.direction == "a" and self.blood > 0:
            self.x -= self.speed
        elif self.direction =="s" and self.blood > 0:
            self.y += self.speed
        elif self.direction == "d" and self.blood > 0:
            self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, 16, 16)

    def fire_bullet(self):
        """根据当前方向发射子弹"""
        if self.fire_cooldown <= 0 < self.blood:
            direction = self.direction
            if direction:  # 只有有方向时才发射
                new_bullet = Bullet(self.x, self.y, direction)
                self.bullets.add(new_bullet)
                resources["sounds"]["arrow"].play()
                self.fire_cooldown = 15  # 设置冷却时间

    def update_bullets(self):
        """更新子弹位置"""
        self.bullets.update()
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

    def draw_bullets(self):
        """绘制所有子弹"""
        for bullet in self.bullets:
            bullet.draw()

    def draw(self):
        """绘制"""
        screen.blit(resource.player_photo, (self.x, self.y))
        render.text(WHITE, f"分数: {self.store}", 15, 5, 20)

        render.text(WHITE, f"x/y:{self.x,self.y}", 15, 5, 40)

        for blood_blit in self.blood_list:
            if self.blood >= blood_blit:
                screen.blit(resource.blood_photo,(blood_x + 15*blood_blit,blood_y))
        for gold_blood in self.gold_blood_list:
            if self.gold_blood >= gold_blood:
                screen.blit(resource.gold_blood_photo,(blood_x + 15*gold_blood,gold_blood_y))

    def check_rect(self):
        """检测玩家碰撞箱和物品的关系"""
        if self.rect.colliderect(thing.things_rect):
            if thing.things == "apple":
                thing.apple += 1
                self.store += 1
                thing.things = None
            elif thing.things == "gold_apple":
                thing.gold_apple += 1
                self.store += 5
                thing.things = None
            elif thing.things == "chorus_fruit":
                thing.chorus_fruit += 1
                self.store += 1
                thing.things = None
            print(self.store,thing.apple,thing.gold_apple,thing.chorus_fruit)

    def reset(self):
        self.die_music = 0
        self.x, self.y = width, height
        self.direction = "d"
        self.blood = 10
        self.gold_blood = 0
        self.store = 0
        self.bullets.empty()  # 清空所有子弹
        thing.things = None
        thing.apple = 0
        thing.gold_apple = 0
        thing.chorus_fruit = 0

    @staticmethod
    def run():
        player.move()
        player.die()
        player.draw()
        player.check_rect()
        player.update_bullets()
        player.draw_bullets()
player = Player()

class Creeper:
    def __init__(self):
        self.shoot = False
        self.x,self.y = 9999,9999
        # 血条设置
        self.hp_bar_width = 100
        self.hp_bar_height = 5
        self.hp_x = WIDTH-110
        self.hp_y = 25
        self.blood = 10
        self.drawing = False
        self.start = False # 检测是否开始倒计时
        self.boom_time = None
        self.product_time = int(time.time())
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.boom_rect = pygame.Rect(self.x - 48, self.y - 48, 112, 112)
        self.creeper = False # 判断是否需要生成苦力怕
        self.product = False # 判断苦力怕是否已经生成

    def creeper_product(self):
        if int(time.time()) - self.product_time >= 5 and not self.product:
            self.creeper = True
            self.product = True
        if self.creeper and player.blood > 0:
            self.drawing = True
            self.y = random.randint(50, HEIGHT - 30)
            self.x = random.randint(50, WIDTH - 50)
            self.boom_rect = pygame.Rect(self.x - 48, self.y - 48, 112, 112)
            self.creeper = False

    def move(self):
        if self.product:
            if (abs(self.x - player.x) > abs(self.y - player.y)
                    and abs(player.x - self.x) > 16):
                if player.x - self.x < 16:
                    self.x -= 1
                elif self.x - player.x < -16:
                    self.x += 1
            else:
                if player.y - self.y > 16:
                    self.y +=  1
                elif player.y - self.y < -16:
                    self.y -=  1
            self.boom_rect = pygame.Rect(self.x - 48, self.y - 48, 112, 112)

    def boom(self):
        if self.boom_rect.colliderect(player.rect) and self.product:
            self.start = True
        if self.start:
            if self.boom_time is None:  # 第一次接触
                resources["sounds"]["fizz"].play()  # 使用预加载的音效
                self.boom_time = time.time()
            # 检查是否到达爆炸时间
            if time.time() - self.boom_time > 1.2:  # 1.2秒后爆炸
                resources["sounds"]["boom"].play()

                # 造成伤害
                if self.boom_rect.colliderect(player.rect):
                    if player.gold_blood > 0:
                        player.gold_blood -= 8
                        player.blood += player.gold_blood
                        player.gold_blood = 0
                    else:
                        player.blood -= 8
                    if player.blood <0:
                        player.die_music = True
                        player.blood = 0
                self.reset()

    def check_rect(self):
        """检查子弹与苦力怕的碰撞"""
        if not self.product:  # 如果苦力怕未生成，直接返回
            return

        # 获取所有子弹
        for bullet in player.bullets.sprites():
            # 创建子弹的rect（确保尺寸合适）
            bullet_rect = pygame.Rect(bullet.rect.x, bullet.rect.y, 8, 8)

            # 创建苦力怕的rect（确保尺寸合适）
            creeper_rect = pygame.Rect(self.x, self.y, 16, 16)

            # 检测碰撞
            if bullet_rect.colliderect(creeper_rect):
                bullet.kill()  # 移除子弹
                self.blood -= 1  # 减少苦力怕血量（原先是-10，可能一次伤害太大）

                # 如果苦力怕血量耗尽，重置
                if self.blood <= 0:
                    self.shoot = True
                    self.reset()
                    player.store += 5  # 击杀奖励
                    break  # 一颗子弹只造成一次伤害

    def reset(self):
        self.drawing = False
        self.creeper = False
        self.x, self.y = -100, -100
        self.boom_time = None
        self.blood = 10
        self.product = False
        self.product_time = int(time.time())
        self.start = False

    def draw(self):
        if self.start:
            screen.blit(resource.boom_photo, (self.x - 48, self.y - 48))
        if self.drawing:
            # 绘制血条背景（灰色）
            pygame.draw.rect(screen, (100, 100, 100), (self.hp_x, self.hp_y, self.hp_bar_width, self.hp_bar_height))
            # 绘制当前血量
            current_hp_width = (self.blood / 10) * self.hp_bar_width
            pygame.draw.rect(screen, GREEN, (self.hp_x, self.hp_y, current_hp_width, self.hp_bar_height))
            screen.blit(resource.creeper_photo,(WIDTH-25,5))
            render.text(WHITE,"苦力怕",15,WIDTH-75,5)
            # 绘制苦力怕
            screen.blit(resource.creeper_photo,(self.x,self.y))

    @staticmethod
    def run():
        creeper.check_rect()
        creeper.draw()
        creeper.move()
        creeper.creeper_product()
        creeper.boom()
creeper = Creeper()

class Game:
    # 游戏主函数
    def __init__(self):
        self.run_game = True
        """按钮绘制"""
        self.button_again_text = text.render("重新开始", True, WHITE)
        self.button_again = pygame.Rect(Width - 95, Height - 10, 200, 50)
        self.button_quit_text = text.render("返回主菜单", True, WHITE)
        self.button_quit = pygame.Rect(Width - 95, Height + 50, 200, 50)
        self.count = 0
        self.start = time.time()

    def main(self,run_game: [0,1]=None):
        if run_game:
            self.run_game = True
        while self.run_game:
            clock.tick(60)
            screen.fill(black)
            # 事件检测
            for event in pygame.event.get():
                self.check_event(event)

            if player.blood > 0:
                # 方法调用
                thing.run()
                creeper.run()
            self.check_fps()
            player.run()
            # 屏幕更新
            pygame.display.flip()

    def check_event(self, event):
        """事件检测"""
        if event.type == pygame.QUIT:
            self.run_game = False
            resource.quit_game()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_w:
                player.direction = "w"
            elif event.key == pygame.K_a:
                player.direction = "a"
            elif event.key == pygame.K_s:
                player.direction = "s"
            elif event.key == pygame.K_d:
                player.direction = "d"
                """物品选择"""
            elif event.key == pygame.K_KP_1:
                thing.things_number = 0
            elif event.key == pygame.K_KP_2:
                thing.things_number = 1
            elif event.key == pygame.K_KP_3:
                thing.things_number = 2
        elif event.type == MOUSEBUTTONDOWN:
            if self.button_quit.collidepoint(event.pos) and player.blood == 0:
                self.run_game = False
                player.reset()
                start_menu(True)
            elif self.button_again.collidepoint(event.pos) and player.blood == 0:
                player.reset()
            elif player.blood > 0 and event.button == 3:
                thing.thing_use()
            elif player.blood > 0 and event.button == 1:
                player.fire_bullet()
        elif event.type == MOUSEWHEEL:
            thing.thing_choose(event)

    def check_fps(self):
        self.count += 1
        now = time.time()
        fps = self.count / (now - self.start)
        render.text(WHITE,f"fps:,{'%.2f' % fps}",15,5,60)

game = Game()

# 游戏计时
time_text = text.render("游戏时间： " + str(game_time), True, WHITE)
start = time.perf_counter()
# 开始菜单
def start_menu(run: [0,1]=True):
    button_text_start = text.render("开始游戏", True, WHITE)
    button_start = pygame.Rect(Width - 95, Height - 20, 200, 50)
    button_text_quit = text.render("退出游戏", True, WHITE)
    button_quit = pygame.Rect(Width - 95, Height + 50, 200, 50)
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                run = False
                resource.quit_game()
            elif event.type == MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    run = False
                    game.main(True)
                    player.reset()
                elif button_quit.collidepoint(event.pos):
                    run = False
                    resource.quit_game()
        screen.fill(black)
        render.text(WHITE, "抢 苹 果", 50, Width - 90, Height - 200)
        screen.blit(resources["images"]["inventory"], (0, 0))
        render.text(WHITE, str(resource.save_apple), 20, 30, 7)
        render.text(WHITE, str(resource.save_gold_apple), 20, 130, 7)
        render.text(WHITE, name, 25, Width + 200, Height + 40)
        screen.blit(time_text, (10, HEIGHT - 25))
        # 按钮渲染
        render.button(gray,button_start, button_text_start)
        # 退出
        render.button(gray,button_quit, button_text_quit)
        pygame.display.flip()

# 成就系统
def check_achievement():
    # 读取成就数据
    with open(os.path.join("data", "information.json"), 'r') as _f:
        _data = json.load(_f)
    achieve = _data["achievement"]
    # 子线程循环
    while resource.running:
        clock.tick(1)
        if thing.apple >= 1 and achievement["get_apple"] == 0:
            achievement["get_apple"] = 1
            print("获得成就：get apple！")
            resource.save()
        elif resource.save_apple >= 64 and achievement["farmer"] == 0:
            achievement["farmer"] = 1
            print("获得成就：农民！")
            resource.save()
        elif creeper.shoot and achievement["shoot_creeper"] == 0:
            achievement["shoot_creeper"] = 1
            print("获得成就：怪物猎人！")
        elif thing.gold_apple >= 1 and achievement["gold_apple"] == 0:
            achievement["gold_apple"] = 1
            print("获得成就：金色传说！")
        elif resource.save_apple >= 64 and achievement["farm_host"] == 0:
            achievement["farm_host"] = 1
            print("获得成就：农场主!")
        elif resource.save_apple + resource.save_gold_apple*5 >= 100 and achievement["get_rich"] == 0:
            achievement["get_rich"] = 1
            print("获得成就：小有所成!")
        elif  resource.save_apple + resource.save_gold_apple*5 >= 100 and achievement["moneybags"] == 0:
            achievement["moneybags"] = 1
            print("获得成就：大富翁!")
        elif  thing.eat and achievement["eat"] == 0:
            achievement["eat"] = 1
            print("获得成就：好吃爱吃")
        print(achievement)

check_achievement = threading.Thread(target=check_achievement)
check_achievement.start()

if __name__ == "__main__":
    start_menu()