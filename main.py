import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from api_token import Bot_Token
from TMDB_api import TMDB_api

bot = Bot(Bot_Token)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привіт! Напиши /film <назва>, і я знайду його для тебе 🎬')

@dp.message(Command('film'))
async def film_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Напиши назву фільму після команди. Приклад: /film Inception")
        return

    film_name = parts[1]
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_api}&query={film_name}&language=uk-UA'
    
    try:
        search_response = requests.get(search_url).json()
    except Exception as e:
        await message.answer(f"Помилка при з'єднанні з TMDB: {e}")
        return

    if search_response.get('results'):
        movie = search_response["results"][0]
        movie_id = movie["id"]
        title = movie.get('title','-')
        year = movie.get("release_date", "—")[:4]
        overview  = movie.get('overview','-')
        poster_path = movie.get('poster_path')

        # --- Додатковий запит для деталей і акторів ---
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_api}&language=uk-UA&append_to_response=credits'
        try:
            details = requests.get(details_url).json()
        except Exception as e:
            await message.answer(f"Помилка при отриманні деталей фільму: {e}")
            return

        rating = details.get("vote_average", "-")
        cast_list = details.get("credits", {}).get("cast", [])
        actors = ", ".join([actor["name"] for actor in cast_list[:5]]) if cast_list else "-"

        # --- Формування повідомлення ---
        caption = f"🎬 {title} ({year})\nРейтинг: {rating}/10\nАктори: {actors}\n\n{overview}"

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await message.answer_photo(poster_url, caption=caption)
        else:
            await message.answer(caption)
    else:
        await message.answer('Не знайшов такий фільм 😔')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  

if __name__ == '__main__':
    asyncio.run(main())
