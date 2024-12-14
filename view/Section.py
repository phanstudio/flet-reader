import flet as ft
from Utility import *
from user_controls import Navbar

class audiomark(ft.Container):
    def __init__(self, num, rang, audio1, src, par=None, 
                 clickable= None, width= None, ondel=None, close_vis = False):
        super().__init__()
        self.audio1 = audio1
        self.rang = rang
        self.ondel = self.remove if ondel != None else self.delete
        self.src = src
        self.tit = num
        self.close_vis = close_vis
        self.close = ft.Ref[ft.IconButton]()
        self.start = ft.Ref[ft.Text]()
        self.bar = ft.Ref[ft.ProgressBar]()
        self.end = ft.Ref[ft.Text]()
        self.pausebut = ft.Ref[ft.IconButton]()
        self.playbut = ft.Ref[ft.IconButton]()
        self.par = par

        self.content = ft.Row([
            ft.Container(
                ft.IconButton(ft.icons.CLOSE, icon_size=13,
                    width= 20, height= 20, 
                    ref= self.close, visible= False, style=ft.ButtonStyle( padding= 0,),
                    on_click= self.ondel),on_hover= self.pause_hover
                ),
            ft.Column([
                    ft.Row([
                        ft.Text(num, weight= BOLD),
                        ft.Container(
                            ft.IconButton(ft.icons.PAUSE, icon_size=13, ref= self.pausebut,
                                width= 30, height= 30, visible= False, 
                                on_click= self.onpause), on_hover= self.pause_hover
                        ),
                        ft.IconButton(ft.icons.REPEAT, icon_size=13,
                                        width= 30, height= 30, visible= False),
                    ], spacing= 0),
                    ft.Row([
                        ft.Text(convertMillis(rang[1]-rang[0],), size= 10, ref= self.start),
                        ft.ProgressBar(value=0, expand= True, ref= self.bar,
                                       color= GOLD,
                                        bgcolor= ft.Colors.with_opacity('0.3',ft.Colors.INVERSE_SURFACE)),
                    ft.Stack([ft.Container(
                            ft.IconButton(ft.icons.PLAY_ARROW, icon_size=13, ref= self.playbut,
                            width= 20, height= 20,
                            on_click= self.onclick, style=ft.ButtonStyle( padding= 0,),
                            ), on_hover= self.pause_hover
                        ),
                        ft.Container(
                            ft.IconButton(ft.icons.PAUSE, icon_size=13, ref= self.pausebut,
                            width= 20, height= 20, 
                            visible= False, 
                            on_click= self.onpause, style=ft.ButtonStyle( padding= 0,),
                            ), on_hover= self.pause_hover
                        ),]),
                    ])
                ], spacing= 0, expand= True),
        ], spacing=0)
        self.bgcolor= ft.Colors.with_opacity(0.1, ft.Colors.INVERSE_SURFACE)
        self.padding= ft.padding.symmetric(2,20)
        self.border_radius= 60
        self.width = width
        self.on_hover = self.onhover
        if clickable == None:
            self.on_click = self.onclick
        else:
            self.on_click = clickable
        self.ink = True
        self.data = 0

    def remove(self, e):
        self.par.grid2.controls.remove(
            self
        )
        if len(self.par.grid2.controls) == 0:
            self.par.defualt.visible = True
        self.par.update()

    def delete(self, e):
        se = self.rang
        srcs = self.src
        name = self.tit
        section = self.page.client_storage.get('section.list')        
        section.remove([name, srcs, se])
        self.page.client_storage.set(
            f'section.list',
            section
        )
        self.remove('e')

    def onhover(self, e: ft.ControlEvent):
        if e.data == 'true':
            self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.INVERSE_SURFACE)
            self.scale = 1.02
            if self.close_vis:
                self.close.current.visible = True
                self.padding = self.padding= ft.padding.symmetric(2,10)
        else:
            self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.INVERSE_SURFACE)
            self.scale = 1
            if self.close_vis:
                self.close.current.visible = False
                self.padding = self.padding= ft.padding.symmetric(2,20)
        self.update()
    
    def onclick(self, e):
        if self.par.grid2 != None:
            for i in self.par.grid2.controls:
                if i.data == 1:
                    i.onpause(e)
        self.audio1.outside = self.playback_control
        self.audio1.Oplay = self.rang[0]
        self.audio1.src = self.src
        self.audio1.page.update()
        self.data = 1
        
        self.pausebut.current.visible = True
        self.playbut.current.visible = False
        self.audio1.play()
        self.audio1.seek(self.audio1.Oplay)
        self.update()

    def onpause(self, e):
        self.data = 0
        self.pausebut.current.visible = False
        self.audio1.pause()
        self.playbut.current.visible = True
        self.start.current.value = convertMillis(self.rang[1]- self.rang[0])
        self.bar.current.value = 0
        self.update()
    
    # def did_mount(self):
    #     self.audio1.pause()
    #     self.audio1.outside = 1
    #     return super().did_mount()

    def will_unmount(self):
        self.audio1.Oplay = None
        self.audio1.outside = None
        return super().will_unmount()

    def pause_hover(self,e: ft.ControlEvent):
        if e.data == 'true':
            self.on_click = None
        else:
            self.on_click = self.onclick
        self.update()
    
    def playback_control(self, e):
        if int(e.data) <= self.rang[1]:
            self.start.current.value = convertMillis(self.rang[1]- int(e.data))
            self.bar.current.value = (int(e.data)-self.rang[0])/(self.rang[1]-self.rang[0])
        else:
            self.onpause(e)
        self.update()

class SectionView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/section",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(3),
        )

        self.grid2 = ft.ListView(
            expand= True,
            spacing= 15,
        )

        self.defualt = ft.Image(
            '/covers/10.png', 
            expand=True
        )

        self.controls = [
            ft.Row(
                controls=[
                    ft.Text(
                        'Bookmarks', 
                        size= 20, 
                        weight= BOLD
                    ), 
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        on_click=self.del_toggle, 
                        data= 0
                    ),
                ], 
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            self.defualt,
            self.grid2,
        ]
        
    def did_mount(self):
        # self.audio1.pause()
        # self.audio1.outside = 1
        section = self.page.client_storage.get('section.list')
        if section is None: section = []
        
        for note in section:
            num, note_prop, rang = note
            self.grid2.controls.append(
                audiomark(num, rang, audio1, note_prop, self)
            )
        
        self.defualt.visible = not len(section) > 0
        self.grid2.visible = not self.defualt.visible
        self.update()

        return super().did_mount()

    def del_toggle(self, e):
        if e.control.data == 0:
            e.control.data = 1
            for i in self.grid2.controls:
                i.close.current.visible = True
        else:
            e.control.data = 0
            for i in self.grid2.controls:
                i.close.current.visible = False
        self.update()

