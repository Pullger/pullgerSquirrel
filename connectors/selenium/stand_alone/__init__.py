class _ConnectorsChrome:
    @property
    def general(self):
        from . import general
        return general.SeleniumStandAlone()


connectorChrome = _ConnectorsChrome()
