from fastapi import FastAPI 
import uvicorn

app = FastAPI()   

@app.get("/") 
async def main_route():     
  return {"message": "Hey, It is me Goku"}


def main():
  print("Hello World")
  uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)

if __name__ == "__main__":
  main()