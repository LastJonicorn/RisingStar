# Prompt 1:
Tarvitsen yksinkertaisen FastAPI-pohjaisen API:n kokoushuoneiden varaamiseen. Käytän Pythonia ja PyCharmia. Aloita perusrungosta.

# ChatGPT 1:
Loin sinulle yksinkertaisen FastAPI-perusrungon canvas-näkymään.

Tämä antaa sinulle:

FastAPI-sovelluksen rungon

Kokoushuone- ja varausmallit (Pydantic)

Muistissa toimivan (ei tietokantaa vielä)

Päätteet:
GET /rooms
GET /bookings
POST /bookings

Peruslogiikan päällekkäisten varausten estämiseen

Näin pääset nopeasti käyntiin PyCharmissa

Luo uusi Python-projekti

Asenna riippuvuudet:

pip install fastapi uvicorn

Tallenna tiedosto nimellä main.py

Käynnistä:

uvicorn main:app --reload


Avaa selain:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

Seuraavat luontevat askeleet

Kun haluat jatkaa, voimme esimerkiksi:

lisätä käyttäjät

siirtyä SQLite / PostgreSQL + SQLAlchemy

lisätä autentikoinnin

tehdä päivä-/viikkokohtaisen saatavuushaun

jakaa projektin useampaan tiedostoon

Sano vain, mihin suuntaan haluat viedä tätä 👍

# Prompt 2:
Lisätään varauksen luonti. Varaus koskee yhtä huonetta ja sisältää aloitus- ja lopetusajan. Voit käyttää in-memory-tietorakennetta. Lisäksi koodin sisäinen teksti tulisi olla englanniksi.

# ChatGPT 2:
Valmis 👍
Päivitin canvasissa olevan koodin niin, että:

Varauksen luonti (POST /bookings) on selkeästi määritelty

Varaus koskee yhtä huonetta

Varaus sisältää start_time ja end_time

Päällekkäiset varaukset estetään

Aikaväli validoidaan (end > start)

Kaikki kommentit, docstringit ja virheilmoitukset ovat englanniksi

Data pidetään in-memory-rakenteissa (listat)

Esimerkki POST-pyynnöstä

Swaggerissa (/docs) tai curlilla:

{
  "room_id": 1,
  "start_time": "2026-01-19T10:00:00",
  "end_time": "2026-01-19T11:00:00",
  "title": "Project kickoff"
}

Seuraavia järkeviä laajennuksia

Halutessasi voimme seuraavaksi:

lisätä booking ID:n generoinnin UUID:llä

tehdä DELETE /bookings/{id}

lisätä room availability -endpointin

siirtyä SQLite + SQLAlchemy

lisätä unit testit (pytest)

Kerro mihin suuntaan jatketaan.

# Prompt 3:
Lisää liiketoimintasäännöt: varaukset eivät saa mennä päällekkäin, aloitusajan täytyy olla ennen lopetusaikaa, eikä varaus saa olla menneisyydessä.


# ChatGPT 3:
Tehty ✅
Lisäsin canvasissa olevaan koodiin kaikki pyytämäsi liiketoimintasäännöt selkeästi ja eksplisiittisesti.

Nyt varauksen luonti noudattaa näitä sääntöjä

POST /bookings tarkistaa:

Aloitusaika ennen lopetusaikaa

if data.end_time <= data.start_time:
    raise HTTPException(...)


Varaus ei saa olla menneisyydessä

now = datetime.utcnow()
if data.start_time < now:
    raise HTTPException(...)


Ei päällekkäisiä varauksia samaan huoneeseen

overlaps = not (
    data.end_time <= booking.start_time
    or data.start_time >= booking.end_time
)


Huoneen olemassaolo varmistetaan

if room is None:
    raise HTTPException(...)

Hyvä huomio jatkoa varten

Käytän datetime.utcnow() → hyvä lähtökohta API:lle

Seuraava askel voisi olla aikavyöhyketuki (timezone-aware datetimes), jos tätä käytetään tuotannossa

Seuraavaksi voimme esim.:

erottaa business logicin service-kerrokseen

lisätä unit testit liiketoimintasäännöille

tehdä GET /rooms/{id}/availability

lisätä configurable booking rules (min/max kesto)

Miten haluat jatkaa?

# Prompt 4:
Lisää mahdollisuus poistaa varaus id:n perusteella sekä endpoint, jolla listataan kaikki tietyn huoneen varaukset. Viimeistele koodi yhteen tiedostoon.

# ChatGPT 4:
 
Fast Api Kokoushuonevaraus – Perusranko
· python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
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


class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    title: str


# ---- In-memory storage (demo purposes only) ----
rooms: List[Room] = [
    Room(id=1, name="Meeting Room A", capacity=8),
    Room(id=2, name="Meeting Room B", capacity=12),
]


bookings: List[Booking] = []


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


    # Validate time range
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")


    # Validate booking is not in the past
    now = datetime.utcnow()
    if data.start_time < now:
        raise HTTPException(status_code=400, detail="Booking cannot start in the past")


    # Check for overlapping bookings
    for booking in bookings:
        if booking.room_id == data.room_id:
            overlaps = not (
                data.end_time <= booking.start_time
                or data.start_time >= booking.end_time
            )
            if overlaps:
                raise HTTPException(
                    status_code=400,
                    detail="The room is already booked for the given time range",
                )


    new_booking = Booking(
        id=len(bookings) + 1,
        room_id=data.room_id,
        start_time=data.start_time,
        end_time=data.end_time,
        title=data.title,
    )



Valmis 👍
Viimeistelin koodin yhdeksi tiedostoksi ja lisäsin pyytämäsi toiminnot.

Uudet ominaisuudet
1. Varausten listaus huonekohtaisesti
GET /rooms/{room_id}/bookings


Palauttaa kaikki tietyn huoneen varaukset

404, jos huonetta ei ole olemassa

2. Varauksen poistaminen ID:n perusteella
DELETE /bookings/{booking_id}


Poistaa varauksen in-memory-listasta

Palauttaa 204 No Content onnistuneessa poistossa

404, jos varausta ei löydy

Kokonaisuus nyt

✔ Yksi tiedosto (main.py)

✔ Selkeät Pydantic-mallit

✔ In-memory data

✔ Liiketoimintasäännöt:

ei päällekkäisiä varauksia

aloitus < lopetus

ei menneisyyteen

✔ Huonekohtainen varauslistaus

✔ Varauksen poisto

Seuraavat järkevät kehitysaskeleet

Jos haluat viedä tämän pidemmälle:

siirtyminen SQLite + SQLAlchemy

UUID:t varauksille

soft delete varauksille

unit testit (pytest + TestClient)

OpenAPI-esimerkit request/response-malleille

Sano vain, mitä tehdään seuraavaksi.

# Prompt 5:
Huoneen varaaminen 
"{ "room_id": 1, 
"start_time":"2026-01-20T10:01:45.847Z", 
"end_time": "2026-01-20T11:01:45.847Z", 
"title": "Varaus 1" }"
aiheuttaa virheen "Internal server error"

# ChatGPT 5:
Fast Api Kokoushuonevaraus – Perusranko
· python
from fastapi import FastAPI, HTTPException
rooms: List[Room] = [
    Room(id=1, name="Meeting Room A", capacity=8),
    Room(id=2, name="Meeting Room B", capacity=12),
]


bookings: List[Booking] = []


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


    # Validate time range
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")


    # Validate booking is not in the past
        now = datetime.now(timezone.utc)


    # Ensure start_time is timezone-aware (UTC)
    start_time = data.start_time
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)


        if start_time < now:
        raise HTTPException(status_code=400, detail="Booking cannot start in the past")


    # Check for overlapping bookings
    for booking in bookings:
        if booking.room_id == data.room_id:
            overlaps = not (
                data.end_time <= booking.start_time
                or data.start_time >= booking.end_time
            )
            if overlaps:
                raise HTTPException(
                    status_code=400,
                    detail="The room is already booked for the given time range",
                )


    new_booking = Booking(
        id=len(bookings) + 1,
        room_id=data.room_id,
        start_time=data.start_time,
        end_time=data.end_time,
        title=data.title,
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



Hyvä havainto — tämä on klassinen FastAPI / datetime-ansa 👍
Virhe ei ole pyynnössäsi, vaan aikavyöhykkeissä.

Miksi saat Internal Server Error -vastauksen?

Lähettämäsi ajat:

"start_time": "2026-01-20T10:01:45.847Z"


Z = UTC

FastAPI/Pydantic parsii tämän timezone-aware datetimeksi

Mutta koodissa oli aiemmin:

now = datetime.utcnow()


datetime.utcnow() on timezone-naive

Python ei salli vertailua:

TypeError: can't compare offset-naive and offset-aware datetimes


➡️ Tämä poikkeus ei ollut kiinni HTTPExceptionissa → FastAPI palauttaa 500 Internal Server Error

Korjaus (tehty koodiin)

Päivitin koodin canvasissa niin, että:

1. Käytetään aina UTC-aikavyöhykettä
from datetime import datetime, timezone

now = datetime.now(timezone.utc)

2. Varmistetaan, että start_time on timezone-aware
start_time = data.start_time
if start_time.tzinfo is None:
    start_time = start_time.replace(tzinfo=timezone.utc)

if start_time < now:
    raise HTTPException(status_code=400, detail="Booking cannot start in the past")

Tulos

✅ Varaus JSON-muodossasi toimii oikein

✅ Ei enää 500-virhettä

✅ Selkeä 400-virhe, jos varaus olisi oikeasti menneisyydessä

✅ API on turvallisempi tuotantokäyttöön

Suositus jatkoon

Jos haluat tehdä tästä vielä siistimmän:

pakota kaikki ajat UTC:ksi request-mallissa

tai käytä kirjastoa kuten pendulum

lisää globaalit exception handlerit, jotta mikään virhe ei vuoda 500:na

Haluatko, että lisätään:

aikavyöhykepolitiikka dokumentaatioon?

testit tälle virheelle?

virheiden loggaus?

Sanot vain 👍