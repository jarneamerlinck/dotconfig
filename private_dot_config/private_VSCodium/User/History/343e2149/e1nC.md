# Notes
## Adresses can be changed with the hydromet
- a is the address of the slave.
- {} are not part of the command but indicate what can stand there.

| What                            |  Command  | Extra info                                                  |
| ------------------------------- | :-------: | ----------------------------------------------------------- |
| Address Query                   |    ?!     | All devices will anser                                      |
| Acknowledge Active              |    a!     |                                                             |
| Send Identification             |    al!    | request compatible level, firmware version and model nummer |
| Change address of slave         |   aAb!    | b is the new address                                        |
| Start Measurement               |    aM!    |                                                             |
| Additional Measurement Commands | aM{0..9}! |                                                             |
## Addr 
# Geolux RSS 2 300W
(The values heree are the ones that worked on testing)
## SDI12
Command: 1M!

max measured current: 170 mA

number of values: 3
1. x
2. y
3. z

# Geolux water level
## SDI12
Command: 6M!

max measured current: 600 mA

number of values: 8
1. relative level depending on sensor height
2. distance from sensor to water
3. temperature inside device
4. water temperature (on request only)
5. accelerometer angle of device in x direction (on request only)
6. accelerometer angle of device in y direction (on request only)
7. SNR of latest measurement
   
# Nephelo TU
## SDI12
Command: 4M!

max measured current: 3 mA

number of values: 3
1. Temperature
2. Turbidity (NTU)
3. Turbidity (mg/L)

# Nephelo salintiy
## SDI12
Command: 3M!

max measured current: 30 mA

number of values: 2
1. Temperature
2. Conductivity


