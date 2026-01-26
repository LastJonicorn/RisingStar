# 1. Mitä tekoäly teki hyvin?
-Tekoäly osaasi hyvin vähäiselläkin promptaamisella tehdä toimivan ja ehdot täyttävän kokonaisuuden.

-Virheidentarkistukset toimivat jo tekoälyn tuottamassa koodissa hyvin.

-Koodi oli alusta asti siistiä ja helposti luettavaa.

-Tekoälyn virheenkäsittely ja virheviestit olivat toimivia ja kuvaavia.


# 2. Mitä tekoäly teki huonosti?
-Tekoäly lisäsi huoneisiin ominaisuuksia, joita se ei kuitenkaan implementoinut koodiin. Ominaisuudet olivat siis tekoälyn lopullisessa koodissa turhia.

-Tekoäly ei ottanut huomioon joitakin kriittisiä asioita ollenkaan, kuten tietoturvaa.

-Tekoälyn luomassa koodissa oli joitain logiikkavirheitä. Oli esimerkiksi mahdollista, että kahdella varauksella oli joissain tilanteissa sama ID.


# 3. Mitkä olivat tärkeimmät parannukset, jotka teit tekoälyn tuottamaan koodiin ja miksi?
-ID logiikan parantelut. Kahdella varauksella ei tietenkään missään tapauksessa saa olla sama ID.

-Tietoturvallisuus. Käyttäjien antamat merkkijonot käydään läpi ja tarkastetaan koodin varalta. Oikeassa tietokannassa, jossa käsitellään sähköposteja, tunnuksia ja salasanoja erityisen tärkeää.

-Lisäsin lisää tunnistetietoja ja testauksia varaajasta ja varattavasta huoneesta. Esimerkiksi varaajan täytyy antaa nimensä varaukseen ja varauksen aihe. Lisäksi tarkastetaan montako ihmistä varauksen kautta huoneeseen tulee ja ylittääkö se huoneen kapasiteetin. Oikeassa varauksessa tärkeitä tietoja kokoushuonetta varatessa.