import time
import inspect
from pullgerExceptions import pullgerSquirrel as exceptions
# from .SquirrelConnectors import Connectors
from . import connectors
from .connectors.selenium import connector
from pullgerLogin.pullgerSquirrel import logger


class Squirrel(object):
    __slots__ = (
        '_connector',
        '_connectorMode',
        '_libraries',
        '_current_url',
        '_initialized'
    )

    class _Libraries:
        __slots__ = ('_driver', '_keyboard', '_implementation')

        @property
        def driver(self):
            return self._driver

        @property
        def keyboard(self):
            return self._keyboard

        @property
        def implementation(self):
            return self._implementation

        def __init__(self, driver, keyboard, implementation, **kwargs):
            self._driver = driver
            self._keyboard = keyboard
            self._implementation = implementation

    @property
    @staticmethod
    def VERSION():
        return (1, 0, 1, 0)
        # versions history
        # 1.0.1.0 adaptation raise exeptatation fore new version of exceptation module

    @property
    @staticmethod
    def VERSION_INFO():
        return '.'.join(str(nv) for nv in Squirrel.VERSION)

    @property
    def __version__(self):
        return self.VERSION_INFO

    @property
    def connector(self):
        return self._connector

    @property
    def libraries(self):
        return self._libraries

    @property
    def current_url(self):
        return self._current_url

    @property
    def initialized(self):
        return self._initialized

    def __init__(self, conn: connector = None, **kwargs):
        self._connector = None
        self._libraries = None
        self._current_url = False
        self._initialized = False

        if conn is not None:
            self._connector = conn
        else:
            raise exceptions.InterfaceData(
                f'Incorrect connector DATA: need one off pullgerSquirrel.connectors classes',
                level=30
            )

    def initialize(self):
        self._libraries = self._Libraries(
            keyboard=self._connector.getKeyboardLibrary(),
            implementation=self._connector.getImplementationLibrary(),
            driver=self._connector.getDriverLibrary()
        )

        self._initialized = True

    def get(self, url=None, **kwargs):
        """
        Procedure for compatibility with Selenium
        """
        return self.get_page(url, **kwargs)

    def get_page(self, url: str = None, **kwargs):
        """
        Loads a web page in current connector

        :kwag param url:
        :kwag param timeout:
        :kwag param xpath:
        :kwag param readyState:
        :return: no return
        """
        if url is not None:
            result = self.connector.get_page(squirrel=self, url=url, **kwargs)
            if result is True:
                self._current_url = self.connector.get_current_url(squirrel=self)
            else:
                self._current_url = None
                raise exceptions.ErrorOnLoadPage(
                    message='Incorrect loading page.',
                    level=40
                )
        else:
            raise exceptions.InterfaceData(
                message='Incorrect call getPage in squirrel (url is mandatory k kwarg)',
                level=30
            )

    def get_html(self,**kwargs):
        return self._connector.get_html(squirrel=self)

    def update_url(self):
        self._current_url = self.driver.current_url

    def close(self):
        return self._connector.close(squirrel=self)

    def find_xpath(self, xpath: str, log_error: bool = False, do_not_log: bool = True):

        return self._connector.find_element_xpath(
            squirrel=self,
            xpath=xpath,
            log_error=log_error,
            do_not_log=do_not_log
        )

    def finds_xpath(self, xpath: str):

        return self._connector.finds_element_xpath(
            squirrel=self,
            xpath=xpath
        )

    def send_end(self):
        self.connector.send_end(squirrel=self)
        return True

    def send_page_down(self):
        self.connector.send_page_down(squirrel=self)
        return True

    def send_TAB(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.TAB)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button TAB on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )

        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_SPACE(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.SPACE)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button SPACE on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_ENTER(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.ENTER)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button ENTER on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )


class WebElements:
    __slots__ = (
        '_squirrel',
        '_web_element',
        '_text'
    )

    @property
    @staticmethod
    def VERSION():
        return 1, 0, 1, 0

    @property
    @staticmethod
    def VERSION_INFO():
        return '.'.join(str(nv) for nv in Squirrel.VERSION)

    @property
    def __version__(self):
        return self.VERSION_INFO

    @property
    def squirrel(self):
        return self._squirrel

    @property
    def web_element(self):
        return self._web_element

    def __init__(self, squirrel: Squirrel, web_element):
        self._squirrel = squirrel
        self._web_element = web_element

    @property
    def text(self):
        return self._squirrel.connector.text(
            web_element=self._web_element
        )

    @property
    def tag_name(self):
        return self._squirrel.connector.tag_name(
            web_element=self._web_element
        )

    def get_attribute(self, name: str):
        return self._squirrel.connector.get_attribute(
            web_element=self._web_element,
            name=name
        )

        # if self._connector == Connectors.selenium:
        #     return self._web_element.get_attribute(inAttribute)
        # else:
        #     raise exceptions.InternalData(
        #         f"Unknown connector.",
        #         level=40
        #     )

    def find_xpath(self, xpath: str, log_error: bool = False, do_not_log: bool = True):

        return self._squirrel.connector.find_element_xpath(
            squirrel=self._squirrel,
            web_element=self._web_element,
            xpath=xpath,
            log_error=log_error,
            do_not_log=do_not_log
        )
    
    def finds_xpath(self, xpath: str):

        return self._squirrel.connector.finds_element_xpath(
            squirrel=self._squirrel,
            web_element=self._web_element,
            xpath=xpath)

    def send_string(self, string: str):
        return self.squirrel.connector.send_string(web_element=self.web_element, string=string)

    def click(self):
        return self.squirrel.connector.click(web_element=self.web_element)
