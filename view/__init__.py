from .Home import HomeView
from .Note import NoteView
from .Add import AddView
from .Lib import LibView
from .Section import SectionView

routes = {
    "/": HomeView,
    "/note": NoteView,
    "/add": AddView,
    "/lib": LibView,
    "/section": SectionView,
}
