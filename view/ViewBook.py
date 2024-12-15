import flet as ft
from Utility import *
from user_controls import AudioPlayer, checking, convertminsec
import flet.canvas as cv
from random import randrange, choice

class BookMarkSection(ft.Container):
    def __init__(self):
        super().__init__()
        # self.listtiles = lts
        self.bgcolor = ft.Colors.SURFACE
        self.alignment = ft.alignment.bottom_center
        self.visible = False
        self.expand = True
        self.padding = 20
        self.body = ft.Ref[ft.Column]()
        self.title = ft.Ref[ft.TextField]()

        self.content = ft.Stack(
            controls=[
                ft.Column(
                    ref= self.body,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    'Section bookmark', 
                                    text_align= 'center', 
                                    expand= True
                                ),
                            ]
                        ),
                        ft.Text(
                            'Bookmark title', 
                            size= 12, 
                            color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),
                        ),
                        ft.TextField(
                            hint_text= 'Add Title',
                            multiline= True,
                            ref= self.title,
                            # label= 'Bookmark Title',
                            border= ft.InputBorder.UNDERLINE,
                            border_color= ft.Colors.with_opacity(0.4, GOLD),
                            text_style= ft.TextStyle(weight= BOLD,),
                            dense= True,
                            hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
                        ),
                        self.new_body(),
                        ft.Divider(),
                        ft.Row(
                            controls=[
                                self.new_but(
                                    'Cancle', 
                                    oncc= self.onclose
                                ),
                                self.new_but(
                                    'Save', 
                                    'iconz/Group 42.svg',
                                    colr= True, 
                                    oncc= self.onsave
                                )
                            ], 
                            alignment= ft.MainAxisAlignment.SPACE_EVENLY,
                        )
                    ],
                ),
            ]
        )
    
    def new_body(self):
        self.start_indicator= ft.Ref[ft.Text]()
        self.end_indicator= ft.Ref[ft.Text]()
        self.bookmark_track= Track(
            on_change_position= self.change_position, 
            rel= self
        )
        self.playimg = ft.Image(
            'iconz/Group 38.svg'
        )
        
        g = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        ft.Image(
                            'iconz/Group 37.svg', 
                            color= 'white',
                            scale=0.6 
                        ),
                        border_radius= 9,
                        rotate= ft.Rotate(
                            0.8, 
                            alignment= ft.alignment.center
                        ),
                        shadow= ft.BoxShadow(
                            blur_style= ft.ShadowBlurStyle.OUTER, 
                            blur_radius= 10,
                            color= ft.Colors.with_opacity(0.7, GOLD),
                            spread_radius= -5.7,
                        ),
                    ),
                    self.playimg,
                ],
            ), 
            on_click= self.onclick, 
            data= '+', 
            alignment= ft.alignment.center,
        )
        bod = ft.Column(
            controls=[
                self.bookmark_track
            ], 
            expand= True, 
            alignment= ft.MainAxisAlignment.CENTER,
        )

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

        self.pointer1 = ft.Container(gd, bgcolor=ft.Colors.AMBER, width=30, height=30, left=0, top=0)
        self.pointer2 = ft.Container(gd1, bgcolor=ft.Colors.RED, width=30, height=30, right=0, top=0)

        self.pointer1.left = -(self.pointer1.width/2)
        self.pointer2.right = -(self.pointer2.width/2)
        cl = ft.Stack([self.pointer1, self.pointer2], expand= True, height=35)

        return ft.Container(
            ft.Column(
                controls=[
                    bod,
                    cl,
                    ft.Row(
                        controls=[
                            ft.Text(
                                ref= self.start_indicator,
                                value= '00:00'
                            ),
                            ft.Text(
                                ref= self.end_indicator,
                                value= '00:00'
                            ),
                        ], 
                        alignment= ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.Icons.FORWARD_10_ROUNDED,
                                icon_color=ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),
                                data= '-', 
                                on_click= self.add_lose
                            ),
                            g,
                            ft.IconButton(
                                ft.Icons.REPLAY_10_ROUNDED,
                                icon_color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),
                                data= '+', 
                                on_click= self.add_lose
                            ),
                        ], 
                        alignment= ft.MainAxisAlignment.CENTER,
                    )
                ], 
                spacing= 30
            ),
            expand=True
        )
    
    def on_pan_update1(self, e: ft.DragUpdateEvent):
        gpc= self.page.window.width-(
            self.pointer2.width+
            self.pointer2.right+
            self.pointer1.width+
            40+
            16
        )
        self.pointer1.left = min(
            gpc, 
            max(
                -(self.pointer1.width/2), 
                self.pointer1.left + e.delta_x
            )
        )
        c_start = self.pointer1.left + (self.pointer1.width/2)
        total = self.page.window.width - (40+16)
        self.pointer1.update()
        Clamp1 = convertMillis(
            round((c_start/total) * 
            self.audiof.track_canvas.audio_duration)
        )
        et = self.end_indicator.current.value
        self.bookmark_track.set_position(self, Clamp1, et)

    def on_pan_update2(self, e: ft.DragUpdateEvent):
        gpc= self.page.window.width-(
            self.pointer1.width+
            self.pointer1.left+
            self.pointer2.width+
            40+
            16
        )
        self.pointer2.right = min(
            gpc, 
            max(
                -(self.pointer2.width/2), 
                self.pointer2.right - e.delta_x
            )
        )
        c_start = self.pointer2.right + (self.pointer2.width/2)
        total = self.page.window.width - (40+16)
        self.pointer2.update()
        Clamp2 = convertMillis(
            round(((total-c_start)/total) * 
            self.audiof.track_canvas.audio_duration)
        )
        st = self.start_indicator.current.value
        self.bookmark_track.set_position(self, st, Clamp2)

    def add_lose(self, e: ft.ControlEvent):
        st = self.start_indicator.current.value
        et = self.end_indicator.current.value
        if e.control.data == '+':
            et = convertMillis(
                convertminsec(self.end_indicator.current.value) + 10*1000
            )
        else:
            sl = convertminsec(self.start_indicator.current.value)- 10*1000
            if not sl < 0:
                st = convertMillis(sl)
        
        # self.bookmark_track.set_position(self, st, et)

    def onclick(self, e: ft.ControlEvent):
        if e.control.data == '+':
            e.control.data = '-'
            self.audiof.audio1.resume()
            self.audiof.clamp_update('')
            e.control.content.controls[1].src = 'iconz/Group 37.svg'
            self.set_playpause(True)
        else:
            e.control.data = '+'
            self.audiof.audio1.pause()
            self.start_indicator.current.value = f"{convertMillis(self.audiof.audio1.clamp_start)}"
            # e.control.content.controls[1].src = 'iconz/Group 38.svg'
            self.set_playpause(False)

        self.page.update()
    
    def set_playpause(self, value):
        if value:
            self.playimg.src = 'iconz/Group 37.svg'
        else:
            self.playimg.src = 'iconz/Group 38.svg'
        self.playimg.update()

    def change_position(self, start, end):
        total_a = self.audiof.track_canvas.audio_duration#/1000
        self.audiof.audio1.clamp_start = round(total_a* (start))
        self.audiof.audio1.clamp_end= round(total_a* (end))
        self.start_indicator.current.value = convertMillis(self.audiof.audio1.clamp_start)
        self.end_indicator.current.value = convertMillis(self.audiof.audio1.clamp_end)
        self.update()
    
    def new_but(self, txt, img= './newproj/assets/Group 43.svg', colr= False, oncc=None):
        colr = ft.Colors.with_opacity(0.8, GOLD) if colr else None
        tcolr = 'white' if colr else ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE)
        if colr:
            xl = ft.Image(
                img, 
                height= 30, 
                width= 30,
            )
        else:
            xl = ft.Icon(
                ft.Icons.CLOSE, 
                color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE)
            )
        return ft.Container(
            content= ft.Column(
                controls=[
                    xl,
                    ft.Text(txt, color= tcolr),
                ], 
                horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
                alignment= ft.MainAxisAlignment.END, 
                spacing= 0,
            ), 
            on_hover= self.onhov, 
            padding= ft.padding.symmetric(5, 15), 
            border_radius= 10,
            bgcolor= colr, 
            data= colr, 
            height= 70, 
            alignment= ft.alignment.center, 
            width= 80, 
            on_click= oncc,
        )
    
    def onhov(self, e: ft.ControlEvent):
        if e.data == 'true':
            e.control.bgcolor = ft.Colors.with_opacity(0.4, GOLD)
        else:
            e.control.bgcolor = e.control.data
        self.update()
    
    def onclose(self, e):
        self.visible = False
        e.control.bgcolor = e.control.data
        self.audiof.audio1.clamp_end = None#self.audiof.track_canvas.audio_duration
        self.update()

    def onsave(self, e):
        se = [
            convertminsec(self.start_indicator.current.value), 
            convertminsec(self.end_indicator.current.value)
        ]
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

    def did_mount(self):
        body = self.parent
        self.audiof = body.open_overlays("audioplayer")
        return super().did_mount()

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
        self.par = rel # parent
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
                self.lines(i, max_num) for i in range(max_num)
            ]
            self.set_position(
                self.par, 
                self.par.start_indicator.current.value, 
                self.par.end_indicator.current.value
            )
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

class QuickNote(ft.Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = ft.Colors.SURFACE
        self.alignment = ft.alignment.bottom_center
        self.visible = False
        self.expand = True
        self.margin = ft.margin.only(top= 45)
        self.padding = 20
        self.border_radius = ft.border_radius.vertical(50)
        self.body = ft.Ref[ft.Column]()

        self.shadow = ft.BoxShadow(
            blur_style= ft.ShadowBlurStyle.OUTER, 
            blur_radius= 4,
            # spread_radius= 1,
            color= ft.Colors.with_opacity(0.2, ft.Colors.INVERSE_SURFACE),
        )

        self.content = ft.Stack(
            controls=[
                ft.Column(
                    ref= self.body,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Close",
                                    height= 40, 
                                    # width= 100, 
                                    expand= True,
                                    on_click= self.onclose,
                                    # bgcolor= ft.Colors.with_opacity(0.3, ft.Colors.INVERSE_SURFACE)
                                ),
                            ]
                        ),
                        ft.TextField(
                            hint_text= 'Untitled Quick Note',
                            multiline= True,
                            # border= ft.InputBorder.NONE,
                            text_style= ft.TextStyle(weight= BOLD,),
                            dense= True,
                            hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
                            label= "Title",
                            align_label_with_hint= True,
                            text_align= ft.TextAlign.CENTER,
                        ),
                        self.text_box(),
                    ], 
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                ),
                ft.ElevatedButton(
                    'submit', 
                    bottom=10, 
                    right= 10, 
                    on_click= self.onsubmit,
                ),
             ]
        )
    
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

    def text_box(self): # add a system to add more options or limit the options
        r = ft.ListView([
            ft.TextField(
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
            ft.TextField(
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

class ViewBookView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/viewbook",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            # navigation_bar= Navbar(2),
            padding= 0
        )
        self.body = ft.Stack(expand= True)
        self.body.open_overlays =  self.open_overlays
        self.controls = [
            self.body
        ]

    def did_mount(self):
        self.book_id = self.page.session.get("BookId")
        self.book_num = self.page.session.get("BookNumber")
        if self.book_id and self.book_num is not None:
            self.audioplayer = AudioPlayer()
            player_container = ft.Container(
                content=self.audioplayer,
                margin= 10,
            )
            # check if the song is new first
            player_container.open_overlays = self.open_overlays
            self.quicknote = QuickNote()
            self.section = BookMarkSection()
            self.body.controls = [
                player_container,
                self.quicknote,
                self.section,
            ]
            subtitles, book = checking(self.book_id, self.book_num, self.page)
            self.update()
            self.audioplayer.load(
                self.book_id,
                self.book_num,
                book["number_of_chunks"], 
                subtitles,
                src=f'{book["path"]}/parts/{int(self.book_num)}.mp3',
            )
        else:
            self.page.go("/bookover")
        return super().did_mount()
    
    def open_overlays(self, overlays):
        _overlay = None
        match overlays:
            case "quicknote":
                _overlay = self.quicknote
            case "section":
                _overlay = self.section
            case "audioplayer":
                _overlay = self.audioplayer
            case _:
                raise ValueError("not an overlay")
        
        return _overlay
