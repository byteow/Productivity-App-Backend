import redis.asyncio as redis
import json
from config import REDIS_URL
from services import ChatGPT
from db import SurveyStatus, update_survey, get_engine

"""questions = [
    {"question": "Сколько часов вы спали прошлой ночью?", "answer_type": "numeric"},
    {"question": "Как вы оцениваете свою продуктивность за неделю?", "answer_type": "scale-1-5"},
    {"question": "Какая личная активность дала наибольшую пользу вашему самочувствию?", "answer_type": "text"},
    {"question": "Сколько задач вы закрыли на прошлой неделе?", "answer_type": "numeric"},
    {"question": "Вы планируете новые цели на следующую неделю?", "answer_type": "single_choice"}
]
"""

client = ChatGPT()

async def async_generate_survey(user_id: int, survey_id: int):
    survey = await client.survey_generate()
    if survey is None:
        print("ChatGPT Response is None")
        return

    _, AsyncSessionLocal = get_engine()

    async with AsyncSessionLocal() as session:
        await update_survey(
            session,
            survey_id=survey_id,
            status=SurveyStatus.PENDING,
            schema=survey
        )

    r = redis.from_url(REDIS_URL)

    notification = {"type": "survey_generated"}
    await r.publish(f"user_event_{user_id}", json.dumps(notification))
    await r.aclose()