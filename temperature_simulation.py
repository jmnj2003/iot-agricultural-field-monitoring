# MCU 1 program (Cisco Packet Tracer, Python)
# Simulates daily temperature swings between 23°C and 38°C.
# Pin 1 = Sun LED (heating), Pin 2 = Moon/Rain LED (cooling).
from gpio import *
from time import *


def main():
    pinMode(1, OUT)  # Sun LED
    pinMode(2, OUT)  # Moon LED
    temp = 23  # Start from 23°C
    rising = True
    print("Simulated Temperature")

    while True:  # Main cycle: 23°C to 38°C oscillation
        if rising:
            if temp < 38:
                temp += 0.5
                digitalWrite(1, HIGH)
                digitalWrite(2, LOW)
            else:
                rising = False  # Start cooling
        else:
            if temp > 23:
                temp -= 0.5
                digitalWrite(1, LOW)
                digitalWrite(2, HIGH)
            else:
                rising = True  # Start heating again
        print("Temperature:", temp)
        delay(2250)


if __name__ == "__main__":
    main()
