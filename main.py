from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List

app = FastAPI(title="Meeting Room Booking API")

# ---- Data Models ----
class Room(BaseModel):
    id: int
    name: str
    capacity: int

class Booking(BaseModel):
    id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    title: str
    booked_by: str

class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    title: str
    booked_by: str

# ---- In-memory storage (demo purposes only) ----
rooms: List[Room] = [
    Room(id=1, name="Meeting Room A", capacity=8),
    Room(id=2, name="Meeting Room B", capacity=12),
]

bookings: List[Booking] = []

# ---- Helper functions ----
def ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware and in UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

# ---- API Endpoints ----
@app.get("/rooms", response_model=List[Room])
def list_rooms():
    """Return all available meeting rooms."""
    return rooms

@app.get("/rooms/{room_id}/bookings", response_model=List[Booking])
def list_bookings_for_room(room_id: int):
    """Return all bookings for a specific room."""
    room = next((r for r in rooms if r.id == room_id), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return [b for b in bookings if b.room_id == room_id]

@app.get("/bookings", response_model=List[Booking])
def list_bookings():
    """Return all existing bookings."""
    return bookings

@app.post("/bookings", response_model=Booking, status_code=201)
def create_booking(data: BookingCreate):
    """
    Create a new booking for a single room.

    Business rules:
    - Room must exist
    - End time must be after start time
    - Booking cannot start in the past
    - No overlapping bookings for the same room
    """
    # Validate room existence
    room = next((r for r in rooms if r.id == data.room_id), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    start_time = ensure_utc(data.start_time)
    end_time = ensure_utc(data.end_time)

    # Validate time range
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    # Validate booking is not in the past
    now = datetime.now(timezone.utc)
    if start_time < now:
        raise HTTPException(status_code=400, detail="Booking cannot start in the past")

    # Check for overlapping bookings
    for booking in bookings:
        if booking.room_id == data.room_id:
            existing_start = ensure_utc(booking.start_time)
            existing_end = ensure_utc(booking.end_time)

            overlaps = not (
                end_time <= existing_start
                or start_time >= existing_end
            )
            if overlaps:
                raise HTTPException(
                    status_code=400,
                    detail="The room is already booked for the given time range",
                )

    new_booking = Booking(
        id=len(bookings) + 1,
        room_id=data.room_id,
        start_time=start_time,
        end_time=end_time,
        title=data.title,
        booked_by=data.booked_by,
    )

    bookings.append(new_booking)
    return new_booking

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int):
    """Delete a booking by its ID."""
    for index, booking in enumerate(bookings):
        if booking.id == booking_id:
            bookings.pop(index)
            return

    raise HTTPException(status_code=404, detail="Booking not found")

# ---- Application startup ----
# Run with:
# uvicorn main:app --reload
