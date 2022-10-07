class _connectorsUndetectedChrome():
    @property
    def headless(self):
        from . import hedless
        return hedless.seleniumChromeUndetectedHeadless()

    @property
    def standard(self):
        from . import standard
        return standard.seleniumChromeUndetectedStandard()

connector_chrome_undetected = _connectorsUndetectedChrome()