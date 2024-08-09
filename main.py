import asyncio
import logging
import os
import sys
from datetime import datetime, date

from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, BotCommand, URLInputFile, KeyboardButton, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv
from redis.asyncio import Redis
from redis_dict import RedisDict

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')

redis = Redis()
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)
database = RedisDict("kvartira")


def grade_buttons(amount):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text='🤢', callback_data='dislike'),
        InlineKeyboardButton(text=f'{amount}/8', callback_data=' '),
        InlineKeyboardButton(text='☺', callback_data='like')
    )
    ikb.add(InlineKeyboardButton(text='Baholashni yakunlash', callback_data='finish_grade'))
    return ikb.adjust(3, 1)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(html.bold(
        f"Assalomu aleykum Varahmatullohi Vabarakotuhu bu bot xonadonimizda kimning navbatchilik qilishini eslatadi"),
        parse_mode=ParseMode.HTML)


# participants = ['@isa_zxc', '@muhammad6220', '@TDTU_40', '@Jaska_ITishnik', '@A1ko_Xursh1d_04', '@ufayzimatov', '@SherMuhammadR']
# photos = [
#     "https://telegra.ph/file/83670a9bc6ff094a75a2b.jpg",
#     "https://telegra.ph/file/b35496066871c9bb370a0.png",
#     "https://telegra.ph/file/04133303daac3d60b8a05.png",
#     "https://telegra.ph/file/c99ed608d31016b686bf3.jpg",
#     "https://telegra.ph/file/542c38f12d284b4e407ed.png",
#     "https://telegra.ph/file/408e8f016ef5604eafe10.jpg",
#     "https://telegra.ph/file/ab7d1d05ddcbd35540ab8.jpg"
# ]
#
# for i in range(len(photos)):
#     database[participants[i]] = photos[i]
# database.clear()
participants = database.keys()


@dp.message(Command('ishim_bor'))
async def ishim_bor_handler(message: Message, bot: Bot):
    if '@' + str(message.from_user.username) in database['kvartira']:
        for participant in participants:
            if participant[1:] == message.from_user.username:
                participants.remove("@" + message.from_user.username)
        await message.answer(text=f"Bajarishi mumkin bo'lgan nomzodlar : {participants}")
    else:
        await message.answer(text='Kechirasiz siz bu kvartirada yashamaysiz🤨!')


# @dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

@dp.message(Command('navbatchi'))
async def group_handler(message: Message, state: FSMContext):
    if '@' + str(message.from_user.username) in participants:
        today = date.today().day
        photo = ''
        navbatchi = ''
        if today % 7 == 1:
            await state.set_data({"navbatchi_ismi": 'Ismat aka'})
            photo = database.values()[4]
            navbatchi = '''
Name: Ismat aka
Username: @isa_zxc
                        '''
        elif today % 7 == 2:
            await state.set_data({"navbatchi_ismi": 'Muhammad aka'})
            photo = database.values()[6]
            navbatchi = '''
Name: Muhammad aka
Username: @muhammad6220
                        '''
        elif today % 7 == 3:
            await state.set_data({"navbatchi_ismi": 'Muslim aka'})
            photo = database.values()[5]
            navbatchi = '''
Name: Muslimbek aka
Username: @TDTU_40
                        '''
        elif today % 7 == 4:
            await state.set_data({"navbatchi_ismi": 'Jasurbek'})
            photo = database.values()[2]
            navbatchi = '''
Name: Jasurbek
Username: @Jaska_ITishnik
                        '''
        elif today % 7 == 5:
            await state.set_data({"navbatchi_ismi": 'Xurshid'})
            photo = database.values()[1]
            navbatchi = '''
Name: Xurshid
Username: @A1ko_Xursh1d_04
                        '''
        elif today % 7 == 6:
            await state.set_data({"navbatchi_ismi": 'Umidjon'})
            photo = database.values()[0]
            navbatchi = '''
Name: Umidjon
Username: @ufayzimatovUmidjon
                        '''
        elif today % 7 == 0:
            await state.set_data({"navbatchi_ismi": 'SherMuhammad'})
            photo = database.values()[3]
            navbatchi = '''
Name: SherMuhammad
Username: @SherMuhammadR
                        '''
        rkb = ReplyKeyboardBuilder()
        rkb.add(
            KeyboardButton(text='👏 Navbatchini baholash'),
            KeyboardButton(text='📈 Vazifalari'),
            KeyboardButton(text='😎Ish yakunlandi')
        )
        img = URLInputFile(url=photo)
        await message.answer_photo(photo=img, caption=f"""
        😊Assalomu aleykum
        Bugun {today} - {date.today().strftime('%B')}
        Soat: {(str(datetime.time(datetime.now()))).split('.')[0]}
        Navbatchi : {navbatchi}
                                """, reply_markup=rkb.as_markup(resize_keyboard=True))
    else:
        await message.answer(text='Kechirasiz siz bu kvartirada yashamaysiz🤨!')


@dp.message(F.text == '😎Ish yakunlandi')
async def complited_handler(message: Message):
    if 19 < int((str(datetime.time(datetime.now()))).split('.')[0][:2]) < 23:
        await message.answer(text=f"Tugallangan vaqt : {(str(datetime.time(datetime.now()))).split('.')[0]}")
    else:
        await message.answer(text='Hali juda erta hamma ishni qilganingizga ishonchingiz komilmi?🤔')


#  await state.set_data({"pos" : 1})
#     data = await state.get_data()
#     pos = data.get('pos')
#
# data = await state.get_data()
# pos = data.get("pos") + 1
# await state.set_data({"pos": pos})

@dp.message(F.text == '👏 Navbatchini baholash')
async def mark_handler(message: Message, state: FSMContext):
    await state.set_data({"amount": 0})
    data = await state.get_data()
    amount = data.get('amount')
    await message.answer(text='Navbatchiga baho bering', reply_markup=grade_buttons(amount).as_markup())


@dp.callback_query(F.data == "like")
async def like_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('amount') < 8:
        amount = data.get('amount') + 1
        await state.set_data({'amount': amount})
        await callback.message.edit_reply_markup(reply_markup=grade_buttons(amount).as_markup())
    else:
        await callback.answer(text="O'zi 8 kishi yashasak nimasi bu qo'shimcha ovoz 🤔")


@dp.callback_query(F.data == "dislike")
async def dislike_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('amount') > 0:
        amount = data.get('amount') - 1
        await state.set_data({'amount': amount})
        await callback.message.edit_reply_markup(reply_markup=grade_buttons(amount).as_markup())
    else:
        await callback.answer(text="Pastga urib tashhlayapsizeeee bolani 🤔")


@dp.message(F.text == "📈 Vazifalari")
async def task_handler(message: Message):
    await message.answer(text="""
Navbatchining qatiy bajarishi kerak bo'lgan vazifalari!
🍞 Non olib kelish
🥙 Ovqat qilish
⌛ 24 soat ishida hamma 🍽 lar toza bo'lishi
🧻 Musorlarni to'kish 
    """)


@dp.callback_query(F.data == 'finish_grade')
async def finish_grade_handletr(callback: CallbackQuery, state: FSMContext):
    grade = await state.get_data()
    if grade.get('amount') > 5:
        await callback.message.answer(text=f"Ofarin👏  -> 🧮 {grade.get('amount')} bal to'pladingiz!")
        await state.clear()
    else:
        await callback.message.answer(text='Uyat yarim odamdan kamroq ovoz yig\'ilgan keyingi safar yaxshiroq qiling😣!')
        await state.clear()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    command = [
        BotCommand(command='ishim_bor', description="Agar sizning navbatingiz bo'lsa va ishingiz bo'lsa bosing!"),
        BotCommand(command='navbatchi', description="Kim navbatchiligini aniqlash")
    ]

    await bot.set_my_commands(command)


async def main() -> None:
    bot = Bot(token=TOKEN)
    # dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
