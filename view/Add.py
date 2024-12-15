import flet as ft
from Utility import *
from user_controls import Navbar
import shutil
import os

def on_dialog_result(file, page, indicator=None): # becove overlayed
    old_path = file
    _, tail = os.path.split(old_path)
    name = tail.split('.')[0]

    path = os.path.join(ROOTPATH, 'Books', name)
    book_path = f'/Books/{name}'
    subtitle = []
    current = 0
    if indicator:
        new_book = HistoryTile(name)

    # Retrieve and update book history
    book_history = page.client_storage.get('Book.hist') 
    if not book_history : book_history = []

    if name not in book_history: # adds to history
        book_history.append(name)
        page.client_storage.set('Book.hist', book_history)
        
        try:
            if indicator:
                indicator.controls.insert(0, new_book)
                new_book_index: HistoryTile = indicator.controls[0]
                indicator.update()
        except:
            print("indicator doesn't exsist")
    
    else:
        # Update the existing book in the list
        try:
            if indicator:
                index = book_history.index(name)
                new_book_index: HistoryTile = indicator.controls[index]
                # new_book_index.change_indicator(1)
        except:
            print("indicator doesn't exsist")
    
    if indicator:
        new_book_index.change_indicator(1)

    # Ensure necessary directories exist
    if not os.path.exists(path):
        os.makedirs(os.path.join(path, 'parts'))
        os.makedirs(os.path.join(path, 'sub'))

    try:
        # Extract details from the book
        total, duration = extraction(old_path, os.path.join(path, 'parts'))
        # Load book image
        img = loader(old_path, name)

        # Store book details in client storage
        page.client_storage.set(
            f'Book.{name}',
            [book_path, subtitle, current, total, duration, img]
        )
        try:
            if indicator:
                new_book_index.change_indicator(0)
        except:
            print("indicator doesn't exsist")
    except:
        try:
            if indicator:
                new_book_index.change_indicator(2)
        except:
            print("indicator doesn't exsist")

class HistoryTile(ft.Container):
    def __init__(self, _id):
        super().__init__(
            # bgcolor= CONTAINER_COLOR,
            border_radius= 5,
            padding= 5,
            border= ft.border.all(2, CONTAINER_COLOR),
            ink= True,
        )
        self.book_id = _id
        self.delete_button = ft.IconButton(ft.Icons.DELETE, on_click= lambda _: self.delete_book())
        self.reload_button = ft.IconButton(ft.Icons.REPLY_ALL_ROUNDED)
        self.book_name = ft.Text(
            self.book_id,
            expand=True,
        )
        self.progressbar = ft.ProgressRing(width= 30, height= 30, stroke_cap= ft.StrokeCap.ROUND)#ft.ProgressBar(width=60) # update queus
        self.content = ft.Row(
            controls=[
                self.book_name,
                self.progressbar,
                self.delete_button,
                self.reload_button,
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self.on_click = self.onclick
    
    def onclick(self, e):
        self.page.session.set("BookId", self.book_id)
        self.page.go(f'/bookover')
    
    def did_mount(self):
        books = self.page.client_storage.get_keys('Book')
        done_loading = 0 if f'Book.{self.book_id}' in books else 2 # reload
        self.change_indicator(done_loading)
        self.overlays = overlay(self.page)
        self.file_picker: ft.FilePicker = self.overlays.filepicker

        self.reload_button.on_click = lambda _: self.file_picker.pick_files(
            dialog_title= 'Find the books path', 
            file_type= ft.FilePickerFileType.AUDIO
        )
        return super().did_mount()
    
    def change_indicator(self, value):
        self.delete_button.visible = False
        self.progressbar.visible = False
        self.reload_button.visible = False
        self.border= ft.border.all(2, CONTAINER_COLOR)
        match value:
            case 0:
                self.delete_button.visible = True
            case 1:
                self.progressbar.visible = True
            case 2:
                self.delete_button.visible = True
                self.reload_button.visible = True
                self.border= ft.border.all(2, ft.Colors.with_opacity(0.3, "red"))
            case _:
                raise ValueError("Invalid value [0-2]")
        self.update()

    def clear(self):
        parent = self.parent
        dts: list = self.page.client_storage.get_keys('Book')
        dts.remove('Book.hist')
        self.page.client_storage.set('Book.hist', [])
        # add clear the path
       
        for i in dts:
            self.page.client_storage.remove(i)
            shutil.rmtree(os.path.join(ROOTPATH,'Books', f'{i.split(".")[-1]}'))
        parent.controls.clear()
        parent.update_icon()
    
    def delete_book(self):
        parent = self.parent
        dts: list = self.page.client_storage.get_keys('Book')
        book = [i for i in dts if self.book_id in i]
        book = book[0] if len(book)> 0 else None
        hist: list = self.page.client_storage.get('Book.hist')
        hist.remove(self.book_id)
        self.page.client_storage.set('Book.hist', hist)
        if book:
            self.page.client_storage.remove(book)
        book_path = os.path.join(ROOTPATH,'Books', f'{self.book_id}')
        if os.path.exists(book_path):
            shutil.rmtree(book_path)
        parent.controls.remove(self)
        parent.update_icon()

class AddView(ft.View): # add a will unmount wauning
    def __init__(self) -> None:
        super().__init__(
            route= "/add",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(1),
        )

        self.add_button = ft.IconButton(
            ft.Icons.ADD_ROUNDED,
            icon_color= 'white',
            bgcolor= GOLD,
            #   icon_size= 10,
            width= 40,
            height= 40,
            style=ft.ButtonStyle(
                bgcolor= {ft.ControlState.HOVERED: ft.Colors.with_opacity(0.3, 'black')}
            ),
        )
        self.empty_placeholder = ft.Container(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self.add_button,
                            ft.Row([ # change to text spans
                                ft.Text('Choose a file to'),
                                ft.Text(' upload ', color= GOLD, weight= ft.FontWeight.BOLD,),
                                ft.Text('here'),
                                ], spacing= 0)
                        ], horizontal_alignment= ft.CrossAxisAlignment.CENTER
                    ),
                ], alignment= ft.MainAxisAlignment.CENTER
            ),
            bgcolor= ft.Colors.with_opacity(0.1, ft.Colors.INVERSE_SURFACE),
            # border= ft.border.all(2),
            border_radius= 5,
            padding= 20,
        )
        self.main_body = ft.ListView(
            expand= True,
            spacing= 10,
        )
        # self.dp = dp
        self.controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        value='Add a Book',
                        weight= ft.FontWeight.BOLD,
                    ),
                    ft.IconButton(
                        ft.Icons.SEARCH, 
                        on_click= self.onclick
                    ),
                ], 
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Container(
                content=ft.Text("Manage books here, add or remove various books", text_align= ft.TextAlign.CENTER),
                bgcolor= CONTAINER_COLOR,
                padding= 5,
            ),
            self.empty_placeholder,
            self.main_body,
        ]
    
    def onclick(self, e):
        print("#")
        
    def did_mount(self):
        self.overlays = overlay(self.page)
        self.file_picker: ft.FilePicker = self.overlays.filepicker
        self.file_picker.on_result = self.on_dialog_result
        # add extras
        past_hist:list = self.page.client_storage.get('Book.hist')
        if past_hist != None:
            for i in past_hist:
                self.main_body.controls.append(HistoryTile(i))
        self.change_icons()
        self.main_body.update_icon = self.change_icons
            
        self.page.update()
        return super().did_mount()
    
    def change_icons(self):
        self.main_body.visible = len(self.main_body.controls) > 0
        self.empty_placeholder.visible = not self.main_body.visible
        addfile = lambda _: self.file_picker.pick_files(
            dialog_title= 'Book Adder', 
            file_type= ft.FilePickerFileType.AUDIO
        )
        if not self.main_body.visible:
            self.add_button.on_click = addfile
            self.floating_action_button = None
        else:
            self.floating_action_button = ft.FloatingActionButton(
                icon= ft.Icons.ADD,
                on_click= addfile,
            )
            self.add_button.on_click = None
        self.page.update()
    
    def on_dialog_result(self, e: ft.FilePickerResultEvent): # needs to be async
        for file in e.files: # for now only accepts one at a time
            if file.path:
                on_dialog_result(file.path, self.page, self.main_body)
        