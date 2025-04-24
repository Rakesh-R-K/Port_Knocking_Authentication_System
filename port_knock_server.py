import socket
import struct
import time

def log(msg):
    print(f"{time.ctime()} - {msg}")

def process_packet(packet):
    try:
        # Unpack IP header (first 20 bytes)
        ip_header = packet[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])
        protocol = iph[6]

        if protocol != 6:  # Only TCP packets
            return

        # TCP header starts from byte 20 to 40
        tcp_header = packet[20:40]
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)
        src_port = tcph[0]
        dst_port = tcph[1]

        log(f"[>] TCP Connection Request: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

    except Exception as e:
        log(f"[!] Error: {e}")

def monitor_connections():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    log("[*] TCP connection monitor started...")

    while True:
        packet, _ = s.recvfrom(65565)
        process_packet(packet)

if __name__ == "__main__":
    try:
        monitor_connections()
    except KeyboardInterrupt:
        log("[!] Exiting monitor.")

