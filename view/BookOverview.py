import flet as ft
from Utility import *
from user_controls import Navbar, readbar

class Chapters(ft.Container):
    def __init__(self, num, tim, ids, uls, sub):
        super().__init__()
        self.down_m = ft.Ref[ft.Icon]()
        self.down_n = ft.Ref[ft.Icon]()
        self.down_d = ft.Ref[ft.Icon]()
        self.down_b = ft.Ref[ft.ProgressRing]()
        self.down_bd = ft.Ref[ft.IconButton]()
        self.ids = ids
        self.num = num
        self.uls = os.path.normpath(f'{uls}/parts/{num}.mp3')
        if self.num not in sub:
            self.pro = 'n'
        else:
            self.pro = 'l'
        if self.pro == 'n':
            self.prog = [True, False, False]
        else:
            self.prog = [False, False, True]

        self.content = ft.IconButton(
            ref= self.down_bd, 
            content= ft.Container(
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f'Part {num}'),
                                ft.Row(
                                    controls=[
                                        ft.Text(f'{tim}'),
                                        # readbar(width= 100, start= 100, align= 'left', fgcolor= GOLD, height= 4),
                                    ], 
                                    spacing= 2,
                                ),   
                            ],
                            expand= 1, 
                            spacing= 1,
                        ),
                        ft.Container(
                            content=ft.Stack(
                                controls=[
                                    ft.Container(
                                        ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.DOWNLOAD_FOR_OFFLINE_ROUNDED,    
                                                    visible= self.prog[0], 
                                                    ref= self.down_m
                                                ),
                                                ft.Icon(
                                                    ft.Icons.ARROW_DOWNWARD_ROUNDED, 
                                                    visible= self.prog[1], 
                                                    ref= self.down_n, 
                                                    size=20
                                                ),
                                                ft.Icon(
                                                    ft.Icons.DELETE, 
                                                    visible= self.prog[2],
                                                    ref= self.down_d
                                                ),
                                            ],
                                            alignment= ft.MainAxisAlignment.CENTER,
                                        ),
                                        alignment= ft.alignment.center
                                    ),
                                    ft.Container(
                                        ft.ProgressRing(
                                            width= 28, 
                                            height= 28, 
                                            #value= 0.4,  
                                            ref= self.down_b,
                                            visible= False,
                                            bgcolor= ft.Colors.with_opacity(0.54,
                                                    ft.Colors.INVERSE_SURFACE), 
                                            stroke_width= 2, 
                                            color= GOLD
                                        ),
                                        alignment= ft.alignment.center
                                    ),    
                                ],
                            ),
                            on_click= self.download_sub, on_hover= self.hov, 
                            border_radius= 5, 
                            # alignment= ft.alignment.center,
                            width= 40, 
                            height= 40
                        ),
                    ], 
                    alignment= ft.MainAxisAlignment.SPACE_BETWEEN, 
                    expand=1,
                ),
                padding= ft.padding.only(10), 
            ), 
            on_click= lambda _: self.onclick(),
            style= ft.ButtonStyle(
                shape= ft.RoundedRectangleBorder(10),
            ),
        )

    def onclick(self):
        self.page.session.set("BookNumber", self.num)
        self.page.go(f'/viewbook')

    def hov(self, e: ft.ControlEvent):
        if e.data == 'true':
            self.down_bd.current.on_click = None
            e.control.bgcolor = ft.Colors.with_opacity(0.1, 
                                        ft.Colors.INVERSE_SURFACE)
        else:
            self.down_bd.current.on_click = lambda _: self.onclick()
            e.control.bgcolor = None
        self.update()

    def download_sub(self, e):
        if self.pro == 'n': # and try clause
            try:
                self.change_icons("load")
                self.update()
                self.download()
                self.change_icons("delete")
                self.update()
                self.pro = "l"
            except:
                self.change_icons("defualt")
        else:
            self.remove_sub()
            self.change_icons("defualt")
            self.pro = "n"
    
    def change_icons(self, value):
        """
        value: [defualt, load, delete]
        """
        # together load
        self.down_b.current.visible = False
        self.down_n.current.visible = False

        # default
        self.down_m.current.visible = False
        
        # delete
        self.down_d.current.visible = False

        match value:
            case "defualt":
                self.down_m.current.visible = True
            case "load":
                self.down_b.current.visible = True
                self.down_n.current.visible = True
            case "delete":
                self.down_d.current.visible = True
            case _:
                raise ValueError("not an case [defualt, load, delete]")
        
        self.update()

    def download(self):
        exctractors_srt(nam= self.ids, num= self.num, 
                        url= os.path.join(ROOTPATH, self.uls))
        info = self.page.client_storage.get(f'Book.{self.ids}')
        
        if self.num not in info[1]:
            info[1].append(self.num)
        
        self.page.client_storage.set(f'Book.{self.ids}', info)

    def remove_sub(self):
        info = self.page.client_storage.get(f'Book.{self.ids}')
        
        if self.num in info[1]:
            info[1].remove(self.num)

        book_path = os.path.join(ROOTPATH,'Books', f'{self.ids}', "sub", f'{self.num}.srt')
        if os.path.exists(book_path):
            os.remove(book_path)
        
        self.page.client_storage.set(f'Book.{self.ids}', info)

class BookOverView(ft.View): # download all creates a loading bar, add play
    def __init__(self) -> None:
        super().__init__(
            route= "/bookover",
            # horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(2),
            floating_action_button= ft.FloatingActionButton(
                "Continue",
                width= 65,
                height= 30,
                on_click= lambda _: self.continue_book()# for open the last read
            )
        )

        self.frame = ft.ListView(
            expand= True,
            spacing= 2,
        )
    
    def did_mount(self):
        self.ids = self.page.session.get("BookId")
        if self.ids:
            self.ndts = self.page.client_storage.get(f'Book.{self.ids}')
            # use checking
            
            self.num = self.ndts[3]

            for i in range(self.num):
                if i != self.num -1:
                    self.frame.controls.append(Chapters(i, '05:00', self.ids, self.ndts[0][1:], self.ndts[1]))
                else:
                    self.frame.controls.append(Chapters(i, self.ndts[4], self.ids, self.ndts[0][1:], self.ndts[1]))
            
            self.controls = [
                self.header(),
                self.info(),
                ft.Text(f'{self.num} Part{"s"if self.num > 1 else ""}'),
                self.frame,
            ]

            self.update()
        else:
            self.page.go("/lib")
        return super().did_mount()

    def continue_book(self):
        self.page.session.set("BookNumber", self.ndts[2])
        self.page.go(f'/viewbook')

    def info(self):
        if len(self.ndts) == 6:
            src = self.ndts[5]
        else: src = 'defualt.jpg'
        src = 'defualt.jpg'
        src = f'covers/'+src
        read_percent = round((int(self.ndts[2])/int(self.ndts[3]))*100)
        r = ft.Row(
            controls=[
                ft.Image(
                    src, 
                    height= 130, 
                    width= 90,
                    border_radius= 5,
                    fit= ft.ImageFit.COVER,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            self.ids.title(), 
                            size= 20,
                            max_lines= 2,
                            overflow= ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            f'Currently reading: {self.ndts[2]}'.title()
                        ),
                        ft.Text(
                            f'{read_percent}% read'.title()
                        ),
                        readbar(
                            GOLD, 
                            align= 'left', 
                            start= read_percent, 
                            height= 4
                        ),
                    ],
                    expand= True,
                ),
            ],
        )
        return r

    def header(self):
        self.tit = ft.Ref[ft.TextField]()
        cont = ft.Row(
            controls=[
                ft.IconButton(
                    icon= ft.Icons.CHEVRON_LEFT, 
                    icon_color= GOLD,
                    on_click= self.onback
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon= ft.Icons.CLOUD_DOWNLOAD_ROUNDED, 
                            icon_color= GOLD,
                            on_click= lambda _: print('#')# downlaod all
                        ),
                        ft.IconButton(
                            icon= ft.Icons.DELETE_FOREVER, 
                            icon_color= GOLD,
                            on_click= lambda _: print('#')
                        ),
                    ],
                ),
            ], 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        return cont

    def onback(self, e: ft.ControlEvent):
        self.page.go('/lib')

    def delete_subs(self):
        info = self.page.client_storage.get(f'Book.{self.ids}')
        
        info[1].clear()

        # delete subs
        # book_path = os.path.join(ROOTPATH,'Books', f'{self.ids}', "sub", f'{self.num}.srt')
        # if os.path.exists(book_path):
        #     os.remove(book_path)
        # for i in self.frame.controls:
        #     i.change_icons(0)
        
        # self.page.client_storage.set(f'Book.{self.ids}', info)
