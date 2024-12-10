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
    

