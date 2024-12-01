import google.generativeai as genai
from typing import List, Dict
import os
from dotenv import load_dotenv

class GeminiAPI:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set. Please check your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(self, prompt: str, context: List[Dict] = None) -> str:
        try:
            # If there's context, include it in the prompt
            if context:
                context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context])
                prompt = f"Previous conversation:\n{context_str}\n\nCurrent message: {prompt}"

            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}") 