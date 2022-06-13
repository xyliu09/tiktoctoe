class GameCache:
    def __init__(self) -> None:
        self.last_game_id = 0
        self.games = {}

class Game:
    def __init__(self, columns, rows, players, game_id):
        self.state = 'IN_PROGRESS'
        self.players = players
        self.last_player = None
        self.rowv = [0] * columns
        self.colv = [0] * rows
        self.diag1 = 0
        self.diag2 = 0
        self.moves = []
        self.move_id = -1
        self.n = columns
        self.winner = None
        self.game_id = game_id
        self.seen_moves = set()

    def move(self, moveType, player, row = None, col = None):
        self.move_id += 1
        if moveType == "QUIT":
            move = {"type": moveType, "player": player}
            self.moves.append(move)
            self.state = 'COMPLETE'
            self.winner = self.players[0] if self.players[0] != player else self.players[1]
            return -1
        move = {"type": moveType, "player": player, "row": row, "column": col}
        self.moves.append(move)
        self.seen_moves.add((row, col))
        
        player_val = 1

        if player == self.players[1]:
            player_val = -1
        self.last_player = player
        self.rowv[row] += player_val
        self.colv[col] += player_val

        if row == col:
            self.diag1 += player_val
            if abs(self.diag1) == self.n:
                self.state = 'COMPLETE'
                self.winner = player
                return 1
        if (self.n - 1 - row) == col:
            self.diag2 += player_val
            if abs(self.diag2) == self.n:
                self.state = 'COMPLETE'
                self.winner = player
                return 1
                
        if abs(self.rowv[row]) == self.n or abs(self.colv[col]) == self.n:
            self.state = 'COMPLETE'
            self.winner = player
            return 1
        if self.move_id == self.n * self.n - 1:
            self.state = 'COMPLETE'
            self.winner = None
        return 0