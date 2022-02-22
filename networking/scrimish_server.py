import asyncio
import socket
import websockets
import json
from scrimish_server_utils import generate_game_id, generate_user_id

USERS = []
GAME_LIST = [
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Expert', 'speed': 'Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Intermediate', 'speed': 'Very Fast', 'connections': [] },
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Expert', 'speed': 'Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Intermediate', 'speed': 'Very Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Expert', 'speed': 'Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Intermediate', 'speed': 'Very Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Expert', 'speed': 'Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Intermediate', 'speed': 'Very Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Expert', 'speed': 'Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Intermediate', 'speed': 'Very Fast', 'connections': []},
    # { 'id': generate_game_id(GAME_ID_LIST), 'level': 'Beginner', 'speed': 'Slow','connections': []}
]

class User:
    def __init__(self, user_id, websocket) -> None:
        self.user_id = user_id
        self.websocket = websocket

    
    def get_user_id(self) -> str:
        return self.user_id
    

    def get_socket(self):
        return self.ws


def new_connection(websocket) -> int:
    user_id = generate_user_id(USERS);
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


async def process_event(user_id, event, websocket):

    eventObj = json.loads(event)

    if eventObj.get('type') == 'move':
        print(str(eventObj))
        await websocket.send(json.dumps(eventObj))

    elif eventObj.get('type') == 'msg':
        print(eventObj.get('text'))

    elif eventObj.get('type') == 'new game':
        # Get available ids
        available_game_ids = []
        for game in GAME_LIST:
            available_game_ids.append(game.get('id'))

        id = generate_game_id(available_game_ids) # generate id

    
        GAME_LIST.append({'id': id, 'level': eventObj.get('level'), 'speed': eventObj.get('speed'), 'connections': [websocket]})

        print(f'[GAME CREATED] - {user_id} created game {id}')

    elif eventObj.get('type') == 'join':
        print(f'[GAME JOINED] - {user_id} joined game {eventObj.get("id")}')

    elif eventObj.get('type') == 'query':
        answer = {}
        if eventObj.get('dataType') == 'available games':
            resulting_list = []
            for game in GAME_LIST :
                game = {'id': game.get('id'), 'level': game.get('level'), 'speed': game.get('speed'), 'connections': len(game.get('connections'))}
                resulting_list.append(game)
            
            answer = {'type': eventObj.get('dataType'), 'data': resulting_list}
        
        await websocket.send(json.dumps(answer))

        print(f'[QUERY] value is {answer}')

    else:
        raise Exception(f'Illegal event type! ({eventObj.get("type")})')


async def handler(websocket):
    user_id = new_connection(websocket)
    while True:
        try:
            event = await websocket.recv()
            await process_event(user_id, event, websocket)
            
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
