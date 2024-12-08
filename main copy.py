from pprint import pprint
from textwrap import TextWrapper, shorten
from random import choice, randrange
import pytweening as pytw
import flet as ft
import ast
import shutil
from flet import Page as pG
from flet import (View, ElevatedButton, Text, IconButton, TextField,
                  ControlEvent, margin, Container, UserControl)
from flet import (RouteChangeEvent, ViewPopEvent, Row, Column,
                  CrossAxisAlignment, MainAxisAlignment, HoverEvent)
from Utility import *
from user_controls import (Library_frame, Library, Note, List_Tile,
                           Note_frame, Reading, Mordern_navbar, readbar)
from pages import subpage2, loads
import flet.canvas as cv


# why

# views

class Page1(ft.Container):
    def __init__(self, dt, ndt, page):
        self.dt = dt
        self.ndt = ndt
        self.page = page
        super().__init__()
        dts: list = page.client_storage.get_keys('Book')
        if dts != []:
            dts.remove('Book.hist')
        self.dts = []
        for i in dts:
            self.dts.append([i[5:]]+page.client_storage.get(i))
        
        self.grid2 = self.grids1()
        notes = load_notes(page)
        for note in notes:
            num = note.split('.')[1]
            note_prop = load_note_prop(page, note)
            self.grid2.controls.append(
                Note_frame(note_prop[0], note_prop[1][0], num)#, pg= page)
            )
    
    def grids1(self) -> ft.GridView:
       return ft.GridView( 
            height= 180, 
            runs_count=2, 
            horizontal= True,
            child_aspect_ratio= 0.55
                    )
    def grids(self) -> ft.ListView:
       return ft.ListView( 
            height= 190, 
            spacing= 10,
            horizontal= True,
                    )

    def build(self):
        grid1 = self.grids()
        
        self.defualt1 = Container(Row([ft.Image('/covers/7.png', height= 200)], 
                            alignment= MainAxisAlignment.CENTER), bgcolor= 
                            ft.colors.with_opacity(0.1, ft.colors.INVERSE_SURFACE))
        self.defualt2 = Row([ft.Image('/covers/11.png', height= 250)], 
                            alignment= MainAxisAlignment.CENTER)

        if len(self.dts) > 0:
            self.defualt1.visible = False
        else:
            grid1.visible = False
        if len(self.grid2.controls) > 0:
            self.defualt2.visible = False
        
        
        grid1.controls += [Library_frame(li=i, page= self.page) for i in self.dts]

        return Column([ Reading(), Library(self.page),
            self.defualt1,
            grid1,
            Note(),
            self.defualt2,
            self.grid2,
            
            # ft.Image('/covers/defualt.png'),
        ])

class Page2(UserControl):
    def __init__(self, dt, ndt, page):
        self.dt = dt
        self.ndt = ndt
        self.page = page
        self.grid1 = self.grids()
        # page.on_resize = lambda _: p221(self, page)
        dts: list = self.page.client_storage.get_keys('Book')
        if dts != []:
            dts.remove('Book.hist')
        self.dts = []
        for i in dts:
            self.dts.append([i[5:]]+self.page.client_storage.get(i))
        super().__init__()

        self.defualt = Container(ft.Image('/covers/9.png'), 
                              margin= margin.only(top= 60))

        if len(dts) > 0:
            self.defualt.visible = False
        
    
    def grids(self) -> ft.GridView:
       return ft.GridView( 
            height= 550,
            # expand= 1,
            # runs_count=0,
            # auto_scroll= True,
            spacing= 25,
            max_extent= 180,#238, #230 #130
            # runs_count= 3,
            run_spacing= 0, #10
            # padding= 20,
            child_aspect_ratio= 0.80,#0.54,#0.38,
                    )
    
    def onchange(self, v):
        base = 245
        var = pytw.easeOutExpo(v/100)
        
        self.grid1.spacing = 0 if v <= 6 and v >= 3 else 30
        self.grid1.spacing = 0 if v <= 10 and v > 6 else 30

        self.grid1.max_extent = base + ((130-base)*var)

    def did_mount(self):
        return p221(self, self.page)

    def cnr(ids, src, val, per, time):
        return {'ids':ids, 'src':src, 'val': val, 'per': per, 'time': time}

    def build(self):
        self.grid1.controls = [Library_frame(li=i, page= self.page, pert= self) for i in self.dts] #change back
        return Column([
            self.defualt,
            Container(
            self.grid1,
            margin=margin.only(top= 60)
            )],)

class Page3(Container):
    def __init__(self, ndt, page:pG):
        self.ndt = ndt
        self.page = page
        super().__init__()

        self.grid2 = self.grids()

        notes = load_notes(page)
        for note in notes:
            num = note.split('.')[1]
            note_prop = load_note_prop(page, note)
            self.grid2.controls.append(
                MainNote(tit= note_prop[0], subt=note_prop[1][0], n= num, pg= page)
            )

        self.opt = self.options()
        self.defualt = ft.Image('/covers/r2.png')

        if len(notes) > 0:
            self.defualt.visible = False

        self.content = Column([
            self.opt,
            self.defualt,
            self.grid2,
            ], expand= True, spacing= 0)
        self.expand = True
        self.margin=margin.only(bottom= 60, top= 60) #+30

    def grids(self) -> ft.ListView:
        return ft.ListView(
            expand= True,
            spacing= 0,
            padding= 0
        )

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

    def options(self): # add popup
        pb = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text='Delete'),
                # ft.PopupMenuItem(text="Item 1"),
                ])


        return Row([Container(Text('Notes', size= 25, weight= BOLD), margin=margin.only(left= 20)),
                    Row([IconButton(ft.icons.DELETE, visible=False, on_click= self.delete),
                        IconButton(ft.icons.SELECT_ALL, on_click= self.selectall),
                         IconButton(ft.icons.SEARCH,), 
                         IconButton(ft.icons.MORE_VERT_ROUNDED, on_click=self.deltoggle),
                        #  pb
                         
                 ]
                ,alignment= 'end', spacing= 0,
                )], alignment= MainAxisAlignment.SPACE_BETWEEN)

class format_panel(UserControl):
    def __init__(self, page, sec):
        self.pg = page
        self.sec = sec
        super().__init__()

    def main_p(self):
        return Row([Column([
            Container(
            Column([
            simple_button(img= r'iconz\heading.svg', size= 16, 
                          func= lambda _: self.onclick('H')),
            simple_button(img= r'iconz\heading-h2.svg', size= 20, 
                          func= lambda _: self.onclick('SH')),
            simple_button(ft.icons.TITLE, size= 14, func= lambda _: self.onclick('T')),
            simple_button(img= r'iconz\\new-section.svg', size= 22, 
                          func= self.add_section),
            simple_button(ft.icons.DRAG_HANDLE),
            ],
            height= 200,
            spacing= 0,
            tight= True,
            ), bgcolor= GOLD, border_radius=ft.border_radius.horizontal(20),),
        ],
        alignment= MainAxisAlignment.CENTER,
        )], alignment= MainAxisAlignment.END,)
    
    def build(self):
        return self.main_p()

    def onclick(self, typ):
        self.pg.frame.controls.append(Editor(self.pg.frame, typ))
        self.pg.frame.update()
        ...
    
    def add_section(self, e):
        self.sec.visible = True
        self.sec.update()

class sub_page3():
    def __init__(self, page, ids):
        self.page = page
        self.ids = ids
        self.ndts = page.client_storage.get(f'Book.{ids}')
        # print(self.ndts)
                    
        self.content: Column = Column([], height= 610,
                                # tight= True,
                                # expand= True,
                                alignment= MainAxisAlignment.CENTER
                                )
        self.cont = Container(self.content, 
                                # bgcolor= 'red',
                                expand= True
                                )

    def LIst_of_chap(self):
        self.frame = ft.ListView([], expand= 5,
                            spacing= 2
                            )
        return self.frame
    
    def info(self):
        if len(self.ndts) == 6:
            src = self.ndts[5]
        else: src = 'defualt.png'
        src = f'covers/'+src
        r = Row([
            ft.Image(src, height= 130, width= 90,
                     border_radius= 5,
                     fit= ft.ImageFit.COVER),
            Column([
                Text(
                    self.ids.title(), size= 20, width= 220,
                ),
                Text(
                    f'Currently readding: {self.ndts[2]}'.title()
                ),
                Text(
                    f'30% read'.title()
                ),
                readbar(GOLD, align= 'left', start= 30, height= 4),
            ])
        ])
        return r
        ...

    def header(self):
        self.tit = ft.Ref[TextField]()
        cont = Row([
            IconButton(icon= ft.icons.CHEVRON_LEFT, icon_color= GOLD,
                on_click= self.onback),
            Row([
                IconButton(icon= ft.icons.DOWNLOAD, icon_color= GOLD,
                on_click= lambda _: print('#')),
                IconButton(icon= ft.icons.MORE_VERT, icon_color= GOLD,
                on_click= lambda _: print('#')),

            ]),
            ], alignment= MainAxisAlignment.SPACE_BETWEEN)
        return cont

    def onback(self, e: ControlEvent):
        self.page.go('/lib')

    def build(self):
        editor = self.LIst_of_chap()
        self.num = self.ndts[3]

        for i in range(self.num):
            if i != self.num -1:
                editor.controls.append(Chapters(i, '05:00', self.ids, self.ndts[0][1:], self.ndts[1]))
            else:
                editor.controls.append(Chapters(i, self.ndts[4], self.ids, self.ndts[0][1:], self.ndts[1]))


        self.content.controls += [self.header(),
            self.info(),
            Text(f'{self.num} Parts'),
            editor,
            ]
        return self.cont

class Page4(Container):
    def __init__(self, file_picker, page, dp):
        super().__init__()
        self.dp = dp
        self.content = Column([
            Row([
                Text(value='Add a Book',
                     weight= ft.FontWeight.BOLD,
                ),
                IconButton(ft.icons.HISTORY, on_click= self.onclick)
            ], alignment= MainAxisAlignment.SPACE_BETWEEN),
            
            Container(Row([Column([
                ft.IconButton(ft.icons.ADD_ROUNDED,
                              icon_color= 'white',
                              bgcolor= GOLD,
                            #   icon_size= 10,
                              width= 40,
                              height= 40,
                              style=ft.ButtonStyle(
                                  bgcolor= {ft.MaterialState.HOVERED: ft.colors.with_opacity(0.3, 'black')}),
                              on_click=lambda _: file_picker.pick_files(
                                dialog_title= 'Book Adder', file_type= ft.FilePickerFileType.AUDIO)),
                Row([
                    ft.Text('Choose a file to'),
                    ft.Text(' upload ', color= GOLD, weight= ft.FontWeight.BOLD,),
                    ft.Text('here'),
                    ], spacing= 0)
            ], horizontal_alignment= CrossAxisAlignment.CENTER),
            ], alignment= MainAxisAlignment.CENTER),
            bgcolor= ft.colors.with_opacity(0.1, ft.colors.INVERSE_SURFACE),
            # border= ft.border.all(2),
            border_radius= 5,
            padding= 20,
            ),
            
            # ElevatedButton(text='Go back',
            #             on_click= lambda _: page.go('/'))
        ])
    
    def onclick(self, e):
        self.dp.open = False if self.dp.open == True else True
        self.dp.update()
        ...

class Page5(Container):
    def __init__(self, page:pG, audio1):
        self.page = page
        self.audio1 = audio1
        super().__init__()

        section = page.client_storage.get('section.list')
        if section is None: section = []

        self.grid2 = self.grids()
        for note in section:
            num, note_prop, rang = note
            self.grid2.controls.append(
                audiomark(num, rang, audio1, note_prop, self)
            )
        
        self.defualt = ft.Image('/covers/10.png')

        if len(section) > 0:
            self.defualt.visible = False

        self.content = Column([
            Row([Text('Bookmarks', size= 20, weight= BOLD), IconButton(icon=ft.icons.DELETE, 
                                                                       on_click=self.del_toggle, data= 0)], 
                alignment= MainAxisAlignment.SPACE_BETWEEN),
            self.defualt,
            self.grid2,
            ], expand= True)
        self.expand = True
        self.padding=ft.padding.only(bottom= 60)

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

    def did_mount(self):
        self.audio1.pause()
        self.audio1.outside = 1
        return super().did_mount()

    def grids(self) -> ft.ListView:
        return ft.ListView(
            expand= True,
            spacing= 15,
        )

class section_overlay(Container):
    def __init__(self, page:pG, spg, audio1):
        self.page = page
        self.audio1 = audio1
        self.spg = spg
        super().__init__()
        self.bgcolor = ft.colors.BACKGROUND
        self.visible = False
        self.padding = ft.padding.all(10)
        self.expand = True
        section = page.client_storage.get('section.list')
        if section is None: section = []

        self.grid2 = self.grids()
        for note in section:
            num, note_prop, rang = note
            self.grid2.controls.append(
                audiomark(num, rang, audio1, note_prop, self.grid2, self.onclick)
            )

        self.content = Column([
            Row([IconButton(ft.icons.CLOSE, on_click= self.onclose),
                Text('Sections', size= 20, weight= BOLD),
                 ]),
            self.grid2,
            ], expand= True)
        
    def grids(self) -> ft.ListView:
        return ft.ListView(
            expand= True,
            spacing= 15,
        )

    def onclick(self, e:ControlEvent):
        self.spg.frame.controls.append(
            audiomark(e.control.tit, e.control.rang, self.audio1,
                      src= e.control.src, par= self.spg.frame,
                      width= 200, close_vis= True, ondel= '0'))
        self.spg.frame.update()
        self.visible = False
        self.audio1.pause()
        self.update()

    def onclose(self, e:ControlEvent):
        self.visible = False
        self.update()

class audiomark(Container):
    def __init__(self, num, rang, audio1, src, par=None, 
                 clickable= None, width= None, ondel=None, close_vis = False):
        super().__init__()
        self.audio1 = audio1
        self.rang = rang
        self.ondel = self.remove if ondel != None else self.delete
        self.src = src
        self.tit = num
        self.close_vis = close_vis
        self.close = ft.Ref[IconButton]()
        self.start = ft.Ref[Text]()
        self.bar = ft.Ref[ft.ProgressBar]()
        self.end = ft.Ref[Text]()
        self.pausebut = ft.Ref[IconButton]()
        self.playbut = ft.Ref[IconButton]()
        self.par = par

        self.content = Row([
            Container(
                IconButton(ft.icons.CLOSE, icon_size=13,
                    width= 20, height= 20, 
                    ref= self.close, visible= False, style=ft.ButtonStyle( padding= 0,),
                    on_click= self.ondel),on_hover= self.pause_hover
                ),
            Column([
                    Row([
                        Text(num, weight= BOLD),
                        Container(
                            ft.IconButton(ft.icons.PAUSE, icon_size=13, ref= self.pausebut,
                                width= 30, height= 30, visible= False, 
                                on_click= self.onpause), on_hover= self.pause_hover
                        ),
                        ft.IconButton(ft.icons.REPEAT, icon_size=13,
                                        width= 30, height= 30, visible= False),
                    ], spacing= 0),
                    Row([
                        Text(convertMillis(rang[1]-rang[0],), size= 10, ref= self.start),
                        ft.ProgressBar(value=0, expand= True, ref= self.bar,
                                       color= GOLD,
                                        bgcolor= ft.colors.with_opacity('0.3',ft.colors.INVERSE_SURFACE)),
                    ft.Stack([Container(
                            ft.IconButton(ft.icons.PLAY_ARROW, icon_size=13, ref= self.playbut,
                            width= 20, height= 20,
                            on_click= self.onclick, style=ft.ButtonStyle( padding= 0,),
                            ), on_hover= self.pause_hover
                        ),
                        Container(
                            ft.IconButton(ft.icons.PAUSE, icon_size=13, ref= self.pausebut,
                            width= 20, height= 20, 
                            visible= False, 
                            on_click= self.onpause, style=ft.ButtonStyle( padding= 0,),
                            ), on_hover= self.pause_hover
                        ),]),
                    ])
                ], spacing= 0, expand= True),
        ], spacing=0)
        self.bgcolor= ft.colors.with_opacity(0.1, ft.colors.INVERSE_SURFACE)
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
        self.page.client_storage.set(f'section.list',
                                section)
        self.remove('e')

    def onhover(self, e: ControlEvent):
        if e.data == 'true':
            self.bgcolor = ft.colors.with_opacity(0.2, ft.colors.INVERSE_SURFACE)
            self.scale = 1.02
            if self.close_vis:
                self.close.current.visible = True
                self.padding = self.padding= ft.padding.symmetric(2,10)
        else:
            self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.INVERSE_SURFACE)
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

    def pause_hover(self,e: ControlEvent):
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

class downlod_pg(ft.BottomSheet):
    def __init__(self, lts, page:pG, height: ft.OptionalNumber = None,):
        super().__init__()
        self.listtiles = lts
        # self.bgcolor = ft.colors.BACKGROUND
        # self.alignment = ft.alignment.bottom_center
        
        self.height = height
        # self.visible = False
        # self.expand = True
        # self.enable_drag =True
        self.show_drag_handle = True
        # self.margin = margin.only(top= 45)
        # self.padding = 20
        # self.border_radius = ft.border_radius.vertical(50)
        self.body = ft.Ref[Column]()


        self.shadow = ft.BoxShadow(
            blur_style= ft.ShadowBlurStyle.OUTER, 
                                   blur_radius= 4,
                                #    spread_radius= 1
            color= ft.colors.with_opacity(0.2, ft.colors.INVERSE_SURFACE)
                                   )

        self.content = Column(
            ref= self.body,
            controls=[
            ElevatedButton(height= 5, width= 100, 
                           on_click= self.onclose,
                           visible= False,
                           bgcolor= ft.colors.with_opacity(0.3, ft.colors.INVERSE_SURFACE)
                           ),
            Text('Latest Adds'),
            ft.ListView([], expand= True),
        ], horizontal_alignment= CrossAxisAlignment.CENTER, expand=True)

        past_hist:list = page.client_storage.get('Book.hist')
        # self.clear(page)
        if past_hist != None:
            books = page.client_storage.get_keys('Book')

            past_hist.reverse()
            w = TextWrapper(25)

            for i in past_hist:
                p = 'f' if 'Book.'+i in books else 'd'
                i = w.fill(i)
                self.content.controls[2].controls.append(List_Tile(page, i, p))


    # height
    @property
    def height(self) -> ft.OptionalNumber:
        return self._get_attr("height")

    @height.setter
    def height(self, value: ft.OptionalNumber):
        self._set_attr("height", value)


    def clear(self, pg):
        dts: list = pg.client_storage.get_keys('Book')
        dts.remove('Book.hist')
        pg.client_storage.set('Book.hist', [])
        # add clear the path
       
        for i in dts:
            pg.client_storage.remove(i)
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

    def onclick(self, e):
        ...

class Track(ft.GestureDetector):
    def __init__(self, 
                 rel,
                on_change_position
                    ):
        super().__init__()
        # self.visible = False
        self.content = ft.Container(
            content=cv.Canvas(
                on_resize=self.canvas_resized,
                shapes=[],
            ),
            height=125,
            width=float("inf"),
        )
        
        self.prev_selct = 0
        self.next_selct = 0
        self.par = rel
        # self.on_pan_start = self.find_position
        # self.on_pan_update = self.find_position
        self.on_hover = self.change_cursor
        self.on_change_position = on_change_position
    
    def lines(self, num, maxnum, multp = 2):
        halfm = maxnum/multp
        mult = max(1, ((((num-halfm)**2)**0.5)*-1)+halfm)*multp # improve 
        max_high = multp * 60
        
        if mult/multp < 5:
            high = randrange(1, round(mult))*3
        else:
            high = choice([
                randrange(10, max_high), 
                randrange(4, round(mult))
                        ])
        return cv.Rect(
                x=0+(6*num),
                y= ((max_high+ 5)/2)-(high/2),
                height= high,
                border_radius=3,
                paint=ft.Paint(color=GOLD),
                width=3,
            )

    def canvas_resized(self, e: cv.CanvasResizeEvent):
        self.track_width = e.width
        max_num = round(e.width/6)
        self.prev_selct = 0
        self.next_selct = max_num
        if self.par.audiof.track_canvas.audio_duration != None:
            self.content.content.shapes = [
                self.lines(i, max_num) for i in range(max_num)]
            self.set_position(self.par, self.par.c_s.current.value, self.par.c_e.current.value)
        e.control.update()
        
    def find_position(self, e):
        ll = max(
            0, min(e.local_x, self.track_width)
        )
        total_sel = round(self.track_width/(6))
        new_sel = round(ll/6)+1
        if new_sel < round(self.track_width/(6*2)):
            if self.prev_selct < new_sel :
                for i in self.content.content.shapes[: new_sel]:
                    i.paint.color = 'grey10'
            else:
                for i in self.content.content.shapes[new_sel-1: self.prev_selct]:
                    i.paint.color = GOLD
            
            self.prev_selct = new_sel
        else:
            if self.next_selct > new_sel:
                for i in self.content.content.shapes[new_sel-1 : ]:
                    i.paint.color = 'grey10'
            else:
                for i in self.content.content.shapes[self.next_selct: new_sel-1]:
                    i.paint.color = GOLD
            
            self.next_selct = new_sel -1

        self.update()
        # self.on_change_position(self.prev_selct/total_sel, self.next_selct/total_sel)

    def set_position(self,sel, sl, el):
        def converter(ob):
            return (convertminsec(ob)/sel.audiof.track_canvas.audio_duration ) * self.track_width
        slm = converter(sl)
        elm = converter(el)
        sl = max(
            0, min(slm, self.track_width-10)
        )
        el = max(
            10, min(elm, self.track_width)
        )
        total_sel = round(self.track_width/(6))
        new_s = round(sl/6)#+1
        new_e = round(el/6)

        if self.prev_selct < new_s:
            for i in self.content.content.shapes[: new_s]:
                i.paint.color = 'grey10'
        else:
            for i in self.content.content.shapes[new_s-1: self.prev_selct]:
                i.paint.color = GOLD
        
        self.prev_selct = new_s

        if self.next_selct > new_e:
            for i in self.content.content.shapes[new_e : ]:
                i.paint.color = 'grey10'
        else:
            for i in self.content.content.shapes[self.next_selct: new_e]:
                i.paint.color = GOLD
        
        self.next_selct = new_e

        self.update()
        self.on_change_position(self.prev_selct/total_sel, self.next_selct/total_sel)

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

class sections_pg(Container):
    def __init__(self, lts, page:pG, audiof,):
        super().__init__()
        self.listtiles = lts
        self.audiof = audiof
        self.bgcolor = ft.colors.BACKGROUND
        self.alignment = ft.alignment.bottom_center
        self.visible = False
        self.expand = True
        self.padding = 20
        self.body = ft.Ref[Column]()
        self.title = ft.Ref[TextField]()

        self.content = ft.Stack([Column(
            ref= self.body,
            controls=[
                Row([
                    Text('Section bookmark', text_align= 'center', expand= True)
                ]),
                Text('Bookmark title', size= 12, color= ft.colors.with_opacity(0.4, ft.colors.INVERSE_SURFACE),),
            TextField(
                hint_text= 'Add Title',
                multiline= True,
                ref= self.title,
                # label= 'Bookmark Title',
                border= ft.InputBorder.UNDERLINE,
                border_color= ft.colors.with_opacity(0.4, GOLD),
                text_style= ft.TextStyle(weight= BOLD,),
                dense= True,
                hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
            ),
            self.new_body(),
            ft.Divider(),
            Row([
                    self.new_but('Cancle', oncc= self.onclose),
                    self.new_but('Save', 'iconz/Group 42.svg',colr= True, oncc= self.onsave)
               ], alignment= MainAxisAlignment.SPACE_EVENLY)
        ],),
        ])
    
    def new_body(self):
        self.c_s= ft.Ref[Text]()
        self.c_e= ft.Ref[Text]()
        self.c_t= Track(on_change_position= self.change_position, 
                  rel= self)
        g = Container(ft.Stack([
                Container(
                    ft.Image('iconz/Group 37.svg', color= 'white',scale=0.6 ),
                        border_radius= 9,
                        rotate= ft.Rotate(0.8, alignment= ft.alignment.center),
                          shadow= ft.BoxShadow(
                    blur_style= ft.ShadowBlurStyle.OUTER, 
                    blur_radius= 10,
                    color= ft.colors.with_opacity(0.7, GOLD),
                    spread_radius= -5.7
                                   )),
                ft.Image('iconz/Group 38.svg')
            ]), on_click= self.onclick, data= '+', alignment= ft.alignment.center)
        bod = Column([
            self.c_t
        ], expand= True, alignment= MainAxisAlignment.CENTER)


        gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=50,
            on_pan_update=self.on_pan_update1,
        )
        
        gd1 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=50,
            on_pan_update=self.on_pan_update2,
        )

        self.pointer1 = ft.Container(gd, bgcolor=ft.colors.AMBER, width=30, height=30, left=0, top=0)
        self.pointer2 = ft.Container(gd1, bgcolor=ft.colors.RED, width=30, height=30, right=0, top=0)

        self.pointer1.left = -(self.pointer1.width/2)
        self.pointer2.right = -(self.pointer2.width/2)
        cl = ft.Stack([self.pointer1, self.pointer2], expand= True, height=35)

        return Container(Column([
            bod,
            cl,
            Row([
                Text(ref= self.c_s,value= '00:00'),
                Text(ref= self.c_e,value= '00:00'),
            ], alignment= MainAxisAlignment.SPACE_AROUND),
            Row([
                IconButton(ft.icons.FORWARD_10_ROUNDED,
                icon_color=ft.colors.with_opacity(0.4, ft.colors.INVERSE_SURFACE),
                data= '-', on_click= self.add_lose
                ),
                g,
                IconButton(ft.icons.REPLAY_10_ROUNDED,
                icon_color= ft.colors.with_opacity(0.4, ft.colors.INVERSE_SURFACE),
                data= '+', on_click= self.add_lose
                ),
                 ], alignment= MainAxisAlignment.CENTER)
        ], spacing= 30),expand=True)
    
    def on_pan_update1(self, e: ft.DragUpdateEvent):
        gpc= self.page.window_width-(self.pointer2.width+
                                     self.pointer2.right+self.pointer1.width+40+16)
        self.pointer1.left = min(gpc, max(-(self.pointer1.width/2), 
                                          self.pointer1.left + e.delta_x))
        c_start = self.pointer1.left + (self.pointer1.width/2)
        total = self.page.window_width - (40+16)
        self.pointer1.update()
        Clamp1 = self.convertMillis(round((c_start/total) * 
                                        self.audiof.track_canvas.audio_duration))
        et = self.c_e.current.value
        self.c_t.set_position(self, Clamp1, et)

    def on_pan_update2(self, e: ft.DragUpdateEvent):
        gpc= self.page.window_width-(self.pointer1.width+
                                     self.pointer1.left+self.pointer2.width+40+16)
        self.pointer2.right = min(gpc, max(-(self.pointer2.width/2), 
                                self.pointer2.right - e.delta_x))
        c_start = self.pointer2.right + (self.pointer2.width/2)
        total = self.page.window_width - (40+16)
        self.pointer2.update()
        Clamp2 = self.convertMillis(round(((total-c_start)/total) * 
                                        self.audiof.track_canvas.audio_duration))
        st = self.c_s.current.value
        self.c_t.set_position(self, st, Clamp2)

    def add_lose(self, e: ft.ControlEvent):
        st = self.c_s.current.value
        et = self.c_e.current.value
        if e.control.data == '+':
            et = self.convertMillis(convertminsec(self.c_e.current.value) + 10*1000)
        else:
            sl = convertminsec(self.c_s.current.value)- 10*1000
            if not sl < 0:
                st = self.convertMillis(sl)
        
        # self.c_t.set_position(self, st, et)

    def onclick(self, e: ControlEvent):
        
        if e.control.data == '+':
            e.control.data = '-'
            self.audiof.audio1.resume()
            self.audiof.clamp_update('')
            e.control.content.controls[1].src = 'iconz/Group 37.svg'
            self.update()
        else:
            e.control.data = '+'
            self.audiof.audio1.pause()
            self.c_s.current.value = f"{self.convertMillis(self.audiof.clamp_start)}"
            e.control.content.controls[1].src = 'iconz/Group 38.svg'
            self.update()
            ...

        self.page.update()

    def change_position(self, start, end):
        total_a = self.audiof.track_canvas.audio_duration#/1000
        self.audiof.clamp_start = round(total_a* (start))
        self.audiof.clamp_end= round(total_a* (end))
        self.c_s.current.value = self.convertMillis(self.audiof.clamp_start)
        self.c_e.current.value = self.convertMillis(self.audiof.clamp_end)
        self.update()

    def convertMillis(self,millis):
        if type(millis) != int: millis = 0
        seconds = int(millis / 1000) % 60
        minutes = int(millis / (1000 * 60)) % 60

        seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
        minutes_str = f"0{minutes}" if minutes < 10 else f"{minutes}"
        return f"{minutes_str}:{seconds_str}"

    def new_but(self, txt, img= './newproj/assets/Group 43.svg', colr= False, oncc=None):
        colr = ft.colors.with_opacity(0.8, GOLD) if colr else None
        tcolr = 'white' if colr else ft.colors.with_opacity(0.4, ft.colors.INVERSE_SURFACE)
        if colr:
            xl = ft.Image(img, height= 30, width= 30)
        else:
            xl = ft.Icon(ft.icons.CLOSE, 
                         color= ft.colors.with_opacity(0.4, ft.colors.INVERSE_SURFACE))
        return Container(content= Column([
                xl,
                Text(txt, color= tcolr),
            ], horizontal_alignment= CrossAxisAlignment.CENTER, alignment= MainAxisAlignment.END, spacing= 0), 
            on_hover= self.onhov, padding= ft.padding.symmetric(5, 15), border_radius= 10,bgcolor= colr, 
            data= colr, height= 70, alignment= ft.alignment.center, width= 80, on_click= oncc,
            )
    
    def onhov(self, e: ControlEvent):
        if e.data == 'true':
            e.control.bgcolor = ft.colors.with_opacity(0.4, GOLD)
        else:
            e.control.bgcolor = e.control.data
        self.update()
    
    def onclose(self, e):
        self.visible = False
        e.control.bgcolor = e.control.data
        self.audiof.clamp_end = None#self.audiof.track_canvas.audio_duration
        self.update()

    def onsave(self, e):
        se = [convertminsec(self.c_s.current.value), 
              convertminsec(self.c_e.current.value)]
        srcs = self.audiof.audio1.src
        name = self.title.current.value
        if len(name) > 1:
            self.title.current.error_text = ''
            # path = f'./newproj/assets/Books/'
            # if not os.path.exists(f'{path}'):
            #         os.makedirs(f'{path}/section')
            
            section = self.page.client_storage.get('section.list')
            
            if not section:
                section = []
                sec = []
            else:
                sec = [i[0] for i in section]
            
            if name not in sec:
                section.append([name, srcs,se])

                self.page.client_storage.set(f'section.list',
                                        section)

                self.title.current.value = ''
                self.onclose(e)
            else:
                self.title.current.value = ''
                self.title.current.error_text = 'Name exists'
                self.update()
        else:
            self.title.current.error_text = 'Add a title'
            self.update()

class quick_note(Container):
    def __init__(self, lts, page:pG):
        super().__init__()
        self.listtiles = lts
        self.bgcolor = ft.colors.BACKGROUND
        self.alignment = ft.alignment.bottom_center
        self.visible = False
        self.expand = True
        self.margin = margin.only(top= 45)
        self.padding = 20
        self.border_radius = ft.border_radius.vertical(50)
        self.body = ft.Ref[Column]()


        self.shadow = ft.BoxShadow(
            blur_style= ft.ShadowBlurStyle.OUTER, 
                                   blur_radius= 4,
                                #    spread_radius= 1
            color= ft.colors.with_opacity(0.2, ft.colors.INVERSE_SURFACE)
                                   )

        self.content = ft.Stack([Column(
            ref= self.body,
            controls=[
            ElevatedButton(height= 5, width= 100, 
                           on_click= self.onclose,
                           bgcolor= ft.colors.with_opacity(0.3, ft.colors.INVERSE_SURFACE)
                           ),
            TextField(
                hint_text= 'Untitled Quick Note',
                multiline= True,
                border= ft.InputBorder.NONE,
                text_style= ft.TextStyle(weight= BOLD,),
                dense= True,
                text_align= 'center',
                hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
            ),
            self.text_box(),
        ], horizontal_alignment= CrossAxisAlignment.CENTER),
        ElevatedButton('submit', bottom=10, right= 10, on_click= self.onsubmit)
        ])
    
    def onsubmit(self, e):
        checks = [0,0,0]
        i1 = self.body.current.controls[1]
        if len(i1.value) > 2: 
            checks[0] = i1.value
            i1.error_text = ''
        else: i1.error_text = 'add a least 3 Text before saving'

        for j, i in enumerate(self.body.current.controls[2].controls):
            if len(i.value) > 3: 
                checks[j+1] = [i.value, i.data]
                i.error_text = ''
            else: i.error_text = 'add a least 3 Text before saving'
        
        self.update()
        if all(checks):
            self.submit(checks)
            for j, i in enumerate(self.body.current.controls[2].controls):
                i.value = ''
            i1.value = ''
            self.visible = False
            self.update()
    
    def submit(self, li):
        random_uuid = uuid.uuid4()
        create_note(self.page, random_uuid, li[0], li[1:])

    def text_box(self):
        r = ft.ListView([
            TextField(
                hint_text= 'add Header',
                label= 'Header',
                border= ft.InputBorder.UNDERLINE,
                multiline= True,
                text_style= ft.TextStyle(
                    color= GOLD,
                    weight= BOLD,
                    size = 18,
                ),
                dense= True,
                on_change= self.onchange,
                data= 'H'
            ),
            TextField(
                hint_text= 'add Body',
                label= 'Body',
                label_style=  ft.TextStyle(
                    size= 12,
                ),
                border= ft.InputBorder.UNDERLINE,
                multiline= True,
                dense= True,
                text_size= 12,
                on_change= self.onchange,
                data= 'T',
            ),
            ], spacing= 0, expand= True)
        return r
    
    def onchange(self, e):
        if len(e.data) > 0:
            e.control.border = ft.InputBorder.NONE
        else:
            e.control.border = ft.InputBorder.UNDERLINE
        self.update()

    def onclose(self, e):
        # if self.expand == True:
        #     self.expand = False
        #     for  i in self.body.current.controls[1:]:
        #         i.visible = False
        # else:
        #     self.expand = True
        #     for  i in self.body.current.controls[1:]:
        #         i.visible = True
        self.visible = False
        self.update()

class Chapters(Container):
    def __init__(self, num, tim, ids, uls, sub):
        super().__init__()
        self.down_m = ft.Ref[ft.Icon]()
        self.down_n = ft.Ref[ft.Icon]()
        self.down_d = ft.Ref[ft.Icon]()
        self.down_b = ft.Ref[ft.ProgressRing]()
        self.down_bd = ft.Ref[ft.IconButton]()
        self.ids = ids
        self.num = num
        self.uls = os.path.normpath(f'{uls}/parts/{num*5}.mp3')
        if self.num not in sub:
            self.pro = 'n'
        else:
            self.pro = 'l'
        if self.pro == 'n':
            self.prog = [True, False, False]
        else:
            self.prog = [False, False, True]


        self.content = IconButton(ref= self.down_bd, content= Container(
        ft.Row([
            Column([
                Text(f'Part {num}'),
                Row([
                    Text(f'{tim}'),
                    # readbar(width= 100, start= 100, align= 'left', fgcolor= GOLD, height= 4),
                    
                ], spacing= 2),
                
            ], expand= 1, spacing= 1),
            ft.Container(
                content=ft.Stack([
                    Container(
                        Row([
                            ft.Icon(ft.icons.DOWNLOAD_FOR_OFFLINE_ROUNDED, 
                                    visible= self.prog[0], 
                                    ref= self.down_m),
                            ft.Icon(ft.icons.ARROW_DOWNWARD_ROUNDED, 
                                    visible= self.prog[1], 
                                    ref= self.down_n, size=20),
                            ft.Icon(ft.icons.DOWNLOAD_DONE_ROUNDED, 
                                    visible= self.prog[2],
                                    ref= self.down_d),
                            ],
                        alignment= MainAxisAlignment.CENTER,
                        ),alignment= ft.alignment.center),
                        Container(
                            ft.ProgressRing(width= 28, height= 28, #value= 0.4,  
                                         ref= self.down_b,
                                         visible= False,
                                     bgcolor= ft.colors.with_opacity(0.54,
                                        ft.colors.INVERSE_SURFACE), stroke_width= 2, 
                                     color= GOLD),
                        alignment= ft.alignment.center),
                        
                    ],),
            on_click= self.download_sub, on_hover= self.hov, 
            border_radius= 60, 
            # alignment= ft.alignment.center,
            width= 40, height= 40
            ),
            
                
        ], MainAxisAlignment.SPACE_BETWEEN, expand=1),
        padding= ft.padding.only(10), 
        ), on_click= lambda _: self.page.go(f'/lib/{self.ids}/{self.num}')
        )

    def hov(self, e: ControlEvent):
        if e.data == 'true':
            self.down_bd.current.on_click = None
            e.control.bgcolor = ft.colors.with_opacity(0.1, 
                                        ft.colors.INVERSE_SURFACE)
        else:
            self.down_bd.current.on_click = lambda _: self.page.go(f'/lib/{self.ids}/{self.num}')
            e.control.bgcolor = None
        self.update()

    def download_sub(self, e):
        if self.pro == 'n':
            self.down_m.current.visible = False
            self.down_b.current.visible = True
            self.down_n.current.visible = True
            self.update()
            self.download()
            self.down_m.current.visible = False
            self.down_b.current.visible = False
            self.down_n.current.visible = False
            self.down_d.current.visible = True
            self.update()

    def download(self):
        exctractors_srt(nam= self.ids, num= self.num, 
                        url= os.path.join(root_path, self.uls))
        info = self.page.client_storage.get(f'Book.{self.ids}')
        
        if self.num not in info[1]:
            info[1].append(self.num)
        
        self.page.client_storage.set(f'Book.{self.ids}', 
                            info)

class sub_page1():
    def __init__(self, page, ids, audio1=None):
        self.page = page
        self.ids = ids
        self.audio1 = audio1
        self.new_ndt = []
        self.head = 'Untitled Note'


        note_prop = load_note_prop(page, f'Note.{self.ids}')

        if note_prop != None:
            self.head = note_prop[0]
            self.new_ndt = note_prop[1]
                    
        self.content: Column = Column([], height= 610,
                                # tight= True,
                                # expand= True,
                                alignment= MainAxisAlignment.CENTER
                                )
        self.cont = Container(self.content, 
                                # bgcolor= 'red',
                                )

    def editor(self):
        self.frame = Column([], expand= 5, tight= True, scroll=ft.ScrollMode.AUTO, 
                            spacing= 2
                            )
        return self.frame
    
    def onclick(self):
        self.page.frame.controls.append(Editor())
        ...

    def header(self):
        self.tit = ft.Ref[TextField]()
        cont = Row([
            IconButton(icon= ft.icons.CHEVRON_LEFT, icon_color= GOLD,
                on_click= self.onback),
            TextField(value=self.head, 
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
            IconButton(icon= ft.icons.HELP, icon_color= GOLD,
                on_click= lambda _: print('#')),
            ], alignment= MainAxisAlignment.SPACE_BETWEEN)
        return cont

    def did_mount(self):
        self.audio1.pause()
        self.audio1.outside = 1
        return super().did_mount()
    
    def onback(self, e: ControlEvent):
        head = self.tit.current.value
        data = []
        for i in self.frame.controls:
            if i.data == 'e':
                data.append([i.content.controls[-1].value,
                    i.content.controls[-1].data])
            else:
                data.append([i.tit,
                             i.rang,
                             i.src, 'S'])
        create_note(self.page, self.ids, head, data)
        self.page.go('/note')
        ...

    def build(self):
        editor = self.editor()
        if len(self.new_ndt) != 0:
            for *n, t in self.new_ndt:
                if t != 'S':
                    editor.controls.append(Editor(value=n[0], typ=t, delfunc= editor)) # add type later
                else:
                    editor.controls.append(audiomark(
                        *n[:2], src=n[2], audio1= self.audio1, par= self.frame,
                      width= 200, close_vis= True, ondel= '0'))
        else:
            editor.controls.append(Editor(delfunc= editor))
        self.content.controls += [self.header(),
            editor,
            ]
        return self.cont

class simple_button(UserControl):
    def __init__(self, icon : ft.Icon = '', page = '', img = '', size = 15,
                func= lambda _: print(9)):
        super().__init__()
        if icon == '':
            frame = IconButton(
                        content= ft.Image(img, 
                            width= size-3, height= size-3,
                            fit=ft.ImageFit.CONTAIN,
                            color=ft.colors.SURFACE,),
                                on_click= func)
        else:
            frame = IconButton(
                            icon, 
                            icon_color= ft.colors.SURFACE,
                            icon_size= size, 
                            on_click= func)
        self.frame = frame

    def build(self):
        return self.frame

class Editor(Container):
    def __init__(self,delfunc: Column,  typ= 'H', value= ''):
        super().__init__()
        self.typs = typ
        self.delfunc = delfunc
        self.data = 'e'

        self.value = value
        
        m = {'H': (15, 'Add a Header', 0, ft.TextCapitalization.WORDS, BOLD, GOLD, 'red', 30),
             'SH': (12, 'Add a Subheader', 5, ft.TextCapitalization.SENTENCES, BOLD, ft.colors.with_opacity(0.8,GOLD), 'yellow', 20),
             'T': (10, 'Add a Body', 10, ft.TextCapitalization.NONE, 'blue', '', '', 15),
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

    def onhover(self, e: ControlEvent):
        if e.data == 'true':
            self.close.current.visible = True
            self.bar.current.visible = True
        else:
            self.close.current.visible = False
            self.bar.current.visible = False
        self.update()
    
    def editor(self):
        # for body can be a row mechnisim
        self.frame = Row([], expand= 5, spacing= 4)
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
            IconButton(
                ft.icons.CLOSE, icon_size= 15,
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
                    ft.MaterialState.HOVERED: GOLD,
                    ft.MaterialState.DEFAULT: self.but_C,
                    ft.MaterialState.PRESSED: ft.colors.SURFACE,
                    },
                overlay_color= ft.colors.with_opacity(0.2,'white')
                ))
        )
        self.frame.controls.append(st)
        return self.frame
    
    def closed(self, e):
        self.delfunc.controls.remove(self)
        self.delfunc.update()

    def onchange(self, e: ControlEvent):
        # self.bar.current.height = 
        self.update()

class MainNote(ft.TextButton):
    def __init__(self, tit, subt, n=0, m= ['learning'], pg= ''):
        super().__init__()
        self.page = pg
        short = shorten(subt[0], 39, placeholder='..')
        short_title = shorten(tit, 20, placeholder='..')
        self.frame = Column([
                Container(Row(spacing= 5, alignment= MainAxisAlignment.END))
                ], alignment= MainAxisAlignment.END)
        
        # for i in m:
        #     self.frame.controls[0].content.controls.append(self.tags(i, choice([GOLD,'#6168CA'])))

        self.check = ft.Ref[ft.Checkbox]()
        
        self.content= Row([
            ft.Checkbox(fill_color= {ft.MaterialState.SELECTED:GOLD}, 
                        # on_change=self.onselect,
                        visible= False,
                        ref= self.check),
        ft.ListTile(
            title= ft.Text(value= short_title.title(), size= 14, 
                            weight= BOLD,),
            subtitle= Row([ft.Text(value= short, size= 10,), self.frame], 
                          alignment= MainAxisAlignment.SPACE_BETWEEN),
        ),
        ], spacing= 0)
        
        self.style = ft.ButtonStyle(padding= ft.padding.symmetric(0,0))
        self.on_click = self.onclick
        self.data = n

    def tags(self, text, color):
        color = color[1:]
        return Container(Text(value=text, color= f'#{color}', size= 8,),
                         bgcolor= f'#22{color}', padding= 3, border_radius= 3)
    
    def onclick(self, e: ControlEvent):
        if not self.check.current.visible:
            self.page.go(f'/note/{e.control.data}')
        else:
            self.check.current.value = (True
                if not self.check.current.value
                else False)
            self.update()

def checking(troute, page):
    inf = page.client_storage.get(f'Book.{troute.id}')
    ld = [[],[]]
    if len(inf[1]) > 0:
        if int(troute.num) in inf[1]:
            for i in inf[1]:
                if int(troute.num) == i:
                    pat = os.path.normpath(f'Books/{troute.id}/sub/{i}.srt')
                    ld = loads(os.path.join(root_path, pat))
    return ld, inf

def main(page: pG) -> None:
    # Meta
    if True:
        page.title = 'BookReader'
        page.theme_mode = 'light'
        page.window.width = 360
        # page.window_resizable = False

    dpo = quick_note(List_Tile, page)
    sub = subpage2(page, dpo)
    dpol = sections_pg(List_Tile, page, sub.content) # note
    sub.content.nox = dpol
    # sub.content.audio1.src = 
    # whe src is added is when the song is loaded so and a try catch
    
    def route_change(e: RouteChangeEvent) -> None:
        if True:
            page.views.clear()
            if len(page.overlay) > 0: page.overlay.clear()
            troute = ft.TemplateRoute(page.route)

            # test
            # page.overlay.append(Column([
            #         ElevatedButton('test', on_click= lambda _: change_theme(page)
            # )],bottom= 80, alignment= 'end'))

            #Home
            home_page = Page1(dt,ndt,page)
            page.views.append(
                View(
                    route='/',
                    controls=[home_page],
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )

        if page.route == '/':
            page.overlay.append(Mordern_navbar(page, 0))
        
        if page.route == '/note':
            note_page = Page3(ndt, page)
            page.overlay.append(Mordern_navbar(page, 4))
            page.overlay.append(Column([Container(Reading(), 
                                        padding= 10, margin= margin.only(top= 0)) #30
                                        ], alignment= MainAxisAlignment.START))
            page.overlay.append(Column([
                    IconButton(ft.icons.ADD_CIRCLE_ROUNDED, icon_color= GOLD, icon_size= 60,
                               on_click= lambda _: open_note(page)
            )],bottom= 70, alignment= 'end', left= page.window_width - 95))
            page.views.append(
                View(
                    route='/note',
                    controls=[note_page],
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )
        
        if page.route == '/lib':
            v_Audio = sub.content.audio1
            page.overlay.append(v_Audio)
            lib_page = Page2(dt, ndt, page)
            # print(lib_page.grid1.controls)
            # page.on_resize = lambda _: p221(lib_page, page)
            page.overlay.append(Mordern_navbar(page, 2)) # add a button for adding music/books
            page.overlay.append(Column([Container(
                Row([IconButton(ft.icons.CHEVRON_LEFT, 
                                on_click= lambda _: page.go(f'/')),
                     Reading(lambda e: play_pause(e, v_Audio)),
                IconButton(ft.icons.MORE_VERT, on_click=
                           lambda _:  delete(lib_page)
                           ),
                ], expand= True),
                padding= 10, bgcolor= ft.colors.BACKGROUND)
                ], alignment= MainAxisAlignment.START))
            page.views.append(
                View(
                    route='/lib',
                    controls=[lib_page,
                    ],
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )
            
        if page.route == '/srch':
            page.overlay.append(Mordern_navbar(page, 1))
            dp = downlod_pg(List_Tile, page, 700)
            page.overlay.append(Mordern_navbar(page, 1))
            page.overlay.append(dp)
            
            file_picker = ft.FilePicker()
            file_picker.on_result = lambda e, p= file_picker, d= dp, pl= page: on_dialog_result(e, p, d, pl)
            page.overlay.append(file_picker)
            page.views.append(
                View(
                    route='/srch',
                    controls=[Page4(file_picker, page, dp)],
                    spacing= 26,
                )
            )
        
        if page.route == '/bmark':
            page.overlay.append(Mordern_navbar(page, 3))
            v_Audio = sub.content.audio1
            page.overlay.append(v_Audio)
            page.views.append(
                View(
                    route='/bmark',
                    controls=[Page5(page, v_Audio)],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )

        if troute.match('/lib/:id'):
            sp3 = sub_page3(page, troute.id)
            page.overlay.append(
                    ft.ElevatedButton(text='Continue', bgcolor= GOLD, color= 'white', 
                                      style= ft.ButtonStyle(shape= ft.RoundedRectangleBorder(radius= 8),
                                                            padding= 18,),
                               on_click= lambda _: print('open'), bottom= 10, right= 10,
            ))
            page.views.append(
                View(
                    route=f'/lib/{troute.id}',
                    controls=[sp3.build()],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )

        if troute.match('/lib/:id/:num'):
            page.overlay.append(Column([dpo], alignment=MainAxisAlignment.END)) # animate
            page.overlay.append(dpol)
            update_current(page, troute.id, troute.num)
            ld, inf = checking(troute, page)
            sub.content.load(troute.id, troute.num, inf[3], ld,
                             src=f'{inf[0]}/parts/{int(troute.num)*5}.mp3')
            sub.content.audio1.outside = None
            page.overlay.append(sub.content.audio1)
            
            page.views.append(
                View(
                    route=f'/lib/{troute.id}/{troute.num}',
                    controls=[sub,],
                    vertical_alignment= MainAxisAlignment.CENTER,
                    horizontal_alignment= CrossAxisAlignment.CENTER,
                    spacing= 26,
                )
            )
        
        if troute.match('/note/:id'):
            v_Audio = sub.content.audio1
            sp1 = sub_page1(page, troute.id, v_Audio)
            sec = section_overlay(page, sp1, v_Audio)
            page.overlay.append(Mordern_navbar(page, 4))
            page.overlay.append(format_panel(sp1, sec))
            page.overlay.append(v_Audio)
            page.overlay.append(sec)
            page.views.append(
                View(
                    route=f'/note/{troute.id}',
                    controls=[
                        sp1.build(),
                    ],
                    spacing= 26,
                )
            )
        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")