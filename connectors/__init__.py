from pullgerExceptions import pullgerSquirrel as exceptions


class _Connector():
    @property
    def selenium(self):
        from . import selenium
        return selenium.connector


connector = _Connector()


def get_by_name(conn: str, **kwargs):
    responseConnector = None

    if type(conn) == str:
        connEl = conn.split('.')
    else:
        raise exceptions.IncorrectParameter(
            f'Incorrect parameter [connector] expect "string".',
            level=30
        )

    if len(connEl) != 0:
        def get_element(connEl, index):
            try:
                return connEl[index]
            except BaseException as e:
                raise exceptions.IncorrectParameter(
                    f'Incorrect format {connEl.join(".")} required element with index {index}.',
                    level=30
                )

        if connEl[0] == 'selenium':
            element = get_element(connEl, 1)

            if element == 'chrome':
                element = get_element(connEl, 2)

                if element == 'standard':
                    responseConnector = _Connector().selenium.chrome.standard
                elif element == 'headless':
                    responseConnector = _Connector().selenium.chrome.headless
                else:
                    raise exceptions.IncorrectParameter(
                        f'Connector element {element} does not supported.',
                        level=30
                    )
            else:
                raise exceptions.IncorrectParameter(
                    f'Connector element {element} does not supported.',
                    level=30
                )
        else:
            raise exceptions.IncorrectParameter(
                f'Connector {connEl[0]} does not exist',
                level=30
            )
    else:
        raise exceptions.InterfaceData(
            f"Incorrect connector format name {conn}",
            level=40
        )

    if responseConnector is not None:
        return responseConnector
    else:
        raise exceptions.InternalAlgoritmError(
            f'Unexpected variable value',
            level=50
        )
