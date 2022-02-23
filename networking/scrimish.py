


class Scrimish:
    players = []
    move_list = []
    last_defender_lost = False
    winner = None

    
    def __init__(self, id: str, level:str, speed:str, players: int) -> None:
        self.id = id
        self.level = level
        self.speed = speed
        self.players = players

    
    # def play(self, move: moves.move.Move):
    #     if move.player != self.active_player:
    #         raise RuntimeError('It is not your turn.')
    #     else:
    #         if type(move) == moves.attack.Attack:
    #             losers = move.player.make_move(move)
    #             crown_killed = False
    #             for loser in losers:
    #                 if loser.is_crown():
    #                     crown_killed = True
    #             self.last_defender_lost = crown_killed
                    
    #             self.move_list.append(move)
    #         self.pass_turn()


    # def last_defender_lost(self) -> bool:
    #     return self.last_defender_lost

    
    # def pass_turn(self):
    #     if self.active_player != self.players[-1]:
    #         next_player_index = self.players.index(self.active_player) + 1
    #         self.active_player = self.players[next_player_index]

