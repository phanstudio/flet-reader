
from flet import (Container, MainAxisAlignment, Colors, Row, margin)


class readbar(Container): #change to progress bar
    def __init__(self, fgcolor:str = 'amber', 
                 height: int = 4, start: int = 60, width: int = 200,
                 radius: int = 20, align = 'right', tight = False, tp= 'c', lp = 0.16):
        super().__init__()

        if tp == 'c': tp =  Colors.INVERSE_SURFACE
        elif tp == 'b': tp = Colors.WHITE10
        else: tp =  Colors.SURFACE
        
        if start > 100: start = 100
        if start < 0: start  = 0
        self.percent = width/100
        S_val = self.percent * start

        align = (MainAxisAlignment.END if align == 'right' 
                 else MainAxisAlignment.START)

        self.value: Container = Container(bgcolor= fgcolor, width= S_val,
                                          border_radius= radius, 
                                          height= height)
        self.cont = Container(bgcolor= Colors.with_opacity(lp, tp)
                                 , width= width, 
                                 height= height, border_radius= radius,
                                 margin= margin.only(right= 20) if not tight else None,
                                 content=Row([self.value], # expand
                                    alignment= align))
        
        self.content = self.cont
    
    # on_new_value
    @property
    def on_new_value(self):
        return self.__on_new_value

    @on_new_value.setter
    def on_new_value(self, handler:int):
        if isinstance(handler, int):
            if handler > 100:
                handler = 100
            self.value.width = handler* self.percent
            if handler < 0: self.value.width  = 0
        self.update()

