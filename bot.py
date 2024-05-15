import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton

import config
from database import on_startup
from queries import add_task, select_all_tasks

dp = Dispatcher()


class Form(StatesGroup):
    start_add = State()
    task_name = State()
    show_all_tasks = State()


@dp.message(StateFilter(None), Command("add"))
async def command_add(message: Message, state: FSMContext) -> None:
    await message.answer("Добавить задачу в список?", reply_markup=ReplyKeyboardRemove(keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        ]
    ],
        resize_keyboard=True, ))

    await state.set_state(Form.start_add)


@dp.message(StateFilter(Form.start_add), Form.start_add, F.text.casefold() == "да")
async def process_start_add_yes(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Напишите название задания: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.task_name)


@dp.message(StateFilter(Form.start_add), Form.start_add, F.text.casefold() == "нет")
async def process_start_add_no(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Отмена",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(None)


@dp.message(StateFilter(Form.task_name), Form.task_name)
async def process_task_name(message: Message, state: FSMContext) -> None:
    await state.update_data(task_name=message.text.lower())
    await add_task(message.from_user.id, message.text.lower())
    await message.answer(
        "Задание добавлено",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(None)


@dp.message(Command("tsk"))
async def command_tsk(message: Message, state: FSMContext) -> None:
    await message.answer("Вывести список задач?", reply_markup=ReplyKeyboardRemove(keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        ]
    ],
        resize_keyboard=True, ))

    await state.set_state(Form.show_all_tasks)


@dp.message(StateFilter(Form.show_all_tasks), Form.show_all_tasks, F.text.casefold() == "да")
async def process_tsk_yes(message: Message, state: FSMContext) -> None:
    tasks = await select_all_tasks()
    if len(tasks) > 0:
        await message.answer(
            "\n".join([t.name for t in tasks]),
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Список задач пуст",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.set_state(None)


@dp.message(StateFilter(Form.show_all_tasks), Form.show_all_tasks, F.text.casefold() == "нет")
async def process_tsk_no(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Отмена",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(None)


async def main() -> None:
    await on_startup(dp)
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
