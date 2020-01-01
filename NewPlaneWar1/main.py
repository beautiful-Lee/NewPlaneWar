"""游戏入口文件"""
from game import war


def run_main():
    """导入war对象，并启动运行游戏方法"""
    war_ing = war.War()
    war_ing.game_run()


if __name__ == "__main__":
    run_main()
