import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.assembly import root_injector

load_dotenv()

app = root_injector.get(FastAPI)

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
