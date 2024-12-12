import time
# import numpy as np
import flet as ft
from textwrap import TextWrapper
from Utility import *
import flet.canvas as cv

def check(t, l: list):
    if len(l) > 0:
        # vn = l[~(l > t)]
        vn = [i for i in l if i <= t]
        if len(vn) == 0: vn = [0]
        return len(vn) -1
    else: return None

def loads(srts= './subtitles.srt'):
    with open(srts, 'r') as newfile:
        tts = newfile.read()
    tts = [i.split('\n') for i in tts.split('\n\n') if i.strip() !='']
    
    ttv = [i[2] for i in tts]
    # ttl = np.array([convertsrc(i[1])[0] for i in tts])
    ttl = [convertsrc(i[1])[0] for i in tts]
    return [ttl,ttv]

def convertMillis(millis):
    if type(millis) != int: millis = 0
    seconds = int(millis / 1000) % 60
    minutes = int(millis / (1000 * 60)) % 60
    # hours = int(millis / (1000 * 60* 60)) % 24

    seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
    minutes_str = f"0{minutes}" if minutes < 10 else f"{minutes}"
    # return f"{hours}:{minutes_str}:{seconds_str}"
    return f"{minutes_str}:{seconds_str}"


def subpage2(page, overl,
             ll= [[],[]],
             url = r'./mod2/0_audiobook_LeavingTheRatRaceWithPython.mp3'
             ):
    
    
    # class Track(ft.GestureDetector):
    #     def __init__(self, audio, on_change_position):
    #         super().__init__()
    #         # self.visible = False
    #         self.content = ft.Container(
    #             content=cv.Canvas(
    #                 on_resize=self.canvas_resized,
    #                 shapes=[
    #                     cv.Rect(
    #                         x=0,
    #                         y=0,
    #                         height=5,
    #                         border_radius=3,
    #                         paint=ft.Paint(color=ft.colors.GREY_500),
    #                         width=100,
    #                     ),
    #                     cv.Rect(
    #                         x=0,
    #                         y=0,
    #                         height=5,
    #                         border_radius=3,
    #                         paint=ft.Paint(color=GOLD),
    #                         width=0,
    #                     ),
    #                 ],
    #             ),
    #             height=10,
    #             width=float("inf"),
    #         )
    #         self.audio = audio
    #         self.audio_duration = None
    #         self.on_pan_start = self.find_position
    #         self.on_pan_update = self.find_position
    #         self.on_hover = self.change_cursor
    #         self.on_change_position = on_change_position

    #     def canvas_resized(self, e: cv.CanvasResizeEvent):
    #         self.track_width = e.width
    #         e.control.shapes[0].width = e.width
    #         e.control.update()

    #     def find_position(self, e):
    #         position = int(self.audio_duration * e.local_x / self.track_width)
    #         self.content.content.shapes[1].width = max(
    #             0, min(e.local_x, self.track_width)
    #         )
    #         self.update()
    #         self.on_change_position(position)

    #     def change_cursor(self, e: ft.HoverEvent):
    #         e.control.mouse_cursor = ft.MouseCursor.CLICK
    #         e.control.update()

    class AudioPlayer(ft.Column):
        def __init__(self, url):
            super().__init__(tight=True)
            self.audio1 = ft.Audio(
                src=url,
                autoplay=False,
                volume=1,
                balance=0,
                on_loaded= self.audio_loaded,
                on_position_changed= self.change_position,
                on_state_changed=self.state_changed,
            )
            self.position = 0
            self.alignment = ft.MainAxisAlignment.START
            self.expand = True
            self.src = ll
            self.audio1.outside = None
            self.audio1.Oplay = None
            self.audio1.pg = page

            self.clamp_end = None
            self.clamp_start = 0
            
            self.tit = ft.Ref[ft.Text]()
            self.prt = ft.Ref[ft.Text]()
            self.num = ''
            self.nx = 0
            self.tot = 1
            self.nox = ''

            self.dlg = ft.AlertDialog(
                title= ft.Text('love'),
                # content= ft.Text('love'),
                inset_padding= 0,
                title_padding= 0,
                content_padding= 0,
                actions_padding= 0,
                shape= ft.RoundedRectangleBorder(radius= 1) ,
            )

            self.nav_bar = ft.Container(ft.Row([
                self.buttom_button(
                ico=ft.Icons.ADD_LINK,
                txt= 'section',
                onc=  self.close_dll,
                ),
                self.buttom_button(
                ico=ft.Icons.SPEED,
                txt= 'speed',
                onc= self.adjust_speed,
                ),
                self.buttom_button(
                ico=ft.Icons.TIMER_OUTLINED,
                txt= 'timer',
                # on_click=self.play,
                ),
                self.buttom_button(
                ico=ft.Icons.LIST_ALT,
                txt= 'chapter',
                onc = lambda _: self.page.go('/lib'+self.num),
                ),
                self.buttom_button(
                ico=ft.Icons.NOTE_ALT,
                txt= 'q-note',
                onc= lambda _: self.opp(),
                ),
            ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN))

            self.track_canvas = Track(
                audio=self.audio1, on_change_position=self.seek_position
            )
            self.play_button = ft.IconButton(
                icon=ft.Icons.PLAY_ARROW,
                icon_color= GOLD,
                icon_size= 30,
                visible=False,
                on_click=self.play,
            )
            self.pause_button = ft.IconButton(
                icon=ft.Icons.PAUSE,
                icon_color= GOLD,
                visible=False,
                on_click=self.pause,
            )
            self.next_button = ft.IconButton(
                icon=ft.Icons.SKIP_NEXT,
                # visible=False,
                on_click= self.next,
            )
            self.fastforward_button = ft.IconButton(
                icon=ft.Icons.FAST_FORWARD,
                # visible=False,
                on_click=self.ff_song,
                data= 10,
            )
            self.prev_button = ft.IconButton(
                icon=ft.Icons.SKIP_PREVIOUS,
                # visible=False,
                on_click=self.prev,
            )
            self.reverse_button = ft.IconButton(
                icon=ft.Icons.FAST_REWIND,
                # visible=False,
                on_click=self.fr_song,
                data= 10,
            )
            
            
            self.start_duration = ft.Text(size= 12, value= '0:00:00') #change later
            self.end_duration = ft.Text(size= 12, value= '0:00:00')
            self.title = ft.Row([
                ft.IconButton(icon= ft.Icons.CHEVRON_LEFT,
                              on_click= lambda _: self.back_but(),
                              ),
                ft.Column([
                    ft.Text('No track', size= 18, ref= self.tit,
                                 text_align= 'center'),
                ft.Text('NaN', size= 10, ref= self.prt,
                                 text_align= 'center')   
                ], spacing= 0,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER),
                ft.IconButton(icon= ft.Icons.STAR),
            ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN)
            self.textt = ft.ListView(expand=True, spacing= 5,
                                     auto_scroll= True)
            self.text = -1
            self.auto = False
            
            self.controls = [
                self.title,
                self.track_canvas,
                ft.Row(
                    [
                        self.start_duration,
                        self.end_duration
                    ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing= 0,
                    controls=[
                        self.prev_button,
                        self.reverse_button,
                        self.play_button,
                        self.pause_button,
                        self.fastforward_button,
                        self.next_button,
                    ],
                ),
                self.textt,
                self.nav_bar,
            ]
        
        def back_but(self):
            self.textt.controls.clear()
            self.update()
            self.page.go('/lib')

        def close_dll(self,e):
            self.nox.visible = True
            s = int(self.position)
            e = s+ 30*1000
            self.nox.c_s.current.value = convertMillis(s)
            self.nox.c_e.current.value = convertMillis(e)
            total = self.track_canvas.audio_duration
            if e > total -30*1000: 
                e = total
                s = e - 30*1000
            scl = (s/ total) * (self.page.window_width- (40+16))
            ecl = ((total-e)/ total) * (self.page.window_width- (40+16))
            self.nox.pointer2.right = -(self.nox.pointer2.width/2) + ecl
            self.nox.pointer1.left = -(self.nox.pointer1.width/2) + scl
            self.nox.update()

        def opp(self):
            overl.visible = True
            overl.update()

        def open_dlg(self, prop = ''):
            self.page.dialog = self.dlg
            # print(self.dlg.__dict__)
            # self.dlg.title.value = str(prop)+'x Speed'
            self.dlg.open = True
            self.page.update()

        def buttom_button(self, ico= ft.Icons.LIST_ALT, txt= 'Love', onc=None):
            return ft.IconButton(content=ft.Column([ft.Icon(
                ico,
                ),
                ft.Text(txt.title(), size= 12, weight= ft.FontWeight.BOLD),
            ], spacing= 0, horizontal_alignment= ft.CrossAxisAlignment.CENTER), on_click=onc)
            ...

        def next(self, e: ft.ControlEvent): # add a list
            if self.nx< self.tot-1: # below total
                self.page.go(f'/lib{self.num}/{self.nx+1}')
        
        def load(self, 
                 ids, num, tot, subt= [[],[]],
                 src = r"C:\Users\ajuga\Music\Benny_Blanco_feat_Halsey_feat_Khalid_Eastside.mp3"
                 ): # add a list
            self.audio1.src = src
            w = TextWrapper(25)
            self.tit.current.value = w.fill(ids)
            self.prt.current.value = 'Part'+num
            self.num = '/'+ids
            self.nx = int(num)
            self.tot = tot
            self.src = subt
            page.update()
        
        def prev(self, e: ft.ControlEvent): # add a list
            if self.nx > 0: # below total
                self.page.go(f'/lib{self.num}/{self.nx-1}')

        def adjust_speed(self, e: ft.ControlEvent):
            if self.audio1.playback_rate == None or self.audio1.playback_rate == 1:
                self.audio1.playback_rate = 2
            elif self.audio1.playback_rate == 2:
                self.audio1.playback_rate = 0.5
            elif self.audio1.playback_rate == 0.5:
                self.audio1.playback_rate = 1
            spd = str(self.audio1.playback_rate)
            spd = '' if spd == 'None' or spd == '1' else (spd + 'x ')
            e.control.content.controls[1].value = spd + 'speed'
            self.page.update()
            ...

        def ff_song(self, e: ft.ControlEvent):
            new_position = int(self.position) + int(e.control.data)*1000
            self.position = new_position
            self.track_canvas.content.content.shapes[1].width = (
                new_position
                / self.track_canvas.audio_duration
                * self.track_canvas.track_width
            )
            self.seek_position(new_position)
            self.page.update()
        
        def clamp_update(self, e: ft.ControlEvent):
            # new_position = int(self.position) + int(e.control.data)*1000
            self.position = self.clamp_start
            self.track_canvas.content.content.shapes[1].width = (
                self.clamp_start
                / self.track_canvas.audio_duration
                * self.track_canvas.track_width
            )
            self.seek_position(self.clamp_start)
            self.page.update()

        def fr_song(self, e: ft.ControlEvent):
            new_position = int(self.position) - int(e.control.data)*1000
            self.position = new_position
            self.track_canvas.content.content.shapes[1].width = (
                new_position
                / self.track_canvas.audio_duration
                * self.track_canvas.track_width
            )
            self.seek_position(new_position)
            self.page.update()

        def audio_loaded(self, e):
            self.nox.c_e.current.value = convertMillis(self.audio1.get_duration())
            self.end_duration.value = f"{convertMillis(self.audio1.get_duration())}"
            self.start_duration.value = f"{convertMillis(0)}"
            self.play_button.visible = True
            self.pause_button.visible = False
            self.track_canvas.audio_duration = self.audio1.get_duration()
            self.text = -1
            page.update()
            if self.auto: 
                self.auto = False
                self.play('')
                page.update()
            if self.audio1.Oplay:
                self.audio1.play()
                self.audio1.seek(self.audio1.Oplay)
            page.update()

        def play(self, e):
            if self.position != 0:
                self.audio1.resume()

            else:
                self.audio1.play()
            self.play_button.visible = False
            self.pause_button.visible = True
            self.audio1.pg.update()

        def pause(self, e):
            self.audio1.pause()
            self.play_button.visible = True
            self.pause_button.visible = False
            self.page.update()

        def state_changed(self, e):
            if e.data == "completed":
                self.play_button.visible = True
                self.pause_button.visible = False

        def seek_position(self, position):
            self.audio1.seek(position)
            self.page.update()

        def mod_list(self):
            list_len = len(self.textt.controls)
            if list_len > 0:
                self.textt.controls[-1].size -= 1
                self.textt.controls[-1].color= ft.colors.with_opacity(0.7, 
                                    ft.colors.INVERSE_SURFACE)
                self.textt.controls[-1].bgcolor= None
            if list_len < self.text+1:
                for i in self.src[1][list_len:self.text+1]:
                    self.textt.controls.append(
                        ft.Text(i, size= 13,
                                color= ft.colors.with_opacity(0.7, 
                                            ft.colors.INVERSE_SURFACE)
                                )
                    )
            else:
                for i in range(list_len - (self.text+1)):
                    self.textt.controls.pop()
            self.textt.controls[-1].size += 1
            self.textt.controls[-1].color= ft.colors.with_opacity(1, 
                                                ft.colors.INVERSE_SURFACE)
            self.textt.controls[-1].bgcolor= ft.colors.with_opacity(0.2,
                                                GOLD)

        def change_position(self, e:ft.ControlEvent):
            if self.audio1.outside == None:
                if self.clamp_end != None:
                    if self.track_canvas.audio_duration != None and\
                        not int(self.position) >= (self.clamp_end):
                        self.position = e.data
                        v = int(e.data)/1000
                        pos = check(v, self.src[0])
                        if pos != None:
                            if self.text != pos:
                                self.text = pos
                                self.mod_list()
                                # scroll to position
                        self.end_duration.value = f"{convertMillis(self.track_canvas.audio_duration)}"
                        self.start_duration.value = f"{convertMillis(int(e.data))}"
                        self.nox.c_s.current.value = f"{convertMillis(int(e.data))}"
                        self.track_canvas.content.content.shapes[1].width = (
                            int(e.data)
                            / self.track_canvas.audio_duration
                            * self.track_canvas.track_width
                        )
                        e.control.page.update()
                    else:
                        self.pause('')
                        self.nox.c_s.current.value = f"{convertMillis(self.clamp_start)}"
                        self.nox.update()
                else:
                    if self.track_canvas.audio_duration != None:
                        self.position = e.data
                        v = int(e.data)/1000
                        pos = check(v, self.src[0])
                        if pos != None:
                            if self.text != pos:
                                self.text = pos
                                self.mod_list()
                                # scroll to position
                        self.end_duration.value = f"{convertMillis(self.track_canvas.audio_duration)}"
                        self.start_duration.value = f"{convertMillis(int(e.data))}"
                        self.track_canvas.content.content.shapes[1].width = (
                            int(e.data)
                            / self.track_canvas.audio_duration
                            * self.track_canvas.track_width
                        )
                        e.control.page.update()
            else:
                if not isinstance(self.audio1.outside, int):
                    self.audio1.outside(e)
                    
    player = AudioPlayer(url=url)

    return ft.Container(player,
                        padding= 10,
                        #  alignment=ft.alignment.center, 
                         expand=True, )

def main(page: ft.Page):
    page.title = "Flet audio player example"
    page.window_width = 360
    page.window_height = 700
    page.theme_mode = 'light'
    page.add(subpage2(page, loads))


if __name__ == "__main__":
    ft.app(target=main)




class Track(ft.GestureDetector):
    def __init__(self, audio, on_change_position):
        super().__init__()
        self.content = ft.Container(
            content=cv.Canvas(
                on_resize=self.canvas_resized,
                shapes=[
                    cv.Rect(
                        x=0,
                        y=0,
                        height=5,
                        border_radius=3,
                        paint=ft.Paint(color= CONTAINER_COLOR),
                        width=100,
                    ),
                    cv.Rect(
                        x=0,
                        y=0,
                        height=5,
                        border_radius=3,
                        paint=ft.Paint(color=GOLD),
                        width=0,
                    ),
                ],
            ),
            height=10,
            width=float("inf"),
        )
        self.audio = audio
        self.audio_duration = None
        self.on_pan_start = self.find_position
        self.on_pan_update = self.find_position
        # self.on_tap = self.tap_position
        self.on_hover = self.change_cursor
        self.on_change_position = on_change_position

    def canvas_resized(self, e: cv.CanvasResizeEvent):
        self.track_width = e.width
        e.control.shapes[0].width = e.width
        e.control.update()

    def tap_position(self, e:ft.ControlEvent):
        print('drag instead')

    def find_position(self, e):
        position = int(self.audio_duration * e.local_x / self.track_width)
        position = max(
                0, min(position, self.audio_duration)
            )
        self.content.content.shapes[1].width = max(
            0, min(e.local_x, self.track_width)
        )
        self.update()
        self.on_change_position(position)

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

# class hover_button(ft.GestureDetector):
#     def __init__(self, controls, bgcolor = ft.colors.TRANSPARENT, onclick = None, ref = None, visible= None):
#         super().__init__(ref= ref, visible= visible)
#         self.content = ft.Container(
#             controls,
#             bgcolor= bgcolor,
#             border_radius= 2,
#             padding= ft.padding.symmetric(horizontal=3, vertical= 1),
#             expand= True,
#             on_click= onclick
#         )
#         self.on_hover = self.onhover
    
#     def onhover(self, e: ft.HoverEvent):
#         e.control.mouse_cursor = ft.MouseCursor.CLICK
#         e.control.update()

# class Audioplayer():
#     def __init__(self, head:ft.Container) -> None:
#         self.head = head
#         self.paused = False

#     def loads(self, e): # this to load text
#         self.head.Pg.session.set('pasted_currrent', self.head.current)
#         if self.head.started:
#             self.head.started = False
#             self.head.audio1.play()
#         if self.head.nexted:
#             self.head.nexted = False
#             self.head.audio1.play()
#         if self.head.skip:
#             position = self.head.skip
#             self.head.skip = False
#             self.head.audio1.play()
#             self.head.audio1.pause()
#             self.head.audio1.seek(position)
#             self.head.audio1.resume()
#             self.head.Pg.update()

#     def change_position(self, e:ft.ControlEvent):
#         current = self.head.current
#         self.head.position = round(sum(self.head.meta[1][:current]))*1000 + int(e.data) # make animation smother
#         progress = self.head.position / self.head.total
#         self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
#         if self.head.set_time != None:
#             self.head.title.current.value = self.head.set_time(self.head.position /1000)
#         self.head.update()
    
#     def seek_position(self, position):
#         for i in range(len(self.head.meta[1])):
#             if round(sum(self.head.meta[1][:i])*1000) <= position < round(sum(self.head.meta[1][:i+1])*1000):
#                 self.head.current = i
#                 position = position - round(sum(self.head.meta[1][:i])*1000)
#                 self.head.skip = position
#                 self.load(self.head.current)
#                 self.head.audio1.play()
#                 break
    
#     def nexts(self, e):
#         if e.data == 'completed':
#             self.head.nexted = True
#             self.head.current += 1
#             if self.head.current == self.head.meta[-1]:
#                 self.head.nexted = False
#                 self.reload()
#                 self.head.started = False
#                 self.head.playbut.current.visible = True
#                 self.head.pausebut.current.visible = False
#                 self.head.title.current.value = self.head.set_time(self.head.total /1000)
#                 self.head.update()
#             else:
#                 self.load(self.head.current)

#     def reload(self):
#         self.head.current = 0
#         self.head.position = 0
#         self.paused = False
#         self.head.track_canvas.content.content.shapes[1].width = (0)
#         self.head.track_canvas.update()

#     def ff_song(self, e: ft.ControlEvent):
#         new_position = (int(self.head.position) - round(sum(self.head.meta[1][:self.head.current])*1000))+ (10-1)*1000
#         self.head.position = round(sum(self.head.meta[1][:self.head.current])*1000) + new_position
#         progress = self.head.position / self.head.total
#         if progress < 1:
#             self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
#             if not new_position <= round(self.head.meta[1][self.head.current]*1000):
#                 for i in range(len(self.head.meta[1])): # use numpy to simplify
#                     if round(sum(self.head.meta[1][:i])*1000) < self.head.position < round(sum(self.head.meta[1][:i+1])*1000):
#                         self.head.current = i
#                         position = new_position - round(sum(self.head.meta[1][:i])*1000)
#                         self.head.skip = position
#                         self.load(self.head.current)
#                         if not self.paused and self.head.started:
#                             self.head.audio1.play()
#                         break
#             else:
#                 self.head.seek_position(new_position)
#         self.head.update()

#     def fr_song(self, e: ft.ControlEvent):
#         if self.head.started:
#             new_position = (int(self.head.position) - round(sum(self.head.meta[1][:self.head.current])*1000)) - (10-1)*1000
#             self.head.position = round(sum(self.head.meta[1][:self.head.current])*1000) + new_position
#             if self.head.position < 0: self.head.position = 0
#             progress = self.head.position / self.head.total
#             if progress < 1:
#                 self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
                
#                 if not new_position >= 0:
#                     for i in range(len(self.head.meta[1])): # use numpy to simplify
#                         if round(sum(self.head.meta[1][:i])*1000) <= self.head.position < round(sum(self.head.meta[1][:i+1])*1000): # decayng function
#                             self.head.current = i
#                             position = new_position - round(sum(self.head.meta[1][:i])*1000)
#                             self.head.skip = position
#                             self.load(self.head.current)
#                             if not self.paused:
#                                 self.head.audio1.play()
#                             break
#                 else:
#                     self.seek_position(new_position)
#             self.head.update()

#     def load(self, n):
#         path = f'{ROOTPATH}/temp_audio/{n}.wav'
#         self.head.audio1.src = path
#         self.head.audio1.update()

#     def pause(self, e):
#         self.paused = True
#         self.head.audio1.pause()
#         self.head.playbut.current.visible = True
#         self.head.pausebut.current.visible = False
#         self.head.update()

#     def play(self, e): # check if start or not 
#         if not self.head.started:
#             self.reload()
#             self.head.started = True
#             self.load(self.head.current)
#             self.head.audio1.play()
#         else:
#             self.head.audio1.resume()
#         self.paused = False
#         self.head.playbut.current.visible = False
#         self.head.pausebut.current.visible = True
#         self.head.update()
    
#     def stop(self, e):
#         self.head.started = False
#         self.pause('')
#         self.head.title.current.value = self.head.set_time(self.head.total /1000)
#         self.head.update()
#         self.reload()

