import asyncio
from http import cookies
from multiprocessing.sharedctypes import Value
from sqlite3 import connect
from telnetlib import GA
from alliance import Alliance
from cards.card import Card
from cards.card_factory import CardFactory
from cards.card_type import CardType
import constants
from realm import Realm
from scrimish import Scrimish
import websockets
import json
from scrimish_server_utils import generate_game_id, generate_user_id

USERS = []
CREATED_GAMES = {}
GAMES_IN_PROGRESS = {}

USE_COOKIES = False

class User:
    def __init__(self, user_id, websocket, player_color) -> None:
        self.user_id = user_id
        self.websocket = websocket
        self.player_color = player_color

    
    def get_user_id(self) -> str:
        return self.user_id
    

    def get_socket(self):
        return self.websocket

    
    def get_player_color(self):
        return self.player_color


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


def get_realm_from_letters(alliance, letters):
    realm_cards = []
    for pile in range(len(letters)):
        realm_cards.append([])
        for card in letters[pile]:
            if card == '1':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.DAGGER))
            if card == '2':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.SWORD))
            if card == '3':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.MORNING_STAR))
            if card == '4':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.WAR_AXE))
            if card == '5':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.HALBERD))
            if card == '6':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.LONGSWORD))
            if card == 'A':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.ARCHER))
            if card == 'S':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.SHIELD))
            if card == 'C':
                realm_cards[pile].append(CardFactory.make_card(alliance, CardType.CROWN))
    return Realm(realm_cards)



def get_card_as_string(card:Card):
    if card.alliance == Alliance.BLUE:
        return 'b_' + card.to_string()
    elif card.alliance == Alliance.RED:
        return 'r_' + card.to_string()


async def join(websocket, game_id, user_id):

    try:
        game, connected, creator = CREATED_GAMES[game_id]
    except KeyError:
        await websocket.send(json.dumps({'type': 'message', 'text': 'This game no longer exists!'}))

        resulting_list = []
        for game, connected, creator in CREATED_GAMES.values():
            _game = {'id': game.id, 'level': game.level, 'speed': game.speed}
            resulting_list.append(_game)

        await websocket.send(json.dumps({'type': 'available games', 'data': resulting_list}))
        # TODO - send error message
        return

    if (creator == user_id):
        await websocket.send(json.dumps({'type': 'message', 'text': 'Cannot join your own game!'}))
        return

    connected.append(User(user_id, websocket, 'r'))

    if (len(connected) < 2):
        del CREATED_GAMES[game_id]
        print('[ERROR] - Not enough players connected')
        return

    # Transfer game to "in progress" list
    GAMES_IN_PROGRESS[game_id] = CREATED_GAMES[game_id]
    del CREATED_GAMES[game_id]
    
    print(f'[GAME JOINED] - {user_id} joined game {game_id}')

    await websocket.send(json.dumps({'type': 'joined game', 'id': game_id, 'userID': user_id, 'userColor': 'r/b'})) # TODO
    
    #Remove the users (because they will become a new user after redirect)
    temp = connected
    if (not USE_COOKIES):
        connected = []

    websockets.broadcast(get_sockets_from_users(temp), json.dumps({'type': 'redirect', 'url': ('?setup=' + game_id)}))

    


def connect_to_game(websocket, game_id, user_id):
    game, connected, creator = GAMES_IN_PROGRESS[game_id]
    
    connected.append(get_user_by_id(USERS, user_id))
    

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

    connected = False
    while not connected:
        # listen for connection event 
        try:
            event = json.loads(await websocket.recv())

            if event.get('type') == 'connection':
                user_id = event.get('userID')
                if user_id == '':
                    user_id = generate_user_id(USERS)
                    USERS.append(User(user_id, websocket, ''))
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
    if (USE_COOKIES):
        pass
    else:
        for user in USERS:
            if user.get_user_id() == user_id:
                USERS.remove(user)
                #USERS.remove(user)
                break
            
    for entry in dict(CREATED_GAMES).values():
        if user_id == entry[2]:
            for id, game_info in dict(CREATED_GAMES).items():
                if game_info == entry:
                    del CREATED_GAMES[id]

        print(f'[ACTIVE CONNECTIONS] {len(USERS)}')

async def query(event_obj, user_id, websocket):
    
        if event_obj.get('dataType') == 'available games':
            resulting_list = []
            for game, connected, creator in CREATED_GAMES.values():
                _game = {'id': game.id, 'level': game.level, 'speed': game.speed}
                resulting_list.append(_game)
            
            answer = {'type': event_obj.get('dataType'), 'data': resulting_list}

        if event_obj.get('dataType') == 'initialGameState':

            game_id = event_obj.get('gameID')
            
            try :
                game, connected, creator = GAMES_IN_PROGRESS[game_id]
            except KeyError:
                print('game not found')
                await websocket.send(json.dumps({'type': 'redirect', 'url': '/'}))
                return
            
            red_realm_output, blue_realm_output = get_realms_as_letters(game_id)

            player_color = 'b or r'

            if len(connected) % 2 == 0:
                player_color = 'b'
            elif len(connected) % 2 == 1:
                player_color = 'r'
            else:
                raise Exception('[ERROR] - Too many connections to the game')

            
            answer = {'type': 'initialGameState', 'redRealm': red_realm_output, 'blueRealm': blue_realm_output, 'playerColor': player_color}
            print('[ANSWER] = ' + str(answer))

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

    CREATED_GAMES[id] = (Scrimish(id, event_obj.get('level'), event_obj.get('speed')), [User(user_id, websocket, 'b')], user_id)
    
    print(f'[GAME CREATED] - {user_id} created game {id}')


async def attack(event_obj, user_id, websocket):

    # event obj = {attack_pile, game_id, defense_pile, player_color}
    player_color = event_obj.get("playerColor")
    attack_pile = event_obj.get('attackPile')
    defense_pile = event_obj.get('defensePile')
    game_id = event_obj.get('game_id')

    try:
        game, connected, creator = GAMES_IN_PROGRESS[game_id]
    except KeyError:
        print('[ERROR] game not found (in attack)')
        # TODO - probably send error event to client

    if game.get_current_player() != player_color:
        print(f"[ERROR] - not {user_id}'s move")
        await websocket.send(json.dumps({'type': 'message', 'text': 'It is not your turn!'}))
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


async def continue_to_game(websocket, game_id, user_id, realm):
    
    try :
        game, connected, creator = GAMES_IN_PROGRESS[game_id]
    except KeyError:
        print('game not found')
        await websocket.send(json.dumps({'type': 'redirect', 'url': '/'}))
        return

    if game.blue_player.realm == None:
        game.blue_player.realm = get_realm_from_letters(Alliance.BLUE, realm)
        # send the player color
        await websocket.send(json.dumps({'type': 'set', 'variable': 'playerColor', 'value': 'b'}))

        # tell the player to wait for their opponent
        await websocket.send(json.dumps({'type': 'continueToGame', 'firstOrSecond': "first"}))

    elif game.red_player.realm == None:
        game.red_player.realm = get_realm_from_letters(Alliance.RED, realm)

        
        temp = connected
        # clear connected list
        if (not USE_COOKIES):
            connected = []

        websockets.broadcast(get_sockets_from_users(temp), json.dumps({'type': 'redirect', 'url': '?game=' + game_id}))

        # # send the player color
        # await websocket.send(json.dumps({'type': 'set', 'variable': 'playerColor', 'value': 'r'}))

        # # broadcast a message to start game
        # red_realm_output, blue_realm_output = get_realms_as_letters(game_id)
        # event = {'type': 'continueToGame', 'firstOrSecond': 'second', 'gameID': game_id, 'redRealm': red_realm_output, 'blueRealm': blue_realm_output}
        
        # print('[BROADCASTING]')
        # websockets.broadcast(get_sockets_from_users(connected), json.dumps(event))

    
def process_data(data, user_id, websocket):
    pass
      
    

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

    elif ev_type == 'connectToGame': 
        connect_to_game(websocket, event_obj.get('id'), user_id)

    elif ev_type == 'continueToGame':
        await continue_to_game(websocket, event_obj.get('id'), user_id, event_obj.get('realm'))

    elif ev_type == 'query':
        await query(event_obj, user_id, websocket)

    elif ev_type == 'data':
        process_data(event_obj, user_id, websocket)

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
