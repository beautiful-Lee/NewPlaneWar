"""子弹类的定义"""
import pygame
import constans
from game import plane


class Bullet(pygame.sprite.Sprite):
    """玩家子弹类定义的实现"""

    # 子弹的存活状态
    active = True

    def __init__(self, screen, plane, speed=10):
        super().__init__()

        # 添加子弹的飞机、速度、屏幕、图片、音效、位置等属性
        self.plane = plane
        self.speed = speed
        self.screen = screen
        self.bullet_image = pygame.image.load(constans.BULLET_IMG)
        self.bullet_sound = None
        self.rect = self.bullet_image.get_rect()
        self.rect.top = self.plane.rect.top
        self.rect.centerx = self.plane.rect.centerx
        self.bullet_music()

    def bullet_music(self):
        # 子弹产生时播放发射音效
        self.bullet_sound = pygame.mixer.Sound(constans.BULLET_SHOOT_SOUND)
        self.bullet_sound.set_volume(0.3)
        self.bullet_sound.play()

    def update(self, wars, *args):
        """子弹的更新方法"""

        # 子弹位置在不断移动
        self.rect.top -= self.speed

        # 子弹飞行的三种状态：存活、飞出屏幕、击中敌机
        if self.active and self.rect.top > 0:
            # 画出子弹
            self.screen.blit(self.bullet_image, self.rect)
            rest = pygame.sprite.spritecollide(self, wars.enemy_planes, False)
            if rest:
                for r in rest:
                    # 对产生碰撞的对象进行检测，敌方飞机才有碰撞检测
                    if isinstance(r, plane.SmallPlane):
                        self.kill()
                        r.down_image()
                        wars.score += 10
                    elif isinstance(r, plane.MediumPlane):
                        self.kill()
                        r.down_image()
                        r.Hp -= 1
                        if r.Hp <= 0:
                            wars.score += 30
                    elif isinstance(r, plane.LargePlane):
                        self.kill()
                        r.down_image()
                        r.Hp -= 1
                        if r.Hp <= 0:
                            wars.score += 50
        elif self.rect.top < 0:
            # 飞出屏幕的子弹从精灵组里删除
            self.remove(self.plane.plane_bullet)


class EnemyBullet(Bullet):
    """敌方子弹的定义继承自玩家子弹类"""

    def __init__(self, screen, enemy_plane, speed=8):
        super().__init__(screen, enemy_plane, speed)

        # 对敌方子弹的发射位置做了一些修改
        self.bullet_image = pygame.image.load(constans.ENEMY_BULLET_IMG)
        self.rect.bottom = self.plane.rect.bottom
        self.bullet_sound = None

    def bullet_music(self):
        """不播放敌方子弹的发射音效"""
        pass

    def update(self, wars, *args):
        """对敌方子弹更新方法的重写，敌方子弹的碰撞检测不需要做，因为在玩家飞机里已经有这个组的碰撞检测了"""
        # 子弹的状态飞行、飞出屏幕
        if self.active and self.rect.bottom > 0:
            self.rect.bottom += self.speed
            self.screen.blit(self.bullet_image, self.rect)
        elif self.rect.top > wars.height:
            self.remove(wars.enemy_planes)
            self.kill()
