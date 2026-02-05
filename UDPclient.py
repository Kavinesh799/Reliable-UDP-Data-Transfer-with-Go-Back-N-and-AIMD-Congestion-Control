import socket
import struct
import time
import threading

# Configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
TOTAL_PACKETS = 500
TIMEOUT = 0.5  # Timeout duration in seconds
ALPHA = 1  # Additive increase factor
BETA = 0.5  # Multiplicative decrease factor
receive_buffer=10

# Congestion control
cwnd = 1  # Congestion window (in packets)
base = 0  # Tracks the lowest unacknowledged packet
next_seq_num = 0  # Next packet to send
lock = threading.Lock()
acked_event = threading.Event()

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

def send_packets():
    global next_seq_num, base, cwnd
    while base < TOTAL_PACKETS:
        with lock:
            while next_seq_num < base + cwnd and next_seq_num < TOTAL_PACKETS:
                #acked_event.wait()
                packet = struct.pack("!I", next_seq_num)
                client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                print(f"Sent Packet {next_seq_num}")
                next_seq_num += 1
                
        #time.sleep(0.01)  # Small delay to prevent overloading network
        # Restart transmission in case of a timeout
        # #acked_event.set()
        # if next_seq_num == base:
        #     print("Restarting transmission after timeout...")  
        #     next_seq_num = base  # Reset and retransmit packets

def receive_acks():
    global base, cwnd, next_seq_num
    while base < TOTAL_PACKETS:
        if base!=next_seq_num:
            try:
                ack_packet, _ = client_socket.recvfrom(4)
                ack_num = struct.unpack("!I", ack_packet)[0]
                
                with lock:
                    if ack_num >= base:
                        print(f"Received ACK {ack_num}")
                        base = ack_num + 1
                        if cwnd<receive_buffer:
                            cwnd += ALPHA  # Additive increase
                        acked_event.set()  # Notify sender
            except socket.timeout:
                with lock:
                    #acked_event.clear()
                    print("Timeout! Multiplicative Decrease.")
                    cwnd = max(1, int(cwnd * BETA))  # Multiplicative decrease
                    next_seq_num = base  # Retransmit from base
                    print("Retransmitting from", base)
                    #send_thread.join()
                    #acked_event.set()

# Start sender and receiver threads
send_thread = threading.Thread(target=send_packets)
recv_thread = threading.Thread(target=receive_acks)
start_time=time.time()
#acked_event.set()
send_thread.start()
recv_thread.start()
send_thread.join()
recv_thread.join()

# Calculate and print average throughput
end_time = time.time()
total_time = end_time - start_time
throughput = TOTAL_PACKETS / total_time
print(f"All packets sent successfully.")
print(f"Average Throughput: {throughput:.2f} packets per second")

client_socket.close()