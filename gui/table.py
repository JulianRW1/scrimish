from multiprocessing.dummy import active_children
from select import select
from tkinter import *
from PIL import ImageTk, Image
from cards.card import Card
from moves.attack import Attack
from player.player import Player
from alliance import Alliance
import constants

class Table:

    primary_player = None
    secondary_player = None

    is_primary_players_turn = True

    selected_card = None
    selected_canvas = None

    primary_canvases = [None]*5
    secondary_canvases = [None]*5

    primary_pile_images = [None]*5
    secondary_pile_imgs = [None]*5

    card_width = 0
    card_height = 0
    
    primary_frame = None
    secondary_frame = None

    def __init__(self, primary_player: Player, secondary_player: Player) -> None:
        self.primary_player = primary_player
        self.secondary_player = secondary_player

        self.card_width = int(2.5 * constants.CARD_SCALE)
        self.card_height = int(3.5 * constants.CARD_SCALE)


    # Handle user clicks on cards
    def card_clicked(self, canvas: Canvas, card: Card):
        card_selected_color = 'YELLOW'

        # Set active player
        active_player = None
        inactive_player = None
        if self.is_primary_players_turn:
            active_player = self.primary_player
            inactive_player = self.secondary_player
        else:
            active_player = self.secondary_player
            inactive_player = self.primary_player
        
        if card != None: # If there is a card on the clicked square
            if self.selected_card == None:  
                # No previosly selected cards
                if card.alliance == active_player.alliance:
                    # card clicked is on own alliance

                    # select the clicked card
                    canvas.configure(bg=card_selected_color)
                    self.selected_card = card
                    self.selected_canvas = canvas

            elif card.alliance != active_player.alliance: # Card is opponents card
                canvas.configure(bg=card_selected_color)

                # Make attack
                attacker_pile = active_player.realm.get_pile(self.selected_card)
                defender_pile = inactive_player.realm.get_pile(card)
                active_player.make_attack(inactive_player.realm, attacker_pile, defender_pile)

                # Reset display
                self.selected_card = None
                self.selected_canvas = None
                self.remove_images()
                self.display_cards()

                # pass turn
                self.is_primary_players_turn = not self.is_primary_players_turn

            elif card == self.selected_card:
                # card is already selected card
                canvas.configure(bg=active_player.color)
                self.selected_canvas = None
                self.selected_card = None
            else:
                # Card is own card

                # Switch selected card
                self.selected_canvas.configure(bg=active_player.color)
                canvas.configure(bg=card_selected_color)
                self.selected_card = card
                self.selected_canvas = canvas


    # Remove all images from 
    def remove_images(self):
        for i in range(constants.STANDARD_REALM_SIZE):
            self.primary_canvases[i].delete('all')
            self.secondary_canvases[i].delete('all')


    def display_cards(self):

        # Loop through the piles
        for i in range(constants.STANDARD_REALM_SIZE):
            if self.secondary_player.realm.get_top(pile=i) != None:
                # Destroy the canvas if it is already displayed
                if self.secondary_canvases[i] != None:
                    self.secondary_canvases[i].destroy()
                    
                # Set up secondary player area
                self.secondary_pile_imgs[i] = Table.resize_image(Image.open(self.secondary_player.realm.get_top(pile=i).get_image_path()), self.card_width, self.card_height),
                self.secondary_canvases[i] = self.set_up_canvas(self.secondary_frame, self.card_width, self.card_height, image=self.secondary_pile_imgs[i], bg=self.secondary_player.color, grid_row=0, grid_column=i);
            
            if self.primary_player.realm.get_top(pile=i) != None:
                # Destroy the canvas already displayed
                if self.primary_canvases[i] != None:
                    self.primary_canvases[i].destroy()
                    
                # Set up primary player area
                self.primary_pile_images[i] = Table.resize_image(Image.open(self.primary_player.realm.get_top(pile=i).get_image_path()), self.card_width, self.card_height)
                self.primary_canvases[i] = self.set_up_canvas(self.primary_frame, self.card_width, self.card_height, image=self.primary_pile_images[i], bg=self.primary_player.color, grid_row=0, grid_column=i)

        self.bind_buttons_to_canvas()


    def set_up(self):
        root = Tk()
        root.title('Scrimish')
        root.configure(bg='brown')

        # Configure frames
        self.primary_frame = LabelFrame(root, text=self.primary_player.color, bg=self.primary_player.color)
        self.secondary_frame = LabelFrame(root, text=self.secondary_player.color, bg=self.secondary_player.color)

        self.display_cards()

        self.secondary_frame.pack()
        self.primary_frame.pack()
        root.mainloop()

    def bind_buttons_to_canvas(self):
        for i in range(len(self.primary_canvases)):
            self.primary_canvases[i].bind('<Button-1>', 
                                lambda event, 
                                canvas = self.primary_canvases[i],
                                card = self.primary_player.realm.get_top(pile=i): 
                                Table.card_clicked(self, canvas, card))
            self.secondary_canvases[i].bind('<Button-1>', 
                                lambda event, 
                                canvas = self.secondary_canvases[i],
                                card = self.secondary_player.realm.get_top(pile=i): 
                                Table.card_clicked(self, canvas, card))

    def set_up_canvas(self, master, width, height, image, bg, grid_row, grid_column):
        canvas = Canvas(master, width=width + 5, height=height + 5, bg=bg)
        canvas.grid(row=grid_row, column=grid_column)
        canvas.create_image(5, 5, anchor=NW, image=image)
        return canvas


    def resize_image(img: Image, width, height):
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_img)