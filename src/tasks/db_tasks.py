from db import (
    get_engine,
    get_old_tasks_ids,
    delete_tasks_list
)

async def async_clean_old_tasks():
    _, AsyncSessionLocal = get_engine()

    async with AsyncSessionLocal() as session:
        old_tasks = await get_old_tasks_ids(session)
        await delete_tasks_list(session, tasks_ids=old_tasks)