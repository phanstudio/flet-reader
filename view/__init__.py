from .Home import HomeView
from .Note import NoteView
from .Add import AddView
from .Lib import LibView
from .Section import SectionView

from .BookOverview import BookOverView
from .ViewBook import ViewBookView
from .EditNote import EditNoteView

# main routes {}+{} sub routes

routes = {
    # Main routes # make it so that main routes always reset the stack
    "/": HomeView,
    "/note": NoteView,
    "/add": AddView,
    "/lib": LibView,
    "/section": SectionView,
    # Sub routes
    "/bookover": BookOverView,
    "/viewbook": ViewBookView,
    "/editnote": EditNoteView,
}
