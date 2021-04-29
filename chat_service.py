from fastapi import Request, FastAPI
import uvicorn

app = FastAPI()


@app.post("/test")
async def get_body():
    return {"msg": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
