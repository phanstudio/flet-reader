from flet import (Text, IconButton, Container, Row, Column, ProgressRing,
                  CrossAxisAlignment, MainAxisAlignment, Colors, Stack, padding, Icons)
from Utility import GOLD, BOLD
import flet as ft

class Reading(ft.Container): # change
    def __init__(self, onclick=None):
        super().__init__(
            border_radius= 50, 
            padding= padding.symmetric(horizontal=5),
            bgcolor= Colors.with_opacity(0.05, Colors.INVERSE_SURFACE),
            ink= True,
        )
        self.current_name = Text(
            value= 'Tales of Fate', 
            color=GOLD, 
            size= 15, 
            weight= BOLD,
        )
        self.onclick = onclick
        self.content = Row(
            controls=[
                Container(
                    content= Row(
                        controls=[
                            Row(
                                controls=[
                                    Stack(
                                        controls=[
                                            Row(
                                                controls=[
                                                    ft.Image(
                                                        src='./covers/defualt.jpg', 
                                                        width= 30, 
                                                        height= 30, 
                                                        border_radius= 360,
                                                        fit= ft.ImageFit.COVER,
                                                    )
                                                ],
                                                width= 40,
                                                height= 40,
                                                vertical_alignment= CrossAxisAlignment.CENTER,
                                                alignment= MainAxisAlignment.CENTER,
                                            ), 
                                            ProgressRing(
                                                width= 40, 
                                                height= 40, 
                                                value= 0.4, 
                                                bgcolor= Colors.with_opacity(0.54, Colors.INVERSE_SURFACE), 
                                                stroke_width= 2, 
                                                color= GOLD,
                                            ),
                                        ]
                                    ),
                                ], 
                                vertical_alignment= CrossAxisAlignment.CENTER, 
                                alignment= MainAxisAlignment.CENTER
                            ),
                            Column(
                                controls=[
                                    Text(value= 'Continue Listening', size=12),
                                    self.current_name,
                                ], 
                                spacing= 0
                            ),
                        ],
                    ), 
                    margin= 5
                ),
                IconButton(
                    Icons.PLAY_CIRCLE_FILL_ROUNDED, 
                    icon_color= GOLD,
                    on_click= self.onclick
                ),
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
        )