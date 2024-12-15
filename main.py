import flet as ft
from Utility import *
from view import routes

# add last read
# reduce the image

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
    page.overlay.append(ft.SnackBar(ft.Text("love"), duration= 1000))
    page.overlay.append(ft.FilePicker())
    # add audio manager
    # add download manager
    # add popup 

def main(page: ft.Page): # add security
    metadata(page)
    add_overlays(page)
    # set_theme(page)
    # overlays = overlay(page)
    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()
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