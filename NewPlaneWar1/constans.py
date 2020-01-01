import os
import pygame

"""常用常量以及静态资源（图片、音效）绑定文件"""

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件目录
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# 字体资源
GAME_FONT = os.path.join(ASSETS_DIR, 'sounds/simhei.ttf')
FONT_COLOR = pygame.Color(255, 255, 255)
SCORE_SHOOT_SMALL = 10

# 游戏结果存储文件
PLAY_RESULT_STORE_FILE = os.path.join(BASE_DIR, 'store/rest.txt')

# 背景图片
BG_IMG = os.path.join(ASSETS_DIR, 'images/background.png')
BG_OVER_IMG = os.path.join(ASSETS_DIR, 'images/game_over.png')

# 标题图片
BG_IMG_TITLE = os.path.join(ASSETS_DIR, 'images/game_title.png')

# 开始按钮图片
BG_IMG_START_BTN = os.path.join(ASSETS_DIR, 'images/game_start.png')

# 背景音乐
BG_MUSIC = os.path.join(ASSETS_DIR, 'sounds/Welcome_to_Planet_Urf.mp3')

"""我方飞机静态资源"""

# 1.飞机飞行图片
OUR_PLANE_IMG_1 = os.path.join(ASSETS_DIR, 'images/hero1.png')
OUR_PLANE_IMG_2 = os.path.join(ASSETS_DIR, 'images/hero2.png')

# 2.飞机爆炸系列图片
OUR_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero_broken_n1.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n2.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n3.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n4.png')
]

# 3.飞机爆炸音效
OUR_DESTROY_SOUND = os.path.join(ASSETS_DIR, 'sounds/game_over.wav')

# 我方子弹图片
BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet1.png')
# 发射子弹音效
BULLET_SHOOT_SOUND = os.path.join(ASSETS_DIR, 'sounds/bullet.wav')

"""敌方飞机静态资源文件"""

ENEMY_BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet2.png')

# 1.敌方小飞机图片
SMALL_ENEMY_PLANE_IMG = os.path.join(ASSETS_DIR, 'images/enemy1.png')

# 敌方小飞机爆炸系列图片
SMALL_ENEMY_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down4.png')
]

# 敌方小飞机爆炸音效
SMALL_ENEMY_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy1_down.wav')

# 2.敌方中型飞机

# 中型飞机图
MEDIUM_PLANE_IMG = os.path.join(ASSETS_DIR, 'images/enemy2.png')

# 中型飞机爆炸图
MEDIUM_PLANE_DOWN_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy2_hit.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy2_down4.png')
]

# 中型飞机爆炸音效
MEDIUM_PLANE_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy2_down.wav')

# 2.敌方大型飞机
# 大型飞机图片
LARGE_PLANE_IMG = [
    os.path.join(ASSETS_DIR, 'images/enemy3_n1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_n2.png')
]
# 大型飞机爆炸图片
LARGE_PLANE_DOWN_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy3_hit.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down4.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down5.png'),
    os.path.join(ASSETS_DIR, 'images/enemy3_down6.png')
]
# 大型飞机爆炸音效
LARGE_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy3_down.wav')
