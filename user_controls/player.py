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

overl = ""#quick_note(List_Tile, page)

class AudioManager(ft.Audio):
    def __init__(self, src = None, src_base64 = None, autoplay = None, volume = None, balance = None, playback_rate = None, release_mode = None, on_position_changed = None, on_seek_complete = None, ref = None, data = None):
        super().__init__(src, src_base64, autoplay, volume, balance, playback_rate, release_mode, None, None, None, on_position_changed, on_seek_complete, ref, data)
        self.on_loaded = self.audio_loaded
        self.on_position_changed= self.change_position
        self.on_state_changed=self.state_changed

        self.track = None
        self.indicators = {
            "start": convertMillis(0),
            "end": convertMillis(0),
        }
        self.set_indicator = None
        self.position = 0
        self.auto = False
        self.outside = None
        self.play_function = None
        self.Oplay = None
        self.clamp_end = None

    def audio_loaded(self, e):
        duration = self.get_duration()
        self._set_indicator(0, duration)
        if self.play_function:
            self.play_function(True) # changes the button to play
        self.track.audio_duration = duration
        self.text = -1 # for subtitles
        self.page.update()
        if self.auto: # fix
            self.auto = False
            self.play()
        if self.Oplay:
            self.play()
            self.seek(self.Oplay)
        self.page.update()
    
    def _set_indicator(self, _start, _end=None):
        if self.set_indicator:
            self.indicators["start"] = convertMillis(_start)
            if _end is not None:
                self.indicators["end"] = convertMillis(
                    _end
                )
            self.set_indicator(self.indicators)
    
    def change_position(self, e:ft.ControlEvent):
        if self.outside == None:
            if self.clamp_end != None:
                if self.track.audio_duration != None and\
                    not int(self.position) >= (self.clamp_end):
                    self.position = int(e.data)
                    v = self.position/1000
                    # pos = check(v, self.src[0])
                    # if pos != None:
                    #     if self.text != pos:
                    #         self.text = pos
                    #         # self.mod_list()
                    #         # scroll to position
                    # self.nox.c_s.current.value = f"{convertMillis(int(e.data))}"
                    self._set_indicator(self.position)
                    self.track.content.content.shapes[1].width = (
                        self.position
                        / self.track.audio_duration
                        * self.track.track_width
                    )
                    e.control.page.update()
                else:
                    self.pause('')
                    self.nox.c_s.current.value = f"{convertMillis(self.clamp_start)}"
                    self.nox.update()
            else:
                if self.track.audio_duration != None:
                    self.position = int(e.data)
                    v = self.position/1000
                    # pos = check(v, self.src[0]) # for subtitles
                    # if pos != None:
                    #     if self.text != pos:
                    #         self.text = pos
                    #         # self.mod_list()
                    #         # scroll to position
                    self._set_indicator(self.position)
                    self.track.content.content.shapes[1].width = (
                        self.position
                        / self.track.audio_duration
                        * self.track.track_width
                    )
                    self.track.update()
        else:
            if not isinstance(self.outside, int):
                self.audio1.outside(e)

    def state_changed(self, e):
        if e.data == "completed":
            self.play_function(True)

    @staticmethod
    def load(url, page:ft.Page, load_func= None):
        overlays = overlay(page)
        audiomanger = None
        if "audiomanger" in overlays._keys():
            audiomanger: AudioManager = overlays.audiomanger

        if audiomanger == None:
            audiomanger = AudioManager(url)
            if load_func:
                load_func(audiomanger)
            page.overlay.append(audiomanger)
            page.update()
        else:
            # add reload function
            audiomanger.src = url
        
        page.update()
        return audiomanger

class AudioPlayer(ft.Column):
    def __init__(self):
        super().__init__(tight=True)
        self.alignment = ft.MainAxisAlignment.START
        self.expand = True
        self.src = None # subtitle

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
            on_change_position=self.seek_position
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
        s = int(self.audio1.position)
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
    
    def load( # create an unload function that remove the dependencies and a reload function
            self, 
            ids, num, tot, subt= [[],[]],
            src = r"C:\Users\ajuga\Music\Benny_Blanco_feat_Halsey_feat_Khalid_Eastside.mp3"
        ): # add a list
        self.audio1 = AudioManager.load(src, self.page, self._load_track) 
        w = TextWrapper(25)
        self.tit.current.value = w.fill(ids)
        self.prt.current.value = 'Part'+str(num)
        self.num = '/'+ids
        self.nx = int(num)
        self.tot = tot
        self.src = subt
        self.page.update()
    
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
        new_position = int(self.audio1.position) + int(e.control.data)*1000
        self.audio1.position = new_position
        self.track_canvas.content.content.shapes[1].width = (
            new_position
            / self.track_canvas.audio_duration
            * self.track_canvas.track_width
        )
        self.seek_position(new_position)
        self.page.update()
    
    def clamp_update(self, e: ft.ControlEvent):
        # new_position = int(self.position) + int(e.control.data)*1000
        self.audio1.position = self.clamp_start
        self.track_canvas.content.content.shapes[1].width = (
            self.clamp_start
            / self.track_canvas.audio_duration
            * self.track_canvas.track_width
        )
        self.seek_position(self.clamp_start)
        self.page.update()

    def fr_song(self, e: ft.ControlEvent):
        new_position = int(self.audio1.position) - int(e.control.data)*1000
        self.audio1.position = new_position
        self.track_canvas.content.content.shapes[1].width = (
            new_position
            / self.track_canvas.audio_duration
            * self.track_canvas.track_width
        )
        self.seek_position(new_position)
        self.page.update()

    def play(self, e):
        if self.audio1.position != 0:
            self.audio1.resume()

        else:
            self.audio1.play()
        self.set_play_pause(False)
        self.page.update()

    def pause(self, e):
        self.audio1.pause()
        self.set_play_pause(True)
        self.page.update()

    def seek_position(self, position):
        self.audio1.seek(position)
        self.page.update()

    def mod_list(self): # subtitle # fix
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

    def did_mount(self):
        self.overlays = overlay(self.page)
        return super().did_mount()
    
    def _load_track(self, audiomanger): # create a way to reload the tracks
        self.audio1 :AudioManager = audiomanger
        self.audio1.track = self.track_canvas
        self.audio1.play_function = self.set_play_pause
        self.audio1.set_indicator = self.set_indictors
        self.track_canvas.find_position(self.track_canvas.stored_e)
        self.set_play_pause(True)

    def set_indictors(self, indicator):
        """
            self.indicators = {
                "start"
                "end"
            }
        """
        self.end_duration.value = indicator["end"]
        self.start_duration.value = indicator["start"]
        # self.nox.c_e.current.value = convertMillis(self.audio1.get_duration())
        self.update()

    def set_play_pause(self, play, pause=None):
        self.play_button.visible = play
        self.pause_button.visible = (not play) if pause == None else pause
        self.update()

class Track(ft.GestureDetector):
    def __init__(self, on_change_position):
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
        self.audio_duration = None
        self.stored_e = None
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
        self.stored_e = None
        if self.audio_duration:
            position = int(self.audio_duration * e.local_x / self.track_width)
            position = max(
                    0, min(position, self.audio_duration)
                )
            self.content.content.shapes[1].width = max(
                0, min(e.local_x, self.track_width)
            )
            self.update()
            self.on_change_position(position)
        else:
            self.stored_e = e

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
