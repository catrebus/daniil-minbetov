from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from core import container
from keyboards.keyboards import main_keyboard

tg_router = Router()

@tg_router.message(CommandStart())
async def cmdStart(message: Message):
    service = container.user_service()
    await service.add_user(message.from_user.id)
    await message.answer("Вы можете сделать ставку или посмотреть ставки других участников", reply_markup=main_keyboard())

@tg_router.message(Command("yes"))
async def cmdYes(message: Message):
    user_service = container.user_service()
    if not user_service.is_admin(message.from_user.id):
        return
    bet_service = container.bet_service()
    await bet_service.set_last_bet_result(True)

    users_bet_service = container.user_guesses_service()
    winners, losers = await users_bet_service.get_last_bet_result()

    text = "Подведем итоги\nСегодня победителями оказались эти люди:\n"
    for winner in winners:
        user = await message.bot.get_chat(winner)
        text += f"@{user.username}\n"
    text += "Проигравшие:\n"
    for loser in losers:
        user = await message.bot.get_chat(loser)
        text += f"@{user.username}\n"
    text += 'Не расстраивайтесь, как-нибудь в следующий раз повезет.'

    for winner in winners:
        await message.bot.send_message(chat_id=winner, text=text)
    for loser in losers:
        await message.bot.send_message(chat_id=loser, text=text)


@tg_router.message(Command("no"))
async def cmdNo(message: Message):
    user_service = container.user_service()
    if not user_service.is_admin(message.from_user.id):
        return
    bet_service = container.bet_service()
    await bet_service.set_last_bet_result(False)

    users_bet_service = container.user_guesses_service()
    winners, losers = await users_bet_service.get_last_bet_result()

    text = "Подведем итоги\nСегодня победителями оказались эти люди:\n"
    for winner in winners:
        user = await message.bot.get_chat(winner)
        text += f"@{user.username}\n"
    text += "Проигравшие:\n"
    for loser in losers:
        user = await message.bot.get_chat(loser)
        text += f"@{user.username}\n"
    text += 'Не расстраивайтесь, как-нибудь в следующий раз повезет.'

    for winner in winners:
        await message.bot.send_message(chat_id=winner, text=text)
    for loser in losers:
        await message.bot.send_message(chat_id=loser, text=text)

@tg_router.message(F.text == "Сделать ставку за")
async def BetYes(message: Message):
    repo = container.user_guesses_service()
    await repo.do_bet(telegram_id=message.from_user.id, bet_value=1)
    await message.answer("Вы сделали ставку за")

@tg_router.message(F.text == "Сделать ставку против")
async def BetNo(message: Message):
    repo = container.user_guesses_service()
    await repo.do_bet(telegram_id=message.from_user.id, bet_value=0)
    await message.answer("Вы сделали ставку против")

@tg_router.message(F.text == "Вывести ставки")
async def print_bets(message: Message):
    service = container.user_guesses_service()
    bets = await service.get_bets_by_last_bet()

    text = "СТАВКИ\nПроголосовавшие за:\n"
    for bet in bets:
        if bet[1] == 1:
            user = await message.bot.get_chat(bet[0])
            text += f"@{user.username}\n"
    text+= "Проголосовавшие против:\n"
    for bet in bets:
        if bet[1] == 0:
            user = await message.bot.get_chat(bet[0])
            text += f"@{user.username}\n"
    await message.bot.send_message(chat_id=message.from_user.id, text=text)

@tg_router.message(F.text == "👤 Профиль")
async def print_bets(message: Message):
    """Отпечатать пользователю его профиль"""
    user_guesses_service = container.user_guesses_service()
    stat = await user_guesses_service.get_user_statistic(message.from_user.id)
    user = await message.bot.get_chat(message.from_user.id)

    text = "👤ВАШ ЛИЧНЫЙ ПРОФИЛЬ\n"
    text += f"- - -    @{user.username}    - - -\n"
    text += f"Количество правильных ставок: {stat}"
    await message.answer(text)
