
import controller as ctrl



# Fazer TESTE DE QUEUE
# colocar um time sleep no código do servidor e verificar como se comporta quando mais de um client tenta se comunicar.
# mudar o numero da queue nos testes para ver como se comporta.

### SERVER CODE ###

# Erro de "too many requests" acontece na AUTENTICAÇÃO
# Solução: fazer uma autenticação por hora do cob.write e do cob.read
# Guardar em um file o token e o horário da última renovação
# Quando faltar menos de 5 minutos para acabar a validade do token, renova ambos o cob.write e o cob.read




# SERVER SIDE #

import socket
import threading
import json
import time
import datetime
import csv


# Function to handle "create_pix" request

# implement "rpi_key"? public key to authenticate?? or not?
def handle_create_pix(rpi_key, price):

    # Make a verification for the raspberry pis (using this "rpi_key")

    pix_qrcode_copiaecola, pix_txid = ctrl.create_pix(price)

    print("handle_create_pix "+rpi_key+" "+str(price))

    response = {"pix_qrcode_copiaecola": pix_qrcode_copiaecola,
                "pix_txid": pix_txid}

    return response


# Function to handle "cob_read" request (placeholder)
def handle_verify_status_pix(rpi_key, txid):
    # Placeholder for actual implementation

    status_cob_pix = ctrl.verify_status_pix(txid)

    print("handle_verify_status_pix " + rpi_key + " " + txid)

    response = {"status_cob_pix": status_cob_pix}

    return response


# Function to handle "auth_rpi" request (placeholder)
def handle_auth_rpi(param1, param2):
    # Placeholder for actual implementation
    pass


# Function to handle "telemetry_get" request (placeholder)
def handle_telemetry_get(param1, param2):
    # Placeholder for actual implementation
    pass

def handle_ping(rpi_key, param2):
    print("handle_ping " + rpi_key)

    response = {"ping": "OK"}

    return response


# Function to handle client requests
def handle_client(conn, addr):
    print(f"Connected to {addr}")

    while True:
        try:
            # Receive request from client
            data = conn.recv(1024).decode()
            if not data:
                break

            # Parse request
            request = json.loads(data)
            request_type = request.get("type")
            param1 = request.get("param1")
            param2 = request.get("param2")

            # Handle request based on type
            if request_type == "create_pix":
                response = handle_create_pix(param1, param2)
            elif request_type == "cob_read":
                response = handle_verify_status_pix(param1, param2)
            elif request_type == "auth_rpi":
                response = handle_auth_rpi(param1, param2)
            elif request_type == "telemetry_get":
                response = handle_telemetry_get(param1, param2)
            elif request_type == "ping":
                response = handle_ping(param1, param2)
            else:
                response = {"error": "Invalid request type"}

            # Send response to client

            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(f"Error processing request: {e}")
            break

    # Close connection
    conn.close()
    print(f"Connection with {addr} closed")


# Function to handle updates and email sending at midnight
def daily_update():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            # Perform daily updates (e.g., update CSV file, send email)
            update_csv()
            send_email()
            # Wait until next midnight
            time.sleep(60)
        else:
            # Check again in 1 minute
            time.sleep(60)


def token_auto_update():
    while True:

        ctrl.update_auth_token()

        # Update once every 30 minutes (token should expire in 60 minutes, so we update it earlier)
        time.sleep(1800)



# Function to update CSV file (placeholder)
def update_csv():
    # Placeholder for actual implementation
    pass


# Function to send email (placeholder)
def send_email():
    # Placeholder for actual implementation
    pass


# Main function
def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to AWS elastic IP and port 8080
    server_socket.bind(('18.230.15.249', 8080))

    # Set the maximum number of queued connections
    server_socket.listen(5)

    print("Server is listening for connections...")

    # Start a thread for daily updates
    update_thread = threading.Thread(target=daily_update)
    update_thread.start()

    token_update_thread = threading.Thread(target=token_auto_update)
    token_update_thread.start()

    # Handle incoming connections
    while True:
        # Accept connection from client
        conn, addr = server_socket.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


if __name__ == "__main__":
    main()


