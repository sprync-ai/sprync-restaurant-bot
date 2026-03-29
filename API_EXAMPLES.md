# API Usage Examples

Complete examples for all Restaurant Booking Chatbot endpoints.

## Base URL
```
Local: http://localhost:8000
Production: https://your-service.onrender.com
```

---

## Chat Endpoint

### POST /api/chat

Process user messages and receive bot responses with conversation state.

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user_123",
    "user_message": "I want to book a table",
    "conversation_history": []
  }'
```

**Response:**
```json
{
  "session_id": "user_123",
  "bot_message": "Great! Let's get you a table. What's your name?",
  "conversation_state": "collect_name",
  "quick_replies": [],
  "is_booking_confirmed": false,
  "booking_reference": null
}
```

### Example: Complete Booking Flow

**Step 1: User says hello**
```json
{
  "session_id": "session_abc123",
  "user_message": "Hi there!",
  "conversation_history": []
}
```
Response: Greeting with options to book, view menu, or get contact info

**Step 2: Request booking**
```json
{
  "session_id": "session_abc123",
  "user_message": "Book a table",
  "conversation_history": [...]
}
```
Response: "What's your name?"

**Step 3: Provide name**
```json
{
  "session_id": "session_abc123",
  "user_message": "Rajesh Patel",
  "conversation_history": [...]
}
```
Response: "How many people will be dining with us?" with quick reply options: [2, 4, 6, 8]

**Step 4: Provide party size**
```json
{
  "session_id": "session_abc123",
  "user_message": "4",
  "conversation_history": [...]
}
```
Response: "What date would you like? (YYYY-MM-DD)"

**Step 5: Provide date**
```json
{
  "session_id": "session_abc123",
  "user_message": "2026-03-29",
  "conversation_history": [...]
}
```
Response: "What time would you prefer? (HH:MM, 11:00 - 23:00)" with suggested times: [19:00, 19:30, 20:00, 20:30]

**Step 6: Provide time**
```json
{
  "session_id": "session_abc123",
  "user_message": "19:30",
  "conversation_history": [...]
}
```
Response: "Any special requests?" with option: ["None"]

**Step 7: Provide special requests**
```json
{
  "session_id": "session_abc123",
  "user_message": "Window table preferred, celebrating anniversary",
  "conversation_history": [...]
}
```
Response: Booking confirmation summary with options: ["Confirm", "Cancel"]

**Step 8: Confirm booking**
```json
{
  "session_id": "session_abc123",
  "user_message": "Confirm",
  "conversation_history": [...]
}
```
Response:
```json
{
  "session_id": "session_abc123",
  "bot_message": "✅ Booking confirmed!\n\nBooking Reference: BK202603271234ABCD\n🍽️ The Golden Plate\n📅 2026-03-29 at 19:30\n👥 Party of 4\n\nSee you soon! Call us if you need to make changes: +44 20 1234 5678",
  "conversation_state": "booking_complete",
  "quick_replies": [],
  "is_booking_confirmed": true,
  "booking_reference": "BK202603271234ABCD"
}
```

---

## Menu Endpoints

### GET /api/menu

Get all menu items.

**Request:**
```bash
curl http://localhost:8000/api/menu
```

**Response:**
```json
{
  "restaurant_name": "The Golden Plate",
  "items": [
    {
      "id": "tandoori_lamb_chops",
      "name": "Tandoori Lamb Chops",
      "description": "Succulent lamb chops marinated in yogurt and spices, cooked in clay oven",
      "price": 14.99,
      "category": "Starters",
      "dietary_tags": ["GF"]
    },
    {
      "id": "butter_chicken",
      "name": "Butter Chicken",
      "description": "Tender chicken in a creamy tomato and butter sauce with aromatic spices",
      "price": 12.99,
      "category": "Mains",
      "dietary_tags": []
    }
  ],
  "total_items": 19
}
```

### GET /api/menu/category/{category}

Get menu items by category.

**Request:**
```bash
curl http://localhost:8000/api/menu/category/Mains
```

**Valid categories:**
- Starters
- Mains
- Sides
- Desserts
- Beverages

**Response:**
```json
{
  "category": "Mains",
  "items": [
    {
      "id": "butter_chicken",
      "name": "Butter Chicken",
      "description": "Tender chicken in a creamy tomato and butter sauce with aromatic spices",
      "price": 12.99,
      "category": "Mains",
      "dietary_tags": []
    },
    {
      "id": "kerala_fish_curry",
      "name": "Kerala Fish Curry",
      "description": "Fresh fish cooked in coconut milk with curry leaves and tamarind",
      "price": 15.99,
      "category": "Mains",
      "dietary_tags": ["GF"]
    }
  ]
}
```

### GET /api/menu/search

Search menu items by name or description.

**Request:**
```bash
curl "http://localhost:8000/api/menu/search?q=curry"
```

**Response:**
```json
{
  "query": "curry",
  "items": [
    {
      "id": "kerala_fish_curry",
      "name": "Kerala Fish Curry",
      "description": "Fresh fish cooked in coconut milk with curry leaves and tamarind",
      "price": 15.99,
      "category": "Mains",
      "dietary_tags": ["GF"]
    },
    {
      "id": "lamb_rogan_josh",
      "name": "Lamb Rogan Josh",
      "description": "Tender pieces of lamb in a rich and aromatic tomato-based curry",
      "price": 14.99,
      "category": "Mains",
      "dietary_tags": ["GF"]
    }
  ],
  "count": 2
}
```

---

## Booking Endpoints

### GET /api/bookings

Get all bookings (admin/management view).

**Request:**
```bash
curl http://localhost:8000/api/bookings
```

**Response:**
```json
{
  "total_bookings": 3,
  "bookings": [
    {
      "id": "BK202603271234ABCD",
      "name": "Rajesh Patel",
      "party_size": 4,
      "booking_date": "2026-03-29",
      "booking_time": "19:30",
      "special_requests": "Window table preferred, celebrating anniversary",
      "phone": null,
      "email": null,
      "created_at": "2026-03-27T14:30:00"
    },
    {
      "id": "BK202603271245EFGH",
      "name": "Sarah Johnson",
      "party_size": 2,
      "booking_date": "2026-03-30",
      "booking_time": "20:00",
      "special_requests": "",
      "phone": "+44 7777 123456",
      "email": "sarah@example.com",
      "created_at": "2026-03-27T14:31:00"
    }
  ]
}
```

### GET /api/bookings/{booking_id}

Get a specific booking by reference ID.

**Request:**
```bash
curl http://localhost:8000/api/bookings/BK202603271234ABCD
```

**Response:**
```json
{
  "id": "BK202603271234ABCD",
  "name": "Rajesh Patel",
  "party_size": 4,
  "booking_date": "2026-03-29",
  "booking_time": "19:30",
  "special_requests": "Window table preferred, celebrating anniversary",
  "phone": null,
  "email": null,
  "created_at": "2026-03-27T14:30:00"
}
```

**Error Response (not found):**
```json
{
  "detail": "Booking not found"
}
```

---

## Restaurant Info Endpoint

### GET /api/restaurant/info

Get restaurant details and contact information.

**Request:**
```bash
curl http://localhost:8000/api/restaurant/info
```

**Response:**
```json
{
  "name": "The Golden Plate",
  "hours": "11:00 AM - 11:00 PM (Daily)",
  "phone": "+44 20 1234 5678",
  "location": "123 Brick Lane, London E1 6PU",
  "cuisine": "Modern British-Indian Fusion"
}
```

---

## Health Check Endpoint

### GET /api/health

Check if the service is running and healthy.

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Sprync Restaurant Bot",
  "version": "1.0.0"
}
```

---

## Error Handling

### Invalid Input Examples

**Invalid party size (too large):**
```json
{
  "detail": "Party size must be between 1 and 20"
}
```

**Invalid date (in the past):**
```json
{
  "detail": "Booking must be at least 1 day in advance"
}
```

**Invalid time (outside hours):**
```json
{
  "detail": "We are open from 11:00 to 23:00"
}
```

**Invalid date format:**
```json
{
  "detail": "Invalid date format. Please use YYYY-MM-DD"
}
```

---

## Using with JavaScript/Fetch

```javascript
async function bookTable(sessionId, message) {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId,
        user_message: message,
        conversation_history: []
      })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    console.log('Bot response:', data.bot_message);
    console.log('Next state:', data.conversation_state);
    console.log('Quick replies:', data.quick_replies);

    if (data.is_booking_confirmed) {
      console.log('Booking confirmed!', data.booking_reference);
    }

    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

## Using with Python/Requests

```python
import requests
import json

def send_chat_message(session_id: str, user_message: str):
    """Send a message to the chatbot and get response."""
    url = "http://localhost:8000/api/chat"

    payload = {
        "session_id": session_id,
        "user_message": user_message,
        "conversation_history": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Bot: {data['bot_message']}")
        print(f"State: {data['conversation_state']}")
        print(f"Quick replies: {data['quick_replies']}")

        if data['is_booking_confirmed']:
            print(f"Booking Reference: {data['booking_reference']}")

        return data
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
session_id = "user_001"
send_chat_message(session_id, "Hi, I want to book a table")
```

---

## Using with cURL Examples

**View restaurant info:**
```bash
curl -s http://localhost:8000/api/restaurant/info | jq .
```

**Search menu for vegetarian items:**
```bash
curl -s "http://localhost:8000/api/menu/search?q=vegetarian" | jq .
```

**Get all bookings for a specific date:**
```bash
curl -s http://localhost:8000/api/bookings | jq '.bookings[] | select(.booking_date == "2026-03-29")'
```

---

## Dietary Tags Reference

- `V` - Vegetarian
- `VG` - Vegan
- `GF` - Gluten-Free

**Example:** `"dietary_tags": ["V", "GF"]` means the dish is both vegetarian and gluten-free.

---

## Rate Limiting & Performance

The API currently has no rate limiting. In production, add:
- Request rate limiting (e.g., 100 requests/minute per session)
- Request size limits
- Response caching for menu queries
- Database connections pooling

---

## WebSocket Support (Future)

Currently using HTTP polling. For real-time chat, implement:
```python
from fastapi import WebSocket

@app.websocket("/ws/chat/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    # Implementation here
```

---

## Security Notes

1. **Input Validation:** All inputs validated via Pydantic
2. **CORS:** Configured to accept all origins (configure for production)
3. **No Authentication:** Add JWT/OAuth for production
4. **Session Management:** Implement proper session timeout
5. **Data Storage:** Currently in-memory; use database for production

---

**For support or questions, refer to the main README.md**
