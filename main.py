from pprint import pprint
from textwrap import TextWrapper, shorten
from random import choice, randrange
import pytweening as pytw
import flet as ft
import shutil
from flet import Page as pG
from flet import (ElevatedButton, Text, IconButton, TextField,
                  ControlEvent, margin, Container)
from flet import (Row, Column,
                  CrossAxisAlignment, MainAxisAlignment)
from Utility import *
from user_controls import (Library_frame, ListTile, readbar, BookProgressSheet)
from pages import subpage2, loads
import flet.canvas as cv
from view import routes


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
                                        bgcolor= ft.Colors.with_opacity('0.3',ft.Colors.INVERSE_SURFACE)),
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
        self.page.client_storage.set(f'section.list',
                                section)
        self.remove('e')

    def onhover(self, e: ControlEvent):
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

class QuickNote(Container):
    def __init__(self, lts):
        super().__init__()
        self.listtiles = lts
        self.bgcolor = ft.Colors.BACKGROUND
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
            color= ft.Colors.with_opacity(0.2, ft.Colors.INVERSE_SURFACE)
                                   )

        self.content = ft.Stack([Column(
            ref= self.body,
            controls=[
            ElevatedButton(height= 5, width= 100, 
                           on_click= self.onclose,
                           bgcolor= ft.Colors.with_opacity(0.3, ft.Colors.INVERSE_SURFACE)
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


def checking(troute, page):
    inf = page.client_storage.get(f'Book.{troute.id}')
    ld = [[],[]]
    if len(inf[1]) > 0:
        if int(troute.num) in inf[1]:
            for i in inf[1]:
                if int(troute.num) == i:
                    pat = os.path.normpath(f'Books/{troute.id}/sub/{i}.srt')
                    ld = loads(os.path.join(ROOTPATH, pat))
    return ld, inf

# def main(page: pG) -> None:
#     dpo = quick_note(List_Tile, page)
#     sub = subpage2(page, dpo)
#     dpol = sections_pg(List_Tile, page, sub.content) # note
#     sub.content.nox = dpol
#     # sub.content.audio1.src = 
#     # whe src is added is when the song is loaded so and a try catch

#         if troute.match('/lib/:id/:num'):
#             page.overlay.append(Column([dpo], alignment=MainAxisAlignment.END)) # animate
#             page.overlay.append(dpol)
#             update_current(page, troute.id, troute.num)
#             ld, inf = checking(troute, page)
#             sub.content.load(troute.id, troute.num, inf[3], ld,
#                              src=f'{inf[0]}/parts/{int(troute.num)*5}.mp3')
#             sub.content.audio1.outside = None
#             page.overlay.append(sub.content.audio1)
            
#             page.views.append(
#                 View(
#                     route=f'/lib/{troute.id}/{troute.num}',
#                     controls=[sub,],
#                     vertical_alignment= MainAxisAlignment.CENTER,
#                     horizontal_alignment= CrossAxisAlignment.CENTER,
#                     spacing= 26,
#                 )
#             )

# from utility import LoadingView, defualt_theme, AlertControl, overlay

def metadata(page: ft.Page):
    page.title = "BookReader"
    page.theme_mode = 'Light'
    page.window.width = 320
    # page.window_resizable = False

# def set_theme(page):
#     save_colors = defualt_theme
#     if not page.client_storage.get("theme_color"):
#         page.client_storage.set('theme_color', save_colors)
#     else:
#         save_colors = page.client_storage.get("theme_color")
#     page.theme = ft.Theme(
#         color_scheme= ft.ColorScheme(
#             primary= save_colors['accent'],
#             primary_container= save_colors['container'],
#             surface= save_colors['background'],
#             on_surface= save_colors['text'],
#             on_surface_variant= save_colors['text'],
#         ),
#     )

def add_overlays(page):
    page.overlay.append(ft.SnackBar(ft.Text("love"), duration= 2000))
    page.overlay.append(BookProgressSheet(1000))
    page.overlay.append(ft.FilePicker())
    # page.overlay.append(
    #     Column(
    #         controls=[
    #             ElevatedButton('test', on_click= lambda _: change_theme(page)
    #         ),
    #     ]
    #         ,bottom= 80, 
    #         alignment= 'end'
    #     )
    # )

def main(page: ft.Page): # add security
    metadata(page)
    add_overlays(page)
    # set_theme(page)
    # overlays = overlay(page)
    def route_change(e: ft.RouteChangeEvent) -> None:
        troute = ft.TemplateRoute(page.route)
        current_view = [i for i in page.views if page.route == i.route]
        if any(current_view): page.views.remove(current_view[0])
        if page.route in ['/']: page.views.clear()
        page.views.append((
            routes[
                page.route
                if page.route in list(routes.keys()) 
                else "/"
            ]
        )())
        page.update()
    
    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        top_view: ft.View = page.views.pop()
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")