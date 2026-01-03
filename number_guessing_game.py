# -*- coding: utf-8 -*-
# 编码声明：避免字符编码问题，确保中文正常显示
import random
from datetime import datetime

def number_guessing_game():
    # 初始化历史记录列表（最多保存5条，按时间倒序排列）
    history_records = []
    
    # 难度配置字典：仅保留文字描述，无特殊符号
    difficulty_config = {
        "1": {"name": "简单", "range": (1, 50), "attempts": 10, "coefficient": 1},
        "2": {"name": "中等", "range": (1, 100), "attempts": 8, "coefficient": 2},
        "3": {"name": "困难", "range": (1, 200), "attempts": 6, "coefficient": 3}
    }
    
    # 游戏欢迎语与规则说明：移除所有特殊emoji，用简洁文字描述
    print("="*50)
    print("【智能猜数字升级版】")
    print("="*50)
    print("游戏规则：")
    print("1. 选择难度后，系统随机生成目标数字，您需在限定次数内猜对；")
    print("2. 难度说明：")
    for key, val in difficulty_config.items():
        print(f"   {key}-{val['name']}：数字范围{val['range'][0]}-{val['range'][1]}，{val['attempts']}次机会，计分系数{val['coefficient']}")
    print("3. 计分规则：得分=难度系数×剩余猜测次数（未猜对得0分）；")
    print("4. 支持查看最近5次游戏记录，可重复游玩。")
    print("="*50 + "\n")
    
    while True:  # 重玩循环：游戏结束后可选择继续
        # 难度选择：引导用户输入有效编号
        print("请选择难度：")
        for key, val in difficulty_config.items():
            print(f"{key}-{val['name']}（数字范围{val['range'][0]}-{val['range'][1]}，{val['attempts']}次机会）")
        
        # 难度输入验证：仅允许输入1/2/3
        while True:
            difficulty = input("请输入难度编号（1/2/3）：")
            if difficulty in difficulty_config:
                config = difficulty_config[difficulty]
                min_num, max_num = config["range"]
                max_attempts = config["attempts"]
                coefficient = config["coefficient"]
                difficulty_name = config["name"]
                print(f"\n您选择了{difficulty_name}难度，数字范围{min_num}-{max_num}，共{max_attempts}次机会！")
                break
            else:
                print("输入错误！请仅输入1、2或3选择难度。")
        
        # 游戏核心逻辑：生成目标数字，循环接收猜测
        target_number = random.randint(min_num, max_num)
        attempts = 0  # 已用猜测次数
        print("游戏开始！请输入数字进行猜测～")
        
        while attempts < max_attempts:
            try:
                # 猜测输入提示：明确当前难度的数字范围，无特殊符号
                guess_input = input(f"请输入{min_num}-{max_num}之间的猜测（第{attempts+1}次）：")
                guess = int(guess_input)  # 转换为整数（非数字会触发异常）
                attempts += 1  # 仅在输入有效数字时计数
                
                # 输入范围验证：确保猜测在当前难度的数字区间内
                if guess < min_num or guess > max_num:
                    print(f"输入错误！请严格输入{min_num}-{max_num}之间的数字。")
                    continue
                
                # 猜测结果反馈：用简洁文字提示偏大/偏小/正确
                if guess < target_number:
                    print("偏小啦！再试试更大的数字～")
                elif guess > target_number:
                    print("偏大啦！再试试更小的数字～")
                else:
                    # 计算得分：难度系数×剩余次数
                    score = coefficient * (max_attempts - attempts + 1)
                    print(f"\n恭喜您猜对了！目标数字就是{target_number}")
                    print(f"您用了{attempts}次机会，得分为：{score}分（难度系数{coefficient}×剩余{max_attempts - attempts + 1}次）")
                    
                    # 记录本次游戏结果：包含时间、难度、次数、得分
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    record = {
                        "time": current_time,
                        "difficulty": difficulty_name,
                        "attempts": attempts,
                        "score": score
                    }
                    history_records.append(record)
                    # 保持历史记录最多5条，并按时间倒序排列（最新在前）
                    history_records = history_records[-5:][::-1]
                    break  # 猜对后退出当前游戏循环
            
            # 非数字输入处理：不消耗猜测次数，提示重新输入
            except ValueError:
                print("输入无效！请输入纯数字，不消耗猜测次数。")
        
        # 次数用完未猜对的逻辑：记录得分0分
        if attempts >= max_attempts and guess != target_number:
            score = 0
            print(f"\n游戏结束！您已经用完{max_attempts}次机会，目标数字是{target_number}")
            print("本次得分为：0分")
            
            # 记录本次游戏结果
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {
                "time": current_time,
                "difficulty": difficulty_name,
                "attempts": attempts,
                "score": score
            }
            history_records.append(record)
            history_records = history_records[-5:][::-1]
        
        # 查看历史记录：用户可选择是否查看最近5次记录
        while True:
            view_history = input("\n是否查看最近5次游戏记录？（y/n）：")
            if view_history.lower() == "y":
                if not history_records:
                    print("暂无游戏记录～")
                else:
                    print("\n最近5次游戏记录：")
                    print("-"*65)
                    print(f"{'日期时间':<22} {'难度':<6} {'猜测次数':<8} {'得分':<4}")
                    print("-"*65)
                    for record in history_records:
                        print(f"{record['time']:<22} {record['difficulty']:<6} {record['attempts']:<8} {record['score']:<4}")
                break
            elif view_history.lower() == "n":
                break
            else:
                print("输入无效！请输入y或n。")
        
        # 重玩功能：用户选择继续游戏或退出
        while True:
            play_again = input("\n是否继续游戏？（y/n）：")
            if play_again.lower() == "y":
                print("\n" + "="*50 + "\n")
                break  # 重新进入难度选择环节
            elif play_again.lower() == "n":
                print("\n感谢游玩！再见～")
                return  # 退出整个游戏
            else:
                print("输入无效！请输入y或n。")

# 程序入口：直接运行游戏
if __name__ == "__main__":
    number_guessing_game()