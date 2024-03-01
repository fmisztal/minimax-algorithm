import math


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, game):
        raise NotImplementedError("Subclasses must implement the get_move method.")


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game):
        while True:
            try:
                move = int(input("Enter your move (1-9): "))
                if 1 <= move <= 9 and game.is_valid_move(move):
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class AIPlayer(Player):
    def __init__(self, symbol, depth):
        super().__init__(symbol)
        self.depth = depth

    def get_move(self, game):
        _, move = minimax_pruning(game.state, self.symbol, self.depth)
        return move


class State:
    def __init__(self):
        self.board = [" "] * 9

    def display(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]}")
            if i < 6:
                print("---------")
        print("\n")

    def is_winner(self, symbol):
        for i in range(0, 9, 3):
            if all(self.board[i + j] == symbol for j in range(3)):
                return True

        for i in range(3):
            if all(self.board[i + j] == symbol for j in range(0, 9, 3)):
                return True

        if all(self.board[i] == symbol for i in range(0, 9, 4)) or all(
            self.board[i] == symbol for i in range(2, 7, 2)
        ):
            return True

        return False

    def is_full(self):
        return " " not in self.board

    def is_terminal(self):
        return self.is_winner("X") or self.is_winner("O") or self.is_full()

    def evaluate(self, player):
        score = 0
        corners = [0, 2, 6, 8]
        center = 4
        sides = [1, 3, 5, 7]
        sign = -1 if player == "X" else 1

        for pos in corners:
            if self.board[pos] == player:
                score += 3
        for pos in sides:
            if self.board[pos] == player:
                score += 2
        if self.board[center] == player:
            score += 4

        return sign * score


class Game:
    def __init__(self, player_X, player_O):
        self.state = State()
        self.players = {"X": player_X, "O": player_O}
        self.current_player = "O"

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def is_valid_move(self, move):
        return self.state.board[move - 1] == " "

    def make_move(self, move):
        if self.is_valid_move(move):
            self.state.board[move - 1] = self.current_player
            return True
        return False

    def play(self):
        while not self.state.is_terminal():
            self.state.display()
            move = self.players[self.current_player].get_move(self)
            if self.make_move(move):
                self.switch_player()

        self.state.display()
        winner = (
            "X"
            if self.state.is_winner("X")
            else "O"
            if self.state.is_winner("O")
            else "Draw"
        )
        print(f"Game over. Winner: {winner}")


def minimax_pruning(
    state, player, depth, alpha=-math.inf, beta=math.inf, indent=0, last_move=None
):
    if state.is_winner("X"):
        print(f"{'  ' * indent}Move: {last_move + 1}, Score: -100")
        return -100, None
    elif state.is_winner("O"):
        print(f"{'  ' * indent}Move: {last_move + 1}, Score: 100")
        return 100, None
    elif state.is_full():
        print(f"{'  ' * indent}Move: {last_move + 1}, Score: 0")
        return 0, None
    elif depth == 0:
        print(
            f"{'  ' * indent}Move: {last_move + 1}, Score: {state.evaluate('O' if player == 'X' else 'X')}"
        )
        return state.evaluate("O" if player == "X" else "X"), None

    scores = []
    moves = []

    for i in range(9):
        if state.board[i] == " ":
            new_state = State()
            new_state.board = state.board.copy()
            new_state.board[i] = player
            opponent = "O" if player == "X" else "X"
            score, _ = minimax_pruning(
                new_state, opponent, depth - 1, alpha, beta, indent + 1, i
            )
            scores.append(score)
            moves.append(i + 1)
            if player == "X":
                beta = min(beta, score)
            else:
                alpha = max(alpha, score)
            if beta <= alpha:
                break

    if player == "X":
        best_score_index = scores.index(min(scores))
    else:
        best_score_index = scores.index(max(scores))

    print(
        f"{'  ' * indent}Move: {moves[best_score_index]}, Score: {scores[best_score_index]} ({player})"
    )
    return scores[best_score_index], moves[best_score_index]


if __name__ == "__main__":
    # player_X = HumanPlayer('O')
    player_O = AIPlayer("O", depth=3)
    player_X = AIPlayer("X", depth=1)
    game = Game(player_X, player_O)
    game.play()
