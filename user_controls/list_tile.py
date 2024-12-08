import flet as ft
import os
import shutil
from Utility import root_path
from textwrap import TextWrapper

GOLD = '#B49455'

class List_Tile(ft.IconButton):
    def __init__(self, pg:ft.Page, txt, prog= 'd'):
        super().__init__()
        self.pg= pg
        self.txt = txt
        self.on_click = self.onclick
        self.fin = False
        if prog == 'd':
            vis = [True,False,False]
            self.fin = False
        elif prog == 'p':
            vis = [False,False,True]
        else:
            self.fin = True
            vis = [False,True,False]
        self.prg = ft.Ref[ft.ProgressBar]()
        self.ico = ft.Ref[ft.Icon]()
        self.exit = ft.Ref[ft.Icon]()

        self.content= ft.Container(
            ft.Row([
                ft.Text(txt, size= 12),
                ft.ProgressBar(width=60, ref= self.prg, visible= vis[0]),
                ft.Icon(name= ft.icons.DONE, color= GOLD, ref= self.ico, visible= vis[1]),
                ft.Icon(name= ft.icons.CANCEL, color= GOLD, ref= self.exit, visible= vis[2])
            ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN), 
            bgcolor= ft.colors.with_opacity(0.1, GOLD),
            border_radius= 60,
            padding= 15,
            expand= True)
    
    def onclick(self, e):
        if self.fin:
            self.pg.go(f'/lib/{self.txt}')
    
    def done(self, prog='d'):
        if prog == 'd':
            self.prg.current.visible = True
            self.ico.current.visible = False
            self.exit.current.visible = False
            self.fin = False
            self.update()
        else:
            self.exit.current.visible = False
            self.prg.current.visible = False
            self.ico.current.visible = True
            self.fin = True
            self.update()

class BookProgressSheet(ft.BottomSheet):
    def __init__(self, height: ft.OptionalNumber = None):
        self.body = ft.Ref[ft.Column]()
        super().__init__(
            show_drag_handle = True,
            content = ft.Column(
                ref= self.body,
                controls=[
                    ft.ElevatedButton(
                        "x",
                        height= 5, 
                        width= 100, 
                        on_click= self.onclose,
                        visible= False,
                        bgcolor= ft.colors.with_opacity(0.3, ft.colors.INVERSE_SURFACE)
                    ),
                    ft.Text('Latest Adds'),
                    ft.ListView([], expand= True),
                ], 
                horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
                expand=True
            )
        )

        self.shadow = ft.BoxShadow(
            blur_style= ft.ShadowBlurStyle.OUTER, 
            blur_radius= 4,
            color= ft.colors.with_opacity(0.2, ft.colors.INVERSE_SURFACE),
        )

        # self.content = ft.Column(
        #     ref= self.body,
        #     controls=[
        #         ft.ElevatedButton(
        #             "x",
        #             height= 5, 
        #             width= 100, 
        #             on_click= self.onclose,
        #             visible= False,
        #             bgcolor= ft.colors.with_opacity(0.3, ft.colors.INVERSE_SURFACE)
        #         ),
        #         ft.Text('Latest Adds'),
        #         ft.ListView([], expand= True),
        #     ], 
        #     horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
        #     expand=True
        # )

        self.height = height

    # height
    @property
    def height(self) -> ft.OptionalNumber:
        return self._get_attr("height")

    @height.setter
    def height(self, value: ft.OptionalNumber):
        self._set_attr("height", value)

    def clear(self):
        dts: list = self.page.client_storage.get_keys('Book')
        dts.remove('Book.hist')
        self.page.client_storage.set('Book.hist', [])
        # add clear the path
       
        for i in dts:
            self.page.client_storage.remove(i)
            shutil.rmtree(os.path.join(root_path,'Books',f'{i.split(".")[-1]}'))
    
    def onclose(self, e):
        # self.visible = False
        if self.expand == True:
            self.expand = False
            self.open = False
            for  i in self.body.current.controls[1:]:
                i.visible = False
        else:
            self.expand = True
            self.open = True
            for  i in self.body.current.controls[1:]:
                i.visible = True
        self.update()

    def popup(self, e):
        self.open()
        self.page.update()

    def did_mount(self):
        past_hist:list = self.page.client_storage.get('Book.hist')
        if past_hist != None:
            books = self.page.client_storage.get_keys('Book')

            past_hist.reverse()
            w = TextWrapper(25)

            for i in past_hist:
                p = 'f' if 'Book.'+i in books else 'd'
                i = w.fill(i)
                self.content.controls[2].controls.append(List_Tile(self.page, i, p))
        return super().did_mount()
