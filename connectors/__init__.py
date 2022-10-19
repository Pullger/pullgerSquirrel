from pullgerInternalControl import pIC_pS


class _Connector:
    @property
    def selenium(self):
        from . import selenium
        return selenium.connector


connector = _Connector()


def get_by_name(conn: str, **kwargs):
    responseConnector = None

    if type(conn) == str:
        conn_el = conn.split('.')
    else:
        raise pIC_pS.InterfaceData(
            msg=f'Incorrect parameter [{conn}] expect "string".',
            level=30
        )

    if len(conn_el) != 0:
        def get_element(in_conn_el, index):
            try:
                return in_conn_el[index]
            except BaseException as e:
                raise pIC_pS.InterfaceData(
                    f'Incorrect format {in_conn_el.join(".")} required element with index {index}.',
                    level=30
                )

        if conn_el[0] == 'selenium':
            element = get_element(conn_el, 1)

            if element == 'chrome':
                element = get_element(conn_el, 2)

                if element == 'standard':
                    responseConnector = _Connector().selenium.chrome.standard
                elif element == 'headless':
                    responseConnector = _Connector().selenium.chrome.headless
                else:
                    raise pIC_pS.InterfaceData(
                        f'Connector element {element} does not supported.',
                        level=30
                    )
            elif element == 'stand_alone':
                element = get_element(conn_el, 2)

                if element == 'general':
                    responseConnector = _Connector().selenium.stand_alone.general
                else:
                    raise pIC_pS.InterfaceData(
                        f'Connector element {element} does not supported.',
                        level=30
                    )
            else:
                raise pIC_pS.InterfaceData(
                    f'Connector element {element} does not supported.',
                    level=30
                )
        else:
            raise pIC_pS.InterfaceData(
                f'Connector {conn_el[0]} does not exist',
                level=30
            )
    else:
        raise pIC_pS.InterfaceData(
            f"Incorrect connector format name {conn}",
            level=40
        )

    if responseConnector is not None:
        return responseConnector
    else:
        raise pIC_pS.InternalError(
            f'Unexpected variable value',
            level=50
        )
