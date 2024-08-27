# server.py
import asyncio
import websockets
import json

class GameServer:
    def __init__(self):
        self.players = []
        self.game_state = self.initialize_game_state()

    def initialize_game_state(self):
        # Initial game state: 5x5 grid with two players
        return {
            "grid": [["" for _ in range(5)] for _ in range(5)],
            "players": {
                "A": ["A-P1", "A-H1", "A-H2", "A-P2", "A-P3"],
                "B": ["B-P1", "B-H1", "B-H2", "B-P2", "B-P3"],
            },
            "turn": "A",
        }

    async def register(self, websocket):
        self.players.append(websocket)
        if len(self.players) == 2:
            await self.start_game()

    async def start_game(self):
        await self.broadcast_state()

    async def unregister(self, websocket):
        self.players.remove(websocket)

    async def broadcast_state(self):
        if len(self.players) == 2:
            state_json = json.dumps(self.game_state)
            await asyncio.wait([player.send(state_json) for player in self.players])

    async def handle_move(self, websocket, move_data):
        # Parse the move data and update the game state accordingly
        # This is where the game logic goes, including move validation and state updates

        # For simplicity, let's assume move_data is a dictionary like:
        # {"player": "A", "move": "P1:F"}
        player = move_data["player"]
        move = move_data["move"]

        # Update game state based on the move
        # ...

        # Switch turns
        self.game_state["turn"] = "B" if self.game_state["turn"] == "A" else "A"

        await self.broadcast_state()

    async def main_logic(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                move_data = json.loads(message)
                await self.handle_move(websocket, move_data)
        finally:
            await self.unregister(websocket)

start_server = websockets.serve(GameServer().main_logic, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
