# Agricultural Field Monitoring: IoT Smart Irrigation Network

A simulated **IoT smart-irrigation network** for a farm, built in **Cisco Packet Tracer**. Wireless and wired sensors report water level, temperature and humidity to an IoT server. Rules on the server switch five sprinklers on and off automatically. Farmers can watch and control everything from a PC or smartphone at the office or at home, over a simulated WAN and cellular link.

> Group project for **SAIAH 1163 Computer Systems and Networks**, Bachelor in Artificial Intelligence, Universiti Teknologi Malaysia (Semester 2, 2024/2025).

<p align="center">
  <img src="assets/network_topology.png" alt="Packet Tracer topology: field with sensors and sprinklers, office with servers, and home with PCs, smartphones and a cell tower" width="900">
</p>

---

## Problem

Traditional field irrigation depends on hand-watering, weather reports and manual checks. This wastes water through over- or under-watering, and nobody sees soil and weather conditions in real time.

**Goal:** design a network that automates irrigation from live sensor data and allows remote monitoring.

## Network design

The model spans three sites:

| Site | What's there |
|---|---|
| **Field** | 5 lawn sprinklers, 5 water level monitors, temperature sensor + monitor, humidity sensor + monitor, 2 MCUs, wireless router, switch |
| **Office** | IoT server (runs the automation rules), DNS server, PC, switch |
| **Home** | Central office server, cell tower, 2 PCs, 2 smartphones |

The sites are linked through a **router → cloud → cable modem** path, which simulates an ISP connection between separate locations.

**Hybrid topology**

- **Star:** the router is the core hub, and the switches form local stars for the PCs and servers.
- **Shared wireless segment:** the field IoT devices share one Wi-Fi channel through the wireless router.
- **Point-to-point:** router → cloud → cable modem, where each link joins exactly two devices.

<details>
<summary><b>Device configuration</b></summary>

| Component | Role | Connection |
|---|---|---|
| MCU 1 | Temperature sensor + heating (Sun) / cooling (Moon/Rain) elements | Wi-Fi |
| MCU 2 | Humidity sensor | Ethernet |
| Water level monitors | Soil moisture readings | Wi-Fi |
| Sprinklers | Water the field when triggered | Wi-Fi |
| Temperature / humidity monitors | Show live readings | Wi-Fi / Ethernet |
| IoT server | Runs automation rules, hosts the IoT dashboard | Ethernet |
| DNS server | Name resolution inside the network | Ethernet |
| Router | Routes between the LANs and the WAN | Ethernet |
| Cable modem + cloud | WAN / internet link | Coaxial / Ethernet |
| Wireless router | Wi-Fi for field devices | Wired / Wi-Fi |
| Central office server | Remote monitoring and data logging | Ethernet |
| Cell tower | Mobile access for smartphones | Coaxial / cellular |
| PCs, smartphones | Access to the IoT dashboard | Ethernet / cellular |

</details>

## Automation logic

### Sprinkler rules (IoT server)

The thresholds are based on watering guidance for soil at 15–30 cm depth.

| Sprinkler **ON** when any of these is true | Sprinkler **OFF** when any of these is true |
|---|---|
| Water level < 8 cm | Water level > 20 cm |
| Temperature > 35 °C **and** water level < 12 cm | Temperature < 25 °C (night or rain) |
| Humidity < 70 % **and** water level < 15 cm | Humidity > 75 % |

### MCU temperature simulation

[`mcu/temperature_simulation.py`](mcu/temperature_simulation.py) runs on MCU 1. It moves the temperature between **23 °C and 38 °C** in 0.5 °C steps. While the temperature rises it lights the **Sun** element (daytime heating), and while it falls it lights the **Moon/Rain** element (night or rain cooling). This gives the sprinkler rules realistic, changing input.

## Simulation result

In Simulation mode, an HTTP request from PC1 to the IoT server was traced through each layer:

| Layer | Detail |
|---|---|
| Application | HTTP request from PC1 |
| Transport | TCP, source port 1037 → destination port 80 |
| Network | 10.20.30.252 (PC1) → 10.20.30.253 (IoT server) |
| Data link | Ethernet II, `000B.BE80.83A3` → `0030.A33C.A989`, with FCS |
| Physical | FastEthernet0 |

The server de-encapsulates the frame layer by layer and sends the HTTP response back down the same stack.

<p align="center"><img src="assets/pdu_simulation.png" alt="Packet Tracer PDU information at Server IoT showing layers 1 to 7" width="480"></p>

## Running the simulation

1. Install **Cisco Packet Tracer** (free with a Cisco Networking Academy account).
2. Open [`packet-tracer/agricultural_field_monitoring.pkt`](packet-tracer/agricultural_field_monitoring.pkt).
3. On any PC or smartphone, open **Desktop → IoT Monitor** and log in to the IoT server at `10.20.30.253`. The simulation's demo password is `plantelligent`.
4. Watch the sprinklers react as MCU 1 cycles the temperature.
5. Switch to **Simulation** mode to step through packets, as in the result above.

## AI extensions (future work)

The current controller uses fixed thresholds. Next steps from an AI point of view:

- **Predictive analytics:** use regression or decision trees to forecast moisture, temperature and humidity, so irrigation can be scheduled ahead of time.
- **Adaptive control:** replace fixed thresholds with fuzzy logic or reinforcement learning.
- **Anomaly detection:** flag sudden sensor drops or outliers that may mean hardware faults.
- **Crop health from images:** use CNNs on drone or camera images to spot disease, pests or drought stress.
- **Field segmentation:** cluster zones by moisture needs (for example with k-means).

## Project structure

```
├── packet-tracer/
│   └── agricultural_field_monitoring.pkt   # Cisco Packet Tracer network model
├── mcu/
│   └── temperature_simulation.py           # MCU 1 program
├── docs/
│   └── presentation.pdf                    # project slides
└── assets/                                 # images used in this README
```

## My contribution

I was responsible for the **network model**: the topology design, device configuration, and the MCU and IoT automation logic.

## Team (Group 4)

**Jessie Moh Ngiik Jun** · Aryl bin Zulkiflee · Muhammad Zarul Hazman bin Abd Halim · Wafa Wan

Lecturer: Dr. Mohd Azri bin Mohd Izhar

## References

- IBM (2023). *What is the Internet of Things (IoT)?*
- Hamadani, H. et al. (2021). *Traditional Farming Practices and Its Consequences.* Microbiota and Biofertilizers, Vol. 2, 119–128.
- Hoffman, M. (2025). *How much should I water my vegetable garden.* The Tree Trove.
- Mouha, R. A. (2021). *Internet of Things (IoT).* Journal of Data Analysis and Information Processing, 9(2), 77–101.
