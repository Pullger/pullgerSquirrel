class _connectors():
    @property
    def chrome(self):
        from . import chrome
        return chrome.connectorChrome

    @property
    def stand_alone(self):
        from . import stand_alone
        return stand_alone.connectorChrome


connector = _connectors()
