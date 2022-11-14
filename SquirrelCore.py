import time
import inspect
import uuid

# from .SquirrelConnectors import Connectors
from . import connectors
from .connectors.selenium import connector

# from pullgerLogin.pullgerSquirrel import logger
from pullgerInternalControl import pIC_pS
from pullgerInternalControl.pullgerSquirrel.logging import logger


class Squirrel(object):
    __slots__ = (
        '_connector',
        '_connectorMode',
        '_libraries',
        '_current_url',
        '_initialized',
        '_auto_elements'
    )

    class _Libraries:
        __slots__ = ('_driver', '_keyboard', '_implementation')

        @property
        def driver(self, **kwargs):
            return self._driver

        @property
        def keyboard(self, **kwargs):
            return self._keyboard

        @property
        def implementation(self, **kwargs):
            return self._implementation

        def __init__(self, driver, keyboard, implementation, **kwargs):
            self._driver = driver
            self._keyboard = keyboard
            self._implementation = implementation

    @property
    def connector(self, **kwargs):
        return self._connector

    @property
    def libraries(self, **kwargs):
        return self._libraries

    @property
    def current_url(self, **kwargs):
        self._current_url = self.connector.get_current_url(squirrel=self)
        return self._current_url

    @property
    def initialized(self, **kwargs):
        return self._initialized

    class AutoElements:
        __slots__ = ('squirrel', '_elements_list', '_current_url')

        class AutoElement:
            __slots__ = ('uuid_auto_element', 'web_element', 'html_element')

            def __init__(self, web_element, **kwargs):
                self.web_element = web_element
                self.html_element = web_element.get_attribute("outerHTML")
                self.uuid_auto_element = uuid.uuid4()

        def __init__(self, squirrel, **kwargs):
            self.squirrel = squirrel
            self._elements_list = None
            self._current_url = None

        def elements_scan(self, **kwargs):
            self._current_url = self.squirrel.current_url
            self._elements_list = {}

            list_search_elements = ['body', 'input', 'button', 'c-wiz']

            for search_elem in list_search_elements:
                input_elements = self.squirrel.finds_xpath(f"//{search_elem}")
                count = 0
                for cur_elem in input_elements:
                    auto_elem = self.AutoElement(cur_elem)
                    self._elements_list.update({str(auto_elem.uuid_auto_element): auto_elem})
                    count += 1

            return count

        def elements_list(self, **kwargs):
            if self._current_url != self.squirrel.current_url \
                    or self._elements_list is None:
                self.elements_scan()

            return_list = []
            for cur_element in self._elements_list.keys():
                return_list.append({
                    "uuid_auto_element": str(self._elements_list[cur_element].uuid_auto_element),
                    "html_element": self._elements_list[cur_element].html_element
                })

            return return_list

        def elements_get(self, uuid_auto_element: str = None, **kwargs):

            if uuid_auto_element in self._elements_list:
                return self._elements_list[uuid_auto_element].web_element
            else:
                raise pIC_pS.InterfaceData(
                    f'Does not exist auto element uuid [{uuid_auto_element}]',
                    level=30
                )

    def __init__(self, conn: connector = None, **kwargs):
        self._connector = None
        self._libraries = None
        self._current_url = False
        self._initialized = False
        self._auto_elements = self.AutoElements(squirrel=self)

        if conn is not None:
            self._connector = conn
        else:
            raise pIC_pS.InterfaceData(
                f'Incorrect connector DATA: need one off pullgerSquirrel.connectors classes',
                level=30
            )

    def initialize(self, **kwargs):
        self._libraries = self._Libraries(
            keyboard=self._connector.get_keyboard_library(),
            implementation=self._connector.get_implementation_library(),
            driver=self._connector.get_driver_library()
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
            self.connector.get_page(squirrel=self, url=url, **kwargs)
            # if result is True:
            self._current_url = self.connector.get_current_url(squirrel=self, **kwargs)
            pass
            # else:
            #     self._current_url = None
            #     raise pIC_pS.ErrorOnLoadPage(
            #         message='Incorrect loading page.',
            #         level=40
            #     )
        else:
            raise pIC_pS.InterfaceData(
                message='Incorrect call getPage in squirrel (url is mandatory k kwarg)',
                level=30
            )

    def get_html(self, **kwargs):
        return self._connector.get_html(squirrel=self, **kwargs)

    def elements_scan(self, **kwargs):
        return self._auto_elements.elements_scan(**kwargs)

    def elements_list(self, **kwargs):
        return self._auto_elements.elements_list(**kwargs)

    def elements_get(self, uuid_auto_element: str = None, **kwargs):
        return self._auto_elements.elements_get(uuid_auto_element, **kwargs)

    def update_url(self, **kwargs):
        self._current_url = self.driver.current_url

    def close(self, **kwargs):
        return self._connector.close(squirrel=self, **kwargs)

    def find_xpath(self, xpath: str, log_error: bool = False, do_not_log: bool = True, **kwargs):
        return self._connector.find_element_xpath(
            squirrel=self,
            xpath=xpath,
            log_error=log_error,
            do_not_log=do_not_log,
            **kwargs
        )

    def finds_xpath(self, xpath: str, **kwargs):
        return self._connector.finds_element_xpath(
            squirrel=self,
            xpath=xpath,
            **kwargs
        )

    def send_end(self, **kwargs):
        self.connector.send_end(squirrel=self, **kwargs)

    def send_page_down(self, **kwargs):
        self.connector.send_page_down(squirrel=self, **kwargs)

    def send_tab(self, **kwargs):
        self.connector.send_tab(squirrel=self, **kwargs)

    def send_space(self, **kwargs):
        self.connector.send_space(squirrel=self, **kwargs)

    def send_enter(self, **kwargs):
        self.connector.send_enter(squirrel=self, **kwargs)


class WebElements:
    __slots__ = (
        '_squirrel',
        '_web_element',
        '_text'
    )

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

    def send_enter(self):
        return self.squirrel.connector.send_enter(
            squirrel=self._squirrel,
            web_element=self._web_element
        )

    def click(self):
        return self.squirrel.connector.click(web_element=self._web_element)


class Session(object):
    __slots__ = ('uuid_session', 'connector', 'squirrel', 'domain',
                 'account', 'authorization', 'active', 'in_use',
                 'initialized', 'ready', 'live')

    def __str__(self):
        return self.uuid_session

    def __init__(self, conn=None, squirrel=None, domain=None,
                 account=None, authorization=None, active: bool = True, in_use: bool = False,
                 initialized: bool = False, ready: bool = False, live: bool = True):

        if squirrel is None:
            squirrel = Squirrel(conn=conn)
            squirrel.initialize()

        if authorization is not None:
            domain_class = authorization.get_domain()
            domain = domain_class(squirrel)

            if domain.initialized is not True:
                pIC_pS.DomainInitialization(
                    msg=f"Unexpected status initialize domain [{str(domain)}]",
                    level=50
                )

        self.uuid_session = str(uuid.uuid4())
        self.connector = conn
        self.squirrel = squirrel
        self.domain = domain
        self.account = account
        self.authorization = authorization
        self.active = active
        self.in_use = in_use
        self.initialized = initialized
        self.ready = ready
        self.live = live

    @property
    def structure(self):
        return {
            'uuid': str(self.uuid_session),
            'uuid_session': str(self.uuid_session),
            'connector': self.connector,
            'authorization': self.authorization,
            'used_account': False if self.account is None else True,
            'active': self.active,
            'in_use': self.in_use,
            'ready': self.ready,
            'live': self.live,
        }

    def get_page(self, **kwargs):
        return self.squirrel.get_page(**kwargs)

    def get_html(self, **kwargs):
        return self.squirrel.get_html(**kwargs)

    def elements_scan(self, **kwargs):
        return self.squirrel.elements_scan(**kwargs)

    def elements_list(self, **kwargs):
        return self.squirrel.elements_list(**kwargs)

    def elements_get(self, **kwargs):
        return self.squirrel.elements_get(**kwargs)

    def update_url(self, **kwargs):
        return self.squirrel.update_url(**kwargs)

    def close(self, **kwargs):
        return self.squirrel.close(**kwargs)

    def find_xpath(self, **kwargs):
        return self.squirrel.find_xpath(**kwargs)

    def finds_xpath(self, **kwargs):
        return self.squirrel.finds_xpath(**kwargs)

    def send_end(self, **kwargs):
        return self.squirrel.send_end(**kwargs)

    def send_page_down(self, **kwargs):
        return self.squirrel.send_end(**kwargs)

    def send_tab(self, **kwargs):
        return self.squirrel.send_end(**kwargs)

    def send_space(self, **kwargs):
        return self.squirrel.send_end(**kwargs)

    def send_enter(self, **kwargs):
        return self.squirrel.send_end(**kwargs)
