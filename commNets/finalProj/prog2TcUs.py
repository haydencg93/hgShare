# prog2TcUs.py
from socket import *
import time

# --- Configuration ---
UDP_SERVER_PORT = 12000 # Port THIS computer listens on
TCP_SERVER_PORT = 13000 # Port the OTHER computer (P1) is listening on

# --- Hybrid Logic ---
def run_hybrid_server_client():
    print("=== PROGRAM 2: UDP Server / TCP Client ===")
    
    # 1. Start UDP Server
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    try:
        udpSocket.bind(('', UDP_SERVER_PORT))
        print(f"[UDP Server] Ready to receive on port {UDP_SERVER_PORT}...")
    except Exception as e:
        print(f"[CRITICAL] Failed to bind UDP port: {e}")
        return

    while True:
        try:
            print("\n[UDP Server] Waiting for message...")
            # 1. Receive message from P1
            message_bytes, clientAddress = udpSocket.recvfrom(1024)
            message = message_bytes.decode()
            
            # Automatically detect P1's IP address from the UDP packet
            p1_ip_address = clientAddress[0]
            
            print(f"[UDP Server] Received '{message}' from {p1_ip_address}")
            
            # --- TCP Client Logic ---
            
            # 2. Reverse the 3-letter message
            reversed_message = message[::-1]
            print(f"[TCP Client] Reversed message: '{reversed_message}'")
            print(f"[TCP Client] Attempting to connect to {p1_ip_address}:{TCP_SERVER_PORT}...")
            
            # 3. Connect to P1 (TCP Server)
            tcpClientSocket = socket(AF_INET, SOCK_STREAM)
            # Set a timeout so we don't hang forever if P1 is blocked
            tcpClientSocket.settimeout(3.0) 
            
            try:
                tcpClientSocket.connect((p1_ip_address, TCP_SERVER_PORT))
                
                # Send reversed message
                tcpClientSocket.send(reversed_message.encode())
                
                # 4. Wait for response from P1
                response_bytes = tcpClientSocket.recv(1024)
                response = response_bytes.decode()
                print(f"[TCP Client] Response from P1: '{response}'")
                
                tcpClientSocket.close()
                
            except Exception as e:
                print(f"[TCP Client] CONNECTION FAILED: {e}")
                print(">>> This usually means Computer A (P1) has a Firewall blocking Port 13000.")
                continue # Skip back to UDP wait
            
            # --- UDP Server Logic Ends ---
            
            # 5. Check response
            if response == "0":
                print("[UDP Server] TCP response was '0' (Invalid). Ignoring.")
            else:
                # 6. Valid response (NUM1,NUM2,NUM3). Calculate Sum.
                print("[UDP Server] TCP response valid. Calculating sum...")
                try:
                    ascii_values = [int(val) for val in response.split(',')]
                    total_sum = sum(ascii_values)
                    final_response = str(total_sum)
                    
                    # 7. Send result back to P1 (UDP Client)
                    udpSocket.sendto(final_response.encode(), clientAddress)
                    print(f"[UDP Server] Sent sum '{final_response}' back to P1.")
                except ValueError:
                    print("[UDP Server] Error parsing numbers.")

        except KeyboardInterrupt:
            print("\nStopping Program 2.")
            break
        except Exception as e:
            print(f"[Error] {e}")
            break

    udpSocket.close()

if __name__ == '__main__':
    run_hybrid_server_client()