import flet as ft
from flet import Page as pG
import uuid, os
from .split_Ter import five_min_splitter, get_duration

def per_clamp(n, minn = 274.4, maxn= 1530.4):
    per = ((n - minn)/(maxn-minn))*100
    return max(min(100, per), 0)

def cnr(ids, src, val, per, time, text):
    return {'ids':ids, 'src':src, 'val': val, 'per': per, 'time': time, 'text': text}

def change_theme(page:pG) -> None:
    page.theme_mode = (
        ft.ThemeMode.LIGHT 
        if page.theme_mode == ft.ThemeMode.DARK 
        else ft.ThemeMode.DARK
    )
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
    chunk_list = sorted([int(x.replace(".mp3", "")) for x in os.listdir(new_path)]) 
    total = len(chunk_list)
    dur = round(get_duration(f"{new_path}/{chunk_list[-1]}.mp3"))
    seconds = dur%60
    minute = dur//60
    seconds_str = f"0{seconds}" if seconds < 10 else f"{seconds}"
    minute_str = f"0{minute}" if minute < 10 else f"{minute}"
    duration = f'{minute_str}:{seconds_str}'

    return total, duration

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
