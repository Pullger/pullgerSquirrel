class _connectors():
    @property
    def chrome(self):
        from . import chrome
        return chrome.connectorChrome

connector = _connectors()