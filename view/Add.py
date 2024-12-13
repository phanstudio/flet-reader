import flet as ft
from Utility import *
from user_controls import Navbar, ListTile, BookProgressSheet
import shutil
import os

def on_dialog_result(e: ft.FilePickerResultEvent): # needs to be async
    if e.files is None:
        return  # Exit early if no files are selected
    
    page = e.page
    overlays = overlay(page)
    Book_sheet: BookProgressSheet = overlays.bookprogresssheet

    Book_sheet.visible = True
    Book_sheet.update()  # Show the progress sheet
    old_path = e.files[0].path
    _, tail = os.path.split(old_path)
    name = tail.split('.')[0]

    path = os.path.join(ROOTPATH, 'Books', name)
    book_path = f'/Books/{name}'
    subtitle = []
    current = 0
    new_book = ListTile(name)

    # Retrieve and update book history
    book_history = page.client_storage.get('Book.hist') 
    if not book_history : book_history = []

    if name not in book_history: # adds to history
        book_history.append(name)
        page.client_storage.set('Book.hist', book_history)
        
        # Prepend new book to the list
        Book_sheet.list_body.controls.insert(0, new_book)
    else:
        # Update the existing book in the list
        index = book_history.index(name)
        Book_sheet.list_body.controls[index].done('d')
        Book_sheet.list_body.controls[index].update()
        print(Book_sheet.list_body.controls[index])
    Book_sheet.popup()

    # Ensure necessary directories exist
    if not os.path.exists(path):
        os.makedirs(os.path.join(path, 'parts'))
        os.makedirs(os.path.join(path, 'sub'))

    # Extract details from the book
    total, duration = extraction(old_path, os.path.join(path, 'parts'))
    # Load book image
    img = loader(old_path, name)

    # Store book details in client storage
    page.client_storage.set(
        f'Book.{name}',
        [book_path, subtitle, current, total, duration, img]
    )

    # Update progress on the UI
    if name in book_history:
        for item in Book_sheet.list_body.controls:
            if item.text_container.value == name:
                item.done('f')
    else:
        new_book.done('f')
    
    Book_sheet.update()

class AddView(ft.View):
    def __init__(self) -> None:
        super().__init__(
            route= "/add",
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            bgcolor = BACKGROUND_COLOR,
            navigation_bar= Navbar(1),
        )

        # self.file_picker = ft.FilePicker()
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
        # self.dp = dp
        self.controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        value='Add a Book',
                        weight= ft.FontWeight.BOLD,
                    ),
                    ft.IconButton(
                        ft.Icons.HISTORY, 
                        on_click= self.onclick
                    ),
                ], 
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            
            ft.Container(
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
            ),
            # ElevatedButton(text='Go back',
            #             on_click= lambda _: page.go('/'))
        ]
    
    def onclick(self, e):
        self.overlays.bookprogresssheet.popup()
        
    def did_mount(self):
        self.overlays = overlay(self.page)
        self.file_picker = self.overlays.filepicker
        self.file_picker.on_result = on_dialog_result
        self.add_button.on_click =lambda _: self.file_picker.pick_files(
                dialog_title= 'Book Adder', file_type= ft.FilePickerFileType.AUDIO)
        self.page.update()

        return super().did_mount()
