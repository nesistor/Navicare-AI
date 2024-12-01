from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from ai.ai_processing import MedicalDocumentProcessor  # Import ai_processing class

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

# Instantiate the AI processor
medical_processor = MedicalDocumentProcessor()

@router.post("/create")
async def create_journey(message: str, context: List[Dict] = None):
    try:
        # Use ai_processing to process the chat and get a response
        ai_response = await medical_processor.process_chat(message, context)

        # Store journey (if needed)
        journey_id = str(len(journeys_db) + 1)
        journey = {
            "journey_id": journey_id,
            "message": ai_response['response'],  # Store the AI response message
            "journey_details": ai_response['journey']  # Store the structured journey
        }

        # Store journey in in-memory database
        journeys_db[journey_id] = journey

        return {"journey_id": journey_id, "message": "Journey created successfully", "ai_response": ai_response['response'], "journey": ai_response['journey']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{journey_id}")
async def get_journey(journey_id: str):
    if journey_id not in journeys_db:
        raise HTTPException(status_code=404, detail="Journey not found")
    return journeys_db[journey_id]
