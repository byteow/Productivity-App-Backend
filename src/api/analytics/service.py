from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    get_weekly_stats,
    get_pomodoro_total_stats,
    get_tasks_total_stats,
    update_pomodoro_count_stat,
    create_pomodoro_daily_stat,
)

class Service:
    def __init__(self):
        ...

    
    async def productivity(self, user_id: int, db: AsyncSession):
        tasks_stats = await get_weekly_stats(db, user_id=user_id)
        maximum = max(tasks_stats)
        if maximum == 0:
            return { "productivity": [0] * 7 }
        tasks_stats = tasks_stats + [0] * (7 - len(tasks_stats))

        return {
            "productivity": [
                round((stat / maximum) * 100, 0)
                for stat in tasks_stats
            ]
        }
    

    async def analytics_stats(self, user_id: int, db: AsyncSession):
        pomodoro_stats = await get_pomodoro_total_stats(db, user_id=user_id)
        tasks_stats = await get_tasks_total_stats(db, user_id=user_id)
        
        return {
            "tasks": tasks_stats,
            "pomodoro":  pomodoro_stats
        }


    async def increment_pomodoro(self, user_id: int, db: AsyncSession):
        rowcount = await update_pomodoro_count_stat(db, user_id=user_id)
        if rowcount == 0:
            await create_pomodoro_daily_stat(db, user_id=user_id, count=1)

        return { "message": "Pomodoro stats successfully incremented" }