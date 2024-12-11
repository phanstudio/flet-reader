import flet as ft
import shutil
from Utility import *
from user_controls import (BookProgressSheet)
from pages import subpage2, loads
import flet.canvas as cv
from view import routes


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