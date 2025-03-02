from fastapi import FastAPI, WebSocket
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_state = {
    "territories": {
        "cubic": {"owner": None, "troops": 0},
        "vadvillio": {"owner": None, "troops": 0},
        "caspiar": {"owner": None, "troops": 0}
    },
    "currentPlayer": "Player 1"
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        action = json.loads(data)

        if action["type"] == "claim_territory":
            territory = action["territory"]
            if game_state["territories"][territory]["owner"] is None:
                game_state["territories"][territory]["owner"] = game_state["currentPlayer"]
                game_state["currentPlayer"] = "Player 2" if game_state["currentPlayer"] == "Player 1" else "Player 1"

        await websocket.send_text(json.dumps(game_state))
