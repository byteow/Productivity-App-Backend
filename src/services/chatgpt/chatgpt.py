from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from typing import List

class ChatGPT:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    
    async def _base_request(self, messages: List[dict]):
        return await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" }
        )
    

    async def survey_generate(self):
        system_instruction = (
            "You are a professional productivity survey generator."
            "Return ONLY a JSON object with the following structure:"
            "[ { 'question': string, 'answer_type': 'numeric' | 'scale-1-5' | 'single_choice' | 'text' } ]"
            "For 'numeric', use a number. For 'single_choice, use Yes/No. For 'scale-1-5' use a mark from 1 to 5. For 'text', use a text"
        )

        response = await self._base_request(messages=[
            { "role": "system", "content": system_instruction },
            { "role": "user", "content": 'Create a performance questionnaire that consists of exactly 5 questions.' }
        ])
        return response.choices[0].message.content