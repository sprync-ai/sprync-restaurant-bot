"""Core chat engine with conversation state management."""
import re
from datetime import datetime
from app.models.schemas import (
    ConversationState,
    ChatMessage,
    BookingRequest,
)
from app.services.booking import BookingService
from app.services.menu import MenuService


class ChatEngine:
    """Core conversation state machine for restaurant booking chatbot."""

    def __init__(self):
        """Initialize chat engine with services."""
        self.booking_service = BookingService()
        self.menu_service = MenuService()
        self.sessions: dict[str, dict] = {}

    def process_message(
        self,
        session_id: str,
        user_message: str,
        conversation_history: list[ChatMessage],
    ) -> tuple[str, ConversationState, list[str], bool, str | None]:
        """Process user message and return bot response.

        Args:
            session_id: Unique session identifier.
            user_message: User's message.
            conversation_history: Previous messages in conversation.

        Returns:
            Tuple of (bot_message, state, quick_replies, is_confirmed, booking_ref).
        """
        # Initialize session if new
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "state": ConversationState.GREETING,
                "booking_data": {},
                "message_count": 0,
            }

        session = self.sessions[session_id]
        current_state = session["state"]

        # Process based on state
        if current_state == ConversationState.GREETING:
            return self._handle_greeting(session, user_message)

        elif current_state == ConversationState.MENU_INQUIRY:
            return self._handle_menu_inquiry(session, user_message)

        elif current_state == ConversationState.BOOKING_START:
            return self._handle_booking_start(session, user_message)

        elif current_state == ConversationState.COLLECT_NAME:
            return self._handle_collect_name(session, user_message)

        elif current_state == ConversationState.COLLECT_PARTY_SIZE:
            return self._handle_collect_party_size(session, user_message)

        elif current_state == ConversationState.COLLECT_DATE:
            return self._handle_collect_date(session, user_message)

        elif current_state == ConversationState.COLLECT_TIME:
            return self._handle_collect_time(session, user_message)

        elif current_state == ConversationState.COLLECT_SPECIAL_REQUESTS:
            return self._handle_collect_special_requests(session, user_message)

        elif current_state == ConversationState.BOOKING_CONFIRMATION:
            return self._handle_booking_confirmation(session, user_message)

        else:
            return "How can I help you today?", ConversationState.GREETING, [], False, None

    def _handle_greeting(self, session: dict, user_message: str) -> tuple:
        """Handle greeting state."""
        session["state"] = ConversationState.BOOKING_START
        bot_message = (
            "🍽️ Welcome to The Golden Plate! I'm your booking assistant.\n\n"
            "How can I help you today?"
        )
        quick_replies = ["Book a Table", "View Menu", "Contact Info"]
        return bot_message, ConversationState.BOOKING_START, quick_replies, False, None

    def _handle_booking_start(self, session: dict, user_message: str) -> tuple:
        """Handle booking start state."""
        message_lower = user_message.lower()

        if any(word in message_lower for word in ["menu", "what do you serve", "food", "drinks"]):
            session["state"] = ConversationState.MENU_INQUIRY
            categories = self.menu_service.get_categories()
            category_list = ", ".join(categories)
            bot_message = (
                f"📋 Our menu includes:\n{category_list}\n\n"
                "What would you like to know about?"
            )
            return bot_message, ConversationState.MENU_INQUIRY, categories, False, None

        elif any(word in message_lower for word in ["book", "reservation", "table", "booking"]):
            session["state"] = ConversationState.COLLECT_NAME
            bot_message = "Great! Let's get you a table. What's your name?"
            return bot_message, ConversationState.COLLECT_NAME, [], False, None

        elif any(word in message_lower for word in ["contact", "phone", "address", "hours", "opening"]):
            bot_message = (
                "📞 The Golden Plate\n"
                "📍 123 Brick Lane, London E1 6PU\n"
                "📱 +44 20 1234 5678\n"
                "⏰ Open Daily: 11:00 AM - 11:00 PM\n\n"
                "Can I help you with a booking?"
            )
            return bot_message, ConversationState.BOOKING_START, ["Book a Table", "View Menu"], False, None

        else:
            bot_message = (
                "I can help you with:\n"
                "🗓️ Booking a table\n"
                "📋 Viewing our menu\n"
                "📞 Contact information\n\n"
                "What would you like?"
            )
            return bot_message, ConversationState.BOOKING_START, ["Book a Table", "View Menu", "Contact Info"], False, None

    def _handle_menu_inquiry(self, session: dict, user_message: str) -> tuple:
        """Handle menu inquiry state."""
        message_lower = user_message.lower()

        # Search by category or keyword
        if any(word in message_lower for word in ["starter", "appetizer", "starters"]):
            items = self.menu_service.get_items_by_category("Starters")
        elif any(word in message_lower for word in ["main", "mains", "curry", "chicken", "fish", "lamb"]):
            items = self.menu_service.get_items_by_category("Mains")
        elif any(word in message_lower for word in ["side", "rice", "bread", "naan", "chips"]):
            items = self.menu_service.get_items_by_category("Sides")
        elif any(word in message_lower for word in ["dessert", "sweet", "pudding"]):
            items = self.menu_service.get_items_by_category("Desserts")
        elif any(word in message_lower for word in ["vegetarian", "vegan", "v", "vg"]):
            items = self.menu_service.get_vegetarian_items()
        elif any(word in message_lower for word in ["gluten", "gf"]):
            items = self.menu_service.get_gluten_free_items()
        else:
            items = self.menu_service.search_items(user_message)

        if not items:
            items = self.menu_service.get_all_items()[:5]
            bot_message = "Here are some of our popular dishes:\n\n"
        else:
            bot_message = "Here are the items:\n\n"

        for item in items[:5]:
            tags = ""
            if item.dietary_tags:
                tags = f" [{', '.join(item.dietary_tags)}]"
            bot_message += f"🍲 {item.name}{tags}\n   {item.description}\n   £{item.price:.2f}\n\n"

        bot_message += "Would you like to book a table?"
        session["state"] = ConversationState.BOOKING_START
        return bot_message, ConversationState.BOOKING_START, ["Book a Table"], False, None

    def _handle_collect_name(self, session: dict, user_message: str) -> tuple:
        """Handle name collection."""
        name = user_message.strip()

        if len(name) < 2:
            return "Please enter a valid name.", ConversationState.COLLECT_NAME, [], False, None

        session["booking_data"]["name"] = name
        session["state"] = ConversationState.COLLECT_PARTY_SIZE

        bot_message = f"Nice to meet you, {name}! How many people will be dining with us?"
        return bot_message, ConversationState.COLLECT_PARTY_SIZE, ["2", "4", "6", "8"], False, None

    def _handle_collect_party_size(self, session: dict, user_message: str) -> tuple:
        """Handle party size collection."""
        try:
            party_size = int(user_message.strip())
            if party_size < 1 or party_size > 20:
                return "Please enter a number between 1 and 20.", ConversationState.COLLECT_PARTY_SIZE, [], False, None
        except ValueError:
            return "Please enter a valid number.", ConversationState.COLLECT_PARTY_SIZE, [], False, None

        session["booking_data"]["party_size"] = party_size
        session["state"] = ConversationState.COLLECT_DATE

        bot_message = f"Perfect! {party_size} guests. What date would you like? (YYYY-MM-DD)"
        return bot_message, ConversationState.COLLECT_DATE, [], False, None

    def _handle_collect_date(self, session: dict, user_message: str) -> tuple:
        """Handle date collection."""
        date_str = user_message.strip()

        try:
            self.booking_service._validate_booking_date(date_str)
        except ValueError as e:
            return f"❌ {str(e)}", ConversationState.COLLECT_DATE, [], False, None

        session["booking_data"]["booking_date"] = date_str
        session["state"] = ConversationState.COLLECT_TIME

        bot_message = f"Great! {date_str} it is. What time would you prefer? (HH:MM, 11:00 - 23:00)"
        return bot_message, ConversationState.COLLECT_TIME, ["19:00", "19:30", "20:00", "20:30"], False, None

    def _handle_collect_time(self, session: dict, user_message: str) -> tuple:
        """Handle time collection."""
        time_str = user_message.strip()

        try:
            self.booking_service._validate_booking_time(time_str)
        except ValueError as e:
            return f"❌ {str(e)}", ConversationState.COLLECT_TIME, [], False, None

        session["booking_data"]["booking_time"] = time_str
        session["state"] = ConversationState.COLLECT_SPECIAL_REQUESTS

        bot_message = (
            "Perfect! Any special requests? (e.g., window table, celebration, dietary notes)\n"
            "Or just say 'None' if you don't have any."
        )
        return bot_message, ConversationState.COLLECT_SPECIAL_REQUESTS, ["None"], False, None

    def _handle_collect_special_requests(self, session: dict, user_message: str) -> tuple:
        """Handle special requests collection."""
        special_requests = user_message.strip()

        if special_requests.lower() == "none":
            special_requests = ""

        session["booking_data"]["special_requests"] = special_requests
        session["state"] = ConversationState.BOOKING_CONFIRMATION

        booking_data = session["booking_data"]
        bot_message = (
            "📋 Please confirm your booking:\n\n"
            f"👤 Name: {booking_data['name']}\n"
            f"👥 Party Size: {booking_data['party_size']}\n"
            f"📅 Date: {booking_data['booking_date']}\n"
            f"🕐 Time: {booking_data['booking_time']}\n"
        )

        if special_requests:
            bot_message += f"📝 Special Requests: {special_requests}\n"

        bot_message += "\nIs everything correct?"

        return bot_message, ConversationState.BOOKING_CONFIRMATION, ["Confirm", "Cancel"], False, None

    def _handle_booking_confirmation(self, session: dict, user_message: str) -> tuple:
        """Handle booking confirmation."""
        message_lower = user_message.lower()

        if any(word in message_lower for word in ["confirm", "yes", "correct", "ok"]):
            booking_data = session["booking_data"]

            try:
                booking_request = BookingRequest(
                    name=booking_data["name"],
                    party_size=booking_data["party_size"],
                    booking_date=booking_data["booking_date"],
                    booking_time=booking_data["booking_time"],
                    special_requests=booking_data.get("special_requests", ""),
                )

                booking = self.booking_service.create_booking(booking_request)
                session["state"] = ConversationState.BOOKING_COMPLETE

                bot_message = (
                    f"✅ Booking confirmed!\n\n"
                    f"Booking Reference: {booking.id}\n"
                    f"🍽️ The Golden Plate\n"
                    f"📅 {booking.booking_date} at {booking.booking_time}\n"
                    f"👥 Party of {booking.party_size}\n\n"
                    f"See you soon! Call us if you need to make changes: +44 20 1234 5678"
                )

                return bot_message, ConversationState.BOOKING_COMPLETE, [], True, booking.id

            except ValueError as e:
                return f"❌ Booking failed: {str(e)}", ConversationState.BOOKING_CONFIRMATION, ["Try Again", "Cancel"], False, None

        elif any(word in message_lower for word in ["cancel", "no", "change"]):
            session["state"] = ConversationState.GREETING
            bot_message = "No problem! Feel free to start over. How can I help you?"
            return bot_message, ConversationState.BOOKING_START, ["Book a Table", "View Menu"], False, None

        else:
            return "Please say 'Confirm' to complete the booking or 'Cancel' to start over.", ConversationState.BOOKING_CONFIRMATION, ["Confirm", "Cancel"], False, None
