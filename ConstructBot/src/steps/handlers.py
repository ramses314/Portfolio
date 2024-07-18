import datetime

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.steps.construct import construct
from src.steps.states import DynamicState, dynamic_state

router = Router(name="main")


@router.message(CommandStart())
async def send_welcome(message: types.Message, state=FSMContext) -> None:
    await state.set_state(DynamicState.start)
    await state.update_data(start=message.text)
    await construct(message=message)
    return None


@router.callback_query(lambda с: True)
async def handle_any_callback(callback: types.CallbackQuery, state=FSMContext):
    await dynamic_state(state=state, callback=callback)
    await construct(callback=callback)
    return None


async def handle_from_checker(chat_id, type_of_check):
    chat = types.Chat(id=chat_id, type="private")
    message = types.Message(message_id=989, text="some",  chat=chat, date=datetime.datetime.now())
    callback = types.CallbackQuery(
        id="1",
        from_user=types.User(id=chat_id, username="None", is_bot=False, first_name='Test'),
        message=message,
        data=type_of_check,
        chat_instance="chat_instance_value",
    )
    await construct(callback=callback)
    return None


@router.message(lambda с: True)
async def echo(message: types.Message, state=FSMContext) -> None:
    await message.answer("🔥 To get the VIP channel 👉🏼 /start")
    return None


@router.message(F.video_note)
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(message.video_note.file_id)


@router.message(F.video)
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(message.video.file_id)


@router.message(F.photo)
async def send_welcome(message: types.Message):
    await message.answer(message.photo[0].file_id)
