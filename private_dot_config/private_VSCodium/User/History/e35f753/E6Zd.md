# Opinion Hydromet/Bausch


## Bausch

+ Compacter dan hydromet
  + Gemakklijk te monteren
+ GUI is sneller te navigeren dan de hydromet
+ Heeft 150mA piek voor sensors aan te sturen over SDI12 (ipv de 100 van de hydromet)


- Geen digital output
- Geen MQTT
- Specifieke kabel voor debuggen
- Niet gemakkelijk om SDI12 sensors aan te spreken via CLI
- Je moet weten hoeveel waardes een SDI12 sensor doorstuurd om iets van de sensor te kunnen lezen
- Bekabeling (Kleuren) niet echt logisch 
- Zonder externe voeding heb je een specifieke batterij nodig
  - Met condensator om de opstart stroom te kunnen leveren
  - Heeft 3.6V nodig
- Manual beknopt
- Power is niet reverse polarity protected

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
+ Gemakklijk te bekabelen
+ Ondersteund ook en aantal andere protocolen naast modbus en SDI12


- Modbus niet gemakkelijk om op te zetten
- Sommige instelling zijn niet zo gemakkelijk te vinden
    


[Option boards](https://www.ydoc.biz/datalogger-option-boards.html)
[MQTT bridge](https://www.ydoc.biz/datalogger-MQTT-COM-BRIDGE.html)
[remote config](https://www.ydoc.biz/datalogger-remote-configuration.html)

Serial number hydromet: 110052556
mogelijk om:
- Scheduled remote connections
- MQTT-Com-tunnel
  - Only at datalog intervall
    - upload an config with faster interval before sending commands to skip 15min delay
  - Send commands to COM devices
  - `YDOC/<device serial number>/comtx/<port>[/<client defined sup-topics]” (QoS=1)`
  - The data logger will publish the reply with the same topic as the command, but will replace the text “comtx” with “comrx”
  - `When a COM-tunnel message is received destined for a device connected at a serial sensor port and the device requires power from the 12V sensor power switch, the data logger will switch on the 12V power and wait a certain warm-up time before sending the command to the device. The warm-up time will not be applied in case of sequential commands in the same MQTT-session.`
    - So only for SDI12 or modbus (no alarm output yet)
    - If sampler has SDI12 or modbus ok problem solved
    - UART optional board
      - send high for atleast 25ms
      - 0x255




