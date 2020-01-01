"""飞机基类及其派生类的定义，在这里我将玩家和敌方飞机的共同属性进行了封装
飞机有一个默认的实例属性rect和父类方法update，请尽量不要改动这两个属性和
方法的名字，以免产生意想不到的后果"""
import random

import pygame

import constans
from game.bullet import Bullet, EnemyBullet


class Plane(pygame.sprite.Sprite):
    """飞机基类定义"""

    # 飞机的基本属性：图片、坠毁音效、爆炸图片、子弹、飞机存活状态等
    plane_images = []
    destroy_image = []
    down_sounds = None
    plane_bullet = pygame.sprite.Group()  # 这里的子弹是一个精灵组对象，用来控制一系列的子弹用的！
    active = True

    def __init__(self, screen, speed=4):
        # 飞机属性的初始化
        super().__init__()
        self.screen = screen

        self.image_list = []
        self.destroy_image_list = []
        self.down_sound = None
        self.speed = speed
        self.static_resource()

        self.rect = self.image_list[0].get_rect()
        self.s_width, self.s_height = self.screen.get_size()

    # 静态资源加载
    def static_resource(self):
        for img in self.plane_images:
            self.image_list.append(pygame.image.load(img))

        for img in self.destroy_image:
            self.destroy_image_list.append(pygame.image.load(img))

        if self.down_sounds:
            self.down_sound = pygame.mixer.Sound(self.down_sounds)

    # 存活状态下所能做的事情：移动位置、发射子弹、飞机的动画绘制
    def move_up(self):
        self.rect.top -= self.speed

    def move_down(self):
        self.rect.top += self.speed

    def move_left(self):
        self.rect.left -= self.speed

    def move_right(self):
        self.rect.left += self.speed

    def shoot_bullet(self):
        """飞机发射子弹的方法"""
        pass

    # 死亡状态下能做的事情：爆炸动画绘制、
    def down_image(self):
        """飞机爆炸后的处理方法"""
        # 设置飞机的存活状态
        self.active = False

        # 播放飞机的爆炸动画和音效
        for img in self.destroy_image_list:
            self.screen.blit(img, self.rect)
        if self.down_sound:
            self.down_sound.play()
            self.down_sound.set_volume(0.4)


class OurPlane(Plane):
    """我方飞机类定义继承自plane类"""

    # 添加图片、音效等静态资源
    plane_images = [constans.OUR_PLANE_IMG_1, constans.OUR_PLANE_IMG_2]
    destroy_image = constans.OUR_DESTROY_IMG_LIST
    down_sounds = constans.OUR_DESTROY_SOUND

    def __init__(self, screen, speed=6):
        """在重写的__init__方法中只对飞机首次出现的位置进行了修改"""
        super().__init__(screen, speed)

        # 对飞机初始位置的获取
        self.o_width, self.o_height = self.image_list[0].get_size()

    def init_position(self):
        """飞机位置和状态的初始化"""

        self.active = True
        self.rect.top = int(self.s_height - self.o_height)
        self.rect.left = int((self.s_width - self.o_width) / 2)

    def update(self, war):
        """飞机的飞行状态方法：包含飞机动画的切换，碰撞检测"""

        # 飞机的飞行动画，每隔5帧切换
        if war.frame % 5:
            self.screen.blit(self.image_list[0], self.rect)
        else:
            self.screen.blit(self.image_list[1], self.rect)

        # 飞机的碰撞检测
        rest = pygame.sprite.spritecollide(self, war.enemy_planes, False)
        if rest:
            # 播放我方飞机爆炸动画
            self.down_image()
            # 设置游戏状态为结束
            war.status = war.OVER
            # 清除所有飞机
            war.enemy_planes.empty()

    def responding(self, event):
        """飞机的控制方法"""

        # 对飞机的按键响应封装到了飞机自己的内部
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.move_up()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.move_down()
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.move_left()
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.move_right()
        elif event.key == pygame.K_SPACE:
            self.shoot_bullet()

    # 飞机的控制方法：上下左右，以及超出屏幕的限制条件
    def move_up(self):
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        super().move_down()
        if self.rect.top >= self.s_height - self.o_height:
            self.rect.top = self.s_height - self.o_height

    def move_left(self):
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        super().move_right()
        if self.rect.left >= self.s_width - self.o_width:
            self.rect.left = self.s_width - self.o_width

    def shoot_bullet(self):
        """调用发射子弹方法时创建一个子弹对象，并将其添加到精灵组中"""
        bullet = Bullet(self.screen, self)
        self.plane_bullet.add(bullet)

    def down_image(self):
        """重写的爆炸方法"""
        super().down_image()
        self.kill()


class SmallPlane(Plane):
    """敌方小型飞机类定义"""

    plane_images = [constans.SMALL_ENEMY_PLANE_IMG]
    destroy_image = constans.SMALL_ENEMY_DESTROY_IMG_LIST
    down_sounds = constans.SMALL_ENEMY_DOWN_SOUND

    def __init__(self, screen, speed=2):
        super().__init__(screen, speed)
        # 获取小飞机图片的高度和宽度，并将初始位置随机化
        self.sma_width, self.sma_height = self.image_list[0].get_size()
        self.init_position()

    # 对小飞机初始位置的设置和重用方法
    def init_position(self):
        """飞机的初始位置随机化"""
        self.rect.top = random.randint(-5 * self.sma_height, -self.sma_height)
        self.rect.left = random.randint(0, self.s_width - self.sma_width)

    def reset(self):
        """飞机的重用，将飞出屏幕的飞机重新初始化位置"""
        self.active = True
        self.init_position()

    # 小型飞机存活状态下能做的事沿直线向下移动、碰撞检测
    def update(self, *args):
        """小飞机的动画更新以及状态监控"""

        self.move_down()
        self.screen.blit(self.image_list[0], self.rect)

        # 超出范围后的重用
        if self.rect.top >= self.s_height:
            self.active = False
            self.reset()

    def down_image(self):
        super().down_image()
        self.reset()


class MediumPlane(Plane):
    """敌方中型飞机类定义"""
    plane_images = [constans.MEDIUM_PLANE_IMG]
    destroy_image = constans.MEDIUM_PLANE_DOWN_IMG_LIST
    down_sounds = constans.MEDIUM_PLANE_SOUND

    def __init__(self, screen, speed=1):
        super().__init__(screen, speed)
        # 血量值
        self.Hp = None
        self.med_width, self.med_height = self.image_list[0].get_size()
        # 子弹发射记录值
        self.bullet_count = 0
        # 设置初始位置
        self.init_position()

    def init_position(self):
        """飞机的初始位置随机化"""
        self.rect.top = random.randint(-5 * self.med_height, -self.med_height)
        self.rect.left = random.randint(0, self.s_width - self.med_width)
        self.Hp = 18

    def update(self, wars, *args):
        self.move_down()
        self.screen.blit(self.image_list[0], self.rect)

        # 超出范围后的重用
        if self.rect.top >= self.s_height:
            self.active = False
            self.reset()

        # 每隔1秒发射一颗子弹
        if (wars.frame % 60 == 0) and (self.bullet_count <= 1) and (self.rect.top >= 0):
            self.bullet_count += 4
            self.shoot_bullet(wars)
        # 发射后隔三秒再发射一颗
        elif wars.frame % 60 == 0 and self.bullet_count >= 1:
            self.bullet_count -= 1

    def reset(self):
        """重用方法"""
        self.active = True
        self.init_position()

    def down_image(self):
        """重写的爆炸动画"""

        # 如果血量值为0飞机销毁
        if self.Hp <= 0:
            super().down_image()
            self.reset()
        # 如果不为0继续飞行
        else:
            self.screen.blit(self.destroy_image_list[0], self.rect)
            if self.down_sound:
                self.down_sound.play()
                self.down_sound.set_volume(0.4)

    def shoot_bullet(self, wars=None):
        """重写的发射子弹的方法"""
        enemy_bullet = EnemyBullet(self.screen, self, speed=2)
        # 添加到war类的敌方精灵组中去了
        enemy_bullet.add(wars.enemy_planes)


class LargePlane(Plane):
    """敌方大型飞机类定义"""

    plane_images = constans.LARGE_PLANE_IMG
    destroy_image = constans.LARGE_PLANE_DOWN_IMG_LIST
    down_sounds = constans.LARGE_PLANE_DOWN_SOUND

    # 飞机初始化
    def __init__(self, screen, speed=1):
        super().__init__(screen, speed)
        self.Hp = 0
        self.l_width, self.l_height = self.image_list[0].get_size()
        self.bullet_count = 0
        self.init_position()

    def init_position(self):
        """飞机位置和血量初始化"""
        self.rect.top = (0 - self.l_height) * 2
        self.rect.left = random.randint(0, self.s_width - self.l_width)
        self.Hp = 45

    def reset(self):
        """飞机方法重用"""
        self.active = True
        self.init_position()

    # 飞机动画更新
    def update(self, wars, *args):

        self.move_down()
        # 根据帧数率切换飞机的飞行动画
        if wars.frame % 10 == 0:
            self.screen.blit(self.image_list[0], self.rect)
        else:
            self.screen.blit(self.image_list[1], self.rect)

        # 超出范围后的重用
        if self.rect.top >= self.s_height:
            self.active = False
            self.reset()

        # 每隔1秒发射一颗子弹
        if (wars.frame % 60 == 0) and (self.bullet_count <= 1) and (self.rect.top >= 0):
            self.bullet_count += 3
            self.shoot_bullet(wars)
        # 发射后3秒再重新发射
        elif (wars.frame % 60 == 0) and (self.bullet_count >= 1):
            self.bullet_count -= 1

    # 爆炸动画
    def down_image(self):
        """重写的爆炸动画"""

        # 如果血量值为0飞机销毁
        if self.Hp <= 0:
            super().down_image()
            self.reset()
        # 如果不为0继续飞行
        else:
            self.screen.blit(self.destroy_image_list[0], self.rect)
            if self.down_sound:
                self.down_sound.play()
                self.down_sound.set_volume(0.4)

    # 飞机发射子弹
    def shoot_bullet(self, wars=None):
        """重写的子弹发射方法"""
        enemy_bullet = EnemyBullet(self.screen, self, speed=2)
        # 添加到war类的敌方精灵组中去了
        enemy_bullet.add(wars.enemy_planes)
