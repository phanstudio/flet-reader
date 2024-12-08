import flet as ft
from Utility import *
from user_controls import Navbar, overlay
import shutil
from textwrap import TextWrapper


class AddView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/add",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(4),
        )

        # self.file_picker = ft.FilePicker()
        self.add_button = ft.IconButton(
            ft.icons.ADD_ROUNDED,
            icon_color= 'white',
            bgcolor= GOLD,
            #   icon_size= 10,
            width= 40,
            height= 40,
            style=ft.ButtonStyle(
                bgcolor= {ft.MaterialState.HOVERED: ft.colors.with_opacity(0.3, 'black')}
            ),
        )
        # self.dp = dp
        self.controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        value='Add a Book',
                        weight= ft.FontWeight.BOLD,
                    ),
                    ft.IconButton(
                        ft.icons.HISTORY, 
                        on_click= self.onclick
                    ),
                ], 
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            
            ft.Container(
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                self.add_button,
                                ft.Row([ # change to text spans
                                    ft.Text('Choose a file to'),
                                    ft.Text(' upload ', color= GOLD, weight= ft.FontWeight.BOLD,),
                                    ft.Text('here'),
                                    ], spacing= 0)
                            ], horizontal_alignment= ft.CrossAxisAlignment.CENTER
                        ),
                    ], alignment= ft.MainAxisAlignment.CENTER
                ),
                bgcolor= ft.colors.with_opacity(0.1, ft.colors.INVERSE_SURFACE),
                # border= ft.border.all(2),
                border_radius= 5,
                padding= 20,
            ),
            # ElevatedButton(text='Go back',
            #             on_click= lambda _: page.go('/'))
        ]
    
    def onclick(self, e):
        self.overlays.bookprogresssheet.popup()
        
    def did_mount(self):
        self.overlays = overlay(self.page)
        self.file_picker = self.overlays.filepicker
        self.file_picker.on_result = (
            lambda e, p= self.file_picker, d= self.overlays.bookprogresssheet, pl= self.page: 
            on_dialog_result(e, p, d, pl)
        )
        self.add_button.on_click =lambda _: self.file_picker.pick_files(
                dialog_title= 'Book Adder', file_type= ft.FilePickerFileType.AUDIO)
        self.page.update()

        return super().did_mount()
