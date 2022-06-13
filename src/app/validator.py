
class ValidatorUtil:
    MAX_GAME_NUMBER = 100
    GAME_INPUT = set(["columns", "rows", "players"])
    BOARD_SIZE = 3
    MOVE_TYPE = set(["MOVE", "QUIT"])

    @staticmethod
    def validateGameId(game_id):
        if game_id < 0 or not isinstance(game_id, int):
            return "Invalid game ID", 400
        return ()

    @staticmethod
    def validateGameInputs(input_json):
        if set(input_json.keys()) != ValidatorUtil.GAME_INPUT or len(set(input_json["players"])) != 2 \
             or input_json["columns"] != ValidatorUtil.BOARD_SIZE or input_json["rows"] != ValidatorUtil.BOARD_SIZE:
            return "Malformed game input", 400
        return ()

    @staticmethod
    def validateMove(game, row, col, move_type):
        if game.state == "COMPLETE":
            return "Game is already completed", 400
        if move_type not in ValidatorUtil.MOVE_TYPE:
            return "Malformed move type", 400
        if move_type == "MOVE":
            if row == -1 or col == -1 or not (0 <= row < ValidatorUtil.BOARD_SIZE) or not (0 <= col < ValidatorUtil.BOARD_SIZE):
                return "Malformed move input", 400
            if (row, col) in game.seen_moves:
                return "Move is illegal", 400

    @staticmethod
    def validatePlayerId(game, player_id):
        if player_id not in game.players:
            return "Player not part of game", 404
        if player_id == game.last_player:
            return "Not player's turn", 409

    @staticmethod
    def validateMoveNumber(game, move_number):
        if not isinstance(move_number, int):
            return "Malformed move number", 400
        if move_number > len(game.moves) - 1 or move_number < 0:
            return "Move not found", 404
