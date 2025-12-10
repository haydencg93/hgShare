from socket import *
import time

# --- Configuration ---
UDP_SERVER_PORT = 12000  # Port THIS computer listens on (UDP)
TCP_SERVER_PORT = 13000  # Port the OTHER computer (P1) is listening on (TCP)

# --- Helper Functions ---
def get_local_ip():
    """
    Retrieves the local IP address to display at startup.
    Matches the style of Program 1.
    """
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# --- TCP Client Logic ---
def run_tcp_client(target_ip, message):
    """
    Connects to Program 1 (TCP Server), sends the reversed message,
    and returns the response (list of numbers or '0').
    """
    # 1. Reverse the message
    reversed_message = message[::-1]
    print(f"[TCP Client] Reversed message: '{reversed_message}'")
    print(f"[TCP Client] Connecting to {target_ip}:{TCP_SERVER_PORT}...")

    tcpClientSocket = socket(AF_INET, SOCK_STREAM)
    tcpClientSocket.settimeout(4.0)  # Match timeout style of Prog 1

    try:
        tcpClientSocket.connect((target_ip, TCP_SERVER_PORT))
        
        # Send reversed message
        tcpClientSocket.send(reversed_message.encode())
        
        # Wait for response (The list of numbers or "0")
        response_bytes = tcpClientSocket.recv(1024)
        response = response_bytes.decode()
        
        print(f"[TCP Client] Response from P1: '{response}'")
        tcpClientSocket.close()
        return response

    except Exception as e:
        print(f"[TCP Client] CONNECTION FAILED: {e}")
        print(">>> CHECK: Is Program 1 running? Is Firewall blocking Port 13000?")
        return None

# --- UDP Server Logic ---
def run_udp_server():
    # Listen for the initial UDP message from Program 1,
    # to trigger the TCP Client, calculate the sum, and reply.
    
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    
    try:
        udpSocket.bind(('', UDP_SERVER_PORT))
        print(f"[UDP Server] Listening on port {UDP_SERVER_PORT}...")
    except Exception as e:
        print(f"[CRITICAL] Failed to bind UDP port: {e}")
        return

    while True:
        try:
            print("\n" + "-"*50)
            print("[UDP Server] Waiting for message from Program 1...")
            
            # Receive message from P1
            message_bytes, clientAddress = udpSocket.recvfrom(1024)
            message = message_bytes.decode()
            p1_ip_address = clientAddress[0]
            
            print(f"[UDP Server] Received '{message}' from {p1_ip_address}")

            # Hand off to TCP Client Logic
            tcp_response = run_tcp_client(p1_ip_address, message)

            # Process the response
            if tcp_response is None:
                print("[UDP Server] TCP handshake failed. Aborting this transaction.")
            elif tcp_response == "0":
                print("[UDP Server] TCP response was '0' (Invalid Message). Ignoring.")
            else:
                # Valid response (NUM1,NUM2,NUM3). Calculate Sum.
                print("[UDP Server] TCP response valid. Calculating sum...")
                try:
                    ascii_values = [int(val) for val in tcp_response.split(',')]
                    total_sum = sum(ascii_values)
                    final_response = str(total_sum)
                    
                    # Send result back to P1 (UDP Client)
                    udpSocket.sendto(final_response.encode(), clientAddress)
                    print(f"[UDP Server] **SUCCESS!** Sent sum '{final_response}' back to P1.")
                except ValueError:
                    print("[UDP Server] Error parsing numbers from TCP response.")

        except KeyboardInterrupt:
            print("\n[Program 2] Stopping...")
            break
        except Exception as e:
            print(f"[Error] {e}")
            break

    udpSocket.close()

# --- Main Execution ---
if __name__ == '__main__':
    print("=== PROGRAM 2: UDP Server / TCP Client ===")
    
    local_ip = get_local_ip()
    print(f"INFO: This computer's IP address is: {local_ip}")
    print("Ensure Program 1 sends to this IP address.\n")

    # Start the main server loop
    run_udp_server()