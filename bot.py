import hashlib
import random
import time
import telebot
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = "8849316294:AAFe1CaQwY3EmdpCDG9_dDQGg5eiWT746To"
ADMIN_ID = 8390198126
CARD_NUMBER = "2204 3206 5735 0775"

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_flask).start()

products = []
orders = {}
order_counter = [0]
user_cart = {}

def add_products():
    products.clear()
    products.append({"id": 1, "name": "Мефедрон Кристалл 1г", "price": 2500, "description": "Чистый кристалл, быстрый клад", "city": "Каменногорск"})
    products.append({"id": 2, "name": "Амфетамин Сульфат 1г", "price": 2000, "description": "Сухой порошок, зип-лок", "city": "Каменногорск"})
    products.append({"id": 3, "name": "Шишки Амнезия 1г", "price": 1200, "description": "Плотные шишки, аромат цитруса", "city": "Каменногорск"})
    products.append({"id": 4, "name": "Гашиш Марокко 1г", "price": 1500, "description": "Мягкий, ароматный, спрессован", "city": "Каменногорск"})
    products.append({"id": 5, "name": "Экстази Синие 1шт", "price": 1800, "description": "Яркая таблетка, ровная дозировка", "city": "Каменногорск"})
    products.append({"id": 6, "name": "Мефедрон Кристалл 1г", "price": 3000, "description": "Чистый кристалл, клад в центре", "city": "Выборг"})
    products.append({"id": 7, "name": "Амфетамин Сульфат 1г", "price": 2200, "description": "Сухой порошок, зип-лок", "city": "Выборг"})
    products.append({"id": 8, "name": "Шишки Лимонный Дизель 1г", "price": 1300, "description": "Плотные шишки, аромат лимона", "city": "Выборг"})
    products.append({"id": 9, "name": "Гашиш Марокко 1г", "price": 1600, "description": "Мягкий, ароматный, спрессован", "city": "Выборг"})
    products.append({"id": 10, "name": "МДМА Кристалл 1г", "price": 3500, "description": "Чистый кристалл, клад в городе", "city": "Выборг"})

add_products()

def generate_dead_drop(city, product_name):
    random.seed(time.time())
    places = {
        "Каменногорск": [
            (60.95412, 29.13045),
            (60.95867, 29.14218),
            (60.96123, 29.11876),
            (60.95678, 29.15234),
            (60.95289, 29.12567),
            (60.94987, 29.13892),
            (60.95345, 29.14521),
            (60.95789, 29.12834),
            (60.96012, 29.15678),
            (60.95123, 29.11456),
            (60.95567, 29.16234),
            (60.94876, 29.13245),
            (60.95934, 29.14892),
            (60.94789, 29.11987),
            (60.96245, 29.13567),
            (60.95012, 29.15923),
            (60.95678, 29.11234),
            (60.95389, 29.16845),
            (60.94567, 29.12678),
            (60.95812, 29.14356)
        ],
        "Выборг": [
            (60.71045, 28.74123),
            (60.71389, 28.75234),
            (60.70876, 28.73567),
            (60.71567, 28.72891),
            (60.70654, 28.74812),
            (60.71234, 28.75923),
            (60.70987, 28.72145),
            (60.71678, 28.74456),
            (60.70456, 28.73123),
            (60.71892, 28.73789),
            (60.70789, 28.76234),
            (60.71423, 28.71876),
            (60.71156, 28.75512),
            (60.70567, 28.74289),
            (60.71934, 28.72645),
            (60.70812, 28.76834),
            (60.71689, 28.73345),
            (60.70234, 28.74987),
            (60.71345, 28.72456),
            (60.71789, 28.75892)
        ]
    }
    city_places = places.get(city, [(55.0, 37.0)])
    lat, lon = random.choice(city_places)
    photo_id = hashlib.md5(f"{city}{lat}{lon}{product_name}".encode()).hexdigest()[:8]
    return f"📍 Город: {city}\n🗺 Координаты: {lat:.5f}, {lon:.5f}\n🔑 Фото ID: {photo_id}"

@bot.message_handler(commands=['start'])
def start(message):
    text = """🔥 ДОБРО ПОЖАЛОВАТЬ 🔥

Ты попал в закрытый магазин. Работаем быстро, чётко и без лишних слов.

📦 ЧТО ЕСТЬ:
Товары для Каменногорска и Выборга. Всё свежее, всё проверенное.

⚡️ КАК КУПИТЬ:
1. Жми «🛍 Товары»
2. Выбирай позицию
3. Напиши количество
4. Переводи оплату на карту
5. Жми «✅ Я оплатил»
6. Жди подтверждения оплаты
7. Получай координаты

🔑 ФОТО ID:
Это код на упаковке клада. Приходишь по координатам, находишь товар, сверяешь код. Совпал — забираешь. Не совпал — не трогай.

❗️ ПРАВИЛА:
— Никому не передавай координаты
— Не пиши лишнего в чат
— Не спорь с ботом
— Оплатил — жми кнопку

Всё. Работаем.
"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🛍 Товары"))
    markup.add(types.KeyboardButton("📦 Мои заказы"))
    markup.add(types.KeyboardButton("ℹ️ Помощь"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🛍 Товары")
def show_products(message):
    if not products:
        bot.send_message(message.chat.id, "Товаров пока нет.")
        return
    markup = types.InlineKeyboardMarkup()
    for p in products:
        markup.add(types.InlineKeyboardButton(f"{p['name']} - {p['price']} RUB ({p['city']})", callback_data=f"product_{p['id']}"))
    bot.send_message(message.chat.id, "Выбери товар:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def product_detail(call):
    product_id = int(call.data.split("_")[1])
    p = next((x for x in products if x["id"] == product_id), None)
    if not p:
        bot.answer_callback_query(call.id, "Товар не найден")
        return
    user_cart[call.message.chat.id] = p["id"]
    text = f"📦 {p['name']}\n\n📝 {p['description']}\n\n📍 Город: {p['city']}\n💰 Цена: {p['price']} RUB\n\n✏️ Напиши количество в граммах или штуках:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: message.chat.id in user_cart and message.text.isdigit())
def choose_amount(message):
    product_id = user_cart.pop(message.chat.id)
    amount = int(message.text)
    p = next((x for x in products if x["id"] == product_id), None)
    if not p:
        bot.send_message(message.chat.id, "Товар не найден")
        return
    order_counter[0] += 1
    order_id = order_counter[0]
    total = p["price"] * amount
    buyer = message.from_user.username or str(message.from_user.id)
    orders[order_id] = {
        "id": order_id,
        "product": p,
        "amount": amount,
        "buyer": buyer,
        "chat_id": message.chat.id,
        "status": "pending"
    }
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"paid_{order_id}"))
    bot.send_message(message.chat.id, f"🧾 Заказ #{order_id}\n\n📦 Товар: {p['name']}\n🔢 Количество: {amount}\n💰 Сумма: {total} RUB\n\n💳 Переведи на карту:\n{CARD_NUMBER}\n\nПосле перевода нажми кнопку.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("paid_"))
def paid_product(call):
    order_id = int(call.data.split("_")[1])
    order = orders.get(order_id)
    if not order:
        bot.answer_callback_query(call.id, "Заказ не найден")
        return
    if order["status"] == "paid":
        bot.answer_callback_query(call.id, "Уже оплачен")
        return
    order["status"] = "checking"
    bot.send_message(call.message.chat.id, "⏳ Мы получили твою заявку. Ожидай подтверждения оплаты.")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{order_id}"))
    markup.add(types.InlineKeyboardButton("❌ Отклонить", callback_data=f"decline_{order_id}"))
    total = order["product"]["price"] * order["amount"]
    bot.send_message(ADMIN_ID, f"🔔 Новый заказ #{order_id}\n\nПокупатель: @{order['buyer']}\nТовар: {order['product']['name']}\nКоличество: {order['amount']}\nСумма: {total} RUB\n\nПроверь оплату.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def confirm_order(call):
    order_id = int(call.data.split("_")[1])
    order = orders.get(order_id)
    if not order:
        bot.answer_callback_query(call.id, "Заказ не найден")
        return
    drop = generate_dead_drop(order["product"]["city"], order["product"]["name"])
    order["status"] = "paid"
    order["drop"] = drop
    bot.send_message(order["chat_id"], f"✅ Оплата подтверждена.\n\n{drop}\n\n🔑 Сверь Фото ID на упаковке. Совпал — забирай.")
    bot.answer_callback_query(call.id, "Подтверждено")

@bot.callback_query_handler(func=lambda call: call.data.startswith("decline_"))
def decline_order(call):
    order_id = int(call.data.split("_")[1])
    order = orders.get(order_id)
    if not order:
        bot.answer_callback_query(call.id, "Заказ не найден")
        return
    order["status"] = "declined"
    bot.send_message(order["chat_id"], "❌ Оплата не подтверждена. Заказ отклонён.")
    bot.answer_callback_query(call.id, "Отклонено")

@bot.message_handler(func=lambda message: message.text == "📦 Мои заказы")
def my_orders(message):
    buyer = message.from_user.username or str(message.from_user.id)
    user_orders = [o for o in orders.values() if o["buyer"] == buyer]
    if not user_orders:
        bot.send_message(message.chat.id, "У тебя нет заказов.")
        return
    text = "📦 Твои заказы:\n\n"
    for o in user_orders:
        if o["status"] == "paid":
            status = "✅ Оплачен"
        elif o["status"] == "checking":
            status = "⏳ Проверяется"
        elif o["status"] == "declined":
            status = "❌ Отклонён"
        else:
            status = "⏳ Не оплачен"
        text += f"#{o['id']} - {status}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "ℹ️ Помощь")
def help(message):
    text = """ℹ️ Помощь

1. Жми «🛍 Товары»
2. Выбирай позицию
3. Напиши количество
4. Переводи оплату на карту
5. Жми «✅ Я оплатил»
6. Жди подтверждения
7. Получай координаты и Фото ID
8. Иди по координатам
9. Найди клад
10. Сверь Фото ID
11. Забери товар

Если что-то пошло не так — жми /start и начни заново.
"""
    bot.send_message(message.chat.id, text)

print("Бот запущен")
bot.polling()
