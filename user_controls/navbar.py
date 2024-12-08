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
                ft.NavigationBarDestination('Home', ft.icons.HOME_ROUNDED, data= '/'),
                ft.NavigationBarDestination('Home', ft.icons.ADD_BOX, data= '/add'),
                ft.NavigationBarDestination('Home', ft.icons.LOCAL_LIBRARY_ROUNDED, data= '/lib'),
                ft.NavigationBarDestination('Home', ft.icons.BOOK, data= '/bmark'),
                ft.NavigationBarDestination('Note', ft.icons.EDIT_NOTE, data= '/note'),
            ],
            on_change= self.onchange,
        )
    
    def onchange(self, e: ft.ControlEvent):
        navbar: Navbar = e.control
        index = int(e.data)
        destination_control = navbar.destinations[index]
        self.page.go(destination_control.data)
