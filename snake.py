import pygame as pg
import sys
import time
import random
from pygame.locals import *

black_color = pg.Color(0, 0, 0)
white_color = pg.Color(255, 255, 255)
red_color = pg.Color(255, 0, 0)
grey_color = pg.Color(150, 150, 15)


def gameover(screen):
    # 设置gameover字体
    gameover_font = pg.font.SysFont("MircosoftYaHei", 16)
    # 设置gameover字体颜色
    gameover_color = gameover_font.render('Game Over', True, grey_color)
    # 设置提示位置
    gameover_location = gameover_color.get_rect()
    gameover_location.midtop = (320, 10)
    # 绑定以上设置到句柄
    screen.blit(gameover_color, gameover_location)
    # 提示运行信息
    pg.display.flip()
    # 休眠5秒
    time.sleep(5)
    # 退出游戏
    pg.quit()
    # 退出程序
    sys.exit()


def main():
    # 初始化
    pg.init()
    pg.time.Clock()
    fps = pg.time.Clock()
    screen = pg.display.set_mode((600, 500))
    pg.display.set_caption("snake")

    # 初始化变量
    # 蛇start
    snakepos = [100, 100]
    # food start
    foodpos = [200, 200]
    # 蛇长度
    snakelength = [[100, 100], [80, 100], [60, 100]]
    # 蛇初始运动方向
    direction = "right"
    # 通过键盘控制改变的蛇的运动方向
    change = direction
    # 食物存在状态
    food_position = 1
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit("thanks for using !")
            # 用键盘控制蛇移动方向
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord("w"):
                    change = "up"
                if event.key == K_DOWN or event.key == ord("s"):
                    change = "down"
                if event.key == K_LEFT or event.key == ord("a"):
                    change = "left"
                if event.key == K_RIGHT or event.key == ord("d"):
                    change = "up"
                if event.key == K_ESCAPE:
                    pg.event.post(pg.event.Event(QUIT))
        # 判断移动方向是否相反
        if change == "left" and not direction == "right":
            direction = change
        if change == "right" and not direction == "left":
            direction = change
        if change == "up" and not direction == "down":
            direction = change
        if change == "down" and not direction == "up":
            direction = change

        # 根据变量,改变坐标
        if direction == "left":
            snakepos[0] -= 20
        if direction == "right":
            snakepos[0] += 20
        if direction == "up":
            snakepos[1] -= 20
        if direction == "down":
            snakepos[1] += 20
        # 增加蛇长度
        snakelength.insert(0, list(snakepos))
        # 判断是否吃掉
        if snakepos[0] == foodpos[0] and snakepos[1] == foodpos[1]:
            food_position = 0
        else:
            snakelength.pop()
        # 重新生成food
        if food_position == 0:
            x = random.randrange(1, 30)
            y = random.randrange(1, 25)
            foodpos = [int(x * 20), int(y * 20)]
            food_position = 1
        # 绘制显示层
        screen.fill(black_color)
        for pos in snakelength:
            pg.draw.rect(screen, white_color, Rect(pos[0], pos[1], 20, 20))
            pg.draw.rect(screen, red_color, Rect(
                foodpos[0], foodpos[1], 20, 20))

        # 刷新显示层
        pg.display.flip()
        if snakepos[0] < 0 or snakepos[0] > 580:
            gameover(screen)
        if snakepos[1] < 0 or snakepos[1] > 480:
            gameover(screen)
        for snakebody in snakelength[1:]:
            if snakepos[0] == snakebody[0] and snakepos[1] == snakebody[1]:
                gameover(screen)

        fps.tick(4)


if __name__ == '__main__':
    main()
