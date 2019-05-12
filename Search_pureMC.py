import random
from copy import deepcopy
from operator import itemgetter

from Game import game


class Agamotto(game):
    # search 해야할 현재 board
    def __init__(self, game):
        super(Agamotto, self).__init__()
        self.board = game.board
        self.cells = game.cells
        self.winner = game.winner
        self.row_board = game.row_board
        self.marker = game.marker
        # 왼쪽눈은 Tree input, 오른쪽눈은 Tree output
        self.EyeOfAgamotto_left = dict()
        self.EyeOfAgamotto_right = dict()
        self.battle_count = 0
        return

    def validate_input_col(self, col):
        # col 조건 1) 숫자, 2) 0~6 사이, 3) 첫턴에는 3이 안됨, 4) col에 5이상
        if self.cells == 42 and col == '4':
            return self.validate_input_col(str(random.randrange(1, 8)))
        elif self.board[5][int(col)-1] != " ":
            return self.validate_input_col(str(random.randrange(1, 8)))
        else:
            return int(col)-1

    def input(self, col):
        self.board[self.row_board[col]][col] = self.marker
        self.marker = "O" if self.marker == "X" else "X"
        self.row_board[col] += 1
        self.cells -= 1
        self.isWin(col)

    def isWin(self, col):
        row = self.row_board[col] - 1
        set_point = self.board[row][col]
        diagonal_SE_emcee = col + row
        diagonal_NE_emcee = col - row

        # 가로 평가
        # start_adj = col 변경
        for start_col in range(max(0, col-3), min(col, 3)+1):
            check_list = self.board[row][start_col:start_col+4]
            if check_list.count("O") == 4 or check_list.count("X") == 4:
                self.winner = set_point
                return
        # 세로 평가
        if row > 2:
            # start_adj = row
            for start_row in range(max(0, row-3), 3):
                if self.board[start_row][col] == " ": continue
                check_list = [self.board[start_row+adj][col] for adj in range(4)]
                if check_list.count("O") == 4 or check_list.count("X") == 4:
                    self.winner = set_point
                    return
        # 우하 평가
        if 9 > diagonal_SE_emcee > 2:
            if diagonal_SE_emcee < 6:
                for start_row in range(diagonal_SE_emcee-2):
                    check_list = [self.board[diagonal_SE_emcee-start_row-adj][start_row+adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        self.winner = set_point
                        return
            else:
                for start_row in range(6, diagonal_SE_emcee-3, -1):
                    check_list = [self.board[diagonal_SE_emcee-start_row+adj][start_row-adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        self.winner = set_point
                        return
        # 우상 평가
        if 4 > diagonal_NE_emcee > -3:
            if diagonal_NE_emcee < 1:
                for start_row in range(diagonal_NE_emcee+3):
                    check_list = [self.board[start_row-diagonal_NE_emcee+adj][start_row+adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        self.winner = set_point
                        return
            else:
                for start_row in range(6, diagonal_NE_emcee+2, -1):
                    check_list = [self.board[start_row-diagonal_NE_emcee-adj][start_row-adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        self.winner = set_point
                        return

    def VictoryNumber(self):
        # EOA = self.EyesOfAgamotto
        self.FutureSight()
        print(f"닥터: {self.battle_count}개의 전투에서 승리할 수 있는 수는 이것뿐이었네")
        for key, value in self.EyeOfAgamotto_right.items():
            print(f"{key}: {value}", end=", ")
        print (max(self.EyeOfAgamotto_right.items(), key=itemgetter(1)))
        return str(max(self.EyeOfAgamotto_right.items(), key=itemgetter(1))[0])[0]

    def FutureSight(self):
        if self.cells == 42:
            self.EyeOfAgamotto_left = {str(i): 0 for i in [1, 2, 3, 5, 6, 7]}  
        else:
            Battle_list = [j for j in range(1,8) if self.board[5][j-1] == " "]
            self.EyeOfAgamotto_left = {str(i): 0 for i in Battle_list}
        for key in self.EyeOfAgamotto_left.keys():
            self.EyeOfAgamotto_right[key] = self.FutureSight_Fight(key)

    def FutureSight_Fight(self, battle_field_num):
        # 턴 확인 0이면 닥터 턴(max), 1이면 유저 턴(min)
        global_turn = len(battle_field_num)%2
        minmax_arr=[]
        for minmax in range(30):
            win = 0
            for winrate in range(30):
                orb = deepcopy(self)
                local_turn = orb.marker
                for battle_code in battle_field_num:
                    orb.input(orb.validate_input_col(battle_code))
                while not orb.winner and orb.cells > 0:
                    orb.input(orb.validate_input_col(str(random.randrange(1, 8))))
                # 닥처차례에 닥터가 승리했거나
                if orb.winner == local_turn and not global_turn:
                    win += 1
                # 유저차례에 유저가 이겼거나 비겼으면
                elif global_turn and orb.winner == local_turn or orb.winner == 0:
                    win += 1
            # print(f'{battle_field_num}전장에서 {win}번 이겼네')
            minmax_arr.append(win)
            self.battle_count += 900
        return (max(minmax_arr), min(minmax_arr))