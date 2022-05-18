# Jonathan Friedman
# CS5007 Homework 2
# Completion Time: 2 hr 40 min

import sys


class ConnectN:
    def __init__(self, rows=6, columns=7, winning_number=4):
        self.__game_state = []
        self.__rows = rows
        self.__columns = columns
        self.__winning_number = winning_number
        self.__player_turn = 1

        for i in range(self.__rows):
            row = []
            for j in range(self.__columns):
                row.append(0)
            self.__game_state.append(row)

        self.__last_row = -1
        self.__last_column = -1

    @property
    def game_state(self):
        return self.__game_state

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def winning_number(self):
        return self.__winning_number

    @property
    def player_turn(self):
        return self.__player_turn

    def switch_turn(self):
        self.__player_turn = self.__player_turn = 2 - (self.__player_turn - 1)


    def __str__(self):

        game_state_string = ''
        
        for i in range(self.rows):
            for j in range(self.columns):
                game_state_string += str(self.game_state[i][j])
                if j != self.columns-1:
                    game_state_string += " "
            if i != self.rows-1:
                game_state_string += '\n'

        return game_state_string


    def reset_game(self):
        self.__init__(self.rows,self.columns, self.winning_number)
        

    def is_game_full(self):
        is_full = True
        
        for j in range(self.columns):
            if self.game_state[0][j] == 0:
                is_full = False

        return is_full

    def insert_chip(self, column_number):

        inserted = False

        for i in range(-1,-self.rows-1,-1):
            if not inserted:
                if self.game_state[i][column_number] == 0:
                    self.game_state[i][column_number] = self.player_turn
                    inserted = True
                    self.__last_column = column_number
                    self.__last_row = self.rows + i

        return inserted

    def detect_win(self):

        winner = -1

        if self.detect_win_by_column() != -1: # player wins
            winner = self.player_turn
        elif self.detect_win_by_row() != -1: #player wins
            winner = self.player_turn
        elif self.detect_win_by_diagonal() != -1: # player wins
            winner = self.player_turn

        return winner


    def detect_win_by_column(self):

        win_column = -1
        counter = 0

        if self.__last_row <= (self.rows - self.winning_number):
            for i in range(self.winning_number):
                if self.game_state[self.__last_row + i][self.__last_column] == self.player_turn:
                    counter += 1

        if counter >= self.winning_number:
            win_column = self.player_turn

        return win_column

    def detect_win_by_row(self):

        win_row = -1
        counter = 1
        stop_left = False
        stop_right = False

        for i in range(1,self.__last_column+1):
            one_to_the_left = self.game_state[self.__last_row][self.__last_column - i]
            if one_to_the_left != self.player_turn:
                stop_left = True
            if not stop_left:
                counter += 1

        for i in range(1,self.columns-self.__last_column):
            one_to_the_right = self.game_state[self.__last_row][self.__last_column + i]
            if one_to_the_right != self.player_turn:
                stop_right = True
            if not stop_right:
                counter +=1

        if counter >= self.winning_number:
            win_row = self.player_turn

        return win_row

    def detect_win_by_diagonal(self):

        win_diagonal = -1
        count_left_to_right = 1
        count_right_to_left = 1
        stop_left1 = False
        stop_right1 = False
        stop_left2 = False
        stop_right2 = False

        # /
        # down to the left
        for i in range(1,self.__last_column+1):
            if self.__last_row + i < self.rows and self.__last_column - i >= 0:
                down_to_the_left = self.game_state[self.__last_row + i][self.__last_column - i]
                if down_to_the_left != self.player_turn:
                    stop_left1 = True
                if not stop_left1:
                    count_left_to_right += 1

        # up to the right
        for i in range(1, self.columns - self.__last_column):
            if self.__last_row - i >= 0 and self.__last_column + i < self.columns:
                up_to_the_right = self.game_state[self.__last_row - i][self.__last_column + i]
                if up_to_the_right != self.player_turn:
                    stop_right1 = True
                if not stop_right1:
                    count_left_to_right += 1

        # \
        # up to the left
        for i in range(1,self.__last_column+1):
            if self.__last_row - i >= 0 and self.__last_column - i >= 0:
                up_to_the_left = self.game_state[self.__last_row - i][self.__last_column - i]
                if up_to_the_left != self.player_turn:
                    stop_left2 = True
                if not stop_left2:
                    count_right_to_left += 1

        # down to the right
        for i in range(1, self.columns - self.__last_column):
            if self.__last_row + i < self.rows and self.__last_column + i < self.columns:
                down_to_the_right = self.game_state[self.__last_row + i][self.__last_column + i]
                if down_to_the_right != self.player_turn:
                    stop_right2 = True
                if not stop_right2:
                    count_right_to_left += 1


        if count_left_to_right >= self.__winning_number or count_right_to_left >= self.__winning_number:
            win_diagonal = self.player_turn

        return win_diagonal


# Done for you!
def main():
    rows = 6
    columns = 7
    winning_number = 4

    if len(sys.argv) == 3+1:
        rows = int(sys.argv[1])
        columns = int(sys.argv[2])
        winning_number = int(sys.argv[3])

    game = ConnectN(rows, columns, winning_number)
    keep_playing = True

    while keep_playing:
        game_on = True
        game.reset_game()

        while game_on:
            print(game)
            print('Player ' + str(game.player_turn) + '\'s turn ')
            # assumes an integer was entered
            # although you should never make this assumption on user input, I have not taught exception handling yet
            column_number = int(input('Enter a column number or -1 to exit\n'))

            # if input is invalid
            if not(column_number == -1 or (0 < column_number <= columns)):
                print('Invalid input')
            elif column_number == -1:
                game_on = False
                keep_playing = False
            else:
                inserted = game.insert_chip(column_number-1)

                if inserted:
                    winner = game.detect_win()

                    if winner != -1 or game.is_game_full():
                        print(game)
                        game_on = False
                        if winner == -1:
                            print('Tie Game')
                        else:
                            print('Player ' + str(winner) + ' has won')
                            play_again = int(input('Enter any number to play again or -1 to exit\n'))
                            if play_again == -1:
                                keep_playing = False
                    else:
                        game.switch_turn()
                else:
                    print('Cannot insert a chip in that column')


if __name__ == '__main__':
    main()
