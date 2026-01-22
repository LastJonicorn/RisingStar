from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List
from itertools import count

app = FastAPI(title="Meeting Room Booking API")

# ---- Data Models ----
class Room(BaseModel):
    id: int
    name: str
    capacity: int

class Booking(BaseModel):
    id: int
    room_id: int
    date: date
    start_time: time
    end_time: time
    attendees: int
    title: str
    booked_by: str

class BookingCreate(BaseModel):
    room_id: int
    date: date
    start_time: time
    end_time: time
    attendees: int
    title: str
    booked_by: str

# ---- In-memory storage ----
rooms: List[Room] = [
    Room(id=1, name="Meeting Room A", capacity=8),
    Room(id=2, name="Meeting Room B", capacity=12),
]

bookings: List[Booking] = []
booking_id_counter = count(1)

# ---- Helper functions ----
def combine_datetime(d: date, t: time) -> datetime:
    return datetime(d.year, d.month, d.day, t.hour, t.minute)

# ---- API Endpoints ----
@app.get("/rooms", response_model=List[Room])
def list_rooms():
    return rooms

@app.get("/rooms/{room_id}/bookings", response_model=List[Booking])
def list_bookings_for_room(room_id: int):
    room = next((r for r in rooms if r.id == room_id), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return sorted([b for b in bookings if b.room_id == room_id], key=lambda b: (b.date, b.start_time))

@app.get("/bookings", response_model=List[Booking])
def list_bookings():
    return sorted(bookings, key=lambda b: (b.date, b.start_time))

@app.post("/bookings", response_model=Booking, status_code=201)
def create_booking(data: BookingCreate):
    room = next((r for r in rooms if r.id == data.room_id), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    start_dt = combine_datetime(data.date, data.start_time)
    end_dt = combine_datetime(data.date, data.end_time)

    if end_dt <= start_dt:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    now = datetime.now()
    if start_dt < now:
        raise HTTPException(status_code=400, detail="Booking cannot start in the past")

    if data.attendees > room.capacity:
        raise HTTPException(status_code=400, detail="Number of attendees exceeds room capacity")

    if data.attendees < 1:
        raise HTTPException(status_code=400, detail="Number of attendees must be at least 1")

    for booking in bookings:
        if booking.room_id == data.room_id:
            existing_start = combine_datetime(booking.date, booking.start_time)
            existing_end = combine_datetime(booking.date, booking.end_time)
            if not (end_dt <= existing_start or start_dt >= existing_end):
                raise HTTPException(status_code=400, detail="The room is already booked for the given time range")

    new_booking = Booking(
        id=next(booking_id_counter),
        room_id=data.room_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        attendees=data.attendees,
        title=data.title,
        booked_by=data.booked_by,
    )

    bookings.append(new_booking)
    return new_booking

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int):
    for index, booking in enumerate(bookings):
        if booking.id == booking_id:
            bookings.pop(index)
            return
    raise HTTPException(status_code=404, detail="Booking not found")

# ---- Application startup ----
# Run with:
# uvicorn main:app --reload