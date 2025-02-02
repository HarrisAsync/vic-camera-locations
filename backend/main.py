from fastapi import FastAPI
from starlette.responses import FileResponse 

app = FastAPI()

@app.get("/")
async def hello_world():
    return FileResponse("static/index.html")