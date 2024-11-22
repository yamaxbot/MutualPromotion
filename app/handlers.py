from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import app.keyboards as kb
import app.database.sqlite_db as sql
from config import ADMINS, CHANEL
import random
import datetime
import string 

router = Router()

class issue_point_state(StatesGroup):
    des = State()

class buy_otzuv_state(StatesGroup):
    price = State()
    des = State()

class earn_state(StatesGroup):
    name = State()
    photo = State()

class newsletter_state(StatesGroup):
    msg = State()

class buy_promo_state(StatesGroup):
    points = State()
    quantity = State()

class use_promo_state(StatesGroup):
    name = State()


@router.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🪄Это сервис Mutual_Promotion, где вы можете бесплатно получить подписки, лайки и комментарии, подписываясь, ставя коментарии и лайки другим\n\n🖍Когда вы подписываетесь, ставите лайки и коментарии другим, мы вам даём монеты, за которые в последующем, вы сможете покупать себе подписчиков, лайки и коментарии от реальных людей\n\n🪙1 Монета = 1 Услуга(1 подписчик, 1 лайк или 1комент)\n\n💎Свои первые 2 монеты, вы можете получить введя команду /point \n\n📜Правила вы можете прочитать введя команду /rules\n\n💬Инструкцию как работать с ботом, вы можете узнать введя команду /help\n\n❓Если есть какие то вопросы пишите сюда: @Mutual_Promotion2_Bot\n\n🤵‍♂️Наш канал: @Mutual_Promotion_Channel', reply_markup=kb.client_reply_keyboards)
    clients_or_no = await sql.get_clients_sql(message.from_user.id)
    if clients_or_no == None:
        await sql.add_all_clients_sql(message.from_user.id)
        if len(str(message.text).split()) == 2:
            referal_id = str(message.text).split()[1]
            await sql.add_one_referal_sql(referal_id)
            await sql.add_two_points_sql(referal_id)


@router.message(F.text == 'На главную')
async def home_keyboard_handler(message: Message, state: FSMContext):
    await message.answer('Вы вернулись на главную', reply_markup=kb.client_reply_keyboards)
@router.message(Command('help'))
async def command_help_handler(message: Message):
    await message.answer('📈Чтобы заработать монеты, вам нужно подписываться, ставить лайки, писать коментарии другим, нажав на кнопку "Заработать монеты"\n\n🛒Для того чтобы купить подписки, лайки, коментарии, нажмите кнопку "Купить услуги"\n\n🏦Чтобы посмотреть баланс монет, нажмите кнопку "Баланс"\n\n🫂Чтобы использовать реферальную систему, нажмите на кнопку "Реферальная система"\n\n⭐️Также вы можете купить монеты за звезды в телеграм, нажав на кнопку "Купить монеты"', reply_markup=kb.client_reply_keyboards)


@router.message(F.text == '🏦Баланс')
async def get_points_handler(message: Message, state: FSMContext):
    await state.clear()
    points = await sql.get_clients_sql(message.from_user.id)
    await message.answer(text=f'Ваш баланс монет:\n{points[1]}💰')


@router.message(F.text == '🫂Реферальная система')
async def referal_system_handler(message: Message, state: FSMContext):
    await state.clear()
    quantity_ref = await sql.get_clients_sql(message.from_user.id)
    quantity_ref = quantity_ref[3]
    await message.answer(text=f'🤝Реферальная система:\n\n🏅За одного приглашённого человека мы даём 2 монеты\n\n❗️Прежде чем начинать приглашать рефералов, посмотрите правила введя команду /rules\n\n👀Ваша реферальная ссылка:\nhttps://t.me/Mutual_Promotion_Bot?start={message.from_user.id}\n\n🫂Количество рефералов: {quantity_ref}')


@router.message(F.text == '📈Заработать монеты')
async def earn_handler_one(message: Message, state: FSMContext):
    await state.clear()
    order = await sql.new_get_all_fast_orders_sql(message.from_user.id)
    if len(order) != 0:
        rand_order = order[-1]
        users = str(rand_order[3]).split('.')
        await sql.update_fast_orders_sql(int(rand_order[2])-1, rand_order[0])
        await sql.update_id_fast_orders_sql(rand_order[0], message.from_user.id)
        await message.answer(text=f'🔎Заказ: {rand_order[0]}\n\n👀Описание: {rand_order[1]}', reply_markup=kb.cancel_inline_keyboard)
        await state.set_state(earn_state.name)
        await state.update_data(name=(rand_order[0], message.from_user.id))
        await message.answer('📸Отправьте фото где отчётливо видно что вы выполнили задание.\n\n✅Если на фото не будет отчётливо видно что задание выполнено, модерация не одобрит ваше задание.\n\n❌Если не хотите выполнять задание, нажмите кнопку Отменить, которая находится чуть выше.')
        await state.set_state(earn_state.photo)
    else:
        await message.answer('🙅‍♂️Заказов пока что нет.\n\n🪙Если вы хотите получить бесплатную монету, введите команду /point\n\n⭐Если вам срочно нужны монеты, вы можете их купить нажав на кнопку\n"💫Купить услуги"')     


@router.message(F.text == '💫Купить монеты')
async def buy_point_stars_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'🤔Сколько монет вы хотите купить?\n\n🪙2 Монеты = ⭐1 Звезда\n\n‼️Учтите что в среднем в день 1 заказ делают 25 человек, но заказов делать можно много!', reply_markup=kb.quantity_buy_point_keyboard)
    
    
@router.message(Command('promo'))
async def promo_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Это система промокодов!\n\nСоздание промокода стоит 10 монет\n\nТакже нужно заплатить за промокод столько монет, сколько монет расчитано на промокод\n\n1 монета которая выдаётся в промокоде = 1 ваша монета\n\n1 человек может воспользоваться определённым промокодом только 1 раз\n\nЕсли хотите вернуться на главную, нажмите кнопку "На главную"', reply_markup=kb.promo_keyboard)


@router.message(F.text == 'Создать промокод')
async def buy_promo_one_handler(message: Message, state: FSMContext):
    money = await sql.get_clients_sql(message.from_user.id)
    await state.clear()
    if int(money[1]) > 10:
        await message.answer(text=f'Создание промокода стоит 10 монет, минимальное количество монет для создание промокода 11\n\nВаш баланс: {money[1]}, с которых мы автоматически спишем 10 монет за создание промокода, на создание промокода у вас есть {int(money[1])-10} монет\n\nВведите сколько монет будет выдаваться за 1 использование промокода')
        await state.set_state(buy_promo_state.points)
    else:
        await message.answer('У вас недостаточно монет, чтобы создать промокод требуется минимум 11 монет')
        await state.clear()

@router.message(buy_promo_state.points)
async def buy_promo_two_handler(message: Message, state: FSMContext):
    if str(message.text).isdigit() == True:
        money = await sql.get_clients_sql(message.from_user.id)
        if int(money[1])-10 >= int(message.text):
            await state.update_data(points=message.text)
            await message.answer(text=f'Теперь введите сколько активаций можт быть у промокода, имейте ввиду что для каждого промокода своё количество монет, которое вы указывали ранее.\n\nМаксимально вы можете сделать активаций: {(int(money[1])-10)//int(message.text)}')
            await state.set_state(buy_promo_state.quantity)
        else:
            await message.answer('У вас недостаточно монет. Действие отменено!')
            await state.clear()
    else:
        await message.answer('Вы ввели не число, действие отменено!')
        await state.clear()

        
@router.message(buy_promo_state.quantity)
async def buy_promo_tree_handler(message: Message, state: FSMContext):
    if str(message.text).isdigit() == True:
        money = await sql.get_clients_sql(message.from_user.id)
        await state.update_data(quantity=message.text)
        data = await state.get_data()
        if (int(money[1])-10)//int(message.text) >= int(data['quantity']):
            while True:
                promokode = [random.choice(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']) for i in range(8)]
                promokode = promokode[0]+promokode[1]+promokode[2]+promokode[3]+promokode[4]+promokode[5]+promokode[6]+promokode[7]
                promo = await sql.get_name_promo_sql(promokode)
                if promo == None:
                    break
            await message.answer(text=f'Промокод создан!\n\nЗа активацию промокод даёт: {data["points"]}\n\nКоличество активаций у промокода: {data["quantity"]}\n\nВаш промокод: {promokode}')
            await sql.add_promo_sql(message.from_user.id, promokode, data['quantity'], data['points'])
            await state.clear()
            await sql.minus_balance_sql(message.from_user.id, (int(data['points'])*int(data['quantity'])+10))
        else:
            await message.answer('У вас недостаточно монет, действие отменено!')
            await state.clear()
    else:
        await message.answer('Вы ввели не число, действие отменено!')
        await state.clear()


@router.message(F.text == 'Ввести промокод')
async def use_promo_one_handler(message: Message, state: FSMContext):
    await message.answer('Введите промокод без лишних символов')
    await state.set_state(use_promo_state.name)

@router.message(use_promo_state.name)
async def use_promo_two_handler(message: Message, state: FSMContext):
    all_promo = await sql.get_all_name_promo_sql()
    flag = False
    for promo in all_promo:
        use_user = str(promo[4]).split('.')
        if message.text == promo[1] and str(message.from_user.id) not in use_user:
            await sql.issue_points_sql(str(message.from_user.id), int(promo[3]))
            await sql.update_promo_sql(message.from_user.id, promo[1])
            await message.answer(text=f'Промокод успешно введён, вы получили {promo[3]}')
            await state.clear()
            flag = True
            break
    if flag == False:
        await message.answer('Промокода не существует или он уже неактивен')
        await state.clear()
    

@router.message(Command('rules'))
async def rules_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('📜ПРИ ПОКУПКЕ УСЛУГ:\n❗️1 Давать полное описание заданию\n❗️2 Заказывать услугу одного вида за 1 раз(Иначе будут приходить одни и теже люди)\n❗️3 Рекламировать только в популярных приложениях и только каналы(группы)\n❗️4 Разрешить делать скриншот на своём канале\n❗️5 Посмотреть может ли пользователь заходить к вам на канал\n\n📜ПРИ ВЫПОЛНЕНИЯ ЗАДАНИЯ:\n❗️1 Выполнять задание в точности и корректно отправлять доказательства\n❗️2 Следовать в точности по инструкциям\n❗️3 Если заказ не выполняет правила нажмите кнопку "Пожаловаться"\n\n📜РЕФЕРАЛЬНАЯ СИСТЕМА:\n❗️1 Рефералы должны быть активными.')

@router.message(Command('point'))
async def add_point_chanel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'💬Подпишитесь на канал и нажмите кнопку проверить.\n\n✅Если вы подписались мы вам выдадим 2 монеты.\n\n{CHANEL}', reply_markup=kb.check_inline_keyboard)

@router.message(F.text == '🛒Купить услуги')
async def buy_otzuv_handler_one(message: Message, state: FSMContext):
    await state.clear()
    points = await sql.get_clients_sql(message.from_user.id)
    await message.answer(text=f'💰Напишите количество услуг, которое хотите купить.\n\n🪙1 Монета = 1 Услуга(1 подписчик, 1 лайк или 1 коментарий)\n\n✅Если вы не ознакомлены с правилами, прочитайте правила воспользуясь командой /rules\n\n🏦Баланс: {points[1]} монет\n\n🧲Минимально можно купить 3 услуги')
    await state.set_state(buy_otzuv_state.price)

@router.message(buy_otzuv_state.price)
async def buy_otzuv_handler_two(message: Message, state: FSMContext):
    if message.text.isdigit() == True and int(message.text) >= 3:
        points = await sql.get_clients_sql(message.from_user.id)
        points = points[1]
        if int(points) >= int(message.text) and int(points) > 0 and int(message.text) > 0:
            await state.update_data(price=message.text)
            await state.set_state(buy_otzuv_state.des)
            await message.answer('📝Теперь введите полное описание того что нужно сделать одному человеку. И объязательно прикрепите ссылку.\n\n🌟Пример:\nНужно подписаться на канал @Mutual_Promotion_Channel\n\n🌗Если описание будет не полное, модерация отклонит ваш запрос. \n\n✅Если вы не ознакомлены с правилами, прочитайте правила воспользуясь командой /rules')
        else: 
            await message.answer('⚠Произошла ошибка одно из нижеперечисленных:\n\n-У вас недостаточно монет\n\n-Вы некорректно ввели количество услуг')
            await state.clear()
    else:
        await message.answer('👻Вы некорректно ввели стоимость, минимально можно купить 3 услуги. Действие отменено.')
        await state.clear()

@router.message(buy_otzuv_state.des)
async def buy_otzuv_handler_tree(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(des=message.text)
    data = await state.get_data()
    await state.clear()
    quality = await sql.get_number_sql()
    await sql.add_number_sql(int(quality[0][0]))
    await message.answer('🌟Ваше задание проверяется модерацией, ожидайте')
    chat_id = await sql.get_chats_sql()
    await sql.minus_balance_sql(message.from_user.id, data["price"])
    await bot.send_message(text=f"Приняте заказа:::{int(quality[0][0])+1}\n\n:::Описание:::{data['des']}\n\n:::Количество_услуг:::{data['price']}\n\n:::id_покупателя:::{message.from_user.id}", chat_id=chat_id[0], reply_markup=kb.buy_otzuv_moderation_)

@router.callback_query(F.data == 'approve')
async def approve_buy_otzuv_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await callback.message.edit_text(text=f'{callback.message.text}\nОдобрен')
    data_buy = str(callback.message.text).split(':::')
    for i in range(len(data_buy)):
        if '\n\n' in data_buy[i] and i != 3:
            data_buy[i] = data_buy[i].replace('\n\n', '')
    await sql.add_fast_orders_sql(data_buy[1], data_buy[3], data_buy[5], data_buy[-1])
    try:
        await bot.send_message(text=f'🌟Модерация приняла ваш заказ номер {data_buy[1]}, ожидайте выбранной услуги', chat_id=data_buy[7])
    except:
        pass

@router.callback_query(F.data == 'reject')
async def approve_buy_otzuv_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await callback.message.edit_text(text=f'{callback.message.text}\nОтклонён')
    data_buy = str(callback.message.text).split(':::')
    for i in range(len(data_buy)):
        if '\n\n' in data_buy[i] and i != 3:
            data_buy[i] = data_buy[i].replace('\n\n', '')
    await sql.return_points_sql(data_buy[-1], data_buy[5])
    try:
        await bot.send_message(text=f'👻Модерация откланила ваш заказ номер {data_buy[1]}, вы нарушили правила, попробуйте ещё раз прочитав правила введя команду /rules', chat_id=data_buy[7])
    except:
        pass

@router.message(earn_state.photo)
async def earn_handler_two(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        await message.answer('👻Как только модерация проверит всё ли правильно вы сделали, вам начислят баллы.')
        chat_id = await sql.get_chats_sql()
        data_state = await state.get_data()
        await state.clear()
        await bot.send_photo(photo=message.photo[-1].file_id, caption=f'Выдача заказа: {data_state["name"][0]}\n\nid_исполнителя: {data_state["name"][1]}', chat_id=chat_id[0], reply_markup=kb.pass_otzuv_moderation_keyboard)
    else:
        await message.answer('👻Это не фото, отправьте фото или нажмите кнопку "Отменить" в сообщении выше')

@router.callback_query(F.data == 'approve_pass')
async def approve_pass_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    data_text = callback.message.caption
    data = str(callback.message.caption).split()
    await sql.add_points_sql(data[-1])
    await sql.update_id_fast_orders_sql(data[2], data[-1])
    fast_order = await sql.activ_order_or_no_sql(str(data[2]))
    if fast_order != None:
        try:
            await bot.send_message(text=f'🌟Ваш заказ номер {fast_order[0]} успешно завершён!', chat_id=fast_order[4])
        except:
            pass
    await callback.message.edit_caption(caption=f'{data_text}\nОдобрен')
    try:
        await bot.send_message(text=f'🌟Вам зачислен бал за выполненный заказ номер {data[2]}', chat_id=data[-1])
    except:
        pass

@router.callback_query(F.data == 'reject_pass')
async def reject_pass_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    data_text = callback.message.caption
    data = str(callback.message.caption).split()
    await sql.get_fast_orders_number_sql(data[2])
    await callback.message.edit_caption(caption=f'{data_text}\nОтклонён')
    try:
        await bot.send_message(text=f'👻К сожаление не все условия были соблюдены когда выполняли заказ номер {data[2]}, попробуйте ещё раз прочитав правила /rules', chat_id=data[-1])
    except:
        pass

@router.message(Command('add_chat'))
async def add_chat1_handler(message: Message):
    if message.from_user.id in ADMINS:
        await sql.add_chats_sql(message.chat.id)
        await message.answer('Чат добавлен')

@router.message(Command('delete_chat'))
async def delete_chat1_handler(message: Message):
    if message.from_user.id in ADMINS:
        await sql.delete_chats_sql()
        await message.answer('Чаты удалены')

@router.callback_query(F.data == 'cancel')
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    number = str(callback.message.text).split()[1]
    await sql.get_fast_orders_number_sql(number)
    await callback.message.answer('👻Вы отменили задание')
    await callback.message.edit_text(text=callback.message.text)

@router.callback_query(F.data == 'сomplain')
async def сomplain_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.answer()
    number = str(callback.message.text).split()[1]
    await sql.get_fast_orders_number_sql(number)
    await callback.message.answer('👻Вы пожаловались на данный заказ, вы можете выполнять другие заказы!')
    await callback.message.edit_text(text=callback.message.text)
    chat_id = await sql.get_chats_sql()
    await bot.send_message(text=f'Жалоба от: {callback.from_user.id}\n\nЖалоба на заказ: {number}', chat_id=chat_id[0])

@router.message(Command('statistics'))
async def statistics_handler(message: Message):
    if message.from_user.id in ADMINS:
        clients = await sql.get_all_clients_sql()
        activ = await sql.active_orders_sql()
        order = await sql.get_number_sql()
        await message.answer(text=f'👻Статистика: \n\n🌟Количество клиентов за всё время: {len(clients)}\n\n🌪Всего заказов за всё время: {order[0][0]}\n\n🧲Количество активных заказов: {len(activ)}')

@router.message(Command('newsletter'))
async def newsletter_handler_one(message: Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer('Отправьте сообщение которое хотите разослать')
        await state.set_state(newsletter_state.msg)

@router.message(newsletter_state.msg)
async def newsletter_handler_two(message: Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        clients = await sql.get_all_clients_sql()
        await state.clear()
        total = 0
        for client in clients:
            try:
                await message.send_copy(chat_id=client[0])
            except:
                total = total + 1
                continue
        await message.answer(text=f'Сообщение разослано, {total} людей')

@router.callback_query(F.data == 'check')
async def check_chanel_handler(callback: CallbackQuery, bot: Bot):
    data = await sql.get_clients_sql(callback.from_user.id)
    await callback.answer()
    if data[2] == '0':
        member = await bot.get_chat_member(CHANEL, callback.from_user.id)
        if str(member.status) == 'ChatMemberStatus.MEMBER':
            await sql.add_two_points_sql(callback.from_user.id)
            await sql.subscription_update_sql(callback.from_user.id)
            await callback.message.answer('Уcпешно! Мы вам выдали баллы')
        else: 
            await callback.message.answer('Вы не подписались на канал, попробуйте ещё раз.')
    else:
        await callback.message.answer('Вы уже пользовались данной функцией. Она одноразовая.')

@router.callback_query(F.data == 'cancel_two')
async def two_cancel_state_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer('Вы отменили действие')
    await callback.message.edit_text(text=callback.message.text)

@router.message(Command('issue'))
async def issue_point_one_handler(message: Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.set_state(issue_point_state.des)
        await message.answer('Введите описание')

@router.message(issue_point_state.des)
async def issue_point_two_handler(message: Message, bot: Bot, state: FSMContext):
    data = str(message.text).split('/')
    await state.clear()
    try:
        await sql.issue_points_sql(data[0], data[1])
        await bot.send_message(text=data[2], chat_id=data[0])
        await message.answer('Успешно!')
    except:
        await message.answer('Ошибка!')

@router.callback_query(F.data == 'one_point_ik')
async def one_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='2 монеты', 
                                          description='🪙За 2 монеты вы сможете купить 2 услуги',
                                          payload='one_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=1)])
    
@router.callback_query(F.data == 'five_point_ik')
async def five_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='10 монет', 
                                          description='🪙За 10 монет вы сможете купить 10 услуг',
                                          payload='five_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=5)])

@router.callback_query(F.data == 'ten_point_ik')
async def ten_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='20 монет', 
                                          description='🪙За 20 монет вы сможете купить 20 услуг',
                                          payload='ten_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=10)])

@router.callback_query(F.data == 'twentyfive_point_ik')
async def twentyfive_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='50 монет', 
                                          description='🪙За 50 монет вы сможете купить 50 услуг',
                                          payload='twentyfive_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=25)])

@router.pre_checkout_query()
async def pre_checkout_handler(pcq: PreCheckoutQuery):
    await pcq.answer(ok=True)

@router.message(F.successful_payment)
async def procces_successful_payment_one_handler(message: Message):
    payload_stars = str(message.successful_payment.invoice_payload)
    date = str(datetime.datetime.now())
    
    if payload_stars == 'one_point_payload':
        await sql.issue_points_sql(message.from_user.id, 2)
        await sql.add_donate_sql(message.from_user.id, '2', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'✅Успешно!\n\n👥Мы начислили вам 2 монеты, спасибо за покупку!\n\n🙋‍♂️Если есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'five_point_payload':
        await sql.issue_points_sql(message.from_user.id, 10)
        await sql.add_donate_sql(message.from_user.id, '10', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'✅Успешно!\n\n👥Мы начислили вам 10 монет, спасибо за покупку!\n\n🙋‍♂️Если есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'ten_point_payload':
        await sql.issue_points_sql(message.from_user.id, 20)
        await sql.add_donate_sql(message.from_user.id, '20', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'✅Успешно!\n\n👥Мы начислили вам 20 монет, спасибо за покупку!\n\n🙋‍♂️Если есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'twentyfive_point_payload':
        await sql.issue_points_sql(message.from_user.id, 50)
        await sql.add_donate_sql(message.from_user.id, '50', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'✅Успешно!\n\n👥Мы начислили вам 50 монет, спасибо за покупку!\n\n🙋‍♂️Если есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

@router.message(Command('refund'))
async def refound_command_handler(message: Message, bot: Bot, command: CommandObject):
    if message.from_user.id in ADMINS:
        transaction_id = command.args
        user_id = await sql.get_id_donates_sql(transaction_id)
        try:
            await bot.refund_star_payment(user_id=user_id[0], telegram_payment_charge_id=transaction_id)
            await sql.update_return_stars_sql(transaction_id)
            await message.answer('Успешно!')
        except:
            await message.answer(text=f'Что то пошло не так!')


@router.message(Command('user'))
async def command_user_handler(message: Message):
    if message.from_user.id in ADMINS:
        user_id = str(message.text).split()[1]
        data = await sql.get_clients_sql(str(user_id))
        await message.answer(text=f'id: {data[0]}\npoints: {data[1]}\nsubscription: {data[2]}\nreferals: {data[3]}')

@router.message(Command('user_donates'))
async def user_donates_command_handler(message: Message):
    if message.from_user.id in ADMINS:
        user_id = str(message.text).split()[1]
        data = await sql.get_user_donates_sql(str(user_id))
        if data != None:
            await message.answer(text=str(data))
        else:
            await message.answer('Данный пользователь не покупал донат')


@router.message(Command('delete_order'))
async def delete_orders_command_handler(message: Message):
    if message.from_user.id in ADMINS:
        number = str(message.text).split()[1]
        try:
            await sql.delete_order_sql(str(number))
            await message.answer('Успешно')
        except:
            await message.answer('Что то пошло не так')


@router.message(Command('minus_point'))
async def minus_point_command_admin_handler(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.id in ADMINS:
        data = str(message.text).split('.')
        try:
            await sql.minus_admin_command_points_sql(data[1], data[2])
            await bot.send_message(text=data[3], chat_id=data[1])
            await message.answer('Успешно!')
        except:
            await message.answer('Ошибка!')


@router.message(Command('message_user'))
async def command_message_user(message: Message, bot: Bot):
    if message.from_user.id in ADMINS:
        data = str(message.text).split('%')
        try:
            await bot.send_message(text=str(data[2]), chat_id=data[1])
            await message.answer('Успешно!')
        except:
            await message.answer('Ошибка!')


@router.message(Command('everyone'))
async def everyone_point_handler(message: Message):
    if message.from_user.id in ADMINS:
        data = str(message.text).split('.')
        try:
            await sql.everyone_point_sql(data[1])
            await message.answer(text='Успешно!')
        except:
            await message.answer(text='Ошибка!')