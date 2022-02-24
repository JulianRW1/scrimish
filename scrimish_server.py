import asyncio
import socket
import player
from scrimish import Scrimish
import websockets
import json
from scrimish_server_utils import generate_game_id, generate_user_id

USERS = []
CREATED_GAMES = {}
    # {'lkjlkjlkjlkj' : (Scrimish('level', 'speed', Player(), Player()), ['connected])}
GAMES_IN_PROGRESS = {}

class User:
    def __init__(self, user_id, websocket) -> None:
        self.user_id = user_id
        self.websocket = websocket

    
    def get_user_id(self) -> str:
        return self.user_id
    

    def get_socket(self):
        return self.ws


def get_realms_as_letters(game_id):
    game, connected, creator = GAMES_IN_PROGRESS[game_id]

    red_realm_output = []
    red_realm = game.red_player.realm.get_realm()
    for pile in range(len(red_realm)):
        red_realm_output.append([])
        for card in red_realm[pile]:
            red_realm_output[pile].append('r_' + card.to_string())

    blue_realm_output = []
    blue_realm = game.blue_player.realm.get_realm()
    for pile in range(len(blue_realm)):
        blue_realm_output.append([])
        for card in blue_realm[pile]:
            blue_realm_output[pile].append('b_' + card.to_string())

    return red_realm_output, blue_realm_output


async def join(websocket, game_id, user_id):

    try:
        game, connected, creator = CREATED_GAMES[game_id]
    except KeyError:
        # TODO - send error message
        return

    connected.append(websocket)

    if (len(connected) < 2):
        del CREATED_GAMES[game_id]
        print('[ERROR] - Not enough players connected')
        return



    # Transfer game to in progress list
    GAMES_IN_PROGRESS[game_id] = CREATED_GAMES[game_id]
    del CREATED_GAMES[game_id]

    
    print(f'[GAME JOINED] - {user_id} joined game {game_id}')

    await websocket.send(json.dumps({'type': 'joined game', 'id': game_id}))

    websockets.broadcast(connected, json.dumps({'type': 'redirect', 'url': ('?game=' + game_id)}))

    # # give the first player the color blue
    # await connected[0].send(json.dumps({'type': 'player color', 'color': 'Blue'})) 
    # # give the second player the color red
    # await connected[1].send(json.dumps({'type': 'player color', 'color': 'Red'})) 
    # # TODO - ^ implement this on client


    # red_realm_output, blue_realm_output = get_realms_as_letters(game_id)
            
    # answer = {'type': 'realms', 'redRealm': red_realm_output, 'blueRealm': blue_realm_output}
                
    # websockets.broadcast(connected, json.dumps(answer))

    try:
        async for message in websocket:
            print('player sent', message)
    finally:
        connected.remove(websocket)


def new_connection(websocket) -> int:
    user_id = generate_user_id(USERS);
    USERS.append(User(user_id, websocket))
    print(f'[NEW CONNECTION] user {user_id} connected') # [NEW CONNNECTION] addr connect
    print(f'[ACTIVE CONNECTION] {len(USERS)}')
    return user_id


def disconnection(user_id):
    for user in USERS:
        if user.get_user_id() == user_id:
            # print(f"[DISCONNECTED] - user {user_id} disconnected")
            USERS.remove(user)
            break
    print(f'[ACTIVE CONNECTIONS] {len(USERS)}')


async def process_event(user_id, event, websocket):

    eventObj = json.loads(event)

    if eventObj.get('type') == 'move':
        print(str(eventObj))
        await websocket.send(json.dumps(eventObj))

    elif eventObj.get('type') == 'msg':
        print('[MESSAGE] ' + eventObj.get('text'))

    elif eventObj.get('type') == 'new game':
        print(f'[CREATED GAMES] - {CREATED_GAMES}')
        # Get available ids
        available_game_ids = []
        for game, connected, creator in CREATED_GAMES.values():
            available_game_ids.append(game.id)

        id = generate_game_id(available_game_ids) # generate id

        CREATED_GAMES[id] = (Scrimish(id, eventObj.get('level'), eventObj.get('speed')), [websocket], user_id)
        
        print(f'[GAME CREATED] - {user_id} created game {id}')

    elif eventObj.get('type') == 'join':
        await join(websocket, eventObj.get('id'), user_id)

    elif eventObj.get('type') == 'query':
        if eventObj.get('dataType') == 'available games':
            resulting_list = []
            for game, connected, creator in CREATED_GAMES.values():
                _game = {'id': game.id, 'level': game.level, 'speed': game.speed}
                resulting_list.append(_game)
            
            answer = {'type': eventObj.get('dataType'), 'data': resulting_list}

        if eventObj.get('dataType') == 'init game state':
            
            try :
                game, connected, creator = GAMES_IN_PROGRESS[eventObj.get('game_id')]
                print('-------------------' + str(GAMES_IN_PROGRESS) + '________________')
            except KeyError:
                print('game not found')
                await websocket.send(json.dumps({'type': 'redirect', 'url': '/'}))
                return

            # give the first player the color blue
            if user_id == creator:
                await websocket.send(json.dumps({'type': 'player color', 'color': 'Blue'})) 
            else:
                # give the second player the color red
                await websocket.send(json.dumps({'type': 'player color', 'color': 'Red'})) 

            red_realm_output, blue_realm_output = get_realms_as_letters(eventObj.get('game_id'))
            
            answer = {'type': eventObj.get('dataType'), 'redRealm': red_realm_output, 'blueRealm': blue_realm_output}

        if eventObj.get('dataType') == 'player color':
            game, connected, creator = CREATED_GAMES[eventObj.get('game_id')]
            if creator == eventObj.get('user_id'):
                answer = {'type': eventObj.get('dataType'), 'color': 'Blue'}
            else:
                answer = {'type': eventObj.get('dataType'), 'color': 'Red'}
            
        
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
    # SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = ''
    async with websockets.serve(handler, SERVER, 8001):
        print(f'[STARTING] Server is starting on port {SERVER}')
        await asyncio.Future() # run forever


if __name__ == "__main__":
    asyncio.run(main())
