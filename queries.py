from asyncpg import UniqueViolationError

from database import Task


async def add_task( user_id: int, name: str):
    try:
        task = Task(user_id=user_id, name=name)
        await task.create()

    except UniqueViolationError:
        print("Задание не добавлено")


async def select_all_tasks():
    tasks = await Task.query.gino.all()
    return tasks
