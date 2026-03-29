"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class ConversationState(str, Enum):
    """Possible conversation states."""

    GREETING = "greeting"
    MENU_INQUIRY = "menu_inquiry"
    BOOKING_START = "booking_start"
    COLLECT_NAME = "collect_name"
    COLLECT_PARTY_SIZE = "collect_party_size"
    COLLECT_DATE = "collect_date"
    COLLECT_TIME = "collect_time"
    COLLECT_SPECIAL_REQUESTS = "collect_special_requests"
    BOOKING_CONFIRMATION = "booking_confirmation"
    BOOKING_COMPLETE = "booking_complete"


class MenuItem(BaseModel):
    """A menu item."""

    id: str
    name: str
    description: str
    price: float
    category: str
    dietary_tags: list[str] = Field(default_factory=list)  # V, VG, GF, etc.

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "tandoori_lamb_chops",
                "name": "Tandoori Lamb Chops",
                "description": "Succulent lamb chops marinated in yogurt and spices, cooked in clay oven",
                "price": 14.99,
                "category": "Starters",
                "dietary_tags": ["GF"],
            }
        }


class ChatMessage(BaseModel):
    """A message in the chat."""

    role: str = Field(..., description="'user' or 'bot'")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    session_id: str = Field(..., description="Unique session identifier")
    user_message: str
    conversation_history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Response body from chat endpoint."""

    session_id: str
    bot_message: str
    conversation_state: ConversationState
    quick_replies: list[str] = Field(default_factory=list)
    is_booking_confirmed: bool = False
    booking_reference: Optional[str] = None


class BookingRequest(BaseModel):
    """A booking request."""

    name: str
    party_size: int
    booking_date: str  # YYYY-MM-DD
    booking_time: str  # HH:MM
    special_requests: str = ""
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator("party_size")
    @classmethod
    def validate_party_size(cls, v: int) -> int:
        """Validate party size is between 1 and 20."""
        if v < 1 or v > 20:
            raise ValueError("Party size must be between 1 and 20")
        return v


class Booking(BaseModel):
    """A confirmed booking."""

    id: str
    name: str
    party_size: int
    booking_date: str
    booking_time: str
    special_requests: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "BK202603271234",
                "name": "Raj Kumar",
                "party_size": 4,
                "booking_date": "2026-03-29",
                "booking_time": "19:30",
                "special_requests": "Window table preferred",
                "phone": "+44 7777 123456",
                "email": "raj@example.com",
            }
        }


class MenuResponse(BaseModel):
    """Response containing menu items."""

    restaurant_name: str
    items: list[MenuItem]
    total_items: int


class BookingsResponse(BaseModel):
    """Response containing all bookings."""

    total_bookings: int
    bookings: list[Booking]
