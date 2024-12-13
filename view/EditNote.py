import flet as ft
from Utility import *
from user_controls import Navbar

textStyleSheet = { # change to dict
    'H': {
        "text_size": 15,
        "hint_text": 'Add a Header',
        "weight": BOLD,
        "color": GOLD,
        "bar_color": 'red',
        "capitalization": ft.TextCapitalization.WORDS,
        "padding": 0,
    },
    'SH': {
        "text_size": 12,
        "hint_text": 'Add a Subheader',
        "weight": BOLD,
        "color": ft.Colors.with_opacity(0.8, GOLD),
        "bar_color": 'yellow',
        "capitalization": ft.TextCapitalization.SENTENCES,
        "padding": 5,
    },
    'T': {
        "text_size": 10,
        "hint_text": 'Add Text',
        "weight": None,
        "color": None,
        "bar_color": 'blue',
        "capitalization": None,
        "padding": 10,
    },
}

class section_overlay(ft.Container):
    def __init__(self, page:pG, spg, audio1):
        self.page = page
        self.audio1 = audio1
        self.spg = spg
        super().__init__()
        self.bgcolor = ft.Colors.BACKGROUND
        self.visible = False
        self.padding = ft.padding.all(10)
        self.expand = True
        section = page.client_storage.get('section.list')
        if section is None: section = []

        self.grid2 = self.grids()
        for note in section:
            num, note_prop, rang = note
            # self.grid2.controls.append(
            #     audiomark(num, rang, audio1, note_prop, self.grid2, self.onclick)
            # )

        self.content = ft.Column([
            ft.Row([ft.IconButton(ft.icons.CLOSE, on_click= self.onclose),
                ft.Text('Sections', size= 20, weight= BOLD),
                 ]),
            self.grid2,
            ], expand= True)
        
    def grids(self) -> ft.ListView:
        return ft.ListView(
            expand= True,
            spacing= 15,
        )

    def onclick(self, e:ft.ControlEvent):
        # self.spg.frame.controls.append(
        #     audiomark(e.control.tit, e.control.rang, self.audio1,
        #               src= e.control.src, par= self.spg.frame,
        #               width= 200, close_vis= True, ondel= '0')
        # )
        self.spg.frame.update()
        self.visible = False
        self.audio1.pause()
        self.update()

    def onclose(self, e:ft.ControlEvent):
        self.visible = False
        self.update()

class Editor(ft.Container):
    def __init__(self, typ= 'H', value= ''):
        super().__init__(
            data = 'e',
            expand = True,
        )
        self.typs = typ
        self.value = value
        self.nobar = False

        self.typ = textStyleSheet[typ]
        self.on_hover = self.onhover
        self.padding = ft.padding.only(self.typ["padding"])
        self.close = ft.Ref[ft.IconButton]()
        self.bar = ft.Ref[ft.Container]()

        self.text_body = ft.TextField(
            value=self.value,
            color= self.typ["color"],
            dense= True,
            capitalization= self.typ["capitalization"],
            border= ft.InputBorder.NONE,
            data= self.typs,
            text_style= ft.TextStyle(
                weight= self.typ["weight"],
            ),
            text_size= self.typ["text_size"],
            # hint_text= self.typ["hint_text"],
            label= self.typ["hint_text"],
            multiline=True, 
            collapsed=True,
            #selection_color= GOLD
            expand= True,
            on_change= self.onchange
        )

        self.frame = ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.CLOSE, 
                    icon_size= 15,
                    ref= self.close,
                    on_click= self.closed,
                    width= 20,
                    height= 20,
                    visible= False,
                    style=ft.ButtonStyle(
                        padding= 0
                    ),
                ),
                ft.Container(
                    content=self.text_body,
                    border= self.hide_border(False),
                    expand= True,
                    padding= ft.padding.only(5),
                    ref= self.bar,
                ),
            ],
            expand=True,
            spacing= 0,
            vertical_alignment= ft.CrossAxisAlignment.START,
        )

        self.content = ft.Container(
            self.frame, 
            padding= 5, 
            expand= True,
        )
    
    def hide_border(self, value):
        bar = not self.nobar
        if bar:
            return  (
                ft.border.only(
                    left= ft.BorderSide(
                        5, 
                        self.typ["bar_color"],
                    ),
                ) 
                if not value else
                None
            )
        else: 
            return None
    
    def onchange(self, e=None):
        if not len(self.text_body.value):
            self.text_body.label = self.typ["hint_text"]
            self.nobar = False
        else:
            self.nobar = True
            self.text_body.label = ""
        self.update()

    def onhover(self, e: ft.ControlEvent):
        self.close.current.visible = (e.data == 'true')
        self.bar.current.border = self.hide_border(self.close.current.visible)
        self.content.bgcolor = (
            ft.Colors.with_opacity(0.2, self.typ["color"]) 
            if self.close.current.visible else None
        )
        self.update()
    
    def closed(self, e):
        self.parent.controls.remove(self)
        self.parent.update()

    def did_mount(self):
        self.onchange()
        self.bar.current.border = self.hide_border(self.close.current.visible)
        self.update()
        return super().did_mount()

class SimpleButton(ft.Container):
    def __init__(self, icon : ft.Icon = '', img = '', size = 15,
                func= lambda _: print(9)):
        super().__init__()
        if icon == '':
            frame = ft.IconButton(
                content= ft.Image(
                    img, 
                    width= size-3, 
                    height= size-3,
                    fit=ft.ImageFit.CONTAIN,
                    color=ft.Colors.SURFACE,
                ),
                on_click= func,
            )
        else:
            frame = ft.IconButton(
                icon, 
                icon_color= ft.Colors.SURFACE,
                icon_size= size, 
                on_click= func
            )
        self.content = frame

class FormatPanel(ft.Container):
    def __init__(self):
        super().__init__(
        )
        self.content = ft.Container(
            ft.Column(
                controls=[
                    SimpleButton(
                        img= r'iconz\heading.svg', 
                        size= 16, 
                        func= lambda _: self.onclick('H')
                    ),
                    SimpleButton(
                        img= r'iconz\heading-h2.svg', 
                        size= 20, 
                        func= lambda _: self.onclick('SH')
                    ),
                    SimpleButton(
                        ft.Icons.TITLE, size= 14, 
                        func= lambda _: self.onclick('T')
                    ),
                    SimpleButton(
                        img= r'iconz\\new-section.svg', 
                        size= 22, 
                        # func= self.add_section
                    ),
                    SimpleButton(
                        ft.Icons.DRAG_HANDLE
                    ),
                ],
                height= 200,
                spacing= 0,
                tight= True,
            ), 
            bgcolor= GOLD, 
            border_radius=ft.border_radius.horizontal(20),
        )

    def onclick(self, typ):
        parent : ft.Column = self.get_parent()
        parent.editor.controls.append(
            Editor(typ)
        )
        parent.editor.update()
    
    # def add_section(self, e):
    #     self.sec.visible = True
    #     self.sec.update()

    def get_parent(self):
        return self.parent.parent

class EditNoteView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/editnote",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(4),
            padding= 0,
        )
        self.new_ndt = []
        self.head = 'Untitled Note'

        self.panel = FormatPanel()
            
        self.content: ft.Column = ft.Column(
            expand= True,
            alignment= ft.MainAxisAlignment.CENTER,
        )
        self.editor = ft.Column(
            expand= 5, 
            tight= True,
            scroll=ft.ScrollMode.AUTO, 
            spacing= 2
        )
        self.controls = [
            ft.Stack(
                controls=[
                    ft.Container(
                        content=self.content,
                        margin= 10,
                    ),
                    self.panel
                ],
                expand= True,
                alignment= ft.alignment.center_right
            )
        ]
    
    def header(self):
        self.tit = ft.Ref[ft.TextField]()
        cont = ft.Row(
            controls=[
                ft.IconButton(icon= ft.Icons.CHEVRON_LEFT, icon_color= GOLD,
                    on_click= self.onback),
                ft.TextField(
                    value=self.head, 
                    ref = self.tit,
                    dense= True,
                    width = 200,
                    multiline= True,
                    border= ft.InputBorder.NONE,
                    text_align= 'center',
                    text_style= ft.TextStyle(
                        weight=  BOLD,
                    ),
                    collapsed= True,
                ),
                ft.IconButton(
                    icon= ft.Icons.HELP, 
                    icon_color= GOLD,
                    on_click= lambda _: print('#')
                ),
            ], 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
        )
        return cont
    
    def onback(self, e: ft.ControlEvent):
        head = self.tit.current.value
        data = []
        for i in self.editor.controls:
            if i.data == 'e':
                data.append([
                    i.text_body.value,
                    i.text_body.data
                ])
            else:
                data.append([
                    i.tit,
                    i.rang,
                    i.src, 
                    'S'
                ])
        create_note(self.page, self.ids, head, data) # saves note
        self.page.go('/note')

    def did_mount(self):
        # self.audio1 = audio1
        # self.audio1.pause()
        # self.audio1.outside = 1
        
        self.ids = self.page.session.get("NoteId")
        if self.ids:
            note_prop = load_note_prop(self.page, f'Note.{self.ids}')
            if note_prop != None:
                self.head = note_prop[0]
                self.new_ndt = note_prop[1]
            
            if len(self.new_ndt) != 0:
                for *n, t in self.new_ndt:
                    if t != 'S':
                        self.editor.controls.append(Editor(value=n[0], typ=t)) # add type later
                    else:
                        # editor.controls.append(
                        #     audiomark(
                        #         *n[:2], 
                        #         src=n[2], 
                        #         audio1= self.audio1, 
                        #         par= self.frame,
                        #         width= 200, 
                        #         close_vis= True, 
                        #         ondel= '0'
                        #     )
                        # )
                        pass
            else:
                self.editor.controls.append(Editor())
            self.content.controls = [
                self.header(),
                self.editor,
            ]
            self.update()
        else:
            self.page.go('/note')

        return super().did_mount()

#             v_Audio = sub.content.audio1
#             sec = section_overlay(page, sp1, v_Audio)
#             page.overlay.append(v_Audio)
#             page.overlay.append(sec)
