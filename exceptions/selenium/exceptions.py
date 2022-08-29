from ..exceptions import General as RootGeneral

class General(RootGeneral):
    def __init__(self, message, **kwargs):
        from pullgerSquirrel.exceptions import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('selenium', kwargs)

        super().__init__(message, **kwargs)

class GetPage(General):
    def __init__(self, message, **kwargs):
        from pullgerSquirrel.exceptions import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('GetPage', kwargs)
        super().__init__(message, **kwargs)

class PageOperation(General):
    def __init__(self, message, **kwargs):
        from pullgerSquirrel.exceptions import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('PageOperation', kwargs)
        super().__init__(message, **kwargs)

class FindElements(General):
    def __init__(self, message, **kwargs):
        from pullgerSquirrel.exceptions import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('PageOperation', kwargs)
        super().__init__(message, **kwargs)