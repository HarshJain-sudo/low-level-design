"""
Tic-Tac-Toe Game Design - Implementation

This file contains the complete implementation of the Tic-Tac-Toe game
following the bottom-up approach as described in solution_theory.md
"""

import abc
import typing
from enum import Enum


class GameStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PLAYER_1_WON = "PLAYER_1_WON"
    PLAYER_2_WON = "PLAYER_2_WON"
    DRAW = "DRAW"


class Symbol:
    def __init__(self, value: str):
        if not value or len(value) != 1:
            raise ValueError("Symbol must be a single character")
        self.value = value.upper()

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)


class Player:
    def __init__(self, name: str, symbol: Symbol):
        self.name = name
        self.symbol = symbol

    def get_name(self) -> str:
        return self.name

    def get_symbol(self) -> Symbol:
        return self.symbol

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Grid:
    def __init__(self, size: int):
        if size < 3:
            raise ValueError("Grid size must be at least 3")
        self.size = size
        self.grid: typing.List[typing.List[typing.Optional[Symbol]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]

    def get_size(self) -> int:
        return self.size

    def is_cell_empty(self, row: int, col: int) -> bool:
        self._validate_position(row, col)
        return self.grid[row][col] is None

    def place_symbol(self, row: int, col: int, symbol: Symbol) -> bool:
        if not self.is_cell_empty(row, col):
            return False
        self.grid[row][col] = symbol
        return True

    def get_symbol(self, row: int, col: int) -> typing.Optional[Symbol]:
        self._validate_position(row, col)
        return self.grid[row][col]

    def is_full(self) -> bool:
        for row in self.grid:
            if None in row:
                return False
        return True

    def _validate_position(self, row: int, col: int):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            raise ValueError(
                f"Position ({row}, {col}) is out of bounds for grid size "
                f"{self.size}"
            )

    def display(self):
        print("\n" + "=" * (self.size * 4 + 1))
        for i, row in enumerate(self.grid):
            print("|", end="")
            for j, cell in enumerate(row):
                symbol_str = str(cell) if cell else " "
                print(f" {symbol_str} |", end="")
            print()
            if i < self.size - 1:
                print("|" + "---|" * self.size)
        print("=" * (self.size * 4 + 1) + "\n")


class WinChecker(abc.ABC):
    @abc.abstractmethod
    def check_win(
        self, grid: Grid, symbol: Symbol, row: int, col: int
    ) -> bool:
        pass


class RowWinChecker(WinChecker):
    def check_win(
        self, grid: Grid, symbol: Symbol, row: int, col: int
    ) -> bool:
        for c in range(grid.get_size()):
            if grid.get_symbol(row, c) != symbol:
                return False
        return True


class ColumnWinChecker(WinChecker):
    def check_win(
        self, grid: Grid, symbol: Symbol, row: int, col: int
    ) -> bool:
        for r in range(grid.get_size()):
            if grid.get_symbol(r, col) != symbol:
                return False
        return True


class DiagonalWinChecker(WinChecker):
    def check_win(
        self, grid: Grid, symbol: Symbol, row: int, col: int
    ) -> bool:
        size = grid.get_size()
        # Check main diagonal (top-left to bottom-right)
        if row == col:
            for i in range(size):
                if grid.get_symbol(i, i) != symbol:
                    break
            else:
                return True

        # Check anti-diagonal (top-right to bottom-left)
        if row + col == size - 1:
            for i in range(size):
                if grid.get_symbol(i, size - 1 - i) != symbol:
                    break
            else:
                return True

        return False


class Game:
    def __init__(self, grid_size: int, player1: Player, player2: Player):
        if player1.get_symbol() == player2.get_symbol():
            raise ValueError("Players must have different symbols")
        self.grid = Grid(grid_size)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.status = GameStatus.IN_PROGRESS
        self.win_checkers: typing.List[WinChecker] = [
            RowWinChecker(),
            ColumnWinChecker(),
            DiagonalWinChecker(),
        ]

    def get_current_player(self) -> Player:
        return self.current_player

    def get_status(self) -> GameStatus:
        return self.status

    def get_grid(self) -> Grid:
        return self.grid

    def make_move(self, row: int, col: int) -> bool:
        if self.status != GameStatus.IN_PROGRESS:
            return False

        if not self.grid.is_cell_empty(row, col):
            return False

        symbol = self.current_player.get_symbol()
        self.grid.place_symbol(row, col, symbol)

        if self._check_win(row, col, symbol):
            if self.current_player == self.player1:
                self.status = GameStatus.PLAYER_1_WON
            else:
                self.status = GameStatus.PLAYER_2_WON
        elif self.grid.is_full():
            self.status = GameStatus.DRAW
        else:
            self._switch_player()

        return True

    def _check_win(self, row: int, col: int, symbol: Symbol) -> bool:
        for checker in self.win_checkers:
            if checker.check_win(self.grid, symbol, row, col):
                return True
        return False

    def _switch_player(self):
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )


class GameController:
    def __init__(self):
        self.game: typing.Optional[Game] = None

    def start_new_game(
        self, grid_size: int, player1_name: str, player1_symbol: str,
        player2_name: str, player2_symbol: str
    ) -> Game:
        player1 = Player(player1_name, Symbol(player1_symbol))
        player2 = Player(player2_name, Symbol(player2_symbol))
        self.game = Game(grid_size, player1, player2)
        return self.game

    def make_move(self, row: int, col: int) -> bool:
        if not self.game:
            raise ValueError("No game in progress. Start a new game first.")
        return self.game.make_move(row, col)

    def get_game_status(self) -> GameStatus:
        if not self.game:
            raise ValueError("No game in progress.")
        return self.game.get_status()

    def display_game(self):
        if not self.game:
            raise ValueError("No game in progress.")
        self.game.get_grid().display()
        print(f"Current Player: {self.game.get_current_player()}")
        print(f"Game Status: {self.game.get_status().value}")

    def is_game_over(self) -> bool:
        if not self.game:
            return True
        return self.game.get_status() != GameStatus.IN_PROGRESS


def get_user_input(prompt: str, validator=None) -> str:
    while True:
        value = input(prompt).strip()
        if validator:
            try:
                validator(value)
            except ValueError as e:
                print(f"Invalid input: {e}")
                continue
        return value


def validate_grid_size(value: str) -> int:
    size = int(value)
    if size < 3:
        raise ValueError("Grid size must be at least 3")
    return size


def validate_symbol(value: str) -> str:
    if not value or len(value) != 1:
        raise ValueError("Symbol must be a single character")
    return value.upper()


def main():
    print("=" * 50)
    print("Welcome to Tic-Tac-Toe Game!")
    print("=" * 50)

    # Get grid size
    grid_size = int(
        get_user_input(
            "Enter grid size (N for N*N grid, minimum 3): ",
            validate_grid_size,
        )
    )

    # Get player 1 details
    player1_name = get_user_input("Enter Player 1 name: ")
    player1_symbol = get_user_input(
        "Enter Player 1 symbol (single character): ", validate_symbol
    )

    # Get player 2 details
    player2_name = get_user_input("Enter Player 2 name: ")
    while True:
        player2_symbol = get_user_input(
            "Enter Player 2 symbol (single character, different from "
            f"Player 1): ",
            validate_symbol,
        )
        if player2_symbol.upper() == player1_symbol.upper():
            print("Player 2 symbol must be different from Player 1!")
            continue
        break

    # Start game
    controller = GameController()
    game = controller.start_new_game(
        grid_size, player1_name, player1_symbol, player2_name, player2_symbol
    )

    print("\n" + "=" * 50)
    print("Game Started!")
    print("=" * 50)

    # Game loop
    while not controller.is_game_over():
        controller.display_game()

        current_player = game.get_current_player()
        print(f"\n{current_player.get_name()}'s turn:")

        while True:
            try:
                row = int(
                    input(f"Enter row (0-{grid_size - 1}): ").strip()
                )
                col = int(
                    input(f"Enter column (0-{grid_size - 1}): ").strip()
                )

                if controller.make_move(row, col):
                    # Display updated grid after successful move
                    controller.display_game()
                    break
                else:
                    print("Invalid move! Cell is already occupied or out of "
                          "bounds. Try again.")
            except ValueError:
                print("Invalid input! Please enter valid numbers.")
            except Exception as e:
                print(f"Error: {e}")

    # Game over
    controller.display_game()
    status = controller.get_game_status()

    if status == GameStatus.PLAYER_1_WON:
        print(f"\n🎉 {game.player1.get_name()} wins!")
    elif status == GameStatus.PLAYER_2_WON:
        print(f"\n🎉 {game.player2.get_name()} wins!")
    else:
        print("\n🤝 It's a draw!")

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()

