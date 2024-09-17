import asyncio

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (Dialog, DialogManager, StartMode, Window,
                            setup_dialogs)
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Next
from aiogram_dialog.widgets.text import Const, Jinja

bot = Bot(token='7289270657:AAHNAnHOLIy6XVYCnMRcz24TestBYy2KEOA')
dp = Dispatcher()
user_data = {}
storage = MemoryStorage()
user_id_global = None

class MySG(StatesGroup):
    main = State()
    desc = State()
    category = State()
    due_date = State()
    result = State()


async def fetch_categories():
    url = "http://127.0.0.1:8000/api/categories/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                categories = await response.json()
                return {category['id']: category['name'] for category in categories}
            else:
                print(f"Ошибка при получении категорий: {response.status}")
                return {}

async def fetch_user(user_id):
    url = f"http://127.0.0.1:8000/api/users/{user_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                await response.json()
                return   # Возвращаем данные пользователя
            else:
                print(f"Ошибка при получении пользователя: {response.status}")
                return None

async def fetch_category_id(category_name):
    url = "http://127.0.0.1:8000/api/categories/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                categories = await response.json()
                # Создаем словарь для поиска ID по имени
                name_to_id = {category['name']: category['id'] for category in categories}
                return name_to_id.get(category_name, None)
            else:
                print(f"Ошибка при получении категорий: {response.status}")
                return None

async def get_tasks(callback: CallbackQuery, button: Button, manager: DialogManager):
    global user_id_global
    if user_id_global is None:
        await callback.message.answer("User ID не найден")
        return

    url = f"http://127.0.0.1:8000/api/tasks/?user_id={user_id_global}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                tasks = await response.json()
                # Получаем категории
                categories = await fetch_categories()

                # Формируем сообщение
                task_list = []
                for task in tasks:
                    category_name = categories.get(task['category'], 'Неизвестная категория')
                    task_list.append(
                        f"Задача: {task['title']}\nОписание: {task['description']}\nКатегория: {category_name}\nСтатус: {'Выполнена' if task['completed'] else 'Не выполнена'}"
                    )
                
                message = "\n\n".join(task_list)
                await callback.message.answer(f"Список задач:\n{message}")
            else:
                await callback.message.answer(f"Ошибка при получении задач: {response.status}")

async def getter(dialog_manager: DialogManager, **kwargs):
    global user_id_global
    if user_id_global is None:
        return None
    user = await fetch_user(user_id_global)
    url = "http://127.0.0.1:8000/api/tasks/"
    category_id = await fetch_category_id(dialog_manager.find("task_category").get_value())
    task_data = {
        "user": int(user_id_global),
        "title": dialog_manager.find("task_name").get_value(),
        "description": dialog_manager.find("task_description").get_value(),
        "category": category_id,  # Передаем название категории
        "due_date": dialog_manager.find("task_due_date").get_value(),
        "completed": "False",  # или True, если задача уже выполнена
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=task_data) as response:
            if response.status == 201:
                print(response)
            else:
                print(response)
    return {
        "task_name": dialog_manager.find("task_name").get_value(),
        "task_description": dialog_manager.find("task_description").get_value(),
        "task_category": dialog_manager.find("task_category").get_value(),
        "task_due_date": dialog_manager.find("task_due_date").get_value(),
    }

main_window = Window(
    Const("Привет ты можешь посмотреть список своих задач или же введи название новой задачи!"),  # just a constant text
    Button(Const("Список задач"), id="button1", on_click=get_tasks),
    TextInput(id="task_name", on_success=Next()),  # button with text and id
    state=MySG.main,  # state is used to identify window between dialogs
)
description_window = Window(
    Const("Введи описание задачи"),
    TextInput(id="task_description", on_success=Next()),
    state=MySG.desc,
)
category_window = Window(
    Const("Введи категорию задачи"),
    TextInput(id="task_category", on_success=Next()),
    state=MySG.category,
)
due_date_window = Window(
    Const("Введи дату и время задачи в формате 2024-00-00 00:00:00"),
    TextInput(id="task_due_date", on_success=Next()),
    state=MySG.due_date,
)
result_window = Window(
    Jinja(
        "<b>Вы ввели</b>:\n\n"
        "<b>название</b>: {{task_name}}\n"
        "<b>описание</b>: {{task_description}}\n"
        "<b>категория</b>: {{task_category}}\n"
        "<b>Дата выполнения</b>: {{task_due_date}}\n"
    ),
    state=MySG.result,
    getter=getter,
    parse_mode="html"
)



setup_dialogs(dp)
dialog = Dialog(main_window, description_window, category_window, due_date_window, result_window)

dp.include_router(dialog)

@dp.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    global user_id_global
    telegram_id = message.from_user.id
    url = "http://127.0.0.1:8000/api/register/"
    url_check_user = f"http://127.0.0.1:8000/api/users/{telegram_id}/"
    # Создаем данные для отправки
    data = {
        "username": str(telegram_id),
        "password": str(telegram_id),
        "email": f"{telegram_id}@gmail.com"
    }

    # Отправляем POST-запрос
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                user_data = await response.json()
                user_id_global = user_data.get("id")
                await message.answer(f"Регистрация прошла успешно! Ваш ID: {user_id_global}")
            elif response.status == 400:
                await message.answer(f"Вы уже зарегистрированы!")
            else:
                await message.answer(f"Ошибка регистрации: {response.status}")
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
