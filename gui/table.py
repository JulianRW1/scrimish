from tkinter import *
from PIL import ImageTk, Image
from player.player import Player
from alliance import Alliance
import constants

class Table:

    def card_clicked(self):
        print('clicked')

    def set_up(self, blue_player: Player, red_player: Player):
        root = Tk()
        root.title('Scrimish')

        root.configure(bg='brown')

        blue_frame = LabelFrame(root, text='BLUE')
        red_frame = LabelFrame(root, text='RED')

        blue_frame.configure(bg='brown')
        red_frame.configure(bg='brown')

        card_width = int(2.5 * constants.CARD_SCALE)
        card_height = int(3.5 * constants.CARD_SCALE)

        card_image = Table.resize_image(Image.open('images/scrimish_box_test.jpg'), card_width, card_height)

        #TODO: Declare other piles (array) and transfer images to canvases
        blue_pile_0_img = Table.resize_image(Image.open(blue_player.realm.get(0, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        blue_pile_1_img = Table.resize_image(Image.open(blue_player.realm.get(1, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        blue_pile_2_img = Table.resize_image(Image.open(blue_player.realm.get(2, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        blue_pile_3_img = Table.resize_image(Image.open(blue_player.realm.get(3, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        blue_pile_4_img = Table.resize_image(Image.open(blue_player.realm.get(4, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)

        blue_canvas_0 = self.set_up_canvas(blue_frame, card_width, card_height, blue_pile_0_img, grid_row=0, grid_column=0) 
        blue_canvas_1 = self.set_up_canvas(blue_frame, card_width, card_height, blue_pile_1_img, grid_row=0, grid_column=1)
        blue_canvas_2 = self.set_up_canvas(blue_frame, card_width, card_height, blue_pile_2_img, grid_row=0, grid_column=2)
        blue_canvas_3 = self.set_up_canvas(blue_frame, card_width, card_height, blue_pile_3_img, grid_row=0, grid_column=3)
        blue_canvas_4 = self.set_up_canvas(blue_frame, card_width, card_height, blue_pile_4_img, grid_row=0, grid_column=4)
        
        red_pile_0_img = Table.resize_image(Image.open(red_player.realm.get(0, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        red_pile_1_img = Table.resize_image(Image.open(red_player.realm.get(1, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        red_pile_2_img = Table.resize_image(Image.open(red_player.realm.get(2, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        red_pile_3_img = Table.resize_image(Image.open(red_player.realm.get(3, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)
        red_pile_4_img = Table.resize_image(Image.open(red_player.realm.get(4, constants.TOP_PILE_INDEX).get_image_path()), card_width, card_height)

        red_canvas_0 = self.set_up_canvas(red_frame, card_width, card_height, red_pile_0_img, grid_row=0, grid_column=0)
        red_canvas_1 = self.set_up_canvas(red_frame, card_width, card_height, red_pile_1_img, grid_row=0, grid_column=1)
        red_canvas_2 = self.set_up_canvas(red_frame, card_width, card_height, red_pile_2_img, grid_row=0, grid_column=2)
        red_canvas_3 = self.set_up_canvas(red_frame, card_width, card_height, red_pile_3_img, grid_row=0, grid_column=3)
        red_canvas_4 = self.set_up_canvas(red_frame, card_width, card_height, red_pile_4_img, grid_row=0, grid_column=4)

        blue_frame.pack()
        red_frame.pack()

        root.mainloop()

    def set_up_canvas(self, master, width, height, image, grid_row, grid_column):
        canvas = Canvas(master, width=width, height=height, bg='brown')
        canvas.grid(row=grid_row, column=grid_column)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.bind('<Button-1>', Table.card_clicked)


    def resize_image(img: Image, width, height):
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_img)