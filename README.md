# The Golden Plate - Restaurant Booking Chatbot

**Built by Sprync AI** - A production-ready AI-powered restaurant booking chatbot showcasing modern full-stack development.

## Overview

The Golden Plate is a sophisticated restaurant booking chatbot that handles customer inquiries, menu browsing, and table reservations. Built with FastAPI, React, and modern web standards, it demonstrates enterprise-grade chatbot architecture suitable for restaurant management, hospitality tech, and customer engagement use cases.

### Key Features

- 🤖 **Intelligent Conversation State Machine** - Multi-step booking flow with context awareness
- 📋 **Dynamic Menu System** - Real-time menu browsing with dietary filters (V, VG, GF)
- 🎫 **Smart Booking Engine** - Date/time validation, availability checking, booking confirmation
- 💬 **Modern Chat UI** - WhatsApp-like interface with typing indicators and quick replies
- 📱 **Fully Responsive** - Works seamlessly on mobile, tablet, and desktop
- 🔒 **Session Management** - Per-user conversation context and booking state
- ⚡ **Production-Ready** - Type hints, comprehensive error handling, API documentation

### Technology Stack

**Backend:**
- FastAPI (async Python web framework)
- Pydantic (data validation with type hints)
- Python 3.11+

**Frontend:**
- React 18 (via CDN, no build step required)
- Tailwind CSS (utility-first styling)
- Vanilla JavaScript with Babel transpilation

**Infrastructure:**
- Docker & Docker Compose for local development
- Render.com for cloud deployment
- REST API architecture

## Project Structure

```
sprync-restaurant-bot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings and configuration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models (ChatMessage, Booking, etc.)
│   │   ├── services/
│   │   │   ├── chat_engine.py   # Conversation state machine
│   │   │   ├── booking.py       # Booking logic and validation
│   │   │   └── menu.py          # Menu data and search
│   │   └── routers/
│   │       └── chat.py          # API endpoints
│   ├── tests/
│   │   └── test_chat.py         # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html               # Single HTML entry point
│   └── static/
│       ├── app.jsx              # React application
│       └── styles.css           # Custom CSS
├── docker-compose.yml           # Local development setup
├── render.yaml                  # Cloud deployment config
├── .env.example                 # Environment template
├── .gitignore
└── README.md
```

## Quick Start

### Local Development with Docker

**Prerequisites:** Docker and Docker Compose installed

```bash
# Clone the repository
git clone https://github.com/sprync-ai/sprync-restaurant-bot.git
cd sprync-restaurant-bot

# Start the application
docker-compose up --build

# The chatbot will be available at http://localhost:8000
```

### Manual Setup (Python 3.11+)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Visit http://localhost:8000
```

## API Documentation

### Chat Endpoint

**POST `/api/chat`**

Send a user message and receive a bot response with conversation state.

**Request:**
```json
{
  "session_id": "user_session_123",
  "user_message": "I'd like to book a table",
  "conversation_history": []
}
```

**Response:**
```json
{
  "session_id": "user_session_123",
  "bot_message": "Great! Let's get you a table. What's your name?",
  "conversation_state": "collect_name",
  "quick_replies": [],
  "is_booking_confirmed": false,
  "booking_reference": null
}
```

### Menu Endpoints

**GET `/api/menu`** - Get all menu items
```json
{
  "restaurant_name": "The Golden Plate",
  "items": [...],
  "total_items": 19
}
```

**GET `/api/menu/category/{category}`** - Get items by category
```bash
GET /api/menu/category/Mains
```

**GET `/api/menu/search?q=chicken`** - Search menu items

### Booking Endpoints

**GET `/api/bookings`** - Get all bookings (admin view)
```json
{
  "total_bookings": 5,
  "bookings": [...]
}
```

**GET `/api/bookings/{booking_id}`** - Get specific booking details

### Restaurant Information

**GET `/api/restaurant/info`** - Get restaurant details
```json
{
  "name": "The Golden Plate",
  "hours": "11:00 AM - 11:00 PM (Daily)",
  "phone": "+44 20 1234 5678",
  "location": "123 Brick Lane, London E1 6PU",
  "cuisine": "Modern British-Indian Fusion"
}
```

**GET `/api/health`** - Health check endpoint

## Conversation Flow

The chatbot guides users through a multi-step conversation:

1. **GREETING** - Welcome and initial options
2. **BOOKING_START** - User chooses to book, view menu, or get info
3. **COLLECT_NAME** - Get customer name
4. **COLLECT_PARTY_SIZE** - Number of guests
5. **COLLECT_DATE** - Booking date (YYYY-MM-DD format)
6. **COLLECT_TIME** - Booking time (HH:MM format, 11:00-23:00)
7. **COLLECT_SPECIAL_REQUESTS** - Special requests or notes
8. **BOOKING_CONFIRMATION** - Review and confirm booking
9. **BOOKING_COMPLETE** - Confirmation with reference number

## Features Demonstrated

### Backend Excellence
- **Async Architecture** - FastAPI with async/await for high performance
- **State Management** - Session-based conversation state machine
- **Data Validation** - Pydantic models with field validators
- **Business Logic** - Booking validation, date/time checks, availability
- **Clean Architecture** - Separation of concerns (models, services, routers)
- **Error Handling** - Comprehensive exception handling and user feedback
- **Type Safety** - Full type hints throughout codebase
- **Testing** - Unit tests for chat engine, booking, and menu services

### Frontend Excellence
- **Modern React** - Hooks-based functional components
- **No Build Step** - React from CDN for simplicity and portability
- **Responsive Design** - Mobile-first, works on all screen sizes
- **UX Polish** - Typing indicators, smooth animations, intuitive UI
- **Accessibility** - Semantic HTML, proper ARIA roles, keyboard support
- **State Management** - useRef, useState, useCallback for efficient rendering

### Deployment Ready
- **Docker Support** - Multi-stage Dockerfile for optimized images
- **Cloud Deployment** - Render.com configuration for one-click deployment
- **Environment Config** - .env support for different environments
- **Health Checks** - /health endpoint for monitoring

## Restaurant Theme: The Golden Plate

A modern British-Indian fusion restaurant in Brick Lane, London. Menu features:

**Starters:** Tandoori Lamb Chops, Vegetable Samosas, Paneer Tikka, Chicken Seekh Kebab
**Mains:** Butter Chicken, Kerala Fish Curry, Lamb Rogan Josh, Chana Masala, Palak Paneer
**Sides:** Naan, Garlic Naan, Masala Chips, Basmati Rice
**Desserts:** Chai Crème Brûlée, Gulab Jamun
**Beverages:** Mango Lassi, Masala Chai

All items include pricing (GBP) and dietary tags (V=Vegetarian, VG=Vegan, GF=Gluten-Free).

## Deployment on Render.com

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/sprync-restaurant-bot.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Set build command: `pip install -r backend/requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Deploy!

Your chatbot will be live at `https://your-service-name.onrender.com`

## Testing

Run the test suite:

```bash
cd backend
pytest tests/ -v
```

Tests cover:
- Chat engine state transitions
- Booking creation and validation
- Menu search and filtering
- Date/time validation
- Party size validation

## Environment Variables

See `.env.example` for all configurable settings:

```bash
# Application
DEBUG=False
PORT=8000

# Restaurant
RESTAURANT_NAME=The Golden Plate
RESTAURANT_PHONE=+44 20 1234 5678
RESTAURANT_HOURS=11:00 AM - 11:00 PM (Daily)

# Booking
MIN_PARTY_SIZE=1
MAX_PARTY_SIZE=20
BOOKING_ADVANCE_DAYS=30
```

## Performance & Scalability

- **Async FastAPI** - Handles thousands of concurrent users
- **Session-based Storage** - In-memory storage suitable for initial phase; upgrade to Redis/database for scale
- **Stateless API** - Each request is independent; easy to scale horizontally
- **CDN-based Frontend** - React and Tailwind served from CDN; minimal server load
- **Caching Ready** - Add Redis caching for menu queries and availability checks

## Security Features

- **CORS Configured** - Prevents unauthorized cross-origin requests
- **Input Validation** - Pydantic validates all inputs
- **SQL Injection Prevention** - Not using SQL directly (in-memory storage)
- **Error Messages** - Generic error messages; no internal details leaked
- **Rate Limiting Ready** - Easy to add with FastAPI middleware

## Future Enhancements

- **Database Integration** - PostgreSQL for persistent storage
- **Payment Processing** - Stripe integration for deposits/pre-payment
- **Email Notifications** - Booking confirmations via email
- **SMS Alerts** - Reminder notifications via SMS
- **Multi-language Support** - i18n for global markets
- **Analytics Dashboard** - Booking trends, popular times, revenue metrics
- **Admin Panel** - Manage bookings, menu, restaurant info
- **Calendar Integration** - Sync with Google Calendar
- **Waitlist Management** - Handle overbooking scenarios

## Support & Contribution

Built by **Sprync AI** - your partner for AI-powered business solutions.

For issues or feature requests, please open a GitHub issue.

## License

This project is provided as a portfolio piece by Sprync AI. Use for reference and learning purposes.

---

**Ready to win restaurant tech clients?** This chatbot demonstrates:
- ✅ Production-grade code quality
- ✅ Full-stack competency
- ✅ Attention to UX and design
- ✅ Deployment expertise
- ✅ Scalable architecture

Perfect for showcasing to potential clients and employers.

**Built with ❤️ by Sprync AI**
