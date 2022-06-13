import sys
sys.path.append("src")

from app.service import app


def test_getAllGames_empty():
    response = app.test_client().get("/tictactoe")
    assert response.status_code == 200
    assert response.json == {"games": []}

    _ = app.test_client().post("/tictactoe/creategame", json = { "players": ["player1", "player2"],
            "columns": 3,
            "rows": 3
        })
    response = app.test_client().get("/tictactoe")
    assert response.status_code == 200
    assert response.json == {"games": [1]}

def test_creategame():
    response = app.test_client().post("/tictactoe/creategame", json = { "players": ["player1", "player2"],
            "columns": 3,
            "rows": 3
        })
    assert response.status_code == 200
    assert response.json == {"gameId": 2}

    response = app.test_client().post("/tictactoe/creategame", json = { "players": ["player3", "player4"],
            "columns": 3,
            "rows": 3
        })
    assert response.status_code == 200
    assert response.json == {"gameId": 3}

def test_creategame_invalid_input():
    response = app.test_client().post("/tictactoe/creategame", json = { "players": ["player1", "player2", "player3"],
            "columns": 3,
            "rows": 3
        })
    assert response.status_code == 400
    assert response.data == b"Malformed game input"

    response = app.test_client().post("/tictactoe/creategame", json = { "players": ["player1", "player2"],
            "columns": 10,
        })
    assert response.status_code == 400
    assert response.data == b"Malformed game input"

    response = app.test_client().post("/tictactoe/creategame", json = { "players": ["player1", "player2"],
            "columns": 10,
            "rows": 3
        })
    assert response.status_code == 400
    assert response.data == b"Malformed game input"

def test_getGameState():
    response = app.test_client().get("/tictactoe/2")
    assert response.status_code == 200
    assert response.json == { "players" : ["player1", "player2"], # The list of players.
            "state": "IN_PROGRESS",
        }

def test_makemove():
    response = app.test_client().post("/tictactoe/2/player1/move", json = {
            "row" : 1,
            "column" : 1
        })
    assert response.status_code == 200
    assert response.json == {
            "move": "2/moves/0",
            "isQuit": False
        }

def test_makemove_quit():
    response = app.test_client().post("/tictactoe/2/player2/quit", json = {
            "row" : 1,
            "column" : 0
        })

    assert response.status_code == 200
    assert response.json == {
            "move": "2/moves/1",
            "isQuit": True
        }

def test_gameState_quit():
    response = app.test_client().get("/tictactoe/2")
    assert response.status_code == 200
    assert response.json == { "players" : ["player1", "player2"], # The list of players.
            "state": "COMPLETE",
            "winner": "player1"
        }

def test_getGameState_invalid_input():
    response = app.test_client().get("/tictactoe/5")
    assert response.status_code == 404
    assert response.data == b"Game not found"

def test_gameState_win():
    _ = app.test_client().post("/tictactoe/1/player1/move", json = {
        "row" : 1,
        "column" : 1
    })
    _ = app.test_client().post("/tictactoe/1/player2/move", json = {
        "row" : 0,
        "column" : 1
    })
    _ = app.test_client().post("/tictactoe/1/player1/move", json = {
        "row" : 0,
        "column" : 0
    })
    _ = app.test_client().post("/tictactoe/1/player2/move", json = {
        "row" : 0,
        "column" : 2
    })
    _ = app.test_client().post("/tictactoe/1/player1/move", json = {
        "row" : 2,
        "column" : 2
    })
    response = app.test_client().get("/tictactoe/1")
    assert response.status_code == 200
    assert response.json == { "players" : ["player1", "player2"], # The list of players.
        "state": "COMPLETE",
        "winner": "player1"
        }

def test_gameState_draw():
    _ = app.test_client().post("/tictactoe/3/player3/move", json = {
        "row" : 1,
        "column" : 1
    })
    _ = app.test_client().post("/tictactoe/3/player4/move", json = {
        "row" : 0,
        "column" : 0
    })
    _ = app.test_client().post("/tictactoe/3/player3/move", json = {
        "row" : 0,
        "column" : 1
    })
    _ = app.test_client().post("/tictactoe/3/player4/move", json = {
        "row" : 2,
        "column" : 1
    })
    _ = app.test_client().post("/tictactoe/3/player3/move", json = {
        "row" : 0,
        "column" : 2
    })
    _ = app.test_client().post("/tictactoe/3/player4/move", json = {
        "row" : 2,
        "column" : 0
    })
    _ = app.test_client().post("/tictactoe/3/player3/move", json = {
        "row" : 2,
        "column" : 2
    })
    _ = app.test_client().post("/tictactoe/3/player4/move", json = {
        "row" : 1,
        "column" : 2
    })
    _ = app.test_client().post("/tictactoe/3/player3/move", json = {
        "row" : 1,
        "column" : 0
    })
    response = app.test_client().get("/tictactoe/3")
    assert response.status_code == 200
    assert response.json == { "players" : ["player3", "player4"], # The list of players.
        "state": "COMPLETE",
        "winner": None
        }

def test_get_move():
    response = app.test_client().get("/tictactoe/2/moves/0")
    assert response.status_code == 200
    assert response.json == {
            "type" : "MOVE",
            "player": "player1",
            "row": 1, 
            "column": 1
        }

def test_get_move_quit():
    response = app.test_client().get("/tictactoe/2/moves/1")
    assert response.status_code == 200
    assert response.json == {
            "type" : "QUIT",
            "player": "player2", # number corresponding to the player
        }

def test_getAllMoves():
    response = app.test_client().get("/tictactoe/2/moves")
    assert response.status_code == 200
    assert response.json == {
         "moves": [{"type": "MOVE", "player": "player1", "row":1, "column":1 }, {"type": "QUIT", "player": "player2"}]
        }

    response = app.test_client().get("/tictactoe/2/moves?start=0&until=1")
    assert response.status_code == 200
    assert response.json == {
         "moves": [{"type": "MOVE", "player": "player1", "row":1, "column":1 }, {"type": "QUIT", "player": "player2"}]
        }


