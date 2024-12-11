import flet as ft
from Utility import *
from user_controls import Note_frame, Library_frame, Reading, Library, Note, Navbar
import pytweening as pytw

# class SectionsPg(ft.Container):
#     def __init__(self, lts, audiof,):
#         super().__init__()
#         self.listtiles = lts
#         self.audiof = audiof
#         self.bgcolor = ft.Colors.BACKGROUND
#         self.alignment = ft.alignment.bottom_center
#         self.visible = False
#         self.expand = True
#         self.padding = 20
#         self.body = ft.Ref[Column]()
#         self.title = ft.Ref[TextField]()

#         self.content = ft.Stack([Column(
#             ref= self.body,
#             controls=[
#                 Row([
#                     Text('Section bookmark', text_align= 'center', expand= True)
#                 ]),
#                 Text('Bookmark title', size= 12, color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),),
#             TextField(
#                 hint_text= 'Add Title',
#                 multiline= True,
#                 ref= self.title,
#                 # label= 'Bookmark Title',
#                 border= ft.InputBorder.UNDERLINE,
#                 border_color= ft.Colors.with_opacity(0.4, GOLD),
#                 text_style= ft.TextStyle(weight= BOLD,),
#                 dense= True,
#                 hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
#             ),
#             self.new_body(),
#             ft.Divider(),
#             Row([
#                     self.new_but('Cancle', oncc= self.onclose),
#                     self.new_but('Save', 'iconz/Group 42.svg',colr= True, oncc= self.onsave)
#                ], alignment= MainAxisAlignment.SPACE_EVENLY)
#         ],),
#         ])
    
#     def new_body(self):
#         self.c_s= ft.Ref[Text]()
#         self.c_e= ft.Ref[Text]()
#         self.c_t= Track(on_change_position= self.change_position, 
#                   rel= self)
#         g = Container(ft.Stack([
#                 Container(
#                     ft.Image('iconz/Group 37.svg', color= 'white',scale=0.6 ),
#                         border_radius= 9,
#                         rotate= ft.Rotate(0.8, alignment= ft.alignment.center),
#                           shadow= ft.BoxShadow(
#                     blur_style= ft.ShadowBlurStyle.OUTER, 
#                     blur_radius= 10,
#                     color= ft.Colors.with_opacity(0.7, GOLD),
#                     spread_radius= -5.7
#                                    )),
#                 ft.Image('iconz/Group 38.svg')
#             ]), on_click= self.onclick, data= '+', alignment= ft.alignment.center)
#         bod = Column([
#             self.c_t
#         ], expand= True, alignment= MainAxisAlignment.CENTER)


#         gd = ft.GestureDetector(
#             mouse_cursor=ft.MouseCursor.MOVE,
#             drag_interval=50,
#             on_pan_update=self.on_pan_update1,
#         )
        
#         gd1 = ft.GestureDetector(
#             mouse_cursor=ft.MouseCursor.MOVE,
#             drag_interval=50,
#             on_pan_update=self.on_pan_update2,
#         )

#         self.pointer1 = ft.Container(gd, bgcolor=ft.Colors.AMBER, width=30, height=30, left=0, top=0)
#         self.pointer2 = ft.Container(gd1, bgcolor=ft.Colors.RED, width=30, height=30, right=0, top=0)

#         self.pointer1.left = -(self.pointer1.width/2)
#         self.pointer2.right = -(self.pointer2.width/2)
#         cl = ft.Stack([self.pointer1, self.pointer2], expand= True, height=35)

#         return Container(Column([
#             bod,
#             cl,
#             Row([
#                 Text(ref= self.c_s,value= '00:00'),
#                 Text(ref= self.c_e,value= '00:00'),
#             ], alignment= MainAxisAlignment.SPACE_AROUND),
#             Row([
#                 IconButton(ft.icons.FORWARD_10_ROUNDED,
#                 icon_color=ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),
#                 data= '-', on_click= self.add_lose
#                 ),
#                 g,
#                 IconButton(ft.icons.REPLAY_10_ROUNDED,
#                 icon_color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE),
#                 data= '+', on_click= self.add_lose
#                 ),
#                  ], alignment= MainAxisAlignment.CENTER)
#         ], spacing= 30),expand=True)
    
#     def on_pan_update1(self, e: ft.DragUpdateEvent):
#         gpc= self.page.window_width-(self.pointer2.width+
#                                      self.pointer2.right+self.pointer1.width+40+16)
#         self.pointer1.left = min(gpc, max(-(self.pointer1.width/2), 
#                                           self.pointer1.left + e.delta_x))
#         c_start = self.pointer1.left + (self.pointer1.width/2)
#         total = self.page.window_width - (40+16)
#         self.pointer1.update()
#         Clamp1 = self.convertMillis(round((c_start/total) * 
#                                         self.audiof.track_canvas.audio_duration))
#         et = self.c_e.current.value
#         self.c_t.set_position(self, Clamp1, et)

#     def on_pan_update2(self, e: ft.DragUpdateEvent):
#         gpc= self.page.window_width-(self.pointer1.width+
#                                      self.pointer1.left+self.pointer2.width+40+16)
#         self.pointer2.right = min(gpc, max(-(self.pointer2.width/2), 
#                                 self.pointer2.right - e.delta_x))
#         c_start = self.pointer2.right + (self.pointer2.width/2)
#         total = self.page.window_width - (40+16)
#         self.pointer2.update()
#         Clamp2 = self.convertMillis(round(((total-c_start)/total) * 
#                                         self.audiof.track_canvas.audio_duration))
#         st = self.c_s.current.value
#         self.c_t.set_position(self, st, Clamp2)

#     def add_lose(self, e: ft.ControlEvent):
#         st = self.c_s.current.value
#         et = self.c_e.current.value
#         if e.control.data == '+':
#             et = self.convertMillis(convertminsec(self.c_e.current.value) + 10*1000)
#         else:
#             sl = convertminsec(self.c_s.current.value)- 10*1000
#             if not sl < 0:
#                 st = self.convertMillis(sl)
        
#         # self.c_t.set_position(self, st, et)

#     def onclick(self, e: ControlEvent):
#         if e.control.data == '+':
#             e.control.data = '-'
#             self.audiof.audio1.resume()
#             self.audiof.clamp_update('')
#             e.control.content.controls[1].src = 'iconz/Group 37.svg'
#             self.update()
#         else:
#             e.control.data = '+'
#             self.audiof.audio1.pause()
#             self.c_s.current.value = f"{self.convertMillis(self.audiof.clamp_start)}"
#             e.control.content.controls[1].src = 'iconz/Group 38.svg'
#             self.update()
#             ...

#         self.page.update()

#     def change_position(self, start, end):
#         total_a = self.audiof.track_canvas.audio_duration#/1000
#         self.audiof.clamp_start = round(total_a* (start))
#         self.audiof.clamp_end= round(total_a* (end))
#         self.c_s.current.value = self.convertMillis(self.audiof.clamp_start)
#         self.c_e.current.value = self.convertMillis(self.audiof.clamp_end)
#         self.update()

#     def convertMillis(self,millis):
#         if type(millis) != int: millis = 0
#         seconds = int(millis / 1000) % 60
#         minutes = int(millis / (1000 * 60)) % 60

#         seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
#         minutes_str = f"0{minutes}" if minutes < 10 else f"{minutes}"
#         return f"{minutes_str}:{seconds_str}"

#     def new_but(self, txt, img= './newproj/assets/Group 43.svg', colr= False, oncc=None):
#         colr = ft.Colors.with_opacity(0.8, GOLD) if colr else None
#         tcolr = 'white' if colr else ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE)
#         if colr:
#             xl = ft.Image(img, height= 30, width= 30)
#         else:
#             xl = ft.Icon(ft.icons.CLOSE, 
#                          color= ft.Colors.with_opacity(0.4, ft.Colors.INVERSE_SURFACE))
#         return Container(content= Column([
#                 xl,
#                 Text(txt, color= tcolr),
#             ], horizontal_alignment= CrossAxisAlignment.CENTER, alignment= MainAxisAlignment.END, spacing= 0), 
#             on_hover= self.onhov, padding= ft.padding.symmetric(5, 15), border_radius= 10,bgcolor= colr, 
#             data= colr, height= 70, alignment= ft.alignment.center, width= 80, on_click= oncc,
#             )
    
#     def onhov(self, e: ControlEvent):
#         if e.data == 'true':
#             e.control.bgcolor = ft.Colors.with_opacity(0.4, GOLD)
#         else:
#             e.control.bgcolor = e.control.data
#         self.update()
    
#     def onclose(self, e):
#         self.visible = False
#         e.control.bgcolor = e.control.data
#         self.audiof.clamp_end = None#self.audiof.track_canvas.audio_duration
#         self.update()

#     def onsave(self, e):
#         se = [convertminsec(self.c_s.current.value), 
#               convertminsec(self.c_e.current.value)]
#         srcs = self.audiof.audio1.src
#         name = self.title.current.value
#         if len(name) > 1:
#             self.title.current.error_text = ''
#             # path = f'./newproj/assets/Books/'
#             # if not os.path.exists(f'{path}'):
#             #         os.makedirs(f'{path}/section')
            
#             section = self.page.client_storage.get('section.list')
            
#             if not section:
#                 section = []
#                 sec = []
#             else:
#                 sec = [i[0] for i in section]
            
#             if name not in sec:
#                 section.append([name, srcs,se])

#                 self.page.client_storage.set(f'section.list',
#                                         section)

#                 self.title.current.value = ''
#                 self.onclose(e)
#             else:
#                 self.title.current.value = ''
#                 self.title.current.error_text = 'Name exists'
#                 self.update()
#         else:
#             self.title.current.error_text = 'Add a title'
#             self.update()

# class sub_page3():
#     def __init__(self, page, ids):
#         self.page = page
#         self.ids = ids
#         self.ndts = page.client_storage.get(f'Book.{ids}')
#         # print(self.ndts)
                    
#         self.content: Column = Column([], height= 610,
#                                 # tight= True,
#                                 # expand= True,
#                                 alignment= MainAxisAlignment.CENTER
#                                 )
#         self.cont = Container(self.content, 
#                                 # bgcolor= 'red',
#                                 expand= True
#                                 )

#     def LIst_of_chap(self):
#         self.frame = ft.ListView([], expand= 5,
#                             spacing= 2
#                             )
#         return self.frame
    
#     def info(self):
#         if len(self.ndts) == 6:
#             src = self.ndts[5]
#         else: src = 'defualt.png'
#         src = f'covers/'+src
#         r = Row([
#             ft.Image(src, height= 130, width= 90,
#                      border_radius= 5,
#                      fit= ft.ImageFit.COVER),
#             Column([
#                 Text(
#                     self.ids.title(), size= 20, width= 220,
#                 ),
#                 Text(
#                     f'Currently readding: {self.ndts[2]}'.title()
#                 ),
#                 Text(
#                     f'30% read'.title()
#                 ),
#                 readbar(GOLD, align= 'left', start= 30, height= 4),
#             ])
#         ])
#         return r
#         ...

#     def header(self):
#         self.tit = ft.Ref[ft.TextField]()
#         cont = ft.Row([
#             ft.IconButton(icon= ft.icons.CHEVRON_LEFT, icon_color= GOLD,
#                 on_click= self.onback),
#             ft.Row([
#                 ft.IconButton(icon= ft.icons.DOWNLOAD, icon_color= GOLD,
#                 on_click= lambda _: print('#')),
#                 ft.IconButton(icon= ft.icons.MORE_VERT, icon_color= GOLD,
#                 on_click= lambda _: print('#')),

#             ]),
#             ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN)
#         return cont

#     def onback(self, e: ft.ControlEvent):
#         self.page.go('/lib')

#     def build(self):
#         editor = self.LIst_of_chap()
#         self.num = self.ndts[3]

#         for i in range(self.num):
#             if i != self.num -1:
#                 editor.controls.append(Chapters(i, '05:00', self.ids, self.ndts[0][1:], self.ndts[1]))
#             else:
#                 editor.controls.append(Chapters(i, self.ndts[4], self.ids, self.ndts[0][1:], self.ndts[1]))


#         self.content.controls += [self.header(),
#             self.info(),
#             ft.Text(f'{self.num} Parts'),
#             editor,
#             ]
#         return self.cont

# class Track(ft.GestureDetector):
#     def __init__(self, 
#                  rel,
#                 on_change_position
#                     ):
#         super().__init__()
#         # self.visible = False
#         self.content = ft.Container(
#             content=cv.Canvas(
#                 on_resize=self.canvas_resized,
#                 shapes=[],
#             ),
#             height=125,
#             width=float("inf"),
#         )
        
#         self.prev_selct = 0
#         self.next_selct = 0
#         self.par = rel
#         # self.on_pan_start = self.find_position
#         # self.on_pan_update = self.find_position
#         self.on_hover = self.change_cursor
#         self.on_change_position = on_change_position
    
#     def lines(self, num, maxnum, multp = 2):
#         halfm = maxnum/multp
#         mult = max(1, ((((num-halfm)**2)**0.5)*-1)+halfm)*multp # improve 
#         max_high = multp * 60
        
#         if mult/multp < 5:
#             high = randrange(1, round(mult))*3
#         else:
#             high = choice([
#                 randrange(10, max_high), 
#                 randrange(4, round(mult))
#                         ])
#         return cv.Rect(
#                 x=0+(6*num),
#                 y= ((max_high+ 5)/2)-(high/2),
#                 height= high,
#                 border_radius=3,
#                 paint=ft.Paint(color=GOLD),
#                 width=3,
#             )

#     def canvas_resized(self, e: cv.CanvasResizeEvent):
#         self.track_width = e.width
#         max_num = round(e.width/6)
#         self.prev_selct = 0
#         self.next_selct = max_num
#         if self.par.audiof.track_canvas.audio_duration != None:
#             self.content.content.shapes = [
#                 self.lines(i, max_num) for i in range(max_num)]
#             self.set_position(self.par, self.par.c_s.current.value, self.par.c_e.current.value)
#         e.control.update()
        
#     def find_position(self, e):
#         ll = max(
#             0, min(e.local_x, self.track_width)
#         )
#         total_sel = round(self.track_width/(6))
#         new_sel = round(ll/6)+1
#         if new_sel < round(self.track_width/(6*2)):
#             if self.prev_selct < new_sel :
#                 for i in self.content.content.shapes[: new_sel]:
#                     i.paint.color = 'grey10'
#             else:
#                 for i in self.content.content.shapes[new_sel-1: self.prev_selct]:
#                     i.paint.color = GOLD
            
#             self.prev_selct = new_sel
#         else:
#             if self.next_selct > new_sel:
#                 for i in self.content.content.shapes[new_sel-1 : ]:
#                     i.paint.color = 'grey10'
#             else:
#                 for i in self.content.content.shapes[self.next_selct: new_sel-1]:
#                     i.paint.color = GOLD
            
#             self.next_selct = new_sel -1

#         self.update()
#         # self.on_change_position(self.prev_selct/total_sel, self.next_selct/total_sel)

#     def set_position(self,sel, sl, el):
#         def converter(ob):
#             return (convertminsec(ob)/sel.audiof.track_canvas.audio_duration ) * self.track_width
#         slm = converter(sl)
#         elm = converter(el)
#         sl = max(
#             0, min(slm, self.track_width-10)
#         )
#         el = max(
#             10, min(elm, self.track_width)
#         )
#         total_sel = round(self.track_width/(6))
#         new_s = round(sl/6)#+1
#         new_e = round(el/6)

#         if self.prev_selct < new_s:
#             for i in self.content.content.shapes[: new_s]:
#                 i.paint.color = 'grey10'
#         else:
#             for i in self.content.content.shapes[new_s-1: self.prev_selct]:
#                 i.paint.color = GOLD
        
#         self.prev_selct = new_s

#         if self.next_selct > new_e:
#             for i in self.content.content.shapes[new_e : ]:
#                 i.paint.color = 'grey10'
#         else:
#             for i in self.content.content.shapes[self.next_selct: new_e]:
#                 i.paint.color = GOLD
        
#         self.next_selct = new_e

#         self.update()
#         self.on_change_position(self.prev_selct/total_sel, self.next_selct/total_sel)

#     def change_cursor(self, e: ft.HoverEvent):
#         e.control.mouse_cursor = ft.MouseCursor.CLICK
#         e.control.update()

class QuickNote(ft.Container):
    def __init__(self, lts):
        super().__init__()
        self.listtiles = lts
        self.bgcolor = ft.Colors.BACKGROUND
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
                                #    spread_radius= 1
            color= ft.Colors.with_opacity(0.2, ft.Colors.INVERSE_SURFACE)
                                   )

        self.content = ft.Stack([ft.Column(
            ref= self.body,
            controls=[
            ft.ElevatedButton(height= 5, width= 100, 
                           on_click= self.onclose,
                           bgcolor= ft.Colors.with_opacity(0.3, ft.Colors.INVERSE_SURFACE)
                           ),
            ft.TextField(
                hint_text= 'Untitled Quick Note',
                multiline= True,
                border= ft.InputBorder.NONE,
                text_style= ft.TextStyle(weight= BOLD,),
                dense= True,
                text_align= 'center',
                hint_style= ft.TextStyle(weight= ft.FontWeight.NORMAL,),
            ),
            self.text_box(),
        ], horizontal_alignment= ft.CrossAxisAlignment.CENTER),
        ft.ElevatedButton('submit', bottom=10, right= 10, on_click= self.onsubmit)
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
            navigation_bar= Navbar(4),
        )



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
    

