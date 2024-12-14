from textwrap import shorten
from flet import (Text,ControlEvent, TextButton, Container, UserControl, Row, Column,
                  CrossAxisAlignment, MainAxisAlignment)
from Utility import GOLD, BOLD
import flet as ft

class Note(ft.Container):
    def __init__(self):
        super().__init__()
        Colors = GOLD

        library_text: TextButton = TextButton(
            content= Row(
                controls= [
                    Text(
                        value= 'My Notes',
                        color=Colors
                    ), 
                    ft.Icon(
                        ft.Icons.CHEVRON_RIGHT, 
                        size= 30,
                        color=Colors
                    )
                ],
                alignment= CrossAxisAlignment.CENTER
            ), 
            on_click= lambda _: self.page.go('/note')
        )
        
        self.content = Row(
            controls=[
                library_text,
            ], 
            alignment= MainAxisAlignment.START,
        )

class Note_frame(ft.Container):
    def __init__(self, titl= 'queen of hearts', content= 'Love', ids= 0):
        super().__init__()
        radius = 8
        self.id = ids
        titl = shorten(titl, 17, placeholder='..')
        content = shorten(content[0], 28, placeholder='..')
        self.frame = Container(
            Column([
                Container(Column([ft.Text(value= titl.title(), size= 12, 
                                          weight= BOLD,),
                                  ft.Text(value= content, size= 8,),
                        
                        ], spacing= 2), margin= 10),
                Container(Row([self.tags('Learning', GOLD), self.tags('writing', '#6168CA'),
                             ], spacing= 5, alignment= MainAxisAlignment.END), margin=5)
                ], spacing= 5), width= 150, bgcolor= ft.Colors.TRANSPARENT, border_radius= radius,
                shadow= ft.BoxShadow(blur_radius= 5, 
                                     color= ft.Colors.with_opacity(0.05, ft.Colors.INVERSE_SURFACE), 
                                     offset= ft.Offset(0,7)),
                ink= True, border= ft.border.all(
                    color= ft.Colors.with_opacity(0.26, ft.Colors.INVERSE_SURFACE)),
            )
        self.frame.on_hover = self.onhover
        self.frame.on_click = self.onclick
        self.content = Column(
            controls=[
                self.frame
            ]
        )

    def onhover(self, e: ControlEvent):
        if e.data == 'true':
            self.frame.scale = 1.02
            e.control.update()
        elif e.data == 'false':
            self.frame.scale = 1
            e.control.update()

    def onclick(self, e: ControlEvent):
        self.frame.scale = 1.01
        e.control.update()
        self.page.session.set("NoteId", self.id)
        self.page.go(f'/editnote')

    def tags(self, text, color):
        color = color[1:]
        return Container(Text(value=text, color= f'#{color}', size= 8,),
                         bgcolor= f'#22{color}', padding= 3, border_radius= 3)

    def build(self):
        return 
