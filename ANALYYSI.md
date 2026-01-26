# 1. Mitä tekoäly teki hyvin?
Tekoäly osaasi hyvin vähäiselläkin ohjeistuksella tehdä toimivan ja ehdot täyttävän kokonaisuuden. 
Koodi oli alusta asti siistiä ja helposti luettavaa ja
tekoälyn virheenkäsittely ja virheviestit olivat toimivia ja kuvaavia. 
Myös tekoälyn ohjeistukset siinä, kuinka projektin kanssa kannattaisi jatkaa olivat avuliaita ja loogisia.


# 2. Mitä tekoäly teki huonosti?
Tekoäly lisäsi huoneisiin ominaisuuksia, joita se ei kuitenkaan implementoinut koodiin. Ominaisuudet olivat siis tekoälyn lopullisessa koodissa turhia.
Tekoäly ei myöskään ottanut huomioon joitakin kriittisiä asioita ollenkaan, kuten tietoturvaa.
Koodissa oli lisäksi joitain logiikkavirheitä. Oli esimerkiksi mahdollista, että kahdella varauksella oli joissain tilanteissa sama ID.


# 3. Mitkä olivat tärkeimmät parannukset, jotka teit tekoälyn tuottamaan koodiin ja miksi?
ID logiikan parantelut oli selkeä logiikan korjaus. Kahdella varauksella ei tietenkään missään tapauksessa saa olla sama ID.
Lopputuloksena voisi olla, että esimerkiksi väärä varaus poistettaisiin järjestelmästä.
Kiinnitin myös huomiota tietoturvallisuuteen. Käyttäjien antamat merkkijonot käydään läpi ja tarkastetaan koodiin viittaavien merkkien varalta. Oikeassa tietokannassa, jossa käsitellään sähköposteja, tunnuksia ja salasanoja tämä on erityisen tärkeää.
Lisäsin myös lisää tunnistetietoja ja testauksia varaajasta ja varattavasta huoneesta. Esimerkiksi varaajan täytyy antaa nimensä varaukseen ja varauksen aihe. Lisäksi tarkastetaan montako ihmistä varauksen kautta huoneeseen tulee ja ylittääkö se huoneen kapasiteetin. Kaikki ovat oikeaa varausta tehtäessä tärkeitä tietoja.