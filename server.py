from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# --------------------------
# Память: игры в RAM
# --------------------------
games = {}
game_counter = 0


class TicTacToeGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.board = [['', '', ''] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.players = {'X': None, 'O': None}  # tg_user_id кто есть кто

    def make_move(self, row, col, player):
        # нельзя ходить если игра закончилась
        if self.game_over:
            return False

        # нельзя сходить не в свою очередь
        if player != self.current_player:
            return False

        # нельзя сходить в занятую клетку
        if self.board[row][col] != '':
            return False

        # выполняем ход
        self.board[row][col] = player

        # проверяем победителя
        if self.check_winner(player):
            self.winner = player
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True
        else:
            self.current_player = 'O' if player == 'X' else 'X'

        return True

    def check_winner(self, player):
        b = self.board
        # строки
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == player:
                return True
        # столбцы
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == player:
                return True
        # диагонали
        if b[0][0] == b[1][1] == b[2][2] == player:
            return True
        if b[0][2] == b[1][1] == b[2][0] == player:
            return True
        return False

    def is_board_full(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    return False
        return True

    def get_state(self):
        return {
            "board": self.board,
            "currentPlayer": self.current_player,
            "winner": self.winner,
            "gameOver": self.game_over,
            "players": self.players
        }


# --------------------------
# РОУТЫ
# --------------------------

# фронт самой игры
@app.route("/")
def index():
    return render_template("index.html")


# создать новую игру
@app.post("/api/game/new")
def api_new_game():
    global game_counter
    game_counter += 1
    game_id = str(game_counter)

    game = TicTacToeGame(game_id)
    games[game_id] = game

    return jsonify({
        "success": True,
        "gameId": game_id,
        "gameState": game.get_state()
    })


# зайти в игру
@app.post("/api/game/<game_id>/join")
def api_join(game_id):
    if game_id not in games:
        return jsonify({"success": False, "error": "Game not found"})

    game = games[game_id]
    data = request.get_json()
    user_id = str(data.get("userId"))

    # назначаем сторону
    if game.players["X"] is None:
        game.players["X"] = user_id
        player = "X"
    elif game.players["O"] is None:
        game.players["O"] = user_id
        player = "O"
    else:
        return jsonify({"success": False, "error": "Game is full"})

    return jsonify({
        "success": True,
        "player": player,
        "gameState": game.get_state()
    })


# сделать ход
@app.post("/api/game/<game_id>/move")
def api_move(game_id):
    if game_id not in games:
        return jsonify({"success": False, "error": "Game not found"})

    game = games[game_id]
    data = request.get_json()

    row = data.get("row")
    col = data.get("col")
    player = data.get("player")

    ok = game.make_move(row, col, player)
    if not ok:
        return jsonify({"success": False, "error": "Invalid move"})

    return jsonify({
        "success": True,
        "gameState": game.get_state()
    })


# стейт игры (поллинг)
@app.get("/api/game/<game_id>")
def api_state(game_id):
    if game_id not in games:
        return jsonify({"success": False, "error": "Game not found"})

    return jsonify({
        "success": True,
        "gameState": games[game_id].get_state()
    })


if __name__ == "__main__":
    # локально поднимаем на 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
