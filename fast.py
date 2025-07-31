from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from story_logic import continue_story, update_inventory

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/story")
async def story_api(request: Request):
    data = await request.json()
    role = data.get("role")
    genre = data.get("genre")
    history = data.get("history", [])
    user_input = data.get("user_input")
    inventory = data.get("inventory", [])

    reply = continue_story(role, genre, history, user_input)
    inventory = update_inventory(reply, inventory)

    return {"response": reply, "inventory": inventory}
