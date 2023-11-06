import random


class Ship:
    def __init__(self, position):
        self.position = position
        self.hits = 0

    def get_status(self):
        if self.hits == len(self.position):
            return "Потоплен"
        elif self.hits > 0:
            return "Ранен"
        else:
            return "Цел"


class Board:
    def __init__(self):
        self.size = 6
        self.ships = []
        self.board = [["О" for _ in range(self.size)] for _ in range(self.size)]

    def place_ship(self, ship):
        for x, y in ship.position:
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                raise ValueError("Корабль выходит за границы доски")
            if self.board[x][y] != "О":
                raise ValueError("Корабли перекрываются")
        for x, y in ship.position:
            self.board[x][y] = "■"
        self.ships.append(ship)

    def shoot(self, x, y):
        if self.board[x][y] == "X" or self.board[x][y] == "T":
            raise ValueError("Ход недопустим")
        if self.board[x][y] == "О":
            self.board[x][y] = "T"
            return False
        else:
            self.board[x][y] = "X"
            for ship in self.ships:
                if (x, y) in ship.position:
                    ship.hits += 1
                    if ship.get_status() == "Потоплен":
                        for ship_x, ship_y in ship.position:
                            self.board[ship_x][ship_y] = "X"
                        self.ships.remove(ship)
                    return True

    def is_game_over(self):
        return len(self.ships) == 0


def print_board(board):
    print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
    print("----------------------------")
    for i in range(board.size):
        print(f" {i + 1} | {' | '.join(board.board[i])} |")
        print("----------------------------")


def player_turn(board):
    try:
        x = int(input("Введите номер строки: ")) - 1
        y = int(input("Введите номер столбца: ")) - 1
        result = board.shoot(x, y)
        if result:
            print("Вы попали!")
        else:
            print("Вы промахнулись.")
    except ValueError as e:
        print(e)
        player_turn(board)


def ai_turn(board):
    valid_moves = []
    for x in range(board.size):
        for y in range(board.size):
            if board.board[x][y] == "О":
                valid_moves.append((x, y))
    x, y = random.choice(valid_moves)
    result = board.shoot(x, y)
    if result:
        print("Компьютер попал!")
    else:
        print("Компьютер промахнулся.")


def play_game():
    player_board = Board()
    ai_board = Board()

    player_ships = [
        Ship([(0, 0), (0, 1), (0, 2)]),
        Ship([(5, 4), (5, 5)]),
        Ship([(3, 0)]),
        Ship([(4, 4), (4, 5)]),
        Ship([(0, 5)]),
    ]

    ai_ships = [
        Ship([(0, 0), (1, 0), (2, 0)]),
        Ship([(1, 4), (2, 4)]),
        Ship([(3, 2)]),
        Ship([(0, 2), (1, 2)]),
        Ship([(2, 5)]),
    ]

    for ship in player_ships:
        player_board.place_ship(ship)

    for ship in ai_ships:
        ai_board.place_ship(ship)

    while True:
        print("Ваше поле:")
        print_board(player_board)

        print("Поле компьютера:")
        print_board(ai_board)

        print("Ваш ход:")
        player_turn(ai_board)
        if ai_board.is_game_over():
            print("Вы выиграли!")
            break

        print("Ход компьютера:")
        ai_turn(player_board)
        if player_board.is_game_over():
            print("Компьютер выиграл!")
            break


play_game()