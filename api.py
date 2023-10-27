from fastapi import FastAPI
from get_character import get_info_for_character

app = FastAPI()

@app.get("/api/characters/{character}")
async def get_character(character: str):
    return get_info_for_character(character)