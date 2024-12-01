from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class JourneyStep(BaseModel):
    title: str
    description: str
    datetime: str
    completed: bool = False

class Journey(BaseModel):
    title: str
    daily_schedule: List[Dict]
    appointments: List[Dict]
    milestones: List[Dict]
    reminders: List[Dict]

# In-memory storage for journeys
journeys_db = {}

@router.post("/create")
async def create_journey(journey: Journey):
    try:
        journey_id = str(len(journeys_db) + 1)
        journeys_db[journey_id] = journey
        return {"journey_id": journey_id, "message": "Journey created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{journey_id}")
async def get_journey(journey_id: str):
    if journey_id not in journeys_db:
        raise HTTPException(status_code=404, detail="Journey not found")
    return journeys_db[journey_id]
