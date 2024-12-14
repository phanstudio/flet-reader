import flet as ft
from Utility import BACKGROUND_COLOR

class Navbar(ft.NavigationBar):
    def __init__(self, currect_index):
        super().__init__(
            selected_index= currect_index,
            # bgcolor= CONTAINER_COLOR,
            indicator_color= BACKGROUND_COLOR,
            indicator_shape= ft.CircleBorder(),
            label_behavior= ft.NavigationBarLabelBehavior.ALWAYS_HIDE,
            destinations= [
                ft.NavigationBarDestination('Home', ft.Icons.HOME_ROUNDED, data= '/'),
                ft.NavigationBarDestination('Add', ft.Icons.ADD_BOX, data= '/add'),
                ft.NavigationBarDestination('Lib', ft.Icons.LOCAL_LIBRARY_ROUNDED, data= '/lib'),
                # ft.NavigationBarDestination('Section', ft.Icons.BOOK, data= '/section'),
                ft.NavigationBarDestination('Note', ft.Icons.EDIT_NOTE, data= '/note'),
            ],
            on_change= self.onchange,
        )
    
    def onchange(self, e: ft.ControlEvent):
        navbar: Navbar = e.control
        index = int(e.data)
        destination_control = navbar.destinations[index]
        self.page.go(destination_control.data)
