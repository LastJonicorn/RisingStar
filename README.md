<h1>Yksinkertainen FastAPI-pohjainen rajapinta kokoushuoneiden varaamiseen.</h1> 

</br>

<h2>Rajapinnan käynnistys ja testaus:</h2>

<h3>Asenna tarvittavat kirjastot:</h3>
pip install fastapi uvicorn

<h3>Käynnistä sovellus projektin juuresta:</h3>
uvicorn main:app --reload

<h3>Avaa rajapinnan testiympäristö selaimessa:</h3>
http://127.0.0.1:8000/docs

Osoitteessa avautuu FastAPI:n automaattisesti generoima Swagger UI, jonka avulla kaikkia rajapinnan toimintoja voidaan testata suoraan selaimesta ilman erillistä frontend-sovellusta.

</br>

<h2>Rajapinnan tarjoamat toiminnot:</h2>

<h3>Huoneet:</h3>
GET /rooms
Palauttaa listan kaikista käytettävissä olevista kokoushuoneista.

<h3>Varaukset:</h3>
GET /bookings
Listaa kaikki varaukset. Varaukset palautetaan järjestettynä päivämäärän ja aloitusajan mukaan.

GET /rooms/{room_id}/bookings
Listaa tietyn huoneen varaukset aikajärjestyksessä.

POST /bookings
Luo uuden varauksen. Varausta luodessa noudatetaan seuraavia sääntöjä:

Varaus ei voi alkaa menneisyydessä
Aloitusajan on oltava ennen lopetusaikaa
Varaukset eivät saa mennä päällekkäin samassa huoneessa
Osallistujamäärän on oltava vähintään 1
Osallistujamäärä ei saa ylittää huoneen kapasiteettia
Tekstikentät (title ja booked_by) eivät saa olla tyhjiä
Tekstikentistä estetään yleisimmät haitalliset syötteet (esim. HTML/script-yritykset ja komentoinjektiot)

DELETE /bookings/{booking_id}
Poistaa varauksen annetun varaus-ID:n perusteella.

</br>

<h3>Toteutusta koskevat huomiot:</h3>

Kaikki data tallennetaan sovelluksen muistiin (in-memory)
Data katoaa, kun sovellus sammutetaan
