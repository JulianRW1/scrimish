import time
from tkinter import *
from PIL import ImageTk, Image
from alliance import Alliance
from cards.card import Card
from cards.card_type import CardType
from cards.specials.crown import Crown
from player.player import Player
import constants


class Table:

    primary_player = Player
    secondary_player = Player

    is_primary_players_turn = True
    user_can_select_card = True

    selected_card = Card

    primary_canvases = [Canvas]
    secondary_canvases = [Canvas]

    primary_pile_images = [PhotoImage]
    secondary_pile_imgs = [PhotoImage]

    card_width = int
    card_height = int
    
    primary_frame = LabelFrame
    secondary_frame = LabelFrame

    main_frame = Frame
    _root = Tk

    def __init__(self, primary_player: Player, secondary_player: Player) -> None:
        self.primary_player = primary_player
        self.secondary_player = secondary_player

        self.card_width = int(2.5 * constants.CARD_SCALE)
        self.card_height = int(3.5 * constants.CARD_SCALE)

        self.selected_card = None
        self.selected_canvas = None

        self.primary_pile_images = [None]*5
        self.secondary_pile_imgs = [None]*5

        self.primary_canvases = [None]*5
        self.secondary_canvases = [None]*5


    def set_up(self):
        self._root = Tk()
        self._root.title('Scrimish')

        self.main_frame = Frame(self._root, bg='BROWN')

        # Configure frames
        self.primary_frame = LabelFrame(self.main_frame, text=self.primary_player.color, bg=self.primary_player.color)
        self.secondary_frame = LabelFrame(self.main_frame, text=self.secondary_player.color, bg=self.secondary_player.color)

        
        #self.display_cards()
        self.create_canvases()

        self.main_frame.pack()
        self.secondary_frame.pack()
        self.primary_frame.pack()
        self._root.mainloop()


    # Handle user clicks on cards
    def card_clicked(self, card: Card):

        # Set active player
        active_player = None
        inactive_player = None
        if self.is_primary_players_turn:
            active_player = self.primary_player
            inactive_player = self.secondary_player
        else:
            active_player = self.secondary_player
            inactive_player = self.primary_player
        
        if card != None and self.user_can_select_card: # If there is a card on the clicked square
            if self.selected_card == None:  
                # No previosly selected cards
                if card.alliance == active_player.alliance:
                    # card clicked is on own alliance

                    # select the clicked card
                    self.display_image(active_player, active_player.realm.get_pile(card))
                    self.selected_card = card

            elif card.alliance != active_player.alliance: # Card is opponents card
                self.perform_attack(self.selected_card, card, active_player, inactive_player)

                # Reset display
                self.selected_card = None

            elif card == self.selected_card:
                # card is already selected card

                # Deselect card
                self.hide_image(active_player, active_player.realm.get_pile(card))
                self.selected_card = None
            else:
                # Card is own card

                # Switch selected card
                self.hide_image(active_player, active_player.realm.get_pile(self.selected_card))
                self.display_image(active_player, active_player.realm.get_pile(card))
                self.selected_card = card
        else:
            print('user cannot select card rn')

    # Helper function for card_clicked()
    def perform_attack(self, attacking_card: Card, defending_card: Card, active_player: Player, inactive_player: Player):
        
        if attacking_card.card_type != CardType.SHIELD:

            self.user_can_select_card = False # Disallow user input during attack

            self.display_image(inactive_player, inactive_player.realm.get_pile(defending_card))

            self.main_frame.update()

            self.pause(constants.DESTROYED_CARD_DELAY)
            
            # Make attack
            attacker_pile = active_player.realm.get_pile(attacking_card)
            defender_pile = inactive_player.realm.get_pile(defending_card)
            losers = active_player.make_attack(inactive_player.realm, attacker_pile, defender_pile)
            
            
            for loser in losers:

                if loser.card_type == CardType.CROWN:
                    self.game_over(loser)
                else:
                    if loser == defending_card:
                        self.hide_image(inactive_player, defender_pile)
                    
                    if loser == attacking_card:
                        self.hide_image(active_player, attacker_pile)

            self.main_frame.update()

            if len(losers) < 2:
                self.pause(constants.WINNER_DELAY)

            self.hide_image(active_player, attacker_pile)
            self.hide_image(inactive_player, defender_pile)

            # pass turn
            self.is_primary_players_turn = not self.is_primary_players_turn

            self.user_can_select_card = True # Re-allow user input


    # Pauses the main_frame for given seconds 
    # Seconds can be a float for better precision
    def pause(self, seconds:float):
        self.main_frame.after(int(1000*seconds), func=None)


    # Displays a message showing which player won
    def game_over(self, destroyed_crown: Crown):

        winner = ''
        if destroyed_crown.alliance == Alliance.BLUE:
            winner = 'Red'
        elif destroyed_crown.alliance == Alliance.RED:
            winner = 'Blue'

        height = self.main_frame.winfo_height()
        width = self.main_frame.winfo_width()

        self.primary_frame.pack_forget()
        self.secondary_frame.pack_forget()

        self._root.minsize(width, height)
        self._root.maxsize(width, height)

        victory_frame = Frame(self.main_frame, bg='GRAY')
        victory_frame.configure(width=width, height=height)
        
        winner_label = Label(victory_frame, text=f'{winner} Wins!', font=('Yonkers', 50), fg='YELLOW', bg='GRAY')

        winner_label.pack()
        victory_frame.pack()


    # Hides the card image at given location
    # player - Player whose pile it is
    # pile - int location of the pile
    def hide_image(self, player: Player, pile:int):

        if player.realm.get_top(pile) != None:
            bg = player.realm.get_top(pile).get_bg_image_path()
                
            if player == self.primary_player:
                # Destroy the canvas already displayed
                if self.primary_canvases[pile] != None:
                    self.primary_canvases[pile].destroy()
                    
                # Set up primary player area
                self.primary_pile_images[pile] = Table.resize_image(Image.open(bg), self.card_width, self.card_height)
                self.primary_canvases[pile] = self.set_up_canvas(self.primary_frame, self.card_width, self.card_height, image=self.primary_pile_images[pile], bg=self.primary_player.color, grid_row=0, grid_column=pile)
            elif player == self.secondary_player:
                # Destroy the canvas if it is already displayed
                if self.secondary_canvases[pile] != None:
                    self.secondary_canvases[pile].destroy()
                    
                # Set up secondary player area
                self.secondary_pile_imgs[pile] = Table.resize_image(Image.open(bg), self.card_width, self.card_height)
                self.secondary_canvases[pile] = self.set_up_canvas(self.secondary_frame, self.card_width, self.card_height, image=self.secondary_pile_imgs[pile], bg=self.secondary_player.color, grid_row=0, grid_column=pile)
        else:
            if player == self.primary_player:
                self.primary_canvases[pile].delete('all')
            elif player == self.secondary_player:
                self.secondary_canvases[pile].delete('all')
                
        self.bind_buttons_to_canvas()


    #
    def display_image(self, player: Player, pile: int):
    
        if player.realm.get_top(pile) != None:
            if player == self.primary_player:
                # Destroy the canvas already displayed
                if self.primary_canvases[pile] != None:
                    self.primary_canvases[pile].destroy()
                    
                # Set up primary player area
                self.primary_pile_images[pile] = Table.resize_image(Image.open(self.primary_player.realm.get_top(pile=pile).get_image_path()), self.card_width, self.card_height)
                self.primary_canvases[pile] = self.set_up_canvas(self.primary_frame, self.card_width, self.card_height, image=self.primary_pile_images[pile], bg=self.primary_player.color, grid_row=0, grid_column=pile)
            elif player == self.secondary_player:
                # Destroy the canvas if it is already displayed
                if self.secondary_canvases[pile] != None:
                    self.secondary_canvases[pile].destroy()
                    
                # Set up secondary player area
                self.secondary_pile_imgs[pile] = Table.resize_image(Image.open(self.secondary_player.realm.get_top(pile=pile).get_image_path()), self.card_width, self.card_height)
                self.secondary_canvases[pile] = self.set_up_canvas(self.secondary_frame, self.card_width, self.card_height, image=self.secondary_pile_imgs[pile], bg=self.secondary_player.color, grid_row=0, grid_column=pile)
        else:
            if player == self.primary_player:
                self.primary_canvases[pile].delete('all')
            elif player == self.secondary_player:
                self.secondary_canvases[pile].delete('all')
        
        self.bind_buttons_to_canvas()


    def bind_buttons_to_canvas(self):
        for i in range(len(self.primary_canvases)):
            self.primary_canvases[i].bind('<Button-1>', lambda event, card = self.primary_player.realm.get_top(pile=i): 
                                Table.card_clicked(self, card))
            
            self.secondary_canvases[i].bind('<Button-1>', lambda event, card = self.secondary_player.realm.get_top(pile=i): 
                                Table.card_clicked(self, card))


    def set_up_canvas(self, master, width, height, image, bg, grid_row, grid_column):
        canvas = Canvas(master, width=width + 5, height=height + 5, bg=bg)
        canvas.grid(row=grid_row, column=grid_column)
        canvas.create_image(5, 5, anchor=NW, image=image)
        return canvas


    def create_canvases(self):
        # Loop through the piles
        for i in range(constants.STANDARD_REALM_SIZE):
            if self.secondary_player.realm.get_top(pile=i) != None:
                # Destroy the canvas if it is already displayed
                if self.secondary_canvases[i] != None:
                    self.secondary_canvases[i].destroy()
                    
                # Set up secondary player area
                self.secondary_pile_imgs[i] = Table.resize_image(Image.open(self.secondary_player.realm.get_top(i).get_bg_image_path()), self.card_width, self.card_height),
                self.secondary_canvases[i] = self.set_up_canvas(self.secondary_frame, self.card_width, self.card_height, image=self.secondary_pile_imgs[i], bg=self.secondary_player.color, grid_row=0, grid_column=i);
            
            if self.primary_player.realm.get_top(pile=i) != None:
                # Destroy the canvas already displayed
                if self.primary_canvases[i] != None:
                    self.primary_canvases[i].destroy()
                    
                # Set up primary player area
                self.primary_player.realm.get_top(i).get_image_path()
                self.primary_pile_images[i] = Table.resize_image(Image.open(self.primary_player.realm.get_top(i).get_bg_image_path()), self.card_width, self.card_height)
                self.primary_canvases[i] = self.set_up_canvas(self.primary_frame, self.card_width, self.card_height, image=self.primary_pile_images[i], bg=self.primary_player.color, grid_row=0, grid_column=i)

        self.bind_buttons_to_canvas()


    def resize_image(img: Image, width, height):
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_img)