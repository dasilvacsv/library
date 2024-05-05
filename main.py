from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk




class StartupFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Load the assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path("Inicio/build/assets/frame0")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        # Create the canvas and place the images and button
        canvas = Canvas(
            self,
            bg="#000000",
            height=502,
            width=795,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.pack()

        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(397.0, 251.0, image=image_image_1)

        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(397.0, 97.0, image=image_image_2)

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.create_login_frame(),
            relief="flat",
        )
        button_1.place(x=287.0, y=432.0, width=219.0, height=52.0)

        image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(378.0, 157.0, image=image_image_3)
