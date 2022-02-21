# import socket
# import threading

# # number of bytes in the first message
# HEADER = 64

# # port to run on
# PORT = 5000
# # gets the local IPv4 address
# SERVER = socket.gethostbyname(socket.gethostname())

# ADDRESS = (SERVER, PORT)

# FORMAT = "utf-8"

# DISCONNECT_MESSAGE = "!DISCONNECT"


# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server.bind(ADDRESS)

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     connected = True
#     while connected:
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)

#             if msg == DISCONNECT_MESSAGE:
#                 connected = False

#             print(f"[{addr}] {msg}")
#             conn.send("Msg recieved".encode(FORMAT))
    
#     conn.close()


# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")

#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target=handle_client, args = (conn, addr))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


# print("[STARTING] server is starting...")
# start()

import asyncio
import socket
import websockets
import json

async def handler(websocket):
    print(f'[NEW CONNECTION]') # [NEW CONNNECTION] addr connected
    while True:
        try:
            # event = {"type": "play", "player": "blue", "attack_pile": 1, "defense_pile": 2} # example event
            # await websocket.send(json.dumps(event))
            message = await websocket.recv()
            print(message)
        except websockets.ConnectionClosedOK:
            break


async def main():
    SERVER = socket.gethostbyname(socket.gethostname())
    async with websockets.serve(handler, SERVER, 8001):
        print(f'[STARTING] Server is starting on port {SERVER}')
        await asyncio.Future() # run forever


if __name__ == "__main__":
    asyncio.run(main())

