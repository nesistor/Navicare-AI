from typing import Dict, List
import re
from fastapi import HTTPException
from .gemini_api import GeminiAPI
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

class MedicalDocumentProcessor:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        self.medical_data = {
            "medications": [],
            "appointments": [],
            "treatments": [],
            "complete": False,
        }

    async def extract_medical_info(self, text: str) -> Dict:
        """
        Use Gemini AI to extract medical information from the given text (medications, treatments, etc.)
        """
        prompt = f"""
        Extract medical information from this text: '{text}'
        Please identify:
        - Medications (name of medications)
        - Appointments (including timing, dates and purposes)
        - Treatments (procedures, dosage, therapies, etc.)
        Format as structured data.
        """
        try:
            response = await self.gemini_api.generate_response(prompt)
            return self._parse_medical_info(response)
        except Exception as e:
            logger.error(f"Error extracting medical information: {e}")
            raise HTTPException(status_code=500, detail="Error extracting medical information")

    def _parse_medical_info(self, ai_response: str) -> Dict:
        """
        Parse the AI response to extract and structure the medical information.
        """
        info = {"medications": [], "appointments": [], "treatments": []}
        if "medication" in ai_response.lower():
            med_matches = re.findall(r"Medication: (.*?) Dosage: (.*?) Time: (.*?)(?:\n|$)", ai_response)
            for med in med_matches:
                info["medications"].append({"name": med[0], "dosage": med[1], "timing": med[2]})
        return info

    async def create_treatment_journey(self) -> Dict:
        """
        Create a treatment journey if enough information is available (medications, appointments, etc.)
        """
        if not self.medical_data["complete"]:
            return {"error": "Insufficient data to create treatment journey."}

        journey_prompt = f"""
        Create a treatment journey based on the following information:
        Medications: {self.medical_data['medications']}
        Appointments: {self.medical_data['appointments']}
        Treatments: {self.medical_data['treatments']}
        """

        try:
            response = await self.gemini_api.generate_response(journey_prompt)
            return self._structure_journey(response), self._parse_medical_info(response)
        except Exception as e:
            logger.error(f"Error creating treatment journey: {e}")
            raise HTTPException(status_code=500, detail="Error creating treatment journey")

    def _structure_journey(self, ai_response: str) -> Dict:
        """
        Structure the AI response into a usable format for the treatment journey.
        """
        journey = {"daily_schedule": [], "appointments": [], "milestones": [], "reminders": []}
        return journey  # Further structure can be added depending on the response format

    async def process_chat(self, message: str, context: List[Dict] = None) -> Dict:
        """
        Process the chat message, extract medical information, and generate a treatment journey if possible.
        """
        try:
            # Log the provided context and the new message
            logger.info(f"Processing message: {message}")
            logger.info(f"Context: {context}")

            # Prepare context for AI, ensuring each message has a 'role' field
            prompt = """
            You are a medical assistant that helps users with creating a medical journey pathway by tracking medical information, such as medications, appointments, and treatments.
            The user will ask you about their medical information, and you need to give detailed and specific responses based on the data structure format and also
            “Given the following medication routine, generate a detailed treatment journey pathway for the user. The pathway should include the following:

            1. **Daily Schedule**: A detailed timeline of when and how the medication should be taken each day. Include:
            - The number of doses per day.
            - The specific time(s) for each dose.
            - Any instructions (e.g., take with food, avoid certain activities).

            2. **Treatment Milestones**: Key events or milestones during the treatment period. This could include the start of treatment, any mid-treatment checkpoints, and the end of treatment.

            3. **Reminders**: Important notes for the user about the treatment. This may include:
            - How to handle missed doses.
            - The importance of completing the full course of treatment.
            - Any special instructions, such as dietary restrictions or activities to avoid.

            4. **Post-Treatment Follow-Up**: Suggested follow-up appointments or checks after the treatment is completed to ensure effectiveness and monitor side effects.

            ### Routine Example:
            - **Drug**: Artemether-Lumefantrine (ACT) - Dosage: Take 4 tablets twice daily for 3 days with food.
            - **Start Date**: [Insert start date]
            - **End Date**: [Insert end date, 3 days after start date]
            - **Frequency**: Twice daily (Morning and Evening)
            - **Time of Day**: 8:00 AM (Morning), 8:00 PM (Evening)

            Based on this routine, create a treatment journey pathway.”
            """

            # Ensure the context has a 'role' field for each message, using 'user' role by default
            messages = [{"role": "user", "content": msg["content"]} for msg in context] if context else []
            messages.append({"role": "user", "content": message})  # Add current message with 'role' field

            # Get a response from the AI system
            chat_response = await self.gemini_api.generate_response(prompt, messages)
            logger.info(f"AI Response: {chat_response}")

            # Extract medical information from the current message
            medical_info = await self.extract_medical_info(chat_response)
            logger.info(f"Extracted Medical Info: {medical_info}")

            # Update internal medical data with the newly extracted information
            self._update_medical_data(medical_info)

            # Generate treatment journey if enough data is available
            journey = None
            if self._check_information_complete():
                self.medical_data["complete"] = True
                journey = await self.create_treatment_journey()

            # Return the AI's response, extracted medical info, and journey if available, filtering out empty data
            response_data = {
                "response": chat_response
            }

            if medical_info and (medical_info.get("medications") or medical_info.get("appointments") or medical_info.get("treatments")):
                response_data["medical_info"] = medical_info

            if journey:
                response_data["journey"] = journey

            response_data["information_complete"] = self.medical_data["complete"]

            return response_data

        except Exception as e:
            logger.error(f"Chat processing error: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")
        
    def _structured_journey(self, ai_response: str) -> Dict:
        """
        Structure the AI response into a usable format for the treatment journey.
        """
        # This is where we structure the raw AI response into the defined journey format.
        # For simplicity, let's assume the AI response contains key components we can extract.

        # Sample data extraction for illustration:
        journey = {
            "daily_schedule": [
                {
                    "time": "8:00 AM",
                    "medication": "Artemether-Lumefantrine",
                    "dosage": "4 tablets",
                    "instructions": "Take with food"
                },
                {
                    "time": "8:00 PM",
                    "medication": "Artemether-Lumefantrine",
                    "dosage": "4 tablets",
                    "instructions": "Take with food"
                }
            ],
            "milestones": [
                {
                    "title": "Start of Treatment",
                    "description": "Begin the medication regimen",
                    "datetime": "2024-11-01 08:00 AM"
                },
                {
                    "title": "End of Treatment",
                    "description": "Complete the 3-day treatment course",
                    "datetime": "2024-11-03 08:00 PM"
                }
            ],
            "reminders": [
                {
                    "message": "It is important to take the full course of treatment.",
                    "priority": "high"
                },
                {
                    "message": "Avoid alcohol during treatment.",
                    "priority": "medium"
                }
            ],
            "appointments": [
                {
                    "date": "2024-11-07",
                    "time": "10:00 AM",
                    "description": "Follow-up check with healthcare provider"
                }
            ]
        }

        # Here you can add more sophisticated parsing and structuring logic as needed

        return journey

    def _update_medical_data(self, new_info: Dict):
        """
        Update internal medical data with the new information extracted from the message.
        """
        for category in ["medications", "appointments", "treatments"]:
            self.medical_data[category].extend(new_info.get(category, []))

        # Remove duplicates from each category
        for category in ["medications", "appointments", "treatments"]:
            self.medical_data[category] = list({str(item): item for item in self.medical_data[category]}.values())

    def _check_information_complete(self) -> bool:
        """
        Check if enough medical information is available to consider the data as complete.
        """
        return len(self.medical_data["medications"]) > 0 or len(self.medical_data["appointments"]) > 0 or len(self.medical_data["treatments"]) > 0
