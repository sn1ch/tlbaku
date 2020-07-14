from bot.handlers.main_handler import register_start_handlers
from bot.handlers.subcategory_handlers import register_subcategory_handlers
from bot.handlers.cart_handlers import register_cart_handlers
from bot.handlers.order_handlers import register_handlers_order
from bot.handlers.casino_handlers import register_handlers_casino
from bot.main import bot, dp



register_start_handlers(dp)
register_subcategory_handlers(dp)
register_cart_handlers(dp)
register_handlers_order(dp)
register_handlers_casino(dp)