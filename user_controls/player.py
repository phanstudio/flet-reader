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

def update_current(page, _id, num):
        """
        # Book
        [
            "path",
            "subtitles_number",
            "current",
            "number_of_chunks",
            "duration",
            "image",
        ]
        """
        info = page.client_storage.get(f'Book.{_id}')
        info[2] = num
        page.client_storage.set(f'Book.{_id}', info)

def checking(_id, _num, page):
    book = page.client_storage.get(f'Book.{_id}')
    new_book = {
        "path": book[0],
        "subtitles_number": book[1],
        "current": book[2],
        "number_of_chunks": book[3],
        "duration": book[4],
        "image": book[5],
    }
    subtities = [[],[]]
    if len(book[1]) > 0:
        if int(_num) in book[1]:
            for i in book[1]:
                if int(_num) == i:
                    pat = os.path.normpath(f'Books/{_id}/sub/{i}.srt')
                    subtities = loads(os.path.join(ROOTPATH, pat))
    return subtities, new_book

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
        self.position = 0
        self.auto = False
        self.outside = None
        self.set_indicator = None
        self.play_function = None
        self.Oplay = None
        self.clamp_end = None
        self.clamp_start = 0
        self.section_access = None
        self.duration = None
        self.nextplay = None

    def audio_loaded(self, e):
        self.duration = self.get_duration()
        self._set_indicator(0, self.duration)
        if self.play_function:
            self.play_function(True if not self.auto else False) # changes the button to play
        self.track.audio_duration = self.duration
        self.text = -1 # for subtitles
        self.page.update()
        if self.auto: # fix
            self.auto = False
            self.play()
        if self.Oplay:
            self.play()
            self.seek(self.Oplay)
        self.page.update()
    
    def audio_reload(self):
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
    
    def _set_indicator(self, _start, _end=None, bookmark=False):
        if self.set_indicator:
            self.indicators["start"] = convertMillis(_start)
            if _end is not None:
                self.indicators["end"] = convertMillis(
                    _end
                )
            self.set_indicator(self.indicators, bookmark)
    
    def change_position(self, e:ft.ControlEvent):
        if self.outside == None:
            if self.clamp_end != None:
                if self.duration != None and\
                    not int(self.position) >= (self.clamp_end):
                    self.position = int(e.data)
                    self._set_indicator(self.position)
                    self.update_track()
                else:
                    self.pause()
                    self._set_indicator(self.clamp_start, bookmark= True)
                    if self.section_access:
                        self.section_access.set_playpause(False)
                self.page.update()
            else:
                if self.duration != None:
                    self.position = int(e.data)
                    self._set_indicator(self.position)
                    self.update_track()
        else:
            if not isinstance(self.outside, int):
                self.audio1.outside(e)

    def state_changed(self, e):
        if e.data == "completed":
            if self.play_function:
                self.play_function(True)
            if self.nextplay:
                self.nextplay()
            self.auto= True

    def update_track(self):
        if self.track is not None: # problem
            self.track.content.content.shapes[1].width = (
                self.position
                / self.track.audio_duration
                * self.track.track_width
            )
            self.track.update()

    @staticmethod
    def load(url, page:ft.Page, load_func= None):
        overlays = overlay(page)
        audiomanager = None
        if "audiomanager" in overlays._keys():
            audiomanager: AudioManager = overlays.audiomanager
        
        if audiomanager == None:
            audiomanager = AudioManager(url)
            if load_func:
                load_func(audiomanager)
            page.overlay.append(audiomanager)
            page.update()
        else:
            # add reload function
            if audiomanager.track is None:
                if load_func:
                    load_func(audiomanager)
            if audiomanager.src != url:
                audiomanager.src = url
            else:
                audiomanager.audio_reload()
        page.update()
        return audiomanager

    @staticmethod
    def unload(page:ft.Page, load_func= None):
        overlays = overlay(page)
        audiomanager = None
        if "audiomanager" in overlays._keys():
            audiomanager: AudioManager = overlays.audiomanager
        
        if audiomanager != None:
            # add reload function
            if load_func:
                load_func(audiomanager)
        page.update()
        return audiomanager

class AudioPlayer(ft.Column):
    def __init__(self):
        super().__init__(tight=True)
        self.alignment = ft.MainAxisAlignment.START
        self.expand = True
        self.src = None # subtitle
        
        self.tit = ft.Ref[ft.Text]()
        self.prt = ft.Ref[ft.Text]()
        self.num = ''
        self.nx = 0
        self.tot = 1
        self.bookmarksection = None

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
            onc=  self.open_section,
            ),
            self.buttom_button(
            ico=ft.Icons.SPEED,
            txt= 'speed',
            onc= self.adjust_speed,
            ),
            self.buttom_button(
            ico=ft.Icons.VOLUME_UP,
            txt= 'mute',
            onc=self.mute,
            ),
            self.buttom_button(
                ico=ft.Icons.LIST_ALT,
                txt= 'Library',
                onc = lambda _: self.page.go('/lib'),
            ),
            self.buttom_button(
                ico=ft.Icons.NOTE_ALT,
                txt= 'q-note',
                onc= lambda _: self.open_quicknote(),
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
        
        self.start_duration = ft.Text(size= 12, value= '00:00s') #change later
        self.end_duration = ft.Text(size= 12, value= '00:00e')
        self.title = ft.Row(
            controls=[
                ft.IconButton(
                    icon= ft.Icons.CHEVRON_LEFT,
                    on_click= lambda _: self.back_but(),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            'No track', 
                            size= 18, 
                            ref= self.tit,
                            text_align= 'center',
                            max_lines= 2,
                        ),
                        ft.Text('NaN', size= 10, ref= self.prt,
                                            text_align= 'center')   
                    ], 
                    spacing= 0,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                ),
                ft.IconButton(
                    icon= ft.Icons.STAR
                ),
            ], 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self.textt = ft.ListView(
            expand=True, 
            spacing= 5,
            auto_scroll= True,
        )
        self.text = -1
        self.auto = False
        self.reloading = False
        
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
        self.page.go('/bookover')

    def open_section(self, e):
        body = self.parent
        self.bookmarksection = body.open_overlays("section")
        self.bookmarksection.visible = True
        start = int(self.audio1.position)
        end = start+ 30*1000
        self.bookmarksection.start_indicator.current.value = convertMillis(start)
        self.bookmarksection.end_indicator.current.value = convertMillis(end)
        total = self.track_canvas.audio_duration
        if end > total -30*1000:
            end = total
            start = end - 30*1000
        scl = (start/ total) * (self.page.window.width- (40+16))
        ecl = ((total-end)/ total) * (self.page.window.width- (40+16))
        self.bookmarksection.pointer2.right = -(
            self.bookmarksection.pointer2.width/2
        ) + ecl
        self.bookmarksection.pointer1.left = -(
            self.bookmarksection.pointer1.width/2
        ) + scl
        self.bookmarksection.update()
        self.audio1.section_access = self.bookmarksection

    def open_quicknote(self):
        body = self.parent
        quicknote = body.open_overlays("quicknote")
        quicknote.visible = True
        quicknote.update()

    def open_dlg(self, prop = ''):
        self.page.dialog = self.dlg
        # print(self.dlg.__dict__)
        # self.dlg.title.value = str(prop)+'x Speed'
        self.dlg.open = True
        self.page.update()

    def buttom_button(self, ico= ft.Icons.LIST_ALT, txt= 'Love', onc=None):
        return ft.IconButton(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ico,
                    ),
                    ft.Text(
                        txt.title(), 
                        size= 12, 
                        weight= ft.FontWeight.BOLD,
                    ),
                ], 
                spacing= 0, 
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            ), 
            on_click=onc,
        )

    def next(self, e: ft.ControlEvent): # add a list
        if self.nx< self.tot-1: # below total
            self.move("+")
            # self.page.go(f'/lib{self.num}/{self.nx+1}')
    
    def prev(self, e: ft.ControlEvent): # add a list
        if self.nx > 0: # below total
            self.move("-")
            # self.page.go(f'/lib{self.num}/{self.nx-1}')
    
    def move(self, operation):
        # problem with next and back in moving
        self.textt.controls.clear()
        self.reloading = True
        _id = self.page.session.get("BookId")
        num = None
        
        match operation:
            case "+":
                num = self.nx+1
            case "-":
                num = self.nx-1
            case _:
                raise ValueError("Opeartion wrong only [+,-]")
        
        subtitles, book= checking(_id, num, self.page)
        src = f'{book["path"]}/parts/{num}.mp3'
        self.load(
            _id,
            num, 
            self.tot, 
            subtitles, 
            src,
        )

    def load( # create an unload function that remove the dependencies and a reload function
            self, 
            ids, 
            num, 
            tot, 
            subt= [[],[]],
            src = r"C:\Users\ajuga\Music\Benny_Blanco_feat_Halsey_feat_Khalid_Eastside.mp3"
        ): # add a list
        self.audio1 = AudioManager.load(src, self.page, self._load_track)
        w = TextWrapper(25)
        self.tit.current.value = w.fill(ids)
        self.prt.current.value = 'Part'+str(num)
        self.num = '/'+ids
        self.nx = int(num)
        self.tot = tot # total
        self.src = subt
        _id = self.page.session.get("BookId")
        update_current(self.page, _id, self.nx)
        self.page.update()
    
    def adjust_speed(self, e: ft.ControlEvent):
        playrate = [1, 1.2, 1.5, 0.8]
        rate = 0 if self.audio1.playback_rate == None else playrate.index(self.audio1.playback_rate)
        rate = (rate + 1) if rate < (len(playrate)-1) else 0
        self.audio1.playback_rate = playrate[rate]
        spd = str(self.audio1.playback_rate)
        spd = '' if spd == 'None' or spd == '1' else (spd + 'x ')
        e.control.content.controls[1].value = spd + 'speed'
        self.page.update()

    def mute(self, e: ft.ControlEvent):
        # self.audio1.volume = 1 - self.audio1.volume if self.audio1.volume is not None else 0
        self.audio1.volume = 0 if self.audio1.volume in (1, None) else 1
        e.control.content.controls[0].name = ft.Icons.VOLUME_UP if self.audio1.volume == 1 else ft.Icons.VOLUME_MUTE
        e.control.content.controls[1].value = "mute" if self.audio1.volume == 1 else "unmute"
        self.page.update()

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
        self.audio1.position = self.audio1.clamp_start
        self.track_canvas.content.content.shapes[1].width = (
            self.audio1.clamp_start
            / self.track_canvas.audio_duration
            * self.track_canvas.track_width
        )
        self.seek_position(self.audio1.clamp_start)
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

    def mod_list(self):
        """
        Modify the list of text controls dynamically, adjusting size, color, and background.
        
        Key improvements:
        - More robust list management
        - Clearer color and styling logic
        - Simplified list manipulation
        """
        list_len = len(self.textt.controls)
        
        # Reduce size and opacity of the previous last item if list is not empty
        if list_len > 0:
            last_control = self.textt.controls[-1]
            last_control.size -= 1
            last_control.color = ft.Colors.with_opacity(0.7, ft.Colors.INVERSE_SURFACE)
            last_control.bgcolor = None
        
        # Add new controls if the list is smaller than the target length
        if list_len < self.text + 1:
            new_controls = [
                ft.Text(
                    text, 
                    size=13,
                    color=ft.Colors.with_opacity(0.7, ft.Colors.INVERSE_SURFACE)
                ) 
                for text in self.src[1][list_len:self.text+1]
            ]
            self.textt.controls.extend(new_controls)
        
        # Remove excess controls if list is too long
        elif list_len > self.text + 1:
            del self.textt.controls[self.text + 1:]
        
        # Highlight the new last control
        if self.textt.controls:
            new_last_control = self.textt.controls[-1]
            new_last_control.size += 1
            new_last_control.color = ft.Colors.with_opacity(1, ft.Colors.INVERSE_SURFACE)
            new_last_control.bgcolor = ft.Colors.with_opacity(0.2, GOLD)

    def did_mount(self):
        self.overlays = overlay(self.page)
        return super().did_mount()
    
    def _load_track(self, audiomanager): # create a way to reload the tracks
        self.audio1 :AudioManager = audiomanager
        self.audio1.track = self.track_canvas
        self.audio1.play_function = self.set_play_pause
        self.audio1.set_indicator = self.set_indictors
        self.audio1.nextplay = lambda : self.next("")
        self.track_canvas.find_position(self.track_canvas.stored_e)
        if "audiomanager" in self.overlays._keys():
            self.set_play_pause(
                True if not self.audio1.get_current_position() > 0 else False
            )
        else:
            self.set_play_pause(True)
    
    def _unload_track(self, audiomanager): # create a way to reload the tracks
        self.audio1 :AudioManager = audiomanager
        self.audio1.track = None
        self.audio1.play_function = None
        self.audio1.set_indicator = None
        self.audio1.nextplay = None
        self.page.update()

    def set_indictors(self, indicator, bookmark=False):
        """
            self.indicators = {
                "start"
                "end"
            }
        """
        if not bookmark:
            self.start_duration.value = indicator["start"]
            self.end_duration.value = indicator["end"]
        if self.bookmarksection != None:
            self.bookmarksection.start_indicator.current.value = indicator["start"]
            # self.bookmarksection.end_indicator.current.value = indicator["end"]
            self.bookmarksection.update()

        if self.track_canvas.audio_duration != None:
            v = self.audio1.position/1000
            
            pos = check(v, self.src[0])
            if self.reloading:
                self.reloading = False
                pos = -1
            
            if pos != None:
                if self.text != pos:
                    self.text = pos
                    self.mod_list()
        self.update()
    
    def set_play_pause(self, play, pause=None):
        self.play_button.visible = play
        self.pause_button.visible = (not play) if pause == None else pause
        self.update()

    def will_unmount(self):
        AudioManager.unload(self.page, self._unload_track)
        return super().will_unmount()

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
