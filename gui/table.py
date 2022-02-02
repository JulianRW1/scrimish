from tkinter import *
from PIL import ImageTk, Image
from player.player import Player
from alliance import Alliance
import constants

class Table:

    def card_clicked(self):
        print('clicked')

    def set_up(self):
        root = Tk()
        root.title('Scrimish')

        blue_player = Player(Alliance.BLUE)
        red_player = Player(Alliance.RED)

        blue_frame = LabelFrame(root, text='BLUE')
        red_frame = LabelFrame(root, text='RED')

        card_width = 60
        card_height = 80
        card_image = Table.resize_image(Image.open('images\scrimish_box_test.jpg'), card_width, card_height)

        blue_canvas_0 = self.set_up_canvas(blue_frame, card_width, card_height, card_image, grid_row=0, grid_column=0) 
        blue_canvas_1 = self.set_up_canvas(blue_frame, card_width, card_height, card_image, grid_row=0, grid_column=1)
        blue_canvas_2 = self.set_up_canvas(blue_frame, card_width, card_height, card_image, grid_row=0, grid_column=2)
        blue_canvas_3 = self.set_up_canvas(blue_frame, card_width, card_height, card_image, grid_row=0, grid_column=3)
        blue_canvas_4 = self.set_up_canvas(blue_frame, card_width, card_height, card_image, grid_row=0, grid_column=4)
        
        red_canvas_0 = self.set_up_canvas(red_frame, card_width, card_height, card_image, grid_row=0, grid_column=0)
        red_canvas_1 = self.set_up_canvas(red_frame, card_width, card_height, card_image, grid_row=0, grid_column=1)
        red_canvas_2 = self.set_up_canvas(red_frame, card_width, card_height, card_image, grid_row=0, grid_column=2)
        red_canvas_3 = self.set_up_canvas(red_frame, card_width, card_height, card_image, grid_row=0, grid_column=3)
        red_canvas_4 = self.set_up_canvas(red_frame, card_width, card_height, card_image, grid_row=0, grid_column=4)

        blue_frame.pack()
        red_frame.pack()

        root.mainloop()

    def set_up_canvas(self, master, width, height, image, grid_row, grid_column):
        red_canvas_0 = Canvas(master, width=width, height=height)
        red_canvas_0.grid(row=grid_row, column=grid_column)
        red_canvas_0.create_image(0, 0, anchor=NW, image=image)
        red_canvas_0.bind('<Button-1>', Table.card_clicked)


    def resize_image(img: Image, width, height):
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_img)