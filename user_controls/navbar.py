from flet import Page as pG
import flet as ft
from Utility import GOLD
from flet import (IconButton,
                  ControlEvent,Container, UserControl, Row, Column, MainAxisAlignment)


class Mordern_navbar(UserControl):
    def __init__(self, page: pG, defualt: int= 0):
        super().__init__()
        self.page = page
        self.defualt_num = defualt
    
    def user_data(self) -> Container:
        self.Nav_container = Container(#height= 60,
                                #   margin= margin.only(bottom= 10),
                                padding= ft.padding.symmetric(10),
                                  content= Row([
                                      IconButton(ft.icons.HOME_ROUNDED, on_click= self.click, data= '/'),
                                      IconButton(ft.icons.ADD_BOX, on_click= self.click, data= '/srch'),
                                      IconButton(ft.icons.LOCAL_LIBRARY_ROUNDED, on_click= self.click, data= '/lib'),
                                      IconButton(ft.icons.BOOK, on_click= self.click, data= '/bmark'),
                                      IconButton(ft.icons.EDIT_NOTE, on_click= self.click, data= '/note'),
                                  ], alignment= MainAxisAlignment.SPACE_EVENLY)
                                  , bgcolor= ft.colors.BACKGROUND)
        
        
        self.set_defualt(self.defualt_num)
        return self.Nav_container
    
    def set_defualt(self, num):
        # print(self.controls)
        for i in self.Nav_container.content.controls:
            if i.bgcolor != None:
                i.bgcolor = None
                i.icon_color = ft.colors.INVERSE_SURFACE
        defualt = self.Nav_container.content.controls[num]
        defualt.bgcolor = GOLD
        defualt.icon_color = ft.colors.ON_INVERSE_SURFACE
        # self.update()

    def click(self, e: ControlEvent) -> None:
        for i in self.Nav_container.content.controls:
            if i.bgcolor != None:
                i.bgcolor = None
                i.icon_color = ft.colors.INVERSE_SURFACE
                self.update()
        e.control.bgcolor = GOLD
        e.control.icon_color = ft.colors.SURFACE
        e.control.update()
        self.page.go(e.control.data)
    
    def build(self) -> Container:
        return Column([self.user_data()], alignment= MainAxisAlignment.END)
