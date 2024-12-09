import flet as ft
from Utility import *
from user_controls import Note_frame, Library_frame, Reading, Library, Note, Navbar

class LibView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/lib",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(2),
        )
