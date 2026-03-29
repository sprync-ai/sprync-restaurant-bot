"""Unit tests for chat functionality."""
import pytest
from pydantic import ValidationError
from app.services.chat_engine import ChatEngine
from app.services.booking import BookingService
from app.services.menu import MenuService
from app.models.schemas import ConversationState, BookingRequest


class TestChatEngine:
    """Test chat engine functionality."""

    @pytest.fixture
    def chat_engine(self):
        """Create a chat engine instance."""
        return ChatEngine()

    def test_greeting_state(self, chat_engine):
        """Test greeting state transitions."""
        session_id = "test_session_1"
        bot_message, state, quick_replies, is_confirmed, booking_ref = chat_engine.process_message(
            session_id, "Hello", []
        )

        assert "Welcome" in bot_message
        assert state == ConversationState.BOOKING_START
        assert len(quick_replies) > 0
        assert not is_confirmed

    def test_booking_flow(self, chat_engine):
        """Test complete booking flow."""
        session_id = "test_session_booking"

        # Start conversation
        chat_engine.process_message(session_id, "Hi", [])

        # Request booking
        _, state, _, _, _ = chat_engine.process_message(session_id, "Book a table", [])
        assert state == ConversationState.COLLECT_NAME

        # Provide name
        _, state, _, _, _ = chat_engine.process_message(session_id, "John Doe", [])
        assert state == ConversationState.COLLECT_PARTY_SIZE

        # Provide party size
        _, state, _, _, _ = chat_engine.process_message(session_id, "4", [])
        assert state == ConversationState.COLLECT_DATE

        # Provide date
        _, state, _, _, _ = chat_engine.process_message(session_id, "2026-03-29", [])
        assert state == ConversationState.COLLECT_TIME

        # Provide time
        _, state, _, _, _ = chat_engine.process_message(session_id, "19:30", [])
        assert state == ConversationState.COLLECT_SPECIAL_REQUESTS

        # Provide special requests
        _, state, _, _, _ = chat_engine.process_message(session_id, "None", [])
        assert state == ConversationState.BOOKING_CONFIRMATION

        # Confirm booking
        _, state, _, is_confirmed, booking_ref = chat_engine.process_message(
            session_id, "Confirm", []
        )
        assert state == ConversationState.BOOKING_COMPLETE
        assert is_confirmed
        assert booking_ref is not None


class TestBookingService:
    """Test booking service functionality."""

    @pytest.fixture
    def booking_service(self):
        """Create a booking service instance."""
        return BookingService()

    def test_create_valid_booking(self, booking_service):
        """Test creating a valid booking."""
        request = BookingRequest(
            name="Jane Smith",
            party_size=2,
            booking_date="2026-03-29",
            booking_time="19:30",
            special_requests="Window table",
        )

        booking = booking_service.create_booking(request)

        assert booking.name == "Jane Smith"
        assert booking.party_size == 2
        assert booking.id is not None

    def test_invalid_party_size(self):
        """Test validation of party size."""
        with pytest.raises(ValidationError):
            BookingRequest(
                name="Jane Smith",
                party_size=25,
                booking_date="2026-03-29",
                booking_time="19:30",
            )

    def test_invalid_date_in_past(self, booking_service):
        """Test validation of past dates."""
        request = BookingRequest(
            name="Jane Smith",
            party_size=2,
            booking_date="2026-01-01",
            booking_time="19:30",
        )

        with pytest.raises(ValueError):
            booking_service.create_booking(request)

    def test_invalid_time_outside_hours(self, booking_service):
        """Test validation of times outside restaurant hours."""
        request = BookingRequest(
            name="Jane Smith",
            party_size=2,
            booking_date="2026-03-29",
            booking_time="06:00",
        )

        with pytest.raises(ValueError):
            booking_service.create_booking(request)


class TestMenuService:
    """Test menu service functionality."""

    @pytest.fixture
    def menu_service(self):
        """Create a menu service instance."""
        return MenuService()

    def test_get_all_items(self, menu_service):
        """Test retrieving all menu items."""
        items = menu_service.get_all_items()
        assert len(items) > 0

    def test_get_items_by_category(self, menu_service):
        """Test retrieving items by category."""
        starters = menu_service.get_items_by_category("Starters")
        assert len(starters) > 0
        assert all(item.category == "Starters" for item in starters)

    def test_search_items(self, menu_service):
        """Test searching for items."""
        results = menu_service.search_items("chicken")
        assert len(results) > 0

    def test_get_vegetarian_items(self, menu_service):
        """Test getting vegetarian items."""
        veg_items = menu_service.get_vegetarian_items()
        assert len(veg_items) > 0
        assert all("V" in item.dietary_tags or "VG" in item.dietary_tags for item in veg_items)

    def test_get_gluten_free_items(self, menu_service):
        """Test getting gluten-free items."""
        gf_items = menu_service.get_gluten_free_items()
        assert len(gf_items) > 0
        assert all("GF" in item.dietary_tags for item in gf_items)
