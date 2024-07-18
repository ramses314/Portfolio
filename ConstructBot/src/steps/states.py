from aiogram.filters.state import State, StatesGroup


class DynamicState(StatesGroup):
    start = State()
    step = State()
    finish = State()


async def get_step(state):
    data = await state.get_data()
    step = data.get("step")
    return step


async def dynamic_state(state, callback):
    step = await get_step(state)
    if not step:
        await state.set_state(DynamicState.step)
    await state.update_data(step=callback.data)
    step = await get_step(state)
    if step == "callback_finish":
        await state.clear()
