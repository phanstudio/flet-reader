from textwrap import shorten
from flet import (Text, IconButton, Container, UserControl, Row, Column, ProgressRing,
                  CrossAxisAlignment, MainAxisAlignment, colors, Stack, padding, icons)
from flet_core.control import Control
from flet_core.ref import Ref
from Utility import GOLD, BOLD
import flet as ft

class Reading(UserControl): # change
    def __init__(self, onclick=None):
        super().__init__()
        self.onclick = onclick

    def main_container(self):
        library_text: Container = Container(content= Row([
            Container(Row([
                Row([
                    Stack([
                        Row([
                            ft.Image(src='./assets/9.png', width= 30, 
                        height= 30, border_radius= 50,)],
                        width= 40,
                        height= 40,
                        vertical_alignment= CrossAxisAlignment.CENTER,
                        alignment= MainAxisAlignment.CENTER,
                        ),
                        
                        ProgressRing(width= 40, height= 40, value= 0.4, 
                                     bgcolor= colors.with_opacity(0.54, colors.INVERSE_SURFACE), stroke_width= 2, 
                                     color= GOLD),
                    ]),
                ], vertical_alignment= CrossAxisAlignment.CENTER, 
                alignment= MainAxisAlignment.CENTER),
                 Column([
                    Text(value= 'Continue Listening', size=12),
                    Text(value= 'Tales of Fate', color=GOLD, size= 15, 
                         weight= BOLD),
                ], spacing= 0),],), margin= 5),
            IconButton(icons.PLAY_CIRCLE_FILL_ROUNDED, icon_color= GOLD,
                       on_click= self.onclick)
            ], alignment= MainAxisAlignment.SPACE_BETWEEN), expand= True, 
             border_radius= 50, padding= padding.symmetric(horizontal=5),
            bgcolor= colors.with_opacity(0.05, colors.INVERSE_SURFACE),
            ink= True,
            )
        
        return library_text
        
    
    def build(self) -> Container:
        return self.main_container()
