import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from api_token import Bot_Token

bot = Bot(Bot_Token)  
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Hello users')

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply('/help - для допомоги \n/start - для старту повідомленнь')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  

if __name__ == '__main__':
    asyncio.run(main())



