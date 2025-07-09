from aiogram.fsm.state import StatesGroup, State

class UploadMovie(StatesGroup):
    waiting_for_code = State()
    waiting_for_description = State()

