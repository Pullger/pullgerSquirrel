from ..exceptions import General as seleniumGeneral

class General(seleniumGeneral):
    def __init__(self, message, **kwargs):
        from pullgerSquirrel.exceptions import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('chrome', kwargs)

        super().__init__(message, **kwargs)