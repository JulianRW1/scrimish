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

    primary_player_color = ''
    secondary_player_color = ''

    primary_player = None
    secondary_player = None

    is_primary_players_turn = True

    selected_card = None
    selected_canvas = None

    primary_canvases = []
    secondary_canvases = []

    def __init__(self, primary_player: Player, secondary_player: Player) -> None:
        self.primary_player = primary_player
        self.secondary_player = secondary_player

        if self.primary_player.alliance == Alliance.RED:
            self.primary_player_color = 'RED'
            self.secondary_player_color = 'BLUE'
        else:
            self.primary_player_color = 'BLUE'
            self.secondary_player_color = 'RED'


    def card_clicked(self, canvas: Canvas, card: Card):
        if self.is_primary_players_turn:
            if self.selected_card == None:  
                # No previosly selected cards
                if card.alliance == self.primary_player.alliance:
                    # selected card is on alliance

                    # selt the selected card
                    canvas.configure(bg='YELLOW')
                    self.selected_card = card
                    self.selected_canvas = canvas
            elif card.alliance != self.primary_player.alliance:
                # Card is opponents card
                canvas.configure(bg='YELLOW')

                attacker_pile = self.primary_player.realm.get_pile(self.selected_card)
                defender_pile = self.secondary_player.realm.get_pile(card)
                losers = self.primary_player.make_attack(self.secondary_player.realm, attacker_pile, defender_pile)
                # TODO: redisplay cards after attack

            elif card == self.selected_card:
                # card is already selected card
                canvas.configure(bg=self.primary_player_color)
                self.selected_canvas = None
                self.selected_card = None
            else:
                # Card is own card

                # Switch selected card
                self.selected_canvas.configure(bg=self.primary_player_color)
                canvas.configure(bg='YELLOW')
                self.selected_card = card
                self.selected_canvas = canvas
                

    def set_up(self):
        root = Tk()
        root.title('Scrimish')
        root.configure(bg='brown')


        # Configure frames
        primary_frame = None
        secondary_frame = None

        primary_frame = LabelFrame(root, text=self.primary_player_color, bg=self.primary_player_color)
        secondary_frame = LabelFrame(root, text=self.secondary_player_color, bg=self.secondary_player_color)
        

        card_width = int(2.5 * constants.CARD_SCALE)
        card_height = int(3.5 * constants.CARD_SCALE)

        secondary_pile_imgs = [
            Table.resize_image(Image.open(self.secondary_player.realm.get(0, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.secondary_player.realm.get(1, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.secondary_player.realm.get(2, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.secondary_player.realm.get(3, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.secondary_player.realm.get(4, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        ]

        self.secondary_canvases = [
            self.set_up_canvas(secondary_frame, card_width, card_height, image=secondary_pile_imgs[0], bg=self.secondary_player_color, grid_row=0, grid_column=0),
            self.set_up_canvas(secondary_frame, card_width, card_height, image=secondary_pile_imgs[1], bg=self.secondary_player_color, grid_row=0, grid_column=1),
            self.set_up_canvas(secondary_frame, card_width, card_height, image=secondary_pile_imgs[2], bg=self.secondary_player_color, grid_row=0, grid_column=2),
            self.set_up_canvas(secondary_frame, card_width, card_height, image=secondary_pile_imgs[3], bg=self.secondary_player_color, grid_row=0, grid_column=3),
            self.set_up_canvas(secondary_frame, card_width, card_height, image=secondary_pile_imgs[4], bg=self.secondary_player_color, grid_row=0, grid_column=4)
        ]
        
        primary_pile_images = [
            Table.resize_image(Image.open(self.primary_player.realm.get(0, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.primary_player.realm.get(1, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.primary_player.realm.get(2, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.primary_player.realm.get(3, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height),
            Table.resize_image(Image.open(self.primary_player.realm.get(4, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        ]

        self.primary_canvases = [
            self.set_up_canvas(primary_frame, card_width, card_height, image=primary_pile_images[0], bg=self.primary_player_color, grid_row=0, grid_column=0),
            self.set_up_canvas(primary_frame, card_width, card_height, image=primary_pile_images[1], bg=self.primary_player_color, grid_row=0, grid_column=1),
            self.set_up_canvas(primary_frame, card_width, card_height, image=primary_pile_images[2], bg=self.primary_player_color, grid_row=0, grid_column=2),
            self.set_up_canvas(primary_frame, card_width, card_height, image=primary_pile_images[3], bg=self.primary_player_color, grid_row=0, grid_column=3),
            self.set_up_canvas(primary_frame, card_width, card_height, image=primary_pile_images[4], bg=self.primary_player_color, grid_row=0, grid_column=4)
        ]

        for i in range(len(self.primary_canvases)):
            self.primary_canvases[i].bind('<Button-1>', 
                                lambda event, 
                                canvas = self.primary_canvases[i],
                                card = self.primary_player.realm.get(pile=i, index=constants.TOP_PILE_INDEX): 
                                Table.card_clicked(self, canvas, card))
            self.secondary_canvases[i].bind('<Button-1>', 
                                lambda event, 
                                canvas = self.secondary_canvases[i],
                                card = self.secondary_player.realm.get(pile=i, index=constants.TOP_PILE_INDEX): 
                                Table.card_clicked(self, canvas, card))

        secondary_frame.pack()
        primary_frame.pack()

        root.mainloop()

    def set_up_canvas(self, master, width, height, image, bg, grid_row, grid_column):
        canvas = Canvas(master, width=width + 5, height=height + 5, bg=bg)
        canvas.grid(row=grid_row, column=grid_column)
        canvas.create_image(5, 5, anchor=NW, image=image)
        return canvas


    def resize_image(img: Image, width, height):
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_img)