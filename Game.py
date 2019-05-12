import random

class game:
    def __init__(self):
        self.board = [[" " for _ in range(7)] for _ in range(6)]
        self.cells = 42
        self.winner = 0
        self.battle = ""
        self.row_board = [0, 0, 0, 0, 0, 0, 0]
        self.marker = "O"

    def print(self):
        row_num = 6
        for row in self.board[::-1]:
            print(f'{row_num}: ' + " | ".join(row))
            print("  ---+---+---+---+---+---+---")
            row_num -= 1
        print("   1   2   3   4   5   6   7 ")

    def validate_input_col(self, col):
        # col 조건 1) 숫자, 2) 0~6 사이, 3) 첫턴에는 3이 안됨, 4) col에 5이상
        if not col.isdecimal():
            col = input('숫자를 입력해야합니다.\n돌을 놓을 자리를 1~7까지 다시 한번 정해주세요')
            return self.validate_input_col(col)
        elif col not in ['1', '2', '3', '4', '5', '6', '7']:
            col = input('1~7 사이의 숫자를 입력해야합니다.\n돌을 놓을 자리를 1~7까지 다시 한번 정해주세요')
            return self.validate_input_col(col)
        elif self.cells == 42 and col == '4':
            # col = input('첫 턴에는 4번 자리에 돌을 놓는 것이 불가능합니다.\n돌을 놓을 자리를 1~7까지 다시 한번 정해주세요')
            # return self.validate_input_col(col)
            return self.validate_input_col(str(random.randrange(1,8)))
        elif self.board[5][int(col)-1] != " ":
            # col = input('선택하신 열은 가득 찼습니다.\n돌을 놓을 자리를 1~7까지 다시 한번 정해주세요')
            # return self.validate_input_col(col)
            return self.validate_input_col(str(random.randrange(1,8)))
        else:
            return int(col)-1

    def input(self, col):
        self.board[self.row_board[col]][col] = self.marker
        self.battle += str(col + 1)
        self.marker = "O" if self.marker == "X" else "X"
        self.row_board[col] += 1
        self.cells -= 1
        self.print()
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
                print(f'{row+1}행 가로 승리')
                self.winner = set_point
                return
        # 세로 평가
        if row > 2:
            # start_adj = row
            for start_row in range(max(0, row-3), 3):
                if self.board[start_row][col] == " ": continue
                check_list = [self.board[start_row+adj][col] for adj in range(4)]
                if check_list.count("O") == 4 or check_list.count("X") == 4:
                    print(f'{col+1}열 세로 승리')
                    self.winner = set_point
                    return
        # 우하 평가
        if 9 > diagonal_SE_emcee > 2:
            if diagonal_SE_emcee < 6:
                for start_row in range(diagonal_SE_emcee-2):
                    check_list = [self.board[diagonal_SE_emcee-start_row-adj][start_row+adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        print(f'{col + 1}, {row + 1}착수점 우하 대각선 승리')
                        self.winner = set_point
                        return
            else:
                for start_row in range(6, diagonal_SE_emcee-3, -1):
                    check_list = [self.board[diagonal_SE_emcee-start_row+adj][start_row-adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        print(f'{col + 1}, {row + 1}착수점 우하 대각선 승리')
                        self.winner = set_point
                        return
        # 우상 평가
        if 4 > diagonal_NE_emcee > -3:
            if diagonal_NE_emcee < 1:
                for start_row in range(diagonal_NE_emcee+3):
                    check_list = [self.board[start_row-diagonal_NE_emcee+adj][start_row+adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        print(f'{col + 1}, {row + 1} 우상 대각선 승리')
                        self.winner = set_point
                        return
            else:
                for start_row in range(6, diagonal_NE_emcee+2, -1):
                    check_list = [self.board[start_row-diagonal_NE_emcee-adj][start_row-adj] for adj in range(4)]
                    if check_list.count("O") == 4 or check_list.count("X") == 4:
                        print(f'{col + 1}, {row + 1} 우상 대각선 승리')
                        self.winner = set_point
                        return
