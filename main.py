from typing import Final
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os
load_dotenv()


TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = '@Digita_Mart_bot'

PRODUCTS = [
    {"id": 1, "name": "E-book: Python Basics", "price": "$5"},
    {"id": 2, "name": "Web Dev Guide", "price": "$10"},
    {"id": 3, "name": "UI Icons Pack", "price": "$3"},
]

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🛍  Products     ", callback_data="products"),
            InlineKeyboardButton("🛒  Buy         ", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("ℹ️  Help        ", callback_data="help"),
            InlineKeyboardButton("📞  Contact     ", callback_data="contact"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to *DigitalMart Bot*!\n\n"
        "🛒 Browse and purchase digital products easily.\n\n"
        "Choose an option below ⬇️",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 *DigitalMart Bot Commands:*\n\n"
        "/start - Start using DigitalMart Bot\n"
        "/products - Browse available digital products\n"
        "/buy - Purchase a product\n"
        "/contact - Contact support\n"
    )

#Buy and Products Commands
async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"product_{p['id']}")]
        for p in PRODUCTS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🛒 Choose a product to buy:",
        reply_markup=reply_markup
    )

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"product_{p['id']}")]
        for p in PRODUCTS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📦 Here are our products:",
        reply_markup=reply_markup
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "This is a custom command"
    )

#Handle button presses

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    #Pruducts
    if query.data == "products":
        keyboard = [
            [InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"product_{p['id']}")]
            for p in PRODUCTS
        ]
        keyboard.append([InlineKeyboardButton("⬅ Back to Menu", callback_data="back_to_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        

        await query.edit_message_text(
        "📦 Here are our products:",
        reply_markup=reply_markup
        )

    elif query.data.startswith("product_"):
        product_id = int(query.data.split("_")[1])
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)

        if product:
            await query.edit_message_text(
                f"🛍 *{product['name']}*\n💰 Price: {product['price']}\n\nClick Buy to purchase.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Buy Now", callback_data=f"buy_{product['id']}")],
                    [InlineKeyboardButton("⬅ Back to Products", callback_data="products")]
                ])
            )
    elif query.data == "buy":
        keyboard = [
            [InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"product_{p['id']}")]
            for p in PRODUCTS
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🛒 Choose a product to buy:",
            reply_markup=reply_markup
        )

    elif query.data.startswith("buy_"):
        product_id = int(query.data.split("_")[1])
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)

        if product:
           
            await query.edit_message_text(
                f"✅ You selected to buy *{product['name']}* for {product['price']}.\n\n"
                "We’ll contact you soon for payment.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅ Back to Menu", callback_data="back_to_menu")]
                ])
            )


    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ Help: Use the menu to browse products or contact support.",
            reply_markup=query.message.reply_markup
        )


    elif query.data == "contact":
        await query.message.reply_text(
            "📞 Contact us at support@digitalmart.com",
            reply_markup=query.message.reply_markup
        )

    elif query.data == "back_to_menu":
        keyboard = [
            [
                InlineKeyboardButton("🛍  Products     ", callback_data="products"),
                InlineKeyboardButton("🛒  Buy         ", callback_data="buy"),
            ],
            [
                InlineKeyboardButton("ℹ️  Help        ", callback_data="help"),
                InlineKeyboardButton("📞  Contact     ", callback_data="contact"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "👋 Welcome to *DigitalMart Bot*!\n\n"
            "🛒 Browse and purchase digital products easily.\n\n"
            "Choose an option below ⬇️",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


# HandleResponses

def handele_response(text: str) -> str:
    processed_text = text.lower().strip()

    if "hello" in processed_text or "hi" in processed_text:
        return "Hello! How can I assist you today?"

    elif "bye" in processed_text or "goodbye" in processed_text:
        return "Goodbye! Have a great day!"

    elif "help" in processed_text:
        return "Sure! You can ask about our products, orders, or anything else related to DigitalMart."

    elif "products" in processed_text:
        return "Here are some of our popular products:\n1. E-books\n2. Software licenses\n3. Online courses\n4. Digital art\n5. Music tracks"

    elif "buy" in processed_text:
        return "To purchase a product, please provide the product name or ID. Or use /cart to view your cart."

    elif "contact" in processed_text:
        return "You can contact our support team at support@digitalmart.com"

    else:
        return "I'm not sure how to respond to that. Can you please rephrase?"
    

# To concact to the bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if text.startswith(BOT_USERNAME):
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handele_response(new_text)
        else:
            return
    else:
        response: str = handele_response(text)

    print(f'Bot response: "{response}"')
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    

if __name__ == '__main__':
    print("Starting DigitalMart Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('buy', buy_command))
    app.add_handler(CommandHandler('products', products_command))
    

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CallbackQueryHandler(button_handler))

    # Error Handler
    app.add_error_handler(error)

    print("Polling started...")
    app.run_polling(poll_interval=3)