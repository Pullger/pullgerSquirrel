class _ConnectorsChrome:
    @property
    def headless(self):
        from . import hedless
        return hedless.SeleniumChromeHeadless()

    @property
    def standard(self):
        from . import standard
        return standard.SeleniumChromeStandard()


connectorChrome = _ConnectorsChrome()
