import flet as ft
from flet import Page as pG
import uuid, os, time
from .split_Ter import five_min_splitter, AudioSegment
from.img_loader import loader
from .custom_classes import overlay
from .constants import ROOTPATH, GOLD, BOLD

# Test Data
dt = [[2, 12,'part 1',20, '03:00', 'Tale of the over powered hero'],
        [4, 13,'part 12',35, '05:06', 'Villain story'],
        [40, 11,'part 7',80, '01:53', 'Night books'],
        [89, 10,'part 4',0, '02:56', 'Soaring sky'],
        [69, 14,'part 20',40, '13:46', 'Revered insanity'],
        [1, 9,'part 5',60, '03:26', 'Chuck'],
        [1, 9,'part 5',60, '03:26', 'Chuck missing 1 required positional argument'],]
ndt = [['Queen of hearts', 'This section focus mustly on elizabet', 9],
        ['Kindness', 'The stupidity it brings', 20],
        ['Love', 'The greatness, before the fall it brings', 12],
        ['Loving you with all my heart', 'The greatness, before the fall it brings', 16],]


def per_clamp(n, minn = 274.4, maxn= 1530.4):
    per = ((n - minn)/(maxn-minn))*100
    return max(min(100, per), 0)

def cnr(ids, src, val, per, time, text):
    return {'ids':ids, 'src':src, 'val': val, 'per': per, 'time': time, 'text': text}

def p221(p2, page:pG):
    p2.onchange(per_clamp(page.window.width, 282.4))
    if page.route == '/lib':
        p2.update()

def change_theme(page:pG) -> None:
    page.theme_mode = (ft.ThemeMode.LIGHT 
                       if page.theme_mode == ft.ThemeMode.DARK 
                       else ft.ThemeMode.DARK)
    page.update()

def create_note(page: pG, num =1, head='', body = [['','H'],]):
    # H, SH, T
    page.client_storage.set(
        f'Note.{num}', 
        [head, body,]
    )

def remove_note(page: pG, num =1):
    # H, SH, T
    page.client_storage.remove(f'Note.{num}')

def load_notes(page: pG):
    return page.client_storage.get_keys('Note')

def load_note_prop(page: pG, ld = 'Note.1'):
    return page.client_storage.get(ld)

def open_note(page:pG):
    random_uuid = uuid.uuid4()
    # page.go(f'/note/{random_uuid}')
    page.session.set("NoteId", random_uuid)
    page.go(f'/editnote')

def convertMillis(millis):
    if type(millis) != int: millis = 0
    seconds = int(millis / 1000) % 60
    minutes = int(millis / (1000 * 60)) % 60
    
    seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
    minutes_str = f"0{minutes}" if minutes < 10 else f"{minutes}"
    return f"{minutes_str}:{seconds_str}"          

def convertsrc(m):
    mj = []
    for j in m.split(' --> '):
        formt = [360,60,1]
        mj.append(sum(int(i) *formt[n] for n, i in enumerate(j[:-4].split(':'))))
    return mj

def convertminsec(millis):
    mint, sec = millis.split(':')

    mint = int(mint)*60
    sec = int(sec)
    return (mint+sec)*1000

def extraction(old_path, new_path):
    five_min_splitter(old_path, new_path)
    newp = os.listdir(new_path)
    total = len(newp)
    dur = round(AudioSegment.from_mp3(new_path+'/'+newp[-1]).duration_seconds)
    seconds = dur%60
    minute = dur//60
    seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
    minute_str = f"0{minute}" if minute < 10 else f"{minute}"
    duration = f'{minute_str}:{seconds_str}'

    return total, duration

def update_current(page:pG, name, num):
    # print(name, num)
    # page.client_storage.set('book.current', 
    #                         [name, num]
    #                         )
    ...

def delete(lib):
    if lib.grid1.controls[0].dels.current.visible != True:
        vis = True
    else:
        vis = False

    for i in lib.grid1.controls:
        i.dels.current.visible = vis
        i.update()

def play_pause(e, v):
    if v.outside == None:
        v.outside = 1
        v.play()
    else:
        v.outside = None
        v.pause()

