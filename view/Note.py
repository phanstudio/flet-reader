import flet as ft
from Utility import *
from user_controls import Navbar
from textwrap import shorten

class MainNote(ft.Button):
    def __init__(self, tit, subt, n=0, m= ['learning'], pg= ''):
        super().__init__(
            style=ft.ButtonStyle(
                shape= ft.RoundedRectangleBorder(5),
                padding= 5,
            )
        )
        self.page = pg
        short = shorten(subt[0], 39, placeholder='..')
        short_title = shorten(tit, 20, placeholder='..')
        self.frame = ft.Column(
            controls=[
                ft.Container(
                    ft.Row(
                        spacing= 5, 
                        alignment= ft.MainAxisAlignment.END
                    )
                )
            ], 
            alignment= ft.MainAxisAlignment.END
        )

        self.check = ft.Ref[ft.Checkbox]()
        
        self.content= ft.Row([
            ft.Checkbox(
                fill_color= {ft.ControlState.SELECTED:GOLD}, 
                # on_change=self.onselect,
                visible= False,
                ref= self.check
            ),
            ft.ListTile(
                title= ft.Text(
                    value= short_title.title(), 
                    size= 14, 
                    weight= BOLD,
                ),
                subtitle= ft.Row(
                    controls=[
                        ft.Text(
                            value= short, 
                            size= 10,
                        ), 
                        self.frame
                    ], 
                    alignment= ft.MainAxisAlignment.SPACE_BETWEEN),
                ),
            ], 
            spacing= 0
        )
        
        # self.style = ft.ButtonStyle(padding= ft.padding.symmetric(0,0))
        self.on_click = self.onclick
        self.data = n

    def tags(self, text, color):
        color = color[1:]
        return ft.Container(
            ft.Text(
                value=text, 
                color= f'#{color}', 
                size= 8,
            ),
            bgcolor= f'#22{color}', 
            padding= 3, 
            border_radius= 3,
        )
    
    def onclick(self, e: ft.ControlEvent):
        if not self.check.current.visible:
            self.page.session.set("NoteId", e.control.data)
            self.page.go(f'/editnote')
            # self.page.go(f'/note/{e.control.data}')
        else:
            self.check.current.value = (
                True
                if not self.check.current.value
                else False
            )
            self.update()

class NoteView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/note",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(4),
            floating_action_button= ft.FloatingActionButton(
                icon= ft.Icons.ADD_CIRCLE_ROUNDED,
            ),
        )

        self.grid2 = ft.ListView(
            expand= True,
            spacing= 5,
            padding= 0
        )

        self.defualt = ft.Image(
            '/covers/r2.png',
            expand= True
        )
        
        pb = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text='Delete'),
                # ft.PopupMenuItem(text="Item 1"),
            ]
        )

        self.opt = ft.Row(
            controls=[
                ft.Container(
                    ft.Text('Notes', size= 25, weight= BOLD), 
                    margin= ft.margin.only(left= 20),
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.DELETE, visible=False, on_click= self.delete),
                        ft.IconButton(ft.Icons.SELECT_ALL, on_click= self.selectall),
                        ft.IconButton(ft.Icons.SEARCH,), 
                        ft.IconButton(ft.Icons.MORE_VERT_ROUNDED, on_click=self.deltoggle),
                        #  pb
                    ],
                    alignment= ft.MainAxisAlignment.END, 
                    spacing= 0,
                ),
            ], 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.controls=[
            self.opt,
            self.defualt,
            self.grid2,
        ]

    def deltoggle(self, e):
        for i in self.grid2.controls:
            if not i.content.controls[0].visible:
                i.content.controls[0].visible = True
                self.opt.controls[1].controls[0].visible = True
            else:
                i.content.controls[0].visible = False
                self.opt.controls[1].controls[0].visible = False
                i.content.controls[0].value = False
        self.update()
    
    def selectall(self, e):
        for i in self.grid2.controls:
            i.content.controls[0].visible = True
            i.content.controls[0].value = (True
            if not i.content.controls[0].value == True
            else False)
            self.opt.controls[1].controls[0].visible = True
        self.update()
    
    def delete(self, e):
        for i in range(len(self.grid2.controls)-1, -1, -1):
            i = self.grid2.controls[i]
            if i.content.controls[0].value == True:
                self.grid2.controls.remove(i)
                remove_note(self.page, i.data)
                
        self.deltoggle(e)
        if len(self.grid2.controls) == 0:
            self.defualt.visible = True
        self.update()
        
    def did_mount(self):
        notes = load_notes(self.page)
        for note in notes:
            num = note.split('.')[1]
            note_prop = load_note_prop(self.page, note)
            self.grid2.controls.append(
                MainNote(tit= note_prop[0], subt=note_prop[1][0], n= num, pg= self.page)
            )
        
        self.defualt.visible = not len(notes) > 0
        self.grid2.visible = not self.defualt.visible 
        self.floating_action_button.on_click= lambda _: open_note(self.page)
        self.update()
        return super().did_mount()
