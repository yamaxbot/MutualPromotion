from aiogram.filters import Command
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


@router.message(Command('start'))
async def command_start_handler(message: Message):
    await message.answer('🪄Это сервис Mutual_Promotion, где вы можете бесплатно получить подписки, лайки, коментарии, делая их другим\n\n🖍Когда вы подписываетесь, ставите лайки и коментарии другим, мы вам даём монеты, за которые в последующем, вы сможете покупать себе подписчиков, лайки и коментарии от реальных людей\n\n🪙1 Монета = 1 Услуга(1 подписчик, 1 лайк или 1комент)\n\n💎Свои первые 2 монеты, вы можете получить введя команду /point \n\n👨‍💻Правила вы можете прочитать введя команду /rules\n\n📈В последующем чтобы заработать монеты, вам нужно подписываться, ставить лайки, писать коментарии другим, нажав на кнопку "Заработать монеты"\n\n🛒Для того чтобы купить подписки, лайки, коментарии, нажмите кнопку "Купить услуги"\n\n🏦Чтобы посмотреть баланс монет, нажмите кнопку "Баланс"\n\n🫂Чтобы использовать реферальную систему, нажмите на кнопку "Реферальная система"\n\n🤵‍♂️Наш канал: @Mutual_Promotion_Channel', reply_markup=kb.client_reply_keyboards)
    clients_or_no = await sql.get_clients_sql(message.from_user.id)
    if clients_or_no == None:
        await sql.add_all_clients_sql(message.from_user.id)
        if len(str(message.text).split()) == 2:
            referal_id = str(message.text).split()[1]
            await sql.add_one_referal_sql(referal_id)
            await sql.add_two_points_sql(referal_id)


@router.message(F.text == '🏦Баланс')
async def get_points_handler(message: Message):
    points = await sql.get_clients_sql(message.from_user.id)
    await message.answer(text=f'Ваш баланс монет:\n{points[1]}💰')


@router.message(F.text == '🫂Реферальная система')
async def referal_system_handler(message: Message):
    quantity_ref = await sql.get_clients_sql(message.from_user.id)
    quantity_ref = quantity_ref[3]
    await message.answer(text=f'🤝Реферальная система:\n\n🏅За одного приглашённого человека мы даём 2 монеты\n\n❗️Прежде чем начинать приглашать рефералов, посмотрите правила введя команду /rules\n\n👀Ваша реферальная ссылка:\nhttps://t.me/Mutual_Promotion_Bot?start={message.from_user.id}\n\n🫂Количество рефералов: {quantity_ref}')


@router.message(F.text == '📈Заработать монеты')
async def earn_handler_one(message: Message, state: FSMContext):
    await state.clear()
    order = await sql.new_get_all_fast_orders_sql(message.from_user.id)
    if len(order) != 0:
        rand_order = random.choice(order)
        users = str(rand_order[3]).split('.')
        await sql.update_fast_orders_sql(int(rand_order[2])-1, rand_order[0])
        await sql.update_id_fast_orders_sql(rand_order[0], message.from_user.id)
        await message.answer(text=f'🔎Заказ: {rand_order[0]}\n\n👀Описание: {rand_order[1]}', reply_markup=kb.cancel_inline_keyboard)
        await state.set_state(earn_state.name)
        await state.update_data(name=(rand_order[0], message.from_user.id))
        await message.answer('📸Отправьте фото где отчётливо видно что вы выполнили задание.\n\n✅Если на фото не будет отчётливо видно что задание выполнено, модерация не одобрит ваше задание.\n\n❌Если не хотите выполнять задание, нажмите кнопку Отменить, которая находится чуть выше.')
        await state.set_state(earn_state.photo)
    else:
        await message.answer('🙅‍♂️Заказов пока что нет.\n\n🪙Если вы хотите получить бесплатную монету, введите команду /point')     


@router.message(F.text == '🛒Купить услуги')
async def buy_otzuv_handler_one(message: Message, state: FSMContext):
    points = await sql.get_clients_sql(message.from_user.id)
    await message.answer(text=f'💰Напишите количество услуг, которое хотите купить.\n\n🪙1 Монета = 1 Услуга(1 подписчик, 1 лайк или 1 коментарий)\n\n✅Если вы не ознакомлены с правилами, нажмите кнопку Отменить и прочитайте правила воспользуясь командой /rules\n\n🏦Баланс: {points[1]} монет', reply_markup=kb.cancel_two_inline_keyboard)
    await state.set_state(buy_otzuv_state.price)

@router.message(buy_otzuv_state.price)
async def buy_otzuv_handler_two(message: Message, state: FSMContext):
    if message.text.isdigit() == True:
        points = await sql.get_clients_sql(message.from_user.id)
        points = points[1]
        if int(points) >= int(message.text) and int(points) > 0 and int(message.text) > 0:
            await state.update_data(price=message.text)
            await state.set_state(buy_otzuv_state.des)
            await message.answer('📝Теперь введите полное описание того что нужно сделать одному человеку. И объязательно прикрепите ссылку.\n\n🌟Пример:\nНужно подписаться на канал @Mutual_Promotion_Channel\n\n🌗Если описание будет не полное, модерация отклонит ваш запрос. \n\n❌Если хотите отменить создание заказа, нажмите кнопку отменить.', reply_markup=kb.cancel_two_inline_keyboard)
        else: 
            await message.answer('⚠Произошла ошибка одно из нижеперечисленных:\n\n-У вас недостаточно монет\n\n-Вы некорректно ввели количество услуг')
            await state.clear()
    else:
        await message.answer('👻Вы некорректно ввели стоимость. Действие отменено.')
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


@router.message(Command('point'))
async def add_point_chanel(message: Message, state: FSMContext):
    await message.answer(text=f'💬Подпишитесь на канал и нажмите кнопку проверить.\n\n✅Если вы подписались мы вам выдадим 2 монеты.\n\n{CHANEL}', reply_markup=kb.check_inline_keyboard)


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


@router.message(Command('rules'))
async def rules_handler(message: Message):
    await message.answer('📜ПРАВИЛА:\n\n📜ПРИ ПОКУПКЕ УСЛУГ:\n❗️1 Давать полное описание заданию\n❗️2 Заказывать услугу одного вида за 1 раз(Иначе будут приходить одни и теже люди)\n❗️3 Рекламировать только в популярных приложениях и только каналы(группы)\n❗️4 Разрешить делать скриншот на своём канале\n\n📜ПРИ ВЫПОЛНЕНИЯ ЗАДАНИЯ:\n❗️1 Выполнять задание в точности и корректно отправлять доказательства\n❗️2 Следовать в точности по инструкциям\n\n📜РЕФЕРАЛЬНАЯ СИСТЕМА:\n❗️1 Рефералы должны быть активными.')


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

@router.message(F.text == '💫Купить монеты')
async def buy_point_stars_handler(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer(text=f'Сколько монет вы хотите купить?\n\n1 Монета = 1 Звезда\n\nВыберите из списка ниже', reply_markup=kb.quantity_buy_point_keyboard)
    else:
        await message.answer('Эта функция пока что не доступна, скоро появится.')

@router.callback_query(F.data == 'one_point_ik')
async def one_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='1 монета', 
                                          description='🪙За 1 монету вы сможете купить 1 услугу',
                                          payload='one_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=1)])
    
@router.callback_query(F.data == 'five_point_ik')
async def five_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='5 монет', 
                                          description='🪙За 5 монету вы сможете купить 5 услугу',
                                          payload='five_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=5)])


@router.callback_query(F.data == 'ten_point_ik')
async def ten_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='10 монет', 
                                          description='🪙За 10 монету вы сможете купить 10 услуг',
                                          payload='ten_point_payload',
                                          currency='XTR',
                                          prices=[LabeledPrice(label='XTR', amount=10)])

@router.callback_query(F.data == 'twentyfive_point_ik')
async def twentyfive_point_plus_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_invoice(title='25 монет', 
                                          description='🪙За 25 монету вы сможете купить 25 услугу',
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
        await sql.issue_points_sql(message.from_user.id, 1)
        await sql.add_donate_sql(message.from_user.id, '1', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'Успешно!\n\nМы начислили вам 1 монету, спасибо за покупку!\n\nЕсли есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'five_point_payload':
        await sql.issue_points_sql(message.from_user.id, 5)
        await sql.add_donate_sql(message.from_user.id, '5', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'Успешно!\n\nМы начислили вам 5 монет, спасибо за покупку!\n\nЕсли есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'ten_point_payload':
        await sql.issue_points_sql(message.from_user.id, 10)
        await sql.add_donate_sql(message.from_user.id, '10', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'Успешно!\n\nМы начислили вам 10 монет, спасибо за покупку!\n\nЕсли есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')

    if payload_stars == 'twentyfive_point_payload':
        await sql.issue_points_sql(message.from_user.id, 25)
        await sql.add_donate_sql(message.from_user.id, '25', str(message.successful_payment.telegram_payment_charge_id), date)
        await message.answer(text=f'Успешно!\n\nМы начислили вам 25 монет, спасибо за покупку!\n\nЕсли есть вопросы, пишите их боту: @Mutual_Promotion2_Bot')