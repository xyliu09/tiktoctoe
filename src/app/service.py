import sys
sys.path.append("src")

from flask import Flask, jsonify, json, request
from app.models.game import Game, GameCache
from app.validator import ValidatorUtil

cache = GameCache() #Todo <xinyuan.liu> Remove this and use flask_caching 

app = Flask(__name__)

@app.route('/tictactoe', methods = ['GET'])
def getAllGames():
    data = {"games": list(cache.games.keys())} #in JSON-serializable type
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route('/tictactoe/creategame', methods = ['POST'])
def createGame():
    if cache.last_game_id >= ValidatorUtil.MAX_GAME_NUMBER:
        return "Reached max game number limit", 400
    input_json = request.get_json()
    validator_error = ValidatorUtil.validateGameInputs(input_json)
    if validator_error:
        return validator_error
    new_game_id = cache.last_game_id + 1
    cache.last_game_id  = new_game_id
    cache.games[new_game_id] = Game(input_json["columns"], input_json["rows"], input_json["players"], new_game_id)
    dictToReturn = {"gameId": new_game_id}
    app.logger.info('New game created + {0}'.format(input_json))
    return jsonify(dictToReturn), 200


@app.route('/tictactoe/<int:game_id>', methods = ['GET'])
def getGameState(game_id):
    game = cache.games.get(game_id, None)
    if not game:
        return "Game not found", 404
    validator_error = ValidatorUtil.validateGameId(game_id)
    if validator_error:
        return validator_error
    data = {
        "players": game.players, 
        "state": game.state,
        "winner": game.winner
    }
    if game.state == "IN_PROGRESS":
        data.pop("winner")
    return jsonify(data), 200

@app.route('/tictactoe/<int:game_id>/moves', methods = ['GET'])
def getAllMoves(game_id):
    #This endpoint also handles optional query parameter: GET /tictactoe/{game_id}/moves?start=0&until=1
    #The optional parameters are passed in request.args
    game = cache.games.get(game_id, None)
    if not game:
        return "Game not found", 404
    move_start_id, move_end_id = request.args.get("start", None), request.args.get("until", None)
    moves = game.moves[int(move_start_id): int(move_end_id) + 1] \
        if move_start_id and move_end_id else game.moves
    return jsonify({"moves": moves}), 200
    
@app.route('/tictactoe/<int:game_id>/<string:player_id>/<string:move_type>', methods = ['POST'])
def makeMove(game_id, player_id, move_type):
    #Both regular move and quit are using this route
    move_type = move_type.upper()
    game = cache.games.get(game_id, None)
    if not game:
        return "Game not found", 404
    row, col = request.get_json().get("row", -1), request.get_json().get("column", -1)
    validator_error = ValidatorUtil.validateGameId(game_id) \
        or ValidatorUtil.validatePlayerId(game, player_id) \
        or ValidatorUtil.validateMove(game, row, col, move_type)
    if validator_error:
        return validator_error
    game.move(move_type, player_id, row, col)
    if move_type == "MOVE":
        data = { "move": "{0}/moves/{1}".format(game_id, game.move_id), "isQuit": False}
    else:
        data = { "move": "{0}/moves/{1}".format(game_id, game.move_id), "isQuit": True}
    return jsonify(data), 200

@app.route('/tictactoe/<int:game_id>/moves/<int:move_number>', methods = ['GET'])
def getMove(game_id, move_number):
    game = cache.games.get(game_id, None)
    if not game:
        return "Game not found", 404
    validator_error = ValidatorUtil.validateGameId(game_id) \
          or ValidatorUtil.validateMoveNumber(game, move_number)  
    if validator_error:
        return validator_error
    return jsonify(game.moves[move_number]), 200

if __name__ == '__main__':
    app.run(debug = False)
