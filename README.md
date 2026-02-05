# 📡 Reliable UDP Data Transfer with Go-Back-N & AIMD Congestion Control

## 📌 Overview

This project implements a **reliable data transfer protocol over UDP** using:

- Go-Back-N retransmission
- Sliding window protocol
- Cumulative acknowledgments
- AIMD (Additive Increase Multiplicative Decrease) congestion control

The client reliably sends **10,000 packets** to a UDP server that simulates a bottleneck link with configurable:

- Link capacity
- Round-trip delay (RTT)
- Packet error rate (PER)
- Finite buffer size

Developed as part of a Communication Networks assignment on reliable transport and congestion control.

---

## 🎯 Features

### Reliable Data Transfer
- Sequence-numbered packets
- Cumulative ACK handling
- Timeout-based loss detection
- Go-Back-N retransmission
- Sliding window sender

### Congestion Control
- Dynamic congestion window (cwnd)
- Additive Increase on ACK
- Multiplicative Decrease on timeout
- Adaptive sending rate

### Network Simulation (Server)
The server simulates:

- RTT delay
- Packet loss probability
- Drop-tail finite buffer
- Fixed link capacity (packets/sec)

---

## 🗂 Project Structure

```
.
├── UDPclient.py
├── server-gbn.py
├── commnet_2.pdf
├── ee5110-assignment-2.pdf
└── README.md
```

- `UDPclient.py` — Reliable UDP client with congestion control  
- `server-gbn.py` — Bottleneck link + cumulative ACK server  
- `commnet_2.pdf` — One-page report (strategy + results)  
- `ee5110-assignment-2.pdf` — Assignment specification  

---

## ⚙️ Protocol Design

### Packet Format

```
4 bytes — Sequence Number (Big Endian unsigned int)
payload — optional
```

Server processes packets instantly and sends **cumulative ACKs**.

---

## 🔁 Go-Back-N Logic

- Sender maintains sliding window
- Sends packets up to congestion window size
- Uses cumulative ACKs
- On timeout → retransmit from last unacknowledged packet

---

## 📈 Congestion Control — AIMD

| Event | cwnd Update |
|--------|-------------|
| ACK received | cwnd = cwnd + 1 |
| Timeout | cwnd = cwnd / 2 |

This ensures:

- Fast growth under good conditions
- Quick reduction under congestion
- Stable throughput

---

## 🚀 How to Run

### Start Server

```
python server-gbn.py <IP> <PORT> <CAPACITY> <RTT_ms> <PER> <BUFFER_SIZE>
```

Example:

```
python server-gbn.py 127.0.0.1 9000 1000 100 0 100
```

---

### Start Client

```
python UDPclient.py <SERVER_IP> <PORT>
```

Example:

```
python UDPclient.py 127.0.0.1 9000
```

---

## 📊 Experimental Results

| Capacity | RTT | PER | Buffer | Throughput |
|------------|--------|------|-----------|---------------|
| 1000 pps | 100 ms | 0% | 100 | 639.14 pps |
| 1000 pps | 100 ms | 0% | 10 | 88.08 pps |
| 10 pps | 1 ms | 0% | 1 | 9.57 pps |
| 10 pps | 1 ms | 10% | 10 | 5.36 pps |

---

## 🧠 Key Concepts Demonstrated

- Reliable transport over UDP
- Sliding window protocols
- Go-Back-N ARQ
- Congestion avoidance
- AIMD control
- Bottleneck link simulation
- Throughput measurement

---

## 🛠 Requirements

- Python 3.x
- No external dependencies

---

## 📘 Academic Context

Course: Communication Networks (IIT Madras) 
Assignment: Reliable Data Transfer & Congestion Control

Includes:

- UDP reliable client
- Congestion control implementation
- Experimental evaluation
- Performance report

---

## 📜 License

MIT License — free to use for learning and experimentation.
