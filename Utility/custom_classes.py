class overlay:
    def __init__(self, page) -> None:
        self.page = page
        self._data = self.clean(page)
        for key, value in self._data.items():
            setattr(self, key, value)
    
    def __getitem__(self, key):
        # Accessing an item, move key to the top of the sequence
        value = self._data[key]
        return value
    
    def __getattr__(self, name):
        # Implementing dot notation for getting attributes
        try:
            return getattr(self._data, name)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __repr__(self) -> str:
        source = ', '.join(f"{value.__repr__().lower()}" for value in self._data.values())
        return f"OverLays({{{source}}})"
    
    def _keys(self):
        return list(self._data.keys())

    @staticmethod
    def _key_formater(key):
        return key.__repr__().split('(')[0].lower()

    @staticmethod
    def clean(page):
        _data = {overlay._key_formater(i): i for i in page.overlay.copy()}
        page.overlay.clear()
        page.overlay.extend(list(_data.values()))
        return _data

    def snackbarmessage(self, mess):
        if 'snackbar' in self._keys():
            self.snackbar.content.value = mess
            self.snackbar.open = True
            self.page.update()
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute, snackbar add in the begining")
