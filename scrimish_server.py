import asyncio
from scrimish import Scrimish
import websockets
import json
from scrimish_server_utils import generate_game_id, generate_user_id

USERS = []
CREATED_GAMES = {}
GAMES_IN_PROGRESS = {}

class User:
    def __init__(self, user_id, websocket) -> None:
        self.user_id = user_id
        self.websocket = websocket

    
    def get_user_id(self) -> str:
        return self.user_id
    

    def get_socket(self):
        return self.websocket


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

    await websocket.send(json.dumps({'type': 'joined game', 'id': game_id, 'userID': user_id}))

    websockets.broadcast(connected, json.dumps({'type': 'redirect', 'url': ('?game=' + game_id)}))

    try:
        async for message in websocket:
            print('player sent', message)
    finally:
        connected.remove(websocket)


async def new_connection(websocket) -> int:
    # TODO - hold username between sessions/reloads
    #       (Probably make login screen)

    connected = False;
    while not connected:
        try:
            event = json.loads(await websocket.recv())
            print(event)

            if event.get('type') == 'connection':
                user_id = event.get('userID')
                if user_id == '':
                    user_id = generate_user_id(USERS)
                    USERS.append(User(user_id, websocket))
                    await websocket.send(json.dumps({'type': 'set', 'variable': 'userID', 'value': user_id}))
                print(f'[NEW CONNECTION] user {user_id} connected') # [NEW CONNNECTION] addr connect
                print(f'[ACTIVE CONNECTION] {len(USERS)}')
                return user_id


            # user_id = generate_user_id(USERS) 
            # USERS.append(User(user_id, websocket))
        except websockets.ConnectionClosedOK or websockets.ConnectionResetError:
            #disconnection(user_id)
            print('disconnected')
            break


def get_user_id():
    pass


def disconnection(user_id):
    for user in USERS:
        if user.get_user_id() == user_id:
            # print(f"[DISCONNECTED] - user {user_id} disconnected")
            USERS.remove(user)
            break
    print(f'[ACTIVE CONNECTIONS] {len(USERS)}')


async def process_event(user_id, event, websocket):

    event_obj = json.loads(event)
    ev_type = event_obj.get('type')

    if ev_type == 'connection':
        if (event_obj.get('userID') != ''):
            # The client sent a userID
            pass
        else:
            # The client did not send a userID
            user_id = generate_user_id(USERS) 
            USERS.append(User(user_id, websocket))
            print(f'[NEW CONNECTION] user {user_id} connected') # [NEW CONNNECTION] addr connect
            print(f'[ACTIVE CONNECTION] {len(USERS)}')
            
    elif ev_type == 'disconnection':
        disconnection(event_obj.get('userID'))
        pass

    elif event_obj.get('type') == 'attack':
        # TODO - implement
        print(str(event_obj))
        await websocket.send(json.dumps(event_obj))

    elif event_obj.get('type') == 'msg':
        print('[MESSAGE] ' + event_obj.get('text'))

    elif event_obj.get('type') == 'new game':
        print(f'[CREATED GAMES] - {CREATED_GAMES}')
        # Get available ids
        available_game_ids = []
        for game, connected, creator in CREATED_GAMES.values():
            available_game_ids.append(game.id)

        id = generate_game_id(available_game_ids) # generate id

        CREATED_GAMES[id] = (Scrimish(id, event_obj.get('level'), event_obj.get('speed')), [websocket], user_id)
        
        print(f'[GAME CREATED] - {user_id} created game {id}')

    elif event_obj.get('type') == 'join':
        await join(websocket, event_obj.get('id'), user_id)

    elif event_obj.get('type') == 'query':
        if event_obj.get('dataType') == 'available games':
            resulting_list = []
            for game, connected, creator in CREATED_GAMES.values():
                _game = {'id': game.id, 'level': game.level, 'speed': game.speed}
                resulting_list.append(_game)
            
            answer = {'type': event_obj.get('dataType'), 'data': resulting_list}

        if event_obj.get('dataType') == 'init game state':
            
            try :
                game, connected, creator = GAMES_IN_PROGRESS[event_obj.get('game_id')]
            except KeyError:
                print('game not found')
                await websocket.send(json.dumps({'type': 'redirect', 'url': '/'}))
                return

            # give the first player the color blue
            print(f'user_id == creator - {user_id} == {creator} => {user_id == creator}')
            if user_id == creator:
                player_color = 'b'
            else:
                # give the second player the color red
                player_color = 'r'

            red_realm_output, blue_realm_output = get_realms_as_letters(event_obj.get('game_id'))
            
            answer = {'type': event_obj.get('dataType'), 'redRealm': red_realm_output, 'blueRealm': blue_realm_output, 'player_color': player_color}

        if event_obj.get('dataType') == 'player color':
            game, connected, creator = CREATED_GAMES[event_obj.get('game_id')]
            if creator == event_obj.get('user_id'):
                answer = {'type': event_obj.get('dataType'), 'color': 'b'}
            else:
                answer = {'type': event_obj.get('dataType'), 'color': 'r'}
            
        
        await websocket.send(json.dumps(answer))

        print(f'[QUERY] value is {answer}')

    else:
        raise Exception(f'Illegal event type! ({event_obj.get("type")})')


async def handler(websocket):
    user_id = await new_connection(websocket)
    while True:
        try:
            event = await websocket.recv()
            await process_event(user_id, event, websocket)
            
        except websockets.ConnectionClosedOK or websockets.ConnectionResetError:
            disconnection(user_id)
            break


async def main():
    SERVER = ''
    async with websockets.serve(handler, SERVER, 8001):
        print(f'[STARTING] Server is starting on port {SERVER}')
        await asyncio.Future() # run forever


if __name__ == "__main__":
    asyncio.run(main())
