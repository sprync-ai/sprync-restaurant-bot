"""Chat and booking API endpoints."""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    MenuResponse,
    BookingsResponse,
    ChatMessage,
    ConversationState,
)
from app.services.chat_engine import ChatEngine
from app.services.menu import MenuService
from app.services.booking import BookingService
from app.config import settings

router = APIRouter(prefix="/api", tags=["chat"])

# Shared service instances
chat_engine = ChatEngine()
menu_service = MenuService()
booking_service = BookingService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return bot response.

    Args:
        request: ChatRequest containing session_id and user_message.

    Returns:
        ChatResponse with bot message, state, and quick replies.
    """
    try:
        bot_message, state, quick_replies, is_confirmed, booking_ref = chat_engine.process_message(
            request.session_id,
            request.user_message,
            request.conversation_history,
        )

        return ChatResponse(
            session_id=request.session_id,
            bot_message=bot_message,
            conversation_state=state,
            quick_replies=quick_replies,
            is_booking_confirmed=is_confirmed,
            booking_reference=booking_ref,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/menu", response_model=MenuResponse)
async def get_menu() -> MenuResponse:
    """Get the restaurant menu.

    Returns:
        MenuResponse with all menu items.
    """
    items = menu_service.get_all_items()
    return MenuResponse(
        restaurant_name=settings.restaurant_name,
        items=items,
        total_items=len(items),
    )


@router.get("/menu/category/{category}")
async def get_menu_by_category(category: str):
    """Get menu items by category.

    Args:
        category: Menu category (Starters, Mains, Sides, Desserts, Beverages).

    Returns:
        List of menu items in that category.
    """
    items = menu_service.get_items_by_category(category)
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found in category '{category}'")
    return {"category": category, "items": items}


@router.get("/menu/search")
async def search_menu(q: str):
    """Search menu items.

    Args:
        q: Search query.

    Returns:
        List of matching menu items.
    """
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")

    items = menu_service.search_items(q)
    return {"query": q, "items": items, "count": len(items)}


@router.get("/bookings", response_model=BookingsResponse)
async def get_bookings() -> BookingsResponse:
    """Get all bookings (admin endpoint).

    Returns:
        BookingsResponse with all bookings.
    """
    bookings = booking_service.get_all_bookings()
    return BookingsResponse(
        total_bookings=len(bookings),
        bookings=bookings,
    )


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    """Get a specific booking by ID.

    Args:
        booking_id: The booking reference ID.

    Returns:
        Booking details.
    """
    booking = booking_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.get("/restaurant/info")
async def restaurant_info():
    """Get restaurant information.

    Returns:
        Restaurant details.
    """
    return {
        "name": settings.restaurant_name,
        "hours": settings.restaurant_hours,
        "phone": settings.restaurant_phone,
        "location": "123 Brick Lane, London E1 6PU",
        "cuisine": "Modern British-Indian Fusion",
    }


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Health status.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }
