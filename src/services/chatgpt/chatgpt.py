from openai import AsyncOpenAI
from config import OPENAI_API_KEY, OPENAI_PROXY
from typing import List
import json

class ChatGPT:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_PROXY)

    
    async def _base_request(self, messages: List[dict]):
        return await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" }
        )
    

    async def survey_generate(self, lang):
        system_instruction = (
            "ACT AS a professional productivity survey generator. "
            "RETURN ONLY a valid JSON ARRAY containing EXACTLY 5 objects. "
            "DO NOT include any introductory or explanatory text. "
            "EACH OBJECT must have this strict schema: "
            "{ 'question': string, 'answer_type': 'numeric' | 'scale-1-5' | 'single_choice' | 'text' }. "
            "CONSTRAINTS: 'numeric' expects a number; 'single_choice' is strictly 'Yes' or 'No'; "
            "'scale-1-5' is a rating from 1 to 5; 'text' is a free-form string."
        )

        response = await self._base_request(messages=[
            { "role": "system", "content": system_instruction },
            { "role": "user", "content": f'Create a performance questionnaire that consists of exactly 5 questions. Use this language: {lang}' }
        ])
        return json.loads(response.choices[0].message.content)