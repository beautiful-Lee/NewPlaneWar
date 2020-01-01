"""这里是游戏类的定义，我将整个游戏过程封装成为一个类，并通过实例来调用游戏启动方法，在这个类里可以
控制游戏的状态画面，添加飞机的数量和出场类型，播放背景音乐，统计最高分和当前分，如果要对游戏进行修改
修改对应的方法即可
"""
import datetime
import sys

import pygame

import constans
from game import plane


class War(object):
    """
    在init方法中初始化了一系列属性，调用其他方法时会用到按照作用划分下面方法作用有以下内容：
    init：初始化实例属性
    ready_bg_img:游戏准备状态时的方法
    play_img:游戏进行时的方法
    over_bg_img:游戏结束时的方法
    control_frame:刷新率控制方法
    add_enemies:控制敌机入场方法
    get_score:获取历史记录分数方法
    set_score:写入最高分记录方法
    musicplay:播放音乐方法
    bind_event:事件监听方法
    game_run:游戏运行方法
    """

    # 0.准备中，1.游戏中，2.结束时
    READY = 0
    PLAYING = 1
    OVER = 2

    # clock对象设置屏幕的刷新率，frame刷新率的参数
    frame = 0
    clock = pygame.time.Clock()

    def __init__(self):
        """游戏初始化"""

        # 游戏初始化
        pygame.init()
        # 开启连续按键
        pygame.key.set_repeat(1, 20)

        # 设置屏幕高度和宽度
        self.width, self.height = 480, 852
        # 获得屏幕对象Surface
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 修改窗口标题
        pygame.display.set_caption('飞机大战小何版')

        # 游戏的状态、分数、分数文字
        self.status = self.READY
        self.score = 0
        self.score_font = pygame.font.Font(constans.GAME_FONT, 32)

        # 背景图片1.游戏准备中，2.游戏结束的，图片
        self.bg = pygame.image.load(constans.BG_IMG)
        self.game_title = None
        self.game_title_rect = None
        self.start_btn = None
        self.start_btn_rect = None
        self.bg_over = None

        # 添加我方飞机
        self.our_plane = plane.OurPlane(self.screen)

        # 添加敌方飞机精灵组
        self.enemy_planes = pygame.sprite.Group()   # 此处的精灵组包括了敌方所有的飞行道具在内，例如子弹！

    def ready_bg_img(self):
        """游戏准备状态的画面"""

        # 标题图片的载入和位置设置
        self.game_title = pygame.image.load(constans.BG_IMG_TITLE)
        self.game_title_rect = self.game_title.get_rect()
        t_width, t_height = self.game_title.get_size()
        self.game_title_rect.topleft = ((self.width - t_width) // 2, int(self.height / 2 - t_height))

        # 游戏开始重置分数
        self.score = 0

        # 开始按钮图片的载入和位置设置
        self.start_btn = pygame.image.load(constans.BG_IMG_START_BTN)
        self.start_btn_rect = self.start_btn.get_rect()
        b_width, b_height = self.start_btn.get_size()
        self.start_btn_rect.topleft = ((self.width - b_width) // 2, self.height // 2 + b_height)

        # 准备界面的绘制
        self.screen.blit(self.bg, self.bg.get_rect())
        self.screen.blit(self.game_title, self.game_title_rect)
        self.screen.blit(self.start_btn, self.start_btn_rect)

        # 玩家飞机的位置状态初始化
        self.our_plane.init_position()

    def play_img(self):
        """游戏进行时的画面"""

        # 背景画面的绘制
        self.screen.blit(self.bg, self.bg.get_rect())

        # 调用所有精灵和精灵组的更新图像方法
        self.our_plane.update(self)
        self.our_plane.plane_bullet.update(self)
        self.enemy_planes.update(self)

        # 画本局分数
        score_text = self.score_font.render('得分:{0}'.format(self.score), False, constans.FONT_COLOR)
        self.screen.blit(score_text, score_text.get_rect())

        # 添加敌方飞机方法
        self.add_enemies(6)

    def over_bg_img(self):
        """游戏结束时的背景画面"""

        # 画背景
        self.bg_over = pygame.image.load(constans.BG_OVER_IMG)
        self.screen.blit(self.bg_over, self.bg_over.get_rect())

        # 获取历史最高分并进行比较
        max_score = self.get_score()
        self.set_score(max_score)

        # 创建本局分数文字对象并设置位置
        score_text = self.score_font.render('{0}'.format(self.score), False, constans.FONT_COLOR)
        score_text_rect = score_text.get_rect()
        text_w, text_h = score_text.get_size()
        score_text_rect.topleft = (int((self.width - text_w) / 2), int(self.height / 2))

        # 画出本局得分
        self.screen.blit(score_text, score_text_rect)

        # 创建和画出历史最高分
        score_his = self.score_font.render('{0}'.format(max_score), False, constans.FONT_COLOR)
        self.screen.blit(score_his, (150, 40))

    def control_frame(self):
        """设置屏幕的刷新率"""
        self.clock.tick(60)
        self.frame += 1
        if self.frame >= 60:
            self.frame = 0

    def add_enemies(self, num):
        """添加飞机出场，此方法还可扩充"""

        # 如果没有飞机则添加num架小飞机
        if not self.enemy_planes:
            for i in range(num):
                sma_planes = plane.SmallPlane(self.screen)
                sma_planes.add(self.enemy_planes)

        # 如果分数达到200分，添加三架中型飞机，并加10分
        if self.score == 200:
            for i in range(3):
                med_planes = plane.MediumPlane(self.screen)
                med_planes.add(self.enemy_planes)
            self.score += 10

        # 如果分数达到500分，添加一架大型飞机，并加10分
        if self.score == 500:
            lar_planes = plane.LargePlane(self.screen)
            lar_planes.add(self.enemy_planes)
            self.score += 10

    def get_score(self):
        """获取记录的最高分,针对可能出现的文件不存在异常采取处理"""
        try:
            with open(constans.PLAY_RESULT_STORE_FILE, 'r', encoding='utf-8') as f_sc:
                score_text = f_sc.read()

        except FileNotFoundError():
            pass
        else:
            if score_text:
                return score_text.split('-')[0]
            else:
                return 0

    def set_score(self, max_score):
        """写入记录的最高分"""

        # 如果本局分数比历史记录高则写入历史记录
        if self.score > int(max_score):
            with open(constans.PLAY_RESULT_STORE_FILE, 'w', encoding='utf-8') as f_sc:
                f_sc.write("{0}-{1}".format(self.score, datetime.datetime.now()))

    def musicplay(self):
        """播放音乐方法"""

        pygame.mixer.music.load(constans.BG_MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)

    def bind_event(self):
        """绑定事件方法，监听事件"""

        # 循环获取事件队列信息
        for event in pygame.event.get():

            # 窗口关闭事件处理
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 鼠标事件的处理
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.status == self.READY:
                    self.status = self.PLAYING
                elif self.status == self.OVER:
                    self.status = self.READY

            # 键盘事件的处理，键盘事件主要是操作玩家飞机飞行
            elif event.type == pygame.KEYDOWN and self.status == self.PLAYING:
                self.our_plane.responding(event)

    def game_run(self):
        """运行游戏"""

        # 游戏运行前循环播放背景音乐
        self.musicplay()

        while True:
            # 控制帧数率
            self.control_frame()

            # 监听事件
            self.bind_event()

            # 更新图片，进行绘制
            if self.status == self.READY:
                """开始界面绘制方法"""
                self.ready_bg_img()

            elif self.status == self.PLAYING:
                """游戏中画面绘制方法"""
                self.play_img()

            elif self.status == self.OVER:
                """游戏结束时画面绘制方法"""
                self.over_bg_img()

            # 屏幕更新
            pygame.display.flip()
