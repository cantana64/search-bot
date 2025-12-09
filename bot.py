from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import httpx

# ←←←← СЮДА ВСТАВЬ СВОЙ ТОКЕН ОТ BOTFATHER ←←←←
TOKEN = 7820961160:AAEGlXIVkDjLHIUWmfsO9adP02Xe3y7zzPw

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message()
async def search(message: types.Message):
    query = message.text.strip()
    if len(query) < 2:
        await message.answer("Напиши подлиннее запрос 😊")
        return
    
    await message.answer(f"🔍 Ищу: {query}...")

    url = "https://ddg-api.sean.taipei/api/v1/search"
    params = {"query": query, "max_results": 6}
    
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, params=params)
            results = r.json()
    except:
        await message.answer("Ошибка интернета, попробуй чуть позже")
        return

    if not results:
        await message.answer("Ничего не нашёл 😔")
        return

    for item in results[:5]:
        title = item['title']
        snippet = item['body']
        link = item['href']

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Открыть ссылку", url=link))

        text = f"*{title}*\n\n{snippet}"
        await message.answer(text, parse_mode="Markdown", reply_markup=kb, disable_web_page_preview=True)
        await asyncio.sleep(0.6)  # чтобы Telegram не ругался

if __name__ == '__main__':
    print("Бот запущен и ищет информацию 24/7!")
    executor.start_polling(dp, skip_updates=True)
