from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend working"}

@app.post("/api/generate")
def generate(data: dict):
    prompt = data.get("prompt", "")
    return {
        "component": "Hero.jsx",
        "code": f"<h1>{prompt}</h1>"
    }
