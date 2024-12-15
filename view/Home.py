import flet as ft
from Utility import *
from user_controls import Note_frame, Library_frame, Reading, Library, Note, Navbar

class HomeView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(0)
        )

        self.grid1 = ft.ListView( 
            height= 190, 
            spacing= 10,
            horizontal= True,
        )
        
        self.grid2 = ft.GridView( 
            height= 180, 
            runs_count=2, 
            horizontal= True,
            child_aspect_ratio= 0.55
        )

        self.libcontrainer= ft.Stack(
            controls=[
				self.grid1,
                ft.Container(
                    ft.Row(
                        controls=[
                            ft.Image('/covers/7.png', height= 200)
                        ], 
                        alignment= ft.MainAxisAlignment.CENTER), 
                        bgcolor= ft.Colors.with_opacity(0.1, ft.Colors.INVERSE_SURFACE)
                    )
            ]
        )

        self.notecontrainer= ft.Stack(
            controls=[
				self.grid2,
                ft.Row(
                    controls=[
                        ft.Image('/covers/11.png', height= 250)
                    ], 
                    alignment= ft.MainAxisAlignment.CENTER
                )
            ]
        )
		
        self.controls= [
            Reading(), # chanhe to a float indicator
            Library(),
            self.libcontrainer,
            Note(),
            self.notecontrainer,
		]
        
    def did_mount(self):
        books: list = self.page.client_storage.get_keys('Book') # change dts to books
        if books != []:
            books.remove('Book.hist')
        self.dts = []
        for i in books:
            self.dts.append([i[5:]]+self.page.client_storage.get(i))
        notes = load_notes(self.page)
        for note in notes:
            num = note.split('.')[1]
            note_prop = load_note_prop(self.page, note)
            self.grid2.controls.append(
                Note_frame(note_prop[0], note_prop[1][0], num)#, pg= page)
            )
        self.grid1.controls = [Library_frame(li=i) for i in self.dts]
        
        self.libcontrainer.controls[0].visible = True if len(self.grid1.controls) > 0 else False
        self.libcontrainer.controls[1].visible = not self.libcontrainer.controls[0].visible
        self.notecontrainer.controls[0].visible = True if len(self.grid2.controls) > 0 else False
        self.notecontrainer.controls[1].visible = not self.notecontrainer.controls[0].visible

        self.update()
        return super().did_mount()
