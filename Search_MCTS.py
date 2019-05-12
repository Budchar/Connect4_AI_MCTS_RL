import random
from copy import deepcopy
from Game import game


class Agamotto(game):
    # search 해야할 현재 board
    def __init__(self, game, EOA, BC):
        super(Agamotto, self).__init__()
        self.board = game.board
        self.cells = game.cells
        self.winner = game.winner
        self.row_board = game.row_board
        self.marker = game.marker
        self.battle = game.battle
        self.EOA = EOA
        self.BC = BC
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
        self.battle += str(col + 1) 
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
        self.FutureSight()
        # ex) 1번 배틀이면 11,12,13,14,15,16,17중에 최고값 선택
        battle_winrate_list = []
        battle_list = [1, 2, 3, 5, 6, 7] if self.cells == 42 else [j for j in range(1,8) if self.board[5][j-1] == " "]
        for battle_field in battle_list:
            next_battle = self.battle + str(battle_field)
            try:
                winrate = self.EOA[next_battle][1] / sum(self.EOA[next_battle])
            except KeyError:
                return self.VictoryNumber()
            battle_winrate_list.append((battle_field, next_battle, winrate))
        print (battle_winrate_list)
        print(f"닥터: {self.BC}개의 전투에서 승리할 수 있는 수는 {str(max(battle_winrate_list, key=lambda x: x[2])[0])[0]}뿐이었네")
        return str(max(battle_winrate_list, key=lambda x: x[2])[0])[0]

    def FutureSight(self):
        for sight in range(250):
            orb = deepcopy(self)
            # 승리자가 나올때 까지 무작위 input 
            while not orb.winner and orb.cells > 0:
                orb.input(orb.validate_input_col(str(random.randrange(1, 8))))
            # local game(orb)에서 승무패에 따라 아가모토의눈에 [승, 무, 패]를 기록
            if orb.winner == self.marker:
                # print(f'{orb.battle}전장에서 이겼네')
                for i in range(len(orb.battle)):
                    win_record = self.EOA.get(orb.battle[0:i+1], [0, 0, 0])
                    win_record[0] += 1
                    self.EOA[orb.battle[0:i+1]] = win_record
            elif orb.winner == 0:
                # print(f'{orb.battle}전장에서 비겼네')
                for i in range(len(orb.battle)):
                    win_record = self.EOA.get(orb.battle[0:i+1], [0, 0, 0])
                    win_record[1] += 1
                    self.EOA[orb.battle[0:i+1]] = win_record
            else:
                # print(f'{orb.battle}전장에서 졌네')
                for i in range(len(orb.battle)):
                    win_record = self.EOA.get(orb.battle[0:i+1], [0, 0, 0])
                    win_record[2] += 1
                    self.EOA[orb.battle[0:i+1]] = win_record
        self.BC += 250
