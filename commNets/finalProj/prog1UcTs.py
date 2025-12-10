from socket import *
import random
import string
import time
import threading

# --- Configuration ---
UDP_SERVER_PORT = 12000 # Port on the OTHER computer (P2)
TCP_SERVER_PORT = 13000 # Port on THIS computer (P1)

# --- TCP Server Logic ---
def run_tcp_server():
    # Listens for the TCP connection from Program 2.
    
    print("[TCP Server] Starting background service...")
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind to 0.0.0.0 to accept connections from external computers
    try:
        serverSocket.bind(('', TCP_SERVER_PORT))
        serverSocket.listen(5)
        print(f"[TCP Server] Listening on port {TCP_SERVER_PORT}...")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] TCP Server failed to bind: {e}")
        print("Check if the port is already in use or if you have permissions.\n")
        return

    while True:
        try:
            # Accept connection from P2
            connectionSocket, clientAddress = serverSocket.accept()
            print(f"[TCP Server] Connection accepted from {clientAddress[0]}")
            
            # Receive reversed 3-letter message from P2
            message_bytes = connectionSocket.recv(1024)
            message = message_bytes.decode()
            
            # Check for validity: Valid if NO vowels (A, E, I, O, U)
            is_valid = not any(char in 'AEIOUaeiou' for char in message)
            
            response_values = []
            
            if is_valid:
                print(f"[TCP Server] Message '{message}' is VALID (no vowels). Sending data.")
                # Calculate response: ASCII of each letter + 41
                for char in message:
                    val = str(ord(char) + 41)
                    response_values.append(val)
                
                # Format: "NUM1,NUM2,NUM3"
                response_message = ",".join(response_values)
            else:
                print(f"[TCP Server] Message '{message}' is INVALID (contains vowels). Sending 0.")
                response_message = "0"
            
            connectionSocket.send(response_message.encode())
            connectionSocket.close()
            
        except Exception as e:
            print(f"[TCP Server] Error: {e}") 

# --- UDP Client Logic ---
def run_udp_client(server_ip):
    # Sends random messages to P2 until a valid response is received.
    print("\n[UDP Client] Starting...")
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    # 4 second timeout for slow networks/human reflexes
    clientSocket.settimeout(4.0) 
    
    response_received = False
    
    while not response_received:
        message = generate_random_message()
        print("-" * 50)
        print(f"[UDP Client] Generated message: '{message}'")
        
        # Check validity locally just for the log
        # P2 reverses it, but 'no vowels' applies same forward or backward
        expect_valid = not any(char in 'AEIOUaeiou' for char in message)
        status_str = "Expect Reply" if expect_valid else "Expect Timeout (Invalid)"
        
        print(f"[UDP Client] Sending to {server_ip}:{UDP_SERVER_PORT} ({status_str})...")
        
        try:
            # Send the random 3-letter message to P2
            clientSocket.sendto(message.encode(), (server_ip, UDP_SERVER_PORT))
            
            # Wait for the aggregated sum response from P2
            modifiedMessage_bytes, serverAddress = clientSocket.recvfrom(1024)
            modifiedMessage = modifiedMessage_bytes.decode()
            
            print(f"[UDP Client] **SUCCESS!** Received final sum from P2: '{modifiedMessage}'")
            response_received = True
            
        except timeout:
            if expect_valid:
                print("[UDP Client] TIMEOUT on VALID message!")
                print(">>> POSSIBLE CAUSE: Firewall is blocking Port 13000 on THIS computer.")
                print(">>> CHECK: Can Program 2 connect back to this IP?")
            else:
                print("[UDP Client] No response (Timeout). Message was invalid (Expected).")
            
            time.sleep(1) 
        
        except Exception as e:
            print(f"[UDP Client] Error: {e}")
            break

    clientSocket.close()
    print("\n[Program 1] Task successfully completed. Shutting down.")

def generate_random_message():
    # Generates a random 3-letter message.
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(3))

def get_local_ip():
    try:
        # Find the local IP connected to the internet
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# --- Main Execution ---
if __name__ == '__main__':
    print("=== PROGRAM 1: UDP Client / TCP Server ===")
    
    local_ip = get_local_ip()
    print(f"INFO: This computer's IP address is: {local_ip}")
    print("Ensure Program 2 can reach this IP address.\n")
    
    # Start the TCP Server thread immediately
    tcp_thread = threading.Thread(target=run_tcp_server)
    tcp_thread.daemon = True 
    tcp_thread.start()
    
    # Give the TCP server a moment to start up
    time.sleep(1)
    
    # Ask user for the OTHER computer's IP
    target_ip = input("Enter IP Address of Program 2 (UDP Server): ").strip()
    
    if not target_ip:
        target_ip = "127.0.0.1"
    
    # Run the UDP client logic
    run_udp_client(target_ip)