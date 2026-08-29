import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
#                  BOT SETTINGS
# =========================================================

# BotFather token Render-এর Environment Variable থেকে আসবে
BOT_TOKEN = os.getenv("BOT_TOKEN")

# তোমার Telegram Channel username
# উদাহরণ: @yourchannel
CHANNEL_USERNAME = "@YOUR_CHANNEL"

# Channel link
CHANNEL_LINK = "https://t.me/YOUR_CHANNEL"

# Admin Telegram ID
# পরে নিজের Telegram ID বসাবে
ADMIN_ID = 123456789

# Admin contact username
ADMIN_USERNAME = "@YOUR_ADMIN"

# Update Group link
UPDATE_GROUP_LINK = "https://t.me/YOUR_GROUP"

# Setup Video link
SETUP_VIDEO_LINK = "https://t.me/YOUR_VIDEO"


# =========================================================
#                  PAYMENT SETTINGS
# =========================================================

BKASH_NUMBER = "01859551645"
NAGAD_NUMBER = "01859551645"

PAYMENT_ACCOUNT_TYPE = "Personal"


# =========================================================
#                  PANEL INFORMATION
# =========================================================
#
# এখানে পরে শুধু photo, price এবং details বসাবে।
#
# photo = Telegram-এর photo file_id
# price = Panel-এর দাম
# details = Panel সম্পর্কে বিস্তারিত
#
# এখন photo ফাঁকা রাখা হয়েছে।
# পরে bot-এ photo পাঠিয়ে file_id নিয়ে এখানে বসাতে পারবে.
#

PANELS = {
    1: {
        "name": "Panel 1",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 1 DETAILS HERE",
    },

    2: {
        "name": "Panel 2",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 2 DETAILS HERE",
    },

    3: {
        "name": "Panel 3",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 3 DETAILS HERE",
    },

    4: {
        "name": "Panel 4",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 4 DETAILS HERE",
    },

    5: {
        "name": "Panel 5",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 5 DETAILS HERE",
    },

    6: {
        "name": "Panel 6",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 6 DETAILS HERE",
    },

    7: {
        "name": "Panel 7",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 7 DETAILS HERE",
    },

    8: {
        "name": "Panel 8",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 8 DETAILS HERE",
    },

    9: {
        "name": "Panel 9",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 9 DETAILS HERE",
    },

    10: {
        "name": "Panel 10",
        "photo": "",
        "price": "PRICE HERE",
        "details": "PANEL 10 DETAILS HERE",
    },
}


# =========================================================
#                  LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
#                  START MESSAGE
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    welcome_text = f"""
👋 আসসালামু আলাইকুম {user.first_name}!

🔥 আমাদের Panel Store Bot-এ আপনাকে স্বাগতম।

📌 Bot ব্যবহার করার জন্য প্রথমে আমাদের Channel-এ Join করুন।

👇 Join করার পর Verify Join চাপুন।
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify Join",
                callback_data="verify_join"
            )
        ],
    ]

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  VERIFY CHANNEL JOIN
# =========================================================

async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ["member", "administrator", "creator"]:

            await query.edit_message_text(
                "✅ Verification Successful!\n\n"
                "🎉 আপনি আমাদের Channel-এ Join করেছেন।\n"
                "এখন নিচের Menu থেকে আপনার প্রয়োজনীয় option নির্বাচন করুন।"
            )

            await show_main_menu(query)

        else:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url=CHANNEL_LINK
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Verify Again",
                        callback_data="verify_join"
                    )
                ],
            ]

            await query.edit_message_text(
                "❌ আপনি এখনো আমাদের Channel-এ Join করেননি।\n\n"
                "আগে Channel-এ Join করুন, তারপর Verify করুন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception as e:

        logger.error(e)

        await query.edit_message_text(
            "⚠️ Verification করা যাচ্ছে না।\n\n"
            "Bot-কে Channel-এর Admin করে আবার চেষ্টা করুন।"
        )


# =========================================================
#                  MAIN MENU
# =========================================================

async def show_main_menu(query):

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Buy Panel",
                callback_data="buy_panel"
            ),
            InlineKeyboardButton(
                "👤 Admin Contact",
                callback_data="admin_contact"
            ),
        ],
        [
            InlineKeyboardButton(
                "📢 Update Group",
                url=UPDATE_GROUP_LINK
            ),
            InlineKeyboardButton(
                "🎥 Setup Video",
                url=SETUP_VIDEO_LINK
            ),
        ],
    ]

    await query.message.reply_text(
        "🏠 MAIN MENU\n\n"
        "নিচের Menu থেকে একটি Option নির্বাচন করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  BUY PANEL
# =========================================================

async def buy_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = []

    for panel_id, panel in PANELS.items():

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"🛒 {panel['name']}",
                    callback_data=f"panel_{panel_id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="main_menu"
            )
        ]
    )

    await query.edit_message_text(
        "🛒 AVAILABLE PANELS\n\n"
        "আপনার পছন্দের Panel নির্বাচন করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  SHOW PANEL DETAILS
# =========================================================

async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    panel_id = int(query.data.split("_")[1])

    panel = PANELS.get(panel_id)

    if not panel:
        await query.message.reply_text(
            "❌ Panel পাওয়া যায়নি।"
        )
        return

    text = f"""
🔥 {panel['name']}

💰 Price: {panel['price']}

📝 Details:
{panel['details']}
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Buy Now",
                callback_data=f"buy_{panel_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back to Panels",
                callback_data="buy_panel"
            )
        ],
    ]

    # যদি photo দেওয়া থাকে
    if panel["photo"]:

        try:

            await query.message.reply_photo(
                photo=panel["photo"],
                caption=text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except Exception:

            await query.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    else:

        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================================================
#                  BUY NOW
# =========================================================

async def buy_now(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    panel_id = int(query.data.split("_")[1])

    # User-এর selected panel memory-তে রাখছি
    context.user_data["selected_panel"] = panel_id

    keyboard = [
        [
            InlineKeyboardButton(
                "💳 bKash",
                callback_data="payment_bkash"
            ),
            InlineKeyboardButton(
                "💳 Nagad",
                callback_data="payment_nagad"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data=f"panel_{panel_id}"
            )
        ],
    ]

    await query.message.reply_text(
        "💳 PAYMENT METHOD\n\n"
        "আপনি কোন মাধ্যমে Payment করতে চান?\n\n"
        "👇 একটি নির্বাচন করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  BKASH PAYMENT
# =========================================================

async def payment_bkash(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await show_payment(
        query,
        "bKash",
        BKASH_NUMBER
    )


# =========================================================
#                  NAGAD PAYMENT
# =========================================================

async def payment_nagad(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await show_payment(
        query,
        "Nagad",
        NAGAD_NUMBER
    )


# =========================================================
#                  PAYMENT DETAILS
# =========================================================

async def show_payment(query, method, number):

    keyboard = [
        [
            InlineKeyboardButton(
                "✍️ Send TrxID",
                callback_data="send_trxid"
            )
        ]
    ]

    text = f"""
💳 {method} PAYMENT

📱 Number:
{number}

👤 Account Type:
{PAYMENT_ACCOUNT_TYPE}

━━━━━━━━━━━━━━

💰 উপরের Number-এ Payment করুন।

Payment করার পর নিচের
"Send TrxID" button-এ চাপ দিয়ে
আপনার Transaction ID পাঠান।

⚠️ সঠিক TrxID দিন।
"""

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  ASK FOR TRXID
# =========================================================

async def ask_trxid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    context.user_data["waiting_trxid"] = True

    await query.message.reply_text(
        "✍️ আপনার Payment-এর TrxID পাঠান।\n\n"
        "উদাহরণ:\n"
        "`ABC123XYZ456`",
        parse_mode="Markdown"
    )


# =========================================================
#                  RECEIVE TRXID
# =========================================================

async def receive_trxid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_trxid"):
        return

    trxid = update.message.text.strip()

    user = update.effective_user

    panel_id = context.user_data.get(
        "selected_panel",
        "Unknown"
    )

    admin_message = f"""
🔔 NEW PAYMENT REQUEST

👤 Name: {user.first_name}
🆔 User ID: {user.id}
🔗 Username: @{user.username if user.username else "N/A"}

🛒 Panel: {panel_id}

🧾 TrxID:
{trxid}
"""

    try:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message
        )

        await update.message.reply_text(
            "✅ TrxID successfully submitted!\n\n"
            "⏳ আপনার Payment এখন Admin যাচাই করবেন।\n"
            "Verification complete হলে আপনাকে জানানো হবে।"
        )

        context.user_data["waiting_trxid"] = False

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "⚠️ TrxID পাঠানো যাচ্ছে না।\n"
            "কিছুক্ষণ পর আবার চেষ্টা করুন।"
        )


# =========================================================
#                  ADMIN CONTACT
# =========================================================

async def admin_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 Contact Admin",
                url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="main_menu"
            )
        ],
    ]

    await query.message.reply_text(
        "👤 ADMIN CONTACT\n\n"
        "কোনো সমস্যা হলে Admin-এর সাথে যোগাযোগ করুন।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
#                  MAIN MENU CALLBACK
# =========================================================

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await show_main_menu(query)


# =========================================================
#                  CALLBACK HANDLER
# =========================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    data = query.data

    if data == "verify_join":
        await verify_join(update, context)

    elif data == "buy_panel":
        await buy_panel(update, context)

    elif data.startswith("panel_"):
        await show_panel(update, context)

    elif data.startswith("buy_"):
        await buy_now(update, context)

    elif data == "payment_bkash":
        await payment_bkash(update, context)

    elif data == "payment_nagad":
        await payment_nagad(update, context)

    elif data == "send_trxid":
        await ask_trxid(update, context)

    elif data == "admin_contact":
        await admin_contact(update, context)

    elif data == "main_menu":
        await main_menu(update, context)


# =========================================================
#                  ERROR HANDLER
# =========================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.error(
        "Exception while handling an update:",
        exc_info=context.error
    )


# =========================================================
#                  START BOT
# =========================================================

def main():

    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN environment variable is missing.")
        return

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_trxid
        )
    )

    application.add_error_handler(error_handler)

    print("🤖 Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
