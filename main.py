from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    return Response(status_code=200)

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
