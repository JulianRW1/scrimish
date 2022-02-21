import asyncio
import socket
import websockets
import json

USERS = []

class User:
    def __init__(self, user_id, websocket) -> None:
        self.user_id = user_id
        self.websocket = websocket

    
    def get_user_id(self):
        return self.user_id
    

    def get_socket(self):
        return self.ws
        

def new_connection(websocket) -> int:
    if len(USERS):
        user_id = USERS[-1].get_user_id() + 1;
    else:
        user_id = 0;
    USERS.append(User(user_id, websocket))
    print(f'[NEW CONNECTION] user {user_id} connected') # [NEW CONNNECTION] addr connect
    print(f'[ACTIVE CONNECTION] {len(USERS)}')
    return user_id


def disconnection(user_id):
    for user in USERS:
        if user.get_user_id() == user_id:
            print(f"[DISCONNECTED] - user {user_id} disconnected")
            USERS.remove(user)
            break
    print(f'[ACTIVE CONNECTIONS] {len(USERS)}')


async def process_event(event, websocket):

    eventObj = json.loads(event)

    if eventObj['type'] == "move":
        print(str(eventObj) +  " --- " + eventObj['type'])
        await websocket.send(json.dumps(event))
        # print(message)
    elif eventObj['type'] == "msg":
        print(eventObj['text'])
        
    else:
        raise Exception("Illegal event type!")


async def handler(websocket):
    user_id = new_connection(websocket)
    while True:
        try:
            event = await websocket.recv()
            await process_event(event, websocket)
            
        except websockets.ConnectionClosedOK or websockets.ConnectionResetError:
            disconnection(user_id)
            break


async def main():
    SERVER = socket.gethostbyname(socket.gethostname())
    async with websockets.serve(handler, SERVER, 8001):
        print(f'[STARTING] Server is starting on port {SERVER}')
        await asyncio.Future() # run forever


if __name__ == "__main__":
    asyncio.run(main())
