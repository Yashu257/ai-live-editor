from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/generate")
def generate(data: dict):
    prompt = data.get("prompt", "")
    return {
        "component": "Hero.jsx",
        "code": f"<h1>{prompt}</h1>"
    }
