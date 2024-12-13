from textwrap import TextWrapper, shorten
from .Read_bar import readbar
from flet import Page as pG
from flet import (Text,ControlEvent, margin, Stack, Icon, Icons, Colors,
                  TextButton, Container, Row, Column,
                  CrossAxisAlignment, MainAxisAlignment)
from Utility import GOLD, BOLD, os, ROOTPATH
from shutil import rmtree
import flet as ft

class Library(ft.Container):
    def __init__(self):
        super().__init__()
        Colors = GOLD
        library_text: TextButton = TextButton(
            content= Row(
                controls= [
                    Text(
                        value= 'My Library',
                        color=Colors
                    ), 
                    Icon(
                        Icons.CHEVRON_RIGHT, 
                        size= 30,
                        color=Colors
                    )
                ],
                alignment= CrossAxisAlignment.CENTER
            ), 
            on_click= lambda _: self.page.go('/lib')
        )
        # library_bar: readbar = readbar(width= 130, 
        #                            fgcolor= Colors, tight= True,)
        library_bar: ft.ProgressBar = ft.ProgressBar(
            color= Colors, 
            width= 130,
            value= 0.1,
            border_radius= 50,
        )
        
        self.content = Row(
            controls=[
                library_text,
                library_bar,
            ], 
            alignment= MainAxisAlignment.SPACE_BETWEEN,
        )

class Library_frame(ft.Container):  
    def __init__(
            self, 
            li=[], 
            src= '12', 
            per= 10,
            pert = None,
            typ= 'TTS'
        ):
        super().__init__()
        self.pert = pert
        text = li[0]
        wrap_lenght = 25
        self.info = li
        if len(li) == 7: src = li[6]
        else: src = 'defualt.jpg'
        src = "defualt.jpg"
        src = f'/covers/'+src
        wrap = TextWrapper(wrap_lenght)
        short = shorten(text, wrap_lenght*3, placeholder='..')
        self.id = li[0]
        self.text = wrap.fill(short)
        radius = 8
        self.bar= ft.Ref[Container]()
        self.dels= ft.Ref[ft.IconButton]()
        # animate_scale= ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT)

        # ft.Container(
        #     content=ft.Image(
        #         src = './default.png' if self.info['img'] == None else None,
        #         src_base64= self.info['img'].get_data if self.info['img'] != None else self.info['img'], 
        #         width= size*1, 
        #         height= size,
        #         fit= ft.ImageFit.COVER,
        #         border_radius= 10,
        #     ),
        #     # padding= 2,
        #     shadow=  ft.BoxShadow(
        #         # spread_radius=1,
        #         blur_radius= 5,
        #         color= ft.colors.SHADOW, #ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
        #         offset= ft.Offset(0, 0),
        #         blur_style= ft.ShadowBlurStyle.OUTER,
        #     ),
        #     border_radius= 10,
        #     animate_scale= ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
        # )

        self.frame = Container(
            content=Column(
                controls=[
                    Stack(
                        controls=[
                            ft.Image(
                                height= 180, 
                                src=src, 
                                opacity= 1,
                                fit= ft.ImageFit.COVER, 
                                border_radius= radius
                            ),
                            Container(
                                bgcolor= Colors.with_opacity(0.35, Colors.BLACK),
                                height= 180, 
                                width= 120, 
                                border_radius= radius
                            ),
                            Container(
                                Text(
                                    value=typ, 
                                    color= Colors.WHITE, 
                                    size= 11
                                ), # fix
                                padding=2.5, 
                                bgcolor= GOLD, 
                                border_radius=5,
                                margin= margin.only(top= 3, left= 3),
                            ),
                            Text(
                                value= self.text, 
                                size= 8, 
                                bottom= 5, 
                                weight= BOLD,
                                left= 5, 
                                color= Colors.WHITE
                            ),
                            ft.IconButton(
                                Icons.DELETE_FOREVER, 
                                top= 50, 
                                left= 30, 
                                ref= self.dels,
                                icon_size= 50, 
                                icon_color= 'Red', 
                                visible= False
                            ),
                            Container(
                                content= readbar(
                                    width= 60, 
                                    height=4, 
                                    align= 'left', 
                                    tight= True, 
                                    tp= 'b', 
                                    start= per, 
                                    fgcolor= GOLD, 
                                    lp= 0.40
                                ), 
                                top= 10, 
                                left= 30, 
                                visible= False, 
                                ref= self.bar
                            ),
                        ]
                    ),
                    
                ], 
                spacing= 5
            ),
            width= 120, 
            border_radius= radius,
            shadow= ft.BoxShadow(
                blur_radius= 10, 
                color= Colors.with_opacity(0.15, Colors.INVERSE_SURFACE), 
                offset= ft.Offset(0,15)
            ),
            ink= True,
        )
        self.frame.on_hover = self.onhover
        self.frame.on_click = self.onclick
        self.content= Column(
            controls=[
                self.frame,
                # above aserting length ... it
                #  Text(value= self.text, weight= BOLD)
            ]
        )
    
    def img_entered(self, e:ft.ControlEvent):
        control = e.control.content.controls[0]
        if e.data == 'true':
            control.scale = 1.1
            # control.padding = 2
        else:
            control.scale = None
            # control.padding = None
        
        self.update()

    def onhover(self, e: ft.HoverEvent):
        if e.data == 'true':
            # e.control.bgcolor = '#99B49455'
            self.bar.current.visible = True
            self.frame.content.controls[0].controls[0].height += 10
            self.frame.content.controls[0].controls[1].height += 10
            # self.frame.content.controls[0].controls[0].opacity = 0.6
            e.control.update()
        elif e.data == 'false':
            self.bar.current.visible = False
            # e.control.bgcolor = Colors.BLACK
            self.frame.scale = 1
            self.frame.content.controls[0].controls[0].height -= 10
            self.frame.content.controls[0].controls[1].height -= 10
            e.control.update()

    def onclick(self, e: ControlEvent):
        self.bar.current.visible = False
        self.frame.scale = 1
        self.frame.content.controls[0].controls[0].height -= 10
        self.frame.content.controls[0].controls[1].height -= 10
        e.control.update()
        if self.dels.current.visible != True:
            self.page.session.set("BookId", self.id)
            self.page.go(f'/bookover')
        else:
            self.page.client_storage.remove(f'Book.{self.info[0]}')
            path = os.path.normpath(f'Books/{self.info[0]}')
            path = os.path.join(ROOTPATH, path)
            if os.path.exists(path):
                rmtree(path)
            past_hist:list = self.page.client_storage.get('Book.hist')
            if self.info[0] in past_hist:
                past_hist.remove(self.info[0])
            
            self.page.client_storage.set(f'Book.hist', 
                                past_hist)
            
            self.pert.grid1.controls.remove(self)
            if len(self.pert.grid1.controls) == 0:
                self.pert.defualt.visible = True
            self.pert.update()
