import asyncio
from alliance import Alliance
from cards.card import Card
from cards.card_type import CardType
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
            red_realm_output[pile].append(get_card_as_string(card))

    blue_realm_output = []
    blue_realm = game.blue_player.realm.get_realm()
    for pile in range(len(blue_realm)):
        blue_realm_output.append([])
        for card in blue_realm[pile]:
            blue_realm_output[pile].append(get_card_as_string(card))

    return red_realm_output, blue_realm_output


def get_card_as_string(card:Card):
    if card.alliance == Alliance.BLUE:
        return 'b_' + card.to_string()
    elif card.alliance == Alliance.RED:
        return 'r_' + card.to_string()


async def join(websocket, game_id, user_id):

    try:
        game, connected, creator = CREATED_GAMES[game_id]
    except KeyError:
        # TODO - send error message
        return
    # if user_id == 

    connected.append(User(user_id, websocket))

    if (len(connected) < 2):
        del CREATED_GAMES[game_id]
        print('[ERROR] - Not enough players connected')
        return

    # Transfer game to "in progress" list
    GAMES_IN_PROGRESS[game_id] = CREATED_GAMES[game_id]
    del CREATED_GAMES[game_id]
    
    print(f'[GAME JOINED] - {user_id} joined game {game_id}')

    await websocket.send(json.dumps({'type': 'joined game', 'id': game_id, 'userID': user_id}))

    websockets.broadcast(get_sockets_from_users(connected), json.dumps({'type': 'redirect', 'url': ('?game=' + game_id)}))

    # TODO - handle game leaving


def get_sockets_from_users(users):
    sockets = []
    for user in users:
        sockets.append(user.get_socket())
    
    return sockets

def get_user_by_id(users, user_id):
    for user in users:
        if user.get_user_id() == user_id:
            return user
    
    return None


async def new_connection(websocket) -> int:
    # TODO - hold username between sessions/reloads
    #       (Probably make login screen)

    connected = False;
    while not connected:
        # listen for connection event 
        try:
            event = json.loads(await websocket.recv())

            if event.get('type') == 'connection':
                user_id = event.get('userID')
                if user_id == '':
                    user_id = generate_user_id(USERS)
                    USERS.append(User(user_id, websocket))
                    await websocket.send(json.dumps({'type': 'set', 'variable': 'userID', 'value': user_id}))
                else:
                    user = get_user_by_id(USERS, user_id)
                    user.websocket = websocket # set socket to current socket

                print(f'[NEW CONNECTION] user {user_id} connected') # [NEW CONNNECTION] addr connect
                print(f'[ACTIVE CONNECTION] {len(USERS)}')
                return user_id

        except websockets.ConnectionClosedOK or websockets.ConnectionResetError:
            #disconnection(user_id)
            print('disconnected')
            break


def disconnection(user_id):
    for user in USERS:
        if user.get_user_id() == user_id:
            USERS.remove(user)
            break
    print(f'[ACTIVE CONNECTIONS] {len(USERS)}')


async def query(event_obj, user_id, websocket):
    
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
            
            connected.append(User(user_id, websocket))

            red_realm_output, blue_realm_output = get_realms_as_letters(event_obj.get('game_id'))
            
            answer = {'type': event_obj.get('dataType'), 'redRealm': red_realm_output, 'blueRealm': blue_realm_output, 'player_color': player_color}

        if event_obj.get('dataType') == 'player color':
            game, connected, creator = CREATED_GAMES[event_obj.get('game_id')]
            if creator == event_obj.get('user_id'):
                answer = {'type': event_obj.get('dataType'), 'color': 'b'}
            else:
                answer = {'type': event_obj.get('dataType'), 'color': 'r'}
            
        
        await websocket.send(json.dumps(answer))


def new_game(event_obj, user_id, websocket):

    print(f'[CREATED GAMES] - {CREATED_GAMES}')
    # Get available ids
    available_game_ids = []
    for game, connected, creator in CREATED_GAMES.values():
        available_game_ids.append(game.id)

    id = generate_game_id(available_game_ids) # generate id

    CREATED_GAMES[id] = (Scrimish(id, event_obj.get('level'), event_obj.get('speed')), [User(user_id, websocket)], user_id)
    
    print(f'[GAME CREATED] - {user_id} created game {id}')


async def attack(event_obj, user_id, websocket):

    # event obj = {attack_pile, game_id, defense_pile, player_color}
    print('ev_obj: ' + json.dumps(event_obj))
    player_color = event_obj.get("playerColor")
    attack_pile = event_obj.get('attackPile')
    defense_pile = event_obj.get('defensePile')
    game_id = event_obj.get('game_id')

    try:
        game, connected, creator = GAMES_IN_PROGRESS[game_id]
    except KeyError:
        print('in attack: game not found [ERROR]')
        # TODO - probably send error event to client

    if game.get_current_player() != player_color:
        print(f"not {user_id}'s move [ERROR]")
        # TODO - send error event to client (Illegal move) - not their turn
        return

    current_player_realm = None
    if player_color == 'b':
        current_player_realm = game.blue_player.realm
    elif player_color == 'r':
        current_player_realm = game.red_player.realm

    if current_player_realm.get_top(attack_pile).card_type == CardType.SHIELD:
        print(f'Shields cannot attack!')
        # TODO - send error???
        return
    
    losers = game.play_attack(player_color, attack_pile, defense_pile)

    str_losers = []
    for card in losers:
        str_losers.append(get_card_as_string(card))

    att_event = {
        'type': 'attack', 
        'player_color': player_color, 
        'att_pile': attack_pile, 'def_pile': defense_pile,
        'losers': str_losers
    }
    websockets.broadcast(get_sockets_from_users(connected), json.dumps(att_event))

    for card in str_losers:
        card_type = card[2:3]
        if card_type == 'C':
            player = card[0:1]
            websockets.broadcast(get_sockets_from_users(connected), json.dumps({
                'type': 'lose',
                'player': player
            }))
    

async def process_event(user_id, event, websocket):

    event_obj = json.loads(event)
    ev_type = event_obj.get('type')

    if ev_type == 'disconnection':
        disconnection(event_obj.get('userID'))
        pass

    elif ev_type == 'attack':
        await attack(event_obj, user_id, websocket)

    elif ev_type == 'msg':
        print('[MESSAGE] ' + event_obj.get('text'))

    elif ev_type == 'new game':
        new_game(event_obj, user_id, websocket)

    elif ev_type == 'join':
        await join(websocket, event_obj.get('id'), user_id)

    elif ev_type == 'query':
        await query(event_obj, user_id, websocket)
    else:
        raise Exception(f'Illegal event type! ({ev_type})')


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
