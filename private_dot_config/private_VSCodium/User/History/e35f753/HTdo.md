# Opinion Hydromet/Bausch


## Bausch

+ Compacter dan hydromet
+ GUI is sneller te navigeren dan de hydromet
+ Heeft 150mA voor sensors aan te sturen over SDI12 (ipv de 100 van de hydromet)


- Geen digital output
- Geen MQTT
- Specifieke kabel voor debuggen
- Niet gemakkelijk om SDI12 sensors aan te spreken via CLI
- Je moet weten hoeveel waardes een SDI12 sensor doorstuurd om iets van de sensor te kunnen lezen
- Bekabeling niet echt logisch
- Zonder externe voeding heb je een specifieke batterij nodig
  - Met condensator om de opstart stroom te kunnen leveren

## Hydromet

+ Gemakkelijker configureren
  + Standaard kabel voor te verbinden
  + Putty of app gebruiken
+ Bluetooth mogelijk voor op locatie de values te zien of configuratie te backuppen/aanpassen
+ Mogelijk om rechtstreeks naar de sensors commando's te sturen
+ Geen apparte app nodig voor configuratie te updaten
+ Mogelijkheid op sneller te meten bij alarm
+ Poortnamen zichtbaar op logger
+ Je kan enkel de eerstse van de SDI12 waarden opvragen zonder te weten hoeveel er na komen


- Modbus niet gemakkelijk om op te zetten
- Sommige instelling zijn niet zo gemakkelijk te vinden
    
