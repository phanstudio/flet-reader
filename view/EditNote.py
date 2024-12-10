import flet as ft
from Utility import *
from user_controls import Note_frame, Library_frame, Reading, Library, Note, Navbar
import pytweening as pytw

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
    def __init__(self,delfunc: ft.Column,  typ= 'H', value= ''):
        super().__init__()
        self.typs = typ
        self.delfunc = delfunc
        self.data = 'e'

        self.value = value
        m = {'H': (15, 'Add a Header', 0, ft.TextCapitalization.WORDS, BOLD, GOLD, 'red', 30),
             'SH': (12, 'Add a Subheader', 5, ft.TextCapitalization.SENTENCES, BOLD, ft.Colors.with_opacity(0.8,GOLD), 'yellow', 20),
             'T': (10, 'Add a Body', 10, None, 'blue', '', '', 15),
              }
        n =['text_size', 'hint_text']
        self.typ = dict(zip(n, m[typ][:-2]))
        self.pad = m[typ][-6]
        self.cap = m[typ][-5]
        self.b = m[typ][-4]
        self.c = m[typ][-3]
        self.but_s = m[typ][-1]
        self.but_C = m[typ][-2]
        self.content = self.editor()
        self.on_hover = self.onhover
        self.padding = ft.padding.only(self.pad)

    def onhover(self, e: ft.ControlEvent):
        if e.data == 'true':
            self.close.current.visible = True
            self.bar.current.visible = True
        else:
            self.close.current.visible = False
            self.bar.current.visible = False
        self.update()
    
    def editor(self):
        # for body can be a row mechnisim
        self.frame = ft.Row([], expand= 5, spacing= 4)
        st = ft.TextField(value=self.value,
                          color= self.c,
                          dense= True,
                          capitalization= self.cap,
                          on_change= self.onchange,
                          border= ft.InputBorder.NONE,
                          data= self.typs,
                          text_style= ft.TextStyle(
                                weight= self.b,
                            ),
                            **self.typ,
                                multiline=True, #selection_color= GOLD
                                )
        
        self.close = ft.Ref[ft.IconButton]()
        self.bar = ft.Ref[ft.ElevatedButton]()

        self.frame.controls.append(
            ft.IconButton(
                ft.Icons.CLOSE, icon_size= 15,
                ref= self.close,
                on_click= self.closed,
                  width= 20,
                  height= 20,
                  visible= False,
                  style=ft.ButtonStyle(
                      padding= 0
                  ))
            )
        self.frame.controls.append(
            ft.ElevatedButton(
                width= 5,
                ref= self.bar,
                height= self.but_s,
                visible= False,
                style=ft.ButtonStyle(
                shape= ft.RoundedRectangleBorder(radius=1),
                bgcolor= {
                    ft.ControlState.HOVERED: GOLD,
                    ft.ControlState.DEFAULT: self.but_C,
                    ft.ControlState.PRESSED: ft.Colors.SURFACE,
                    },
                overlay_color= ft.Colors.with_opacity(0.2,'white')
                ))
        )
        self.frame.controls.append(st)
        return self.frame
    
    def closed(self, e):
        self.delfunc.controls.remove(self)
        self.delfunc.update()

    def onchange(self, e: ft.ControlEvent):
        # self.bar.current.height = 
        self.update()

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
    def __init__(self, page, sec):
        self.pg = page
        self.sec = sec
        super().__init__()

        self.content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
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
                                        ft.icons.TITLE, size= 14, 
                                        func= lambda _: self.onclick('T')
                                    ),
                                    SimpleButton(
                                        img= r'iconz\\new-section.svg', 
                                        size= 22, 
                                        func= self.add_section
                                    ),
                                    SimpleButton(
                                        ft.icons.DRAG_HANDLE
                                    ),
                                ],
                                height= 200,
                                spacing= 0,
                                tight= True,
                            ), 
                            bgcolor= GOLD, 
                            border_radius=ft.border_radius.horizontal(20),
                        ),
                    ],
                    alignment= ft.MainAxisAlignment.CENTER,
                )
            ], 
            alignment= ft.MainAxisAlignment.END,
        )
    
    def onclick(self, typ):
        self.pg.frame.controls.append(Editor(self.pg.frame, typ))
        self.pg.frame.update()
    
    def add_section(self, e):
        self.sec.visible = True
        self.sec.update()

class EditNoteView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/editnote",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(4),
        )
        self.new_ndt = []
        self.head = 'Untitled Note'
            
        self.content: ft.Column = ft.Column(
            [], 
            # height= 610,
            # tight= True,
            expand= True,
            alignment= ft.MainAxisAlignment.CENTER
        )
        self.cont = ft.Container(
            self.content, 
            # bgcolor= 'red',
        )
        self.controls = [
            self.cont
        ]
    
    def onclick(self):
        self.page.frame.controls.append(Editor())

    def header(self):
        self.tit = ft.Ref[ft.TextField]()
        cont = ft.Row([
            ft.IconButton(icon= ft.Icons.CHEVRON_LEFT, icon_color= GOLD,
                on_click= self.onback),
            ft.TextField(value=self.head, 
                      ref = self.tit,
                      dense= True,
                      width = 200,
                      multiline= True,
                      border= ft.InputBorder.NONE,
                      text_align= 'center',
                      text_style= ft.TextStyle(
                            weight=  BOLD,
                        ),
                    ),
            ft.IconButton(icon= ft.Icons.HELP, icon_color= GOLD,
                on_click= lambda _: print('#')),
            ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN)
        return cont
    
    def onback(self, e: ft.ControlEvent):
        head = self.tit.current.value
        data = []
        for i in self.frame.controls:
            if i.data == 'e':
                data.append([
                    i.content.controls[-1].value,
                    i.content.controls[-1].data
                ])
            else:
                data.append([
                    i.tit,
                    i.rang,
                    i.src, 
                    'S'
                ])
        # create_note(self.page, self.ids, head, data) # saves note
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
            
            editor = ft.Column(
                expand= 5, 
                tight= True,
                scroll=ft.ScrollMode.AUTO, 
                spacing= 2
            )
            if len(self.new_ndt) != 0:
                for *n, t in self.new_ndt:
                    if t != 'S':
                        editor.controls.append(Editor(value=n[0], typ=t, delfunc= editor)) # add type later
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
                editor.controls.append(Editor(delfunc= editor))
            self.content.controls += [
                self.header(),
                editor,
            ]
            self.update()
        else:
            self.page.go('/note')

        return super().did_mount()

#             v_Audio = sub.content.audio1
#             sec = section_overlay(page, sp1, v_Audio)
#             page.overlay.append(format_panel(sp1, sec))
#             page.overlay.append(v_Audio)
#             page.overlay.append(sec)
#             page.views.append(
#                 View(
#                     route=f'/note/{troute.id}',
#                     controls=[
#                         sp1.build(),
#                     ],
#                     spacing= 26,
#                 )
#             )
#         page.update()
