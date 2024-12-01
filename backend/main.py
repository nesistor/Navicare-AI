from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.chatbot_api import router as chatbot_router
from apis.journey_api import router as journey_router

app = FastAPI(title="Medical Treatment Journey API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(journey_router, prefix="/journey", tags=["Journey"])

@app.get("/")
async def root():
    return {"message": "Medical Treatment Journey API"}


