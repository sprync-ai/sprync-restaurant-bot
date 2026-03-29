"""Booking management and validation."""
import uuid
from datetime import datetime, timedelta
from app.models.schemas import Booking, BookingRequest


class BookingService:
    """Service for managing restaurant bookings."""

    def __init__(self):
        """Initialize booking service with empty bookings storage."""
        self.bookings: dict[str, Booking] = {}
        self.restaurant_hours = {
            "open": datetime.strptime("11:00", "%H:%M").time(),
            "close": datetime.strptime("23:00", "%H:%M").time(),
        }

    def create_booking(self, request: BookingRequest) -> Booking:
        """Create a new booking after validation.

        Args:
            request: BookingRequest with booking details.

        Returns:
            Booking: The created booking object.

        Raises:
            ValueError: If validation fails.
        """
        # Validate date
        self._validate_booking_date(request.booking_date)

        # Validate time
        self._validate_booking_time(request.booking_time)

        # Validate party size
        if request.party_size < 1 or request.party_size > 20:
            raise ValueError("Party size must be between 1 and 20")

        # Generate booking ID
        booking_id = self._generate_booking_id()

        # Create booking object
        booking = Booking(
            id=booking_id,
            name=request.name,
            party_size=request.party_size,
            booking_date=request.booking_date,
            booking_time=request.booking_time,
            special_requests=request.special_requests,
            phone=request.phone,
            email=request.email,
        )

        # Store booking
        self.bookings[booking_id] = booking

        return booking

    def _validate_booking_date(self, date_str: str) -> None:
        """Validate that booking date is in future and within advance booking window.

        Args:
            date_str: Date string in YYYY-MM-DD format.

        Raises:
            ValueError: If date is invalid or not bookable.
        """
        try:
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD") from e

        today = datetime.now().date()
        min_date = today + timedelta(days=1)
        max_date = today + timedelta(days=30)

        if booking_date < min_date:
            raise ValueError("Booking must be at least 1 day in advance")

        if booking_date > max_date:
            raise ValueError("We can only accept bookings up to 30 days in advance")

    def _validate_booking_time(self, time_str: str) -> None:
        """Validate that booking time is within restaurant hours.

        Args:
            time_str: Time string in HH:MM format.

        Raises:
            ValueError: If time is invalid or outside hours.
        """
        try:
            booking_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError as e:
            raise ValueError("Invalid time format. Please use HH:MM (24-hour)") from e

        if booking_time < self.restaurant_hours["open"] or booking_time > self.restaurant_hours["close"]:
            raise ValueError(
                f"We are open from {self.restaurant_hours['open'].strftime('%H:%M')} to "
                f"{self.restaurant_hours['close'].strftime('%H:%M')}"
            )

    def _generate_booking_id(self) -> str:
        """Generate a unique booking ID.

        Returns:
            str: Booking reference ID.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_suffix = str(uuid.uuid4())[:8].upper()
        return f"BK{timestamp}{unique_suffix}"

    def get_booking(self, booking_id: str) -> Booking | None:
        """Get a booking by ID.

        Args:
            booking_id: The booking ID.

        Returns:
            Booking or None if not found.
        """
        return self.bookings.get(booking_id)

    def get_all_bookings(self) -> list[Booking]:
        """Get all bookings.

        Returns:
            List of all bookings.
        """
        return list(self.bookings.values())

    def get_bookings_by_date(self, date_str: str) -> list[Booking]:
        """Get bookings for a specific date.

        Args:
            date_str: Date in YYYY-MM-DD format.

        Returns:
            List of bookings on that date.
        """
        return [b for b in self.bookings.values() if b.booking_date == date_str]

    def check_availability(self, date_str: str, time_str: str, party_size: int) -> bool:
        """Check if a time slot is available.

        For simplicity, we allow multiple bookings at same time.
        In production, this would check table availability.

        Args:
            date_str: Date in YYYY-MM-DD format.
            time_str: Time in HH:MM format.
            party_size: Party size to check.

        Returns:
            bool: True if available, False otherwise.
        """
        # Simple implementation: always available if date/time are valid
        # In production, this would check against actual table inventory
        return True
