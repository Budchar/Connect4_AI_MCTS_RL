import csv
import random
import Search_MCTS as level2
import Search_MCTS_Reinforce as level3
import Search_pureMC as level1
from Game import game

if __name__ == '__main__':
    g = game()

    # 턴 정하기
    user_turn = ""
    while user_turn != 'O' and user_turn != 'X':
        user_turn = input('O(선턴)나 X(후턴)를 입력해 먼저 시작할 지를 결정해주세요')
        user_turn = user_turn.upper()
    com_turn = "X" if user_turn == "O" else "O"

    # turn_now 가 0이면 유저 선턴 1이면 빠요엔 선턴
    emcee = 0 if user_turn == "O" else 1

    # 난이도 선택
    level = ""
    while level != "1" and level != "2" and level !="3":
        level = input("난이도 숫자를 입력 해주세요\n 1)MD.Weird 2)Weird the Sorcerer 3)Dr.Weird")
    EyesOfAgamotto = dict()
    Battle_Count = 0
    csv_name = 'Data_csv.csv'
    if level == "3":
        # 유저 선턴 기준
        with open(csv_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                EyesOfAgamotto[row['battle_code']] = [int(row['win']),int(row['draw']),int(row['lose'])]
        with open('battle_count.txt', mode='r') as battle_count:
            Battle_Count = int(battle_count.read().strip())

    while not g.winner and g.cells > 0:
        print(f'{43 - g.cells}번째 턴입니다.')
        if emcee == 0:
            # Time_Stone = level3.Agamotto(g)
            # g.input(g.validate_input_col(Time_Stone.VictoryNumber()))
            col = g.validate_input_col(input("돌을 놓으실 1~7사이의 숫자를 입력해주세요"))
            # 00 기준으로 착수점 col, g.row_board[col]
            # g.input(g.validate_input_col(str(random.randrange(1,8))))
            emcee = 1
        else:
            print("Dr.Weird 차례입니다.")
            if level == "1":
                Time_Stone = level1.Agamotto(g)
            if level == "2":
                Time_Stone = level2.Agamotto(g, EyesOfAgamotto, Battle_Count)
            if level == "3":
                Time_Stone = level3.Agamotto(g, EyesOfAgamotto, Battle_Count)
            g.input(g.validate_input_col(Time_Stone.VictoryNumber()))
            EyesOfAgamotto = Time_Stone.EOA
            if level == "3":
                Battle_Count = Time_Stone.BC
            emcee = 0

    if level == "3":
        with open(csv_name, mode='w') as csv_file:
            fieldnames = ['battle_code', 'win', 'draw', 'lose']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for key, values in EyesOfAgamotto.items():
                writer.writerow({'battle_code': key, 'win': values[0], 'draw': values[1], 'lose': values[2]})
        with open('battle_count.txt', mode='w') as battle_count:
            battle_count.write(str(Battle_Count))

    if g.winner == com_turn:
        winner = "Dr.Weird"
    elif g.winner == 0:
        winner = "무승부"
    else:
        winner = "당신"
    print(f'승리자는 {winner}입니다!!')
