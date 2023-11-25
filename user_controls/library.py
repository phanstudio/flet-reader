from textwrap import TextWrapper, shorten
from .Read_bar import readbar
from flet import Page as pG
from flet import (Text,ControlEvent, margin, Stack, Icon, icons, colors,
                  TextButton, Container, UserControl, Row, Column,
                  CrossAxisAlignment, MainAxisAlignment)
from Utility import GOLD, BOLD, os, root_path
from shutil import rmtree
import flet as ft



class Library(UserControl):
    def __init__(self, page: pG):
        super().__init__()
        self.page = page
    
    def main_container(self):
        colors = GOLD
        library_text: TextButton = TextButton(content= Row([
                                          Text(value= 'My Library', color=colors), 
                                          Icon(icons.CHEVRON_RIGHT, size= 30,
                                                  color=colors)],
                                          alignment= CrossAxisAlignment.CENTER), 
                                          on_click= lambda _: self.page.go('/lib'))
        library_bar: readbar = readbar(width= 130, 
                                   fgcolor= colors, tight= True,)
        
        return Row([
                library_text,
                library_bar,
            ], alignment= MainAxisAlignment.SPACE_BETWEEN)
    
    def build(self) -> Row:
        return self.main_container()

class Library_frame(UserControl):  
    def __init__(self, page:pG, li=[], src= '12', per= 10,
                 pert = None,
                 typ= 'TTS'):
        super().__init__()
        self.pert = pert
        text = li[0]
        wrap_lenght = 25
        self.info = li
        if len(li) == 7:
            src = li[6]
        else: src = 'defualt.png'
        self.page = page
        src = f'/covers/'+src
        wrap = TextWrapper(wrap_lenght)
        short = shorten(text, wrap_lenght*3, placeholder='..')
        self.id = li[0]
        self.text = wrap.fill(short)
        radius = 8
        self.bar  =ft.Ref[Container]()
        self.dels  =ft.Ref[ft.IconButton]()
        self.frame = Container(
            Column([
                Stack([
                    ft.Image(height= 180, src=src, opacity= 1,
                            fit= ft.ImageFit.COVER, border_radius= radius),
                    Container(bgcolor= colors.with_opacity(0.35, colors.BLACK),
                              height= 180, width= 120, border_radius= radius),
                    Container(Text(value=typ, color= colors.WHITE, size= 11), # fix
                               padding=2.5, bgcolor= GOLD, border_radius=5,
                               margin= margin.only(top= 3, left= 3)),
                    Text(value= self.text, size= 8, bottom= 5, weight= BOLD,
                         left= 5, color= colors.WHITE),
                    ft.IconButton(icons.DELETE_FOREVER, top= 50, left= 30, ref= self.dels,
                                   icon_size= 50, icon_color= 'Red', visible= False),
                    Container(readbar(width= 60, height=4, align= 'left', tight= True, tp= 'b', 
                                     start= per, fgcolor= GOLD, lp= 0.40), 
                                     top= 10, left= 30, visible= False, ref= self.bar),
                    
                ]),
                
                ], spacing= 5), width= 120, border_radius= radius,
                shadow= ft.BoxShadow(blur_radius= 10, color= colors.with_opacity(0.15, colors.INVERSE_SURFACE), 
                                     offset= ft.Offset(0,15)),
                ink= True,
            )
        self.frame.on_hover = self.onhover
        self.frame.on_click = self.onclick

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
            # e.control.bgcolor = colors.BLACK
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
            self.page.go(f'/lib/{self.id}')
        else:
            self.page.client_storage.remove(f'Book.{self.info[0]}')
            path = os.path.normpath(f'Books/{self.info[0]}')
            path = os.path.join(root_path, path)
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
    
    def build(self):
        return Container(Column([self.frame, # above aserting length ... it
                                #  Text(value= self.text, weight= BOLD)
                                ]), 
                                #  border= ft.border.all(2)
                                 )
