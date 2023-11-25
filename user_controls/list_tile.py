import flet as ft

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
