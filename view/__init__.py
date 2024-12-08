from .Home import HomeView
from .Note import NoteView
from .Add import AddView
routes = {
    "/": HomeView,
    "/note": NoteView,
    "/add": AddView
}
