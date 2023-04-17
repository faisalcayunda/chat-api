
import pyrebase
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


pb = pyrebase.initialize_app(json.load(open("firebase_config.json")))

app = FastAPI(title="Chat API", description="API for simple chat application", version="1.0.0")
db = pb.database()
allow_all = ["*"]
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)


@app.post("/chats", tags=["Chats"])
async def send_chat(request: Request):
  req : dict = await request.json()
  from_user = req.get('from_user')
  to_user = req.get('to_user')
  message = req.get('message')
  db.child("chats").child(from_user).child(to_user).push(message)
  return JSONResponse(content={"message": "Chat message sent successfully."}, status_code=200)

@app.get("/chats/{from_user}", tags=["Chats"])
async def get_chats(from_user: str):
  chats = db.child("chats").child(from_user).get()
  return chats.val()

@app.get("/chats/{from_user}/{to_user}", tags=["Chats"])
async def get_chats_specify(from_user: str, to_user: str):
  chats = db.child("chats").child(from_user).child(to_user).get()
  return chats.val()