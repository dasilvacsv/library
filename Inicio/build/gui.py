from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\REZE\Desktop\mariavic\Maria Victoria biblioteca\Inicio\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_start_frame(parent_frame, relative_to_assets):
    print(relative_to_assets("image_1.png"))  # Add this line
    canvas = Canvas(
        parent_frame,
        bg="#000000",
        height=502,
        width=795,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.pack(fill=tk.BOTH, expand=True)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(397.0, 251.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(397.0, 97.0, image=image_image_2)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        canvas,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(x=287.0, y=432.0, width=219.0, height=52.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(378.0, 157.0, image=image_image_3)