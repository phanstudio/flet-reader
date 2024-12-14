import flet as ft
from Utility import *
from user_controls import Library_frame, Navbar

class LibView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/lib",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(2),
        )

        # self.grid1 = ft.GridView( 
        #     height= 550,
        #     # expand= 1,
        #     # runs_count=0,
        #     # auto_scroll= True,
        #     spacing= 25,
        #     max_extent= 180,#238, #230 #130
        #     # runs_count= 3,
        #     run_spacing= 0, #10
        #     # padding= 20,
        #     child_aspect_ratio= 0.80,#0.54,#0.38,
        # )
        self.grid1 = ft.GridView( 
            # height= 550,
            expand= True,
            # runs_count=0,
            # auto_scroll= True,
            spacing= 25,
            max_extent= 180,#238, #230 #130
            # runs_count= 3,
            run_spacing= 0, #10
            # padding= 20,
            child_aspect_ratio= 0.667,#0.54,#0.38,
        )
        self.defualt = ft.Image(
            '/covers/9.png',
            expand= True,
        )
        self.controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        'Library', 
                        size= 20, 
                        weight= BOLD
                    ), 
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        on_click= lambda _: self.page.go("/add"), 
                        data= 0
                    ),
                ], 
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            self.defualt,
            self.grid1,
        ]

    def did_mount(self):
        dts: list = self.page.client_storage.get_keys('Book')
        if dts != []:
            dts.remove('Book.hist')
        self.dts = []
        for i in dts:
            self.dts.append([i[5:]]+self.page.client_storage.get(i))
        self.grid1.controls = [Library_frame(li=i, pert= self) for i in self.dts] 
        self.defualt.visible = not len(dts) > 0
        self.grid1.visible = not self.defualt.visible
        self.update()
        return super().did_mount()

    def cnr(ids, src, val, per, time): # check for this
        return {'ids':ids, 'src':src, 'val': val, 'per': per, 'time': time}

# if page.route == '/lib':
#     v_Audio = sub.content.audio1
#     page.overlay.append(v_Audio)
#     page.overlay.append(
#         Column(
#             [
#                 Container(
#                     Row(
#                         [
#                             IconButton(
#                                 ft.icons.CHEVRON_LEFT, 
#                                 on_click= lambda _: page.go(f'/')
#                             ),
#                             Reading(
#                                 lambda e: play_pause(e, v_Audio)
#                             ),
#                             IconButton(ft.icons.MORE_VERT, on_click=
#                                 lambda _:  delete(lib_page)
#                             ),
#                         ], 
#                         expand= True
#                     ),
#                     padding= 10, 
#                     bgcolor= ft.Colors.BACKGROUND
#                 )
#             ], 
#             alignment= MainAxisAlignment.START
#         )
#     )