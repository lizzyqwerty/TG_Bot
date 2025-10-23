import telebot
from telebot import types
import random
from datetime import datetime, timedelta
import time


bot = telebot.TeleBot('8496322496:AAESLPl4Glz1BdTEVn5tkRIB7glfwP36BTE')

# Базы данных
USER_DATA = {}
USER_BOOKS = {}
BOOK_REVIEWS = {}


# Коллекция отрывков из книг
BOOK_EXCERPTS = [
    {
        "text": "Все счастливые семьи похожи друг на друга, каждая несчастливая семья несчастлива по-своему.",
        "author": "Лев Толстой",
        "book": "Анна Каренина",
        "genre": "Классика"
    },
    {
        "text": "Человек он умный, но чтобы умно поступать — одного ума мало.",
        "author": "Фёдор Достоевский",
        "book": "Преступление и наказание",
        "genre": "Классика"
    },
    {
        "text": "Никогда не сдавайтесь, никогда, никогда, никогда, никогда — ни в великом, ни в малом, ни в большом, ни в маленьком.",
        "author": "Уинстон Черчилль",
        "book": "",
        "genre": "История"
    },
    {
        "text": "Я мыслю, следовательно, я существую.",
        "author": "Рене Декарт",
        "book": "Рассуждение о методе",
        "genre": "Философия"
    },
    {
        "text": "Быть или не быть — вот в чем вопрос.",
        "author": "Уильям Шекспир",
        "book": "Гамлет",
        "genre": "Драма"
    }
]

# Рекомендации книг по жанрам
BOOK_RECOMMENDATIONS = {
    "Фантастика": [
        {"title": "1984", "author": "Джордж Оруэлл", "description": "Антиутопия о тоталитарном обществе"},
        {"title": "451° по Фаренгейту", "author": "Рэй Брэдбери", "description": "Мир, где книги под запретом"},
        {"title": "Солярис", "author": "Станислав Лем", "description": "Философская фантастика о контакте с разумным океаном"}
    ],
    "Фэнтези": [
        {"title": "Властелин Колец", "author": "Дж.Р.Р. Толкин", "description": "Эпическая сага о Средиземье"},
        {"title": "Гарри Поттер", "author": "Дж.К. Роулинг", "description": "Приключения юного волшебника"},
        {"title": "Ведьмак", "author": "Анджей Сапковский", "description": "Приключения Геральта из Ривии"}
    ],
    "Классика": [
        {"title": "Война и мир", "author": "Лев Толстой", "description": "Эпопея о войне 1812 года"},
        {"title": "Преступление и наказание", "author": "Ф.М. Достоевский", "description": "Психологический роман о преступлении и раскаянии"},
        {"title": "Мастер и Маргарита", "author": "М.А. Булгаков", "description": "Мистическая сатира о добре и зле"}
    ],
    "Детектив": [
        {"title": "Убийство в Восточном экспрессе", "author": "Агата Кристи", "description": "Знаменитый детектив Эркюля Пуаро"},
        {"title": "Шерлок Холмс", "author": "Артур Конан Дойл", "description": "Приключения гениального сыщика"},
        {"title": "Десять негритят", "author": "Агата Кристи", "description": "Классический детектив-изоляция"}
    ]
}
def get_user_data(user_id):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {
            'reading_streak': 0,
            'last_reading_date': None,
            'daily_excerpt_received': False,
            'reminder_time': None,
            'books_read': 0
        }
    return USER_DATA[user_id]


def get_user_books(user_id):
    return USER_BOOKS.setdefault(user_id, [])

def get_book_reviews(book_title):
    return BOOK_REVIEWS.setdefault(book_title, [])


def get_daily_excerpt(user_id):
    #✅ Проверяет, получал ли пользователь отрывок сегодня

#📅 Обновляет серию чтения (streak)

#🎯 Выбирает случайный отрывок

#🔄 Обновляет данные пользователя

    user_data = get_user_data(user_id)
    today = datetime.now().date()

    # Проверка на повторное получение
    if user_data['last_reading_date'] == today and user_data['daily_excerpt_received']:
        return None

    # Обновление серии чтения
    last_date = user_data['last_reading_date']
    if last_date:
        if today == last_date + timedelta(days=1):
            user_data['reading_streak'] += 1
        elif today > last_date + timedelta(days=1):
            user_data['reading_streak'] = 1
    else:
        user_data['reading_streak'] = 1

    # Обновление данных и возврат отрывка
    user_data.update({
        'last_reading_date': today,
        'daily_excerpt_received': True
    })

    return random.choice(BOOK_EXCERPTS)

def create_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        ["📖 Ежедневный отрывок", "📚 Рекомендации"],
        ["📊 Мои книги", "⭐ Обзоры"],
        ["⏰ Напоминания", "ℹ️ Помощь"]
    ]
    for row in buttons:
        keyboard.row(*row)
    return keyboard

def create_genre_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for genre in BOOK_RECOMMENDATIONS.keys():
        keyboard.add(types.InlineKeyboardButton(genre, callback_data=f"genre_{genre}"))
    return keyboard

def create_reminder_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    times = ["09:00", "12:00", "18:00", "20:00", "21:00", "22:00"]
    for i in range(0, len(times), 2):
        if i + 1 < len(times):
            keyboard.row(
                types.InlineKeyboardButton(times[i], callback_data=f"remind_{times[i]}"),
                types.InlineKeyboardButton(times[i+1], callback_data=f"remind_{times[i+1]}")
            )
        else:
            keyboard.row(types.InlineKeyboardButton(times[i], callback_data=f"remind_{times[i]}"))
    keyboard.row(types.InlineKeyboardButton("Выключить", callback_data="remind_off"))
    return keyboard


def reminder_worker():
    """Отправляет напоминания в нужное время"""
    while True:
        current_time = datetime.now().strftime("%H:%M")

        # Проверяем только тех, у кого есть напоминания
        for user_id, user_data in USER_DATA.items():
            if should_send_reminder(user_data, current_time):
                send_reminder(user_id)

        time.sleep(60)


def should_send_reminder(user_data, current_time):
    """Проверяет, нужно ли отправлять напоминание"""
    return (user_data.get('reminder_time') == current_time and
            not user_data.get('daily_excerpt_received', False))


def send_reminder(user_id):
    """Отправляет напоминание одному пользователю"""
    try:
        bot.send_message(user_id, "⏰ Время почитать! 📖")
    except:
        pass


@bot.message_handler(commands=['start'])
def start(message):
    user_data = get_user_data(message.from_user.id)

    welcome_text = f"""
📚 Привет, {message.from_user.first_name}!

Я - бот для чтения с полным функционалом:

✅ *Ежедневные отрывки из книг* - новая цитата каждый день
✅ *Рекомендации книг* - подборки по жанрам  
✅ *Отслеживание прочитанного* - твоя библиотека
✅ *Обзоры и рецензии* - делиться мнением о книгах
✅ *Напоминания о чтении* - не пропусти день

Выбери действие в меню ниже 👇
    """

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=create_main_menu()
    )


@bot.message_handler(func=lambda message: message.text == "📖 Ежедневный отрывок")
def daily_excerpt(message):
    user_id = message.from_user.id

    # Получаем отрывок
    excerpt = get_daily_excerpt(user_id)
    if not excerpt:
        bot.send_message(message.chat.id, "📖 Уже получал сегодня! Завтра новая цитата! 🌟")
        return

    # Формируем сообщение
    author_line = f"— *{excerpt['author']}*"
    if excerpt['book']:
        author_line += f", \"{excerpt['book']}\""

    streak = get_user_data(user_id)['reading_streak']

    response = f"""📖 *Ежедневный отрывок:*

"{excerpt['text']}"

{author_line}

🏷️ *Жанр:* {excerpt['genre']}
🔥 *Серия чтения:* {streak} дней подряд!"""

    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == "📚 Рекомендации")
def recommendations(message):
    bot.send_message(message.chat.id, "🎯 Выбери жанр:", reply_markup=create_genre_keyboard())


@bot.message_handler(func=lambda message: message.text == "📊 Мои книги")
def my_books(message):
    user_id = message.from_user.id
    books = get_user_books(user_id)

    if not books:
        text = """📚 *Твоя библиотека пуста*

Добавь первую книгу:
`/addbook Название - Автор`
Пример: `/addbook 1984 - Джордж Оруэлл`"""
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        return

    # Формируем список книг
    books_list = "\n".join([
        f"{i}. *{b['title']}* - {b['author']}" +
        (f"\n   💫 {b['review']}" if b.get('review') else "")
        for i, b in enumerate(books[:5], 1)
    ])

    user_data = get_user_data(user_id)
    text = f"""📚 *Твоя библиотека:*

{books_list}

📊 Всего: *{user_data['books_read']}* книг
🔥 Серия: *{user_data['reading_streak']}* дней"""

    if len(books) > 5:
        text += f"\n\n... и еще {len(books) - 5} книг"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == "⭐ Обзоры")
def reviews(message):
    text = """⭐ *Обзоры и рецензии*

Посмотреть отзывы:
`/reviews Название книги`

Оставить отзыв:
`/addbook Название - Автор`
`/review Название - Твой отзыв`"""

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == "⏰ Напоминания")
def reminders(message):
    user_data = get_user_data(message.from_user.id)
    time = user_data.get('reminder_time', 'не установлено')

    bot.send_message(
        message.chat.id,
        f"⏰ Напоминание: *{time}*\n\nВыбери время:",
        parse_mode='Markdown',
        reply_markup=create_reminder_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "ℹ️ Помощь")
def help_command(message):
    text = """📚 *Помощь*

*Меню:*
📖 Ежедневный отрывок
📚 Рекомендации по жанрам  
📊 Мои книги
⭐ Обзоры и рецензии
⏰ Напоминания

*Команды:*
`/addbook Название - Автор`
`/review Название - Отзыв`
`/reviews Название`
`/start`"""

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['addbook'])
def add_book_command(message):
    """Добавляет книгу в библиотеку пользователя"""
    try:
        # Извлекаем название и автора
        parts = message.text.replace('/addbook', '').strip().split(' - ', 1)
        if len(parts) != 2:
            raise ValueError

        title, author = parts[0].strip(), parts[1].strip()
        user_id, user_books = message.from_user.id, get_user_books(message.from_user.id)

        # Проверяем дубликаты
        if any(book['title'].lower() == title.lower() for book in user_books):
            bot.send_message(message.chat.id, f"📚 Книга \"{title}\" уже есть!")
            return

        # Добавляем книгу
        user_books.append({
            'title': title,
            'author': author,
            'added_date': datetime.now().strftime("%d.%m.%Y"),
            'review': None
        })
        get_user_data(user_id)['books_read'] += 1

        bot.send_message(
            message.chat.id,
            f"✅ *{title}* - {author}\n\nТеперь оставь отзыв:\n`/review {title} - твой отзыв`",
            parse_mode='Markdown'
        )

    except:
        bot.send_message(
            message.chat.id,
            "❌ Используй: /addbook Название - Автор\nПример: `/addbook 1984 - Джордж Оруэлл`",
            parse_mode='Markdown'
        )


@bot.message_handler(commands=['review'])
def add_review_command(message):
    """Добавляет отзыв к книге в библиотеке пользователя"""
    try:
        parts = message.text.replace('/review', '').strip().split(' - ', 1)
        if len(parts) != 2:
            raise ValueError

        title, review_text = parts[0].strip(), parts[1].strip()
        user_id, user_books = message.from_user.id, get_user_books(message.from_user.id)

        # Ищем книгу для отзыва
        for book in user_books:
            if book['title'].lower() == title.lower():
                book['review'] = review_text
                # Добавляем в общие отзывы
                get_book_reviews(title).append({
                    'user': message.from_user.first_name,
                    'review': review_text,
                    'date': datetime.now().strftime("%d.%m.%Y")
                })

                bot.send_message(message.chat.id, f"⭐ *{title}*\n💫 {review_text}", parse_mode='Markdown')
                return

        bot.send_message(
            message.chat.id,
            f"❌ Сначала добавь книгу:\n`/addbook {title} - Автор`",
            parse_mode='Markdown'
        )

    except:
        bot.send_message(
            message.chat.id,
            "❌ Используй: /review Название - Отзыв\nПример: `/review 1984 - Отличная книга!`",
            parse_mode='Markdown'
        )


@bot.message_handler(commands=['reviews'])
def show_reviews_command(message):
    """Показывает все отзывы на указанную книгу"""
    title = message.text.replace('/reviews', '').strip()
    if not title:
        bot.send_message(message.chat.id, "❌ Укажи название: /reviews Название")
        return

    reviews = get_book_reviews(title)
    if not reviews:
        bot.send_message(message.chat.id, f"📖 На \"{title}\" пока нет отзывов")
        return

    # Формируем список отзывов
    reviews_list = "\n".join([
        f"{i}. *{r['user']}* ({r['date']}):\n   {r['review']}"
        for i, r in enumerate(reviews[:5], 1)
    ])

    text = f"⭐ *Отзывы на \"{title}\":*\n\n{reviews_list}"
    if len(reviews) > 5:
        text += f"\n\n... и еще {len(reviews) - 5} отзывов"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    """Обрабатывает нажатия инлайн-кнопок"""
    user_id = call.from_user.id

    if call.data.startswith("genre_"):
        # Показываем книги выбранного жанра
        genre = call.data.replace("genre_", "")
        books = BOOK_RECOMMENDATIONS.get(genre, [])

        if not books:
            bot.send_message(call.message.chat.id, f"❌ В жанре '{genre}' пока нет рекомендаций")
            return

        books_list = "\n".join([f"• *{b['title']}* - {b['author']}\n  {b['description']}" for b in books])
        text = f"📚 *{genre}:*\n\n{books_list}\n\n💡 Добавь: `/addbook Название - Автор`"
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data.startswith("remind_"):
        # Устанавливает или выключает напоминания
        user_data = get_user_data(user_id)

        if call.data == "remind_off":
            user_data['reminder_time'] = None
            bot.send_message(call.message.chat.id, "🔕 Напоминания выключены")
        else:
            time_str = call.data.replace("remind_", "")
            user_data['reminder_time'] = time_str
            bot.send_message(call.message.chat.id, f"🔔 Напоминание: *{time_str}*", parse_mode='Markdown')


if __name__ == "__main__":
    print("📚 Бот запущен!")
    bot.polling(none_stop=True)
