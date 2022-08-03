import secrets;


GAME_ID_LENGTH = 6;

# Generates new unique game id
def generate_game_id(active_game_ids: list ) -> str:
    id = secrets.token_urlsafe(GAME_ID_LENGTH);

    while active_game_ids.count(id):
        id = secrets.token_urlsafe(GAME_ID_LENGTH);
    
    return id


# Generates new unique user id
def generate_user_id(active_users) -> str:
    if len(active_users):
        last_number = int(active_users[-1].get_user_id()[5]) + 1
        user_id = f'Guest{last_number}'
    else:
        user_id = 'Guest0'
    return user_id
