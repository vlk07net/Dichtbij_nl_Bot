import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# SETTINGS
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

# Your own site — hardcoded so the link can't be silently changed.
SITE_URL = "https://findrent.nl/"

EMAIL = "hello@findrent.nl"

# Optional extras — fill in to show the buttons (empty = hidden).
INSTAGRAM_URL = ""
FACEBOOK_URL = ""

BRAND = "Findrent"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# PROPERTY TYPES
# key -> (title, desc, [points])
# ============================================
TYPES = {
    "apartments": (
        "🏢 Apartments",
        "Self-contained flats across the Netherlands, from studios to family sizes.",
        ["Furnished & unfurnished", "All budgets", "20+ cities"],
    ),
    "rooms": (
        "🚪 Rooms",
        "Private rooms in shared houses — the budget-friendly way to live in the city.",
        ["Shared facilities", "Great for singles", "Often near universities"],
    ),
    "studios": (
        "🛋 Studios",
        "Compact self-contained studios: your own kitchen and bathroom.",
        ["Independent living", "Central locations", "Ideal for one person"],
    ),
    "houses": (
        "🏠 Houses",
        "Whole houses for families or sharers who want more space.",
        ["More space & privacy", "Gardens in some", "Family friendly"],
    ),
    "student": (
        "🎓 Student housing",
        "Rooms and units aimed at students, close to campuses.",
        ["Near universities", "Budget options", "Short & long term"],
    ),
    "antikraak": (
        "🔑 Anti-squat (anti-kraak)",
        "Temporary, low-cost living in buildings awaiting a new use.",
        ["Low rent", "Flexible terms", "Temporary by nature"],
    ),
    "houseboats": (
        "⛵ Houseboats",
        "A characterful Dutch classic — living on the water.",
        ["Unique living", "Canal & waterside spots", "Limited availability"],
    ),
}

TYPE_ORDER = ["apartments", "rooms", "studios", "houses", "student", "antikraak", "houseboats"]

CITIES = [
    "Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven",
    "Groningen", "Tilburg", "Leiden", "Delft", "Maastricht",
]


# ============================================
# TEXTS
# ============================================
TEXT_START = (
    f"🏠 <b>{BRAND}</b>\n\n"
    "<i>One search across the major Dutch rental sites — rooms, studios, apartments "
    "and more, in 20+ cities.</i>\n\n"
    "The moment a matching listing goes live, you can be the first to know. "
    "Start your search on the website."
)

TEXT_BROWSE = (
    "🔎 <b>Browse by type</b>\n\n"
    "Pick what you're looking for. Full search, filters and listings are on the website."
)

TEXT_CITIES = (
    "📍 <b>Popular cities</b>\n\n"
    + " · ".join(CITIES)
    + "\n\nSearch any of 20+ Dutch cities on the website — set your city and filters there."
)

TEXT_HOW = (
    "⚙️ <b>How Findrent works</b>\n\n"
    "• <b>One search</b> — listings from major Dutch rental platforms in one place.\n"
    "• <b>Instant alerts</b> — an e-mail the moment a new match goes live.\n"
    "• <b>Smart filters</b> — AI-assisted grading to surface the best fits.\n"
    "• <b>Browse by city</b> — 20+ cities across the Netherlands.\n\n"
    "Speed matters in the Dutch rental market — being first to reply helps."
)

TEXT_GUIDES = (
    "📖 <b>Renting in the Netherlands — guides</b>\n\n"
    "• <b>Deposits</b> — what's normal and what to check.\n"
    "• <b>Contracts</b> — key terms before you sign.\n"
    "• <b>Avoiding scams</b> — red flags and safe practices.\n\n"
    "Never pay a deposit before viewing and signing a proper contract. "
    "Full guides are on the website."
)

TEXT_MENU = (
    "🗂 <b>Menu</b>\n\n"
    "• <b>Browse</b> rentals by type.\n"
    "• See <b>popular cities</b>.\n"
    "• Learn <b>how Findrent works</b>.\n"
    "• Read the <b>renting guides</b>.\n"
    "• FAQ and contact."
)

TEXT_FAQ = (
    "❓ <b>Frequently asked questions</b>\n\n"
    "<b>How do I search?</b>\n"
    "Tap “Search rentals” to open the website, set your city and filters, and browse "
    "live listings.\n\n"
    "<b>How do alerts work?</b>\n"
    "Save a search on the website and get an e-mail the instant a matching listing appears.\n\n"
    "<b>Does Findrent list the properties itself?</b>\n"
    "Findrent aggregates listings from major Dutch rental platforms so you can search them "
    "in one place.\n\n"
    "<b>How do I avoid scams?</b>\n"
    "Never pay before a viewing and a signed contract. See the guides for red flags."
)

TEXT_CONTACT = (
    "✏️ <b>Contact</b>\n\n"
    f"• E-mail: {EMAIL}\n"
    "• Website: findrent.nl\n\n"
    "Questions about your search or alerts? Drop us a line."
)

HIGHLIGHTS = "Good to know:"
SEARCH_NOTE = "Search and filters on the website."


# ============================================
# HELPERS
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def url_btn(text, url):
    return types.InlineKeyboardButton(text=text, url=url)


def site_btn():
    return types.InlineKeyboardButton(text="🌐 Website", web_app=types.WebAppInfo(url=SITE_URL))


def search_btn():
    return types.InlineKeyboardButton(
        text="🔎 Search rentals", web_app=types.WebAppInfo(url=SITE_URL)
    )


def ig_btn():
    return url_btn("📸 Instagram", INSTAGRAM_URL) if INSTAGRAM_URL else None


def fb_btn():
    return url_btn("📘 Facebook", FACEBOOK_URL) if FACEBOOK_URL else None


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [b for b in row if b is not None]
        if row:
            markup.row(*row)
    return markup


BTN_BROWSE = ("🔎 Browse rentals", "browse")
BTN_MENU = ("🗂 Menu", "menu")


# ============================================
# SCREEN / CARD BUILDERS
# ============================================
def type_text(key):
    title, desc, points = TYPES[key]
    lines = "\n".join(f"• {p}" for p in points)
    return f"<b>{title}</b>\n\n{desc}\n\n<b>{HIGHLIGHTS}</b>\n{lines}\n\n<i>{SEARCH_NOTE}</i>"


def type_rows(key):
    return [
        [search_btn()],
        [btn("‹ Back to types", "browse"), btn(*BTN_MENU)],
    ]


def screen(action):
    if action in ("home", "start"):
        return TEXT_START, [
            [btn(*BTN_BROWSE)],
            [search_btn()],
            [btn("⚙️ How it works", "how"), btn("📖 Guides", "guides")],
            [site_btn()],
            [ig_btn(), fb_btn()],
        ]
    if action == "browse":
        rows = [[btn(TYPES[k][0], f"type:{k}")] for k in TYPE_ORDER]
        rows.append([btn("📍 Cities", "cities")])
        rows.append([btn(*BTN_MENU)])
        return TEXT_BROWSE, rows
    if action == "cities":
        return TEXT_CITIES, [[search_btn()], [btn(*BTN_BROWSE), btn(*BTN_MENU)]]
    if action == "how":
        return TEXT_HOW, [[search_btn()], [btn(*BTN_BROWSE), btn(*BTN_MENU)]]
    if action == "guides":
        return TEXT_GUIDES, [[site_btn()], [btn(*BTN_BROWSE), btn(*BTN_MENU)]]
    if action == "menu":
        return TEXT_MENU, [
            [btn(*BTN_BROWSE)],
            [btn("⚙️ How it works", "how"), btn("📖 Guides", "guides")],
            [btn("❓ FAQ", "faq"), btn("✏️ Contact", "contact")],
            [site_btn()],
            [ig_btn(), fb_btn()],
        ]
    if action == "faq":
        return TEXT_FAQ, [[search_btn()], [btn(*BTN_BROWSE)], [btn(*BTN_MENU)]]
    if action == "contact":
        return TEXT_CONTACT, [[search_btn()], [ig_btn(), fb_btn()], [btn(*BTN_BROWSE), btn(*BTN_MENU)]]
    return None


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    text, rows = screen("home")
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


def render(call, text, rows):
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text, chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=markup,
        )
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("type:"))
def show_type(call):
    bot.answer_callback_query(call.id)
    key = call.data.split(":", 1)[1]
    if key in TYPES:
        render(call, type_text(key), type_rows(key))


@bot.callback_query_handler(func=lambda call: True)
def show_screen(call):
    bot.answer_callback_query(call.id)
    result = screen(call.data)
    if result:
        render(call, result[0], result[1])


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    try:
        bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(
                type="web_app",
                text="Search",
                web_app=types.WebAppInfo(url=SITE_URL),
            )
        )
    except ApiTelegramException:
        pass

    bot_identity = bot.get_me()
    logging.info("%s connected to Telegram as @%s", BRAND, bot_identity.username)
    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
