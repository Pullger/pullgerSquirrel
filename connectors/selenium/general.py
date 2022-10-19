import time
import abc
from pullgerSquirrel.SquirrelCore import WebElements, Squirrel

from pullgerInternalControl import pIC_pS
from pullgerInternalControl.pullgerSquirrel.connectors.selenium.logging import logger


class SeleniumConnector:
    __slots__ = ()

    @abc.abstractmethod
    def getDriverLibrary(self):
        pass

    def getKeyboardLibrary(self):
        from selenium.webdriver.common.keys import Keys
        return Keys

    def getImplementationLibrary(self):
        from selenium.webdriver.common.by import By
        return By

    def get_page(self, squirrel, url: str, timeout: int = None, xpath: str = None, ready_state=None, **kwargs):
        """
        Open url in current browser

        :param squirrel:
        :param url:
        :param timeout:
        :param xpath:
        :param ready_state:
        :param kwargs:
        :return:
        """

        driver = squirrel.libraries.driver

        try:
            time.sleep(1)
            if url.find('"') == -1:
                sHooks = '"'
            else:
                sHooks = "'"

            loading_url = f"window.location.href={sHooks}{url}{sHooks}"

            driver.execute_script(loading_url)
            time.sleep(3)
        except BaseException as e:
            raise pIC_pS.connectors.selenium.GetPage(
                f'Exception on load: [{loading_url}]. Discription:',
                level=50,
                exception=e
            )

        # Wait for render page with timing out
        if timeout is None:
            timeout = 5;
        isRendered = False
        circleCalc = 0

        if ready_state is not None:
            time.sleep(1)
            try:
                curState = driver.execute_script('return document.readyState');

                while isRendered is False and (circleCalc < timeout or isRendered is True):
                    if ready_state == curState:
                        isRendered = True

                    if isRendered is False:
                        time.sleep(1)
                    circleCalc += 1

                result = isRendered
            except BaseException as e:
                result = True

        elif xpath is not None:
            while isRendered is False and (circleCalc < timeout or isRendered is True):
                CheckBlock = self.find_element_xpath(squirrel=squirrel, xpath=xpath)
                if CheckBlock is not None:
                    isRendered = True
                if isRendered is False:
                    time.sleep(1)
                circleCalc += 1

            result = isRendered
        else:
            result = True

        return result

    @staticmethod
    def get_current_url(squirrel, **kwargs):
        """
        Return full current URL in connector.

        :param squirrel:
        :param kwargs:
        :return: str
        """

        driver = squirrel.libraries.driver

        try:
            time.sleep(5)  # Wait for rendering
            currentURL = driver.current_url
        except BaseException as e:
            logger.error(msg=f"Error on get url ('current_url') description: {str(e)}")
            time.sleep(25)  # More wait for rendering
            currentURL = driver.current_url

        return currentURL

    @staticmethod
    def get_html(squirrel, **kwargs):
        driver = squirrel.libraries.driver

        try:
            page_source = driver.page_source
        except BaseException as e:
            raise pIC_pS.connectors.selenium.General(
                msg=f'Exception on getting page source. Function (get_html)',
                level=50,
                exception=e
            )

        return page_source

    @staticmethod
    def send_page_down(squirrel: Squirrel, **kwargs):
        """
        Send push key event on current page.

        :param squirrel:
        :param kwargs:
        :return: None
        """

        driver = squirrel.libraries.driver
        implementation = squirrel.libraries.implementation
        keyboard = squirrel.libraries.keyboard

        webElementBody = driver.find_element(implementation.XPATH, "//body")
        if webElementBody is not None:
            try:
                webElementBody.send_keys(keyboard.PAGE_DOWN)
            except BaseException as e:
                raise pIC_pS.connectors.selenium.PageOperation(
                    msg="Error on sending keyboad event PAGE_DOWN. Function: send_page_down.",
                    level=50,
                    exception=e
                )
        else:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Incorrect page HTML structure (no body).",
                level=50,
            )

    @staticmethod
    def send_tab(squirrel: Squirrel, **kwargs):
        """
        Send push key event on current page.

        :param squirrel:
        :param kwargs:
        :return: None
        """

        driver = squirrel.libraries.driver
        implementation = squirrel.libraries.implementation
        keyboard = squirrel.libraries.keyboard

        webElementBody = driver.find_element(implementation.XPATH, "//body")
        if webElementBody is not None:
            try:
                webElementBody.send_keys(keyboard.TAB)
            except BaseException as e:
                raise pIC_pS.connectors.selenium.PageOperation(
                    msg="Error on sending keyboad event TAB.",
                    level=50,
                    exception=e
                )
        else:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Incorrect page HTML structure (no body).",
                level=50,
            )

    @staticmethod
    def send_space(squirrel: Squirrel, **kwargs):
        """
        Send push key event on current page.

        :param squirrel:
        :param kwargs:
        :return: None
        """

        driver = squirrel.libraries.driver
        implementation = squirrel.libraries.implementation
        keyboard = squirrel.libraries.keyboard

        webElementBody = driver.find_element(implementation.XPATH, "//body")
        if webElementBody is not None:
            try:
                webElementBody.send_keys(keyboard.SPACE)
            except BaseException as e:
                raise pIC_pS.connectors.selenium.PageOperation(
                    msg="Error on sending keyboad event SPACE.",
                    level=50,
                    exception=e
                )
        else:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Incorrect page HTML structure (no body).",
                level=50,
            )

    @staticmethod
    def send_enter(squirrel: Squirrel = None, web_element=None, **kwargs):
        """
        Send push key event on current page.

        :param web_element:
        :param squirrel:
        :param kwargs:
        :return: None
        """

        driver = squirrel.libraries.driver
        implementation = squirrel.libraries.implementation
        keyboard = squirrel.libraries.keyboard

        if web_element is None:
            try:
                inst = driver.find_element(implementation.XPATH, "//body")
            except BaseException as e:
                raise pIC_pS.connectors.selenium.General(
                    msg="Cant find BODY on page",
                    level=50,
                    exception=e
                )
        else:
            inst = web_element

        try:
            inst.send_keys(keyboard.ENTER)
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on sending keyboad event ENTER.",
                level=50,
                exception=e
            )

    @staticmethod
    def send_end(squirrel: Squirrel, **kwargs):
        """
        Send push key (END) event on current page.

        :param squirrel:
        :param kwargs:
        :return: None or raise the exception
        """

        driver = squirrel.libraries.driver
        implementation = squirrel.libraries.implementation
        keyboard = squirrel.libraries.keyboard

        web_element_body = driver.find_element(implementation.XPATH, "//body")
        if web_element_body is not None:
            try:
                web_element_body.send_keys(keyboard.END)
            except BaseException as e:
                raise pIC_pS.connectors.selenium.PageOperation(
                    msg="Error on sending keyboad event PAGE_DOWN. Function: send_page_down.",
                    level=50,
                    exception=e
                )
        else:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Incorrect page HTML structure (no body).",
            )

    @staticmethod
    def send_string(web_element, string: str):
        try:
            web_element.send_keys(string)
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on sending keyboad event (character set). Function: send_string.",
                level=50,
                exception=e
            )

    @staticmethod
    def click(web_element):
        try:
            web_element.click()
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on sending mouse click event. Function: click.",
                level=50,
                exception=e
            )

    @staticmethod
    def find_element_xpath(squirrel: Squirrel = None, web_element=None, xpath: str = "", log_error: bool = False, do_not_log: bool = True, **kwargs):
        """
        :param squirrel:
        :param web_element:
        :param xpath:
        :param log_error:
        :param do_not_log:
        :param kwargs:
        :return: class:pullgerSquirrel.WebElement
        """
        try:
            if web_element is None:
                inst = squirrel.libraries.driver
            else:
                inst = web_element

            implementation = squirrel.libraries.implementation
            result = None
            try:
                fEl = inst.find_element(by=implementation.XPATH, value=xpath)
                result = WebElements(squirrel=squirrel, web_element=fEl)
            except BaseException as e:
                if log_error is True or do_not_log is False:
                    inf = f'Error on finding {xpath} on page {squirrel.current_url}. \
                        Function: (find_element_xpath).  Internal description: {str(e)}'
                    logger.info(inf)
        except BaseException as e:
            raise pIC_pS.connectors.selenium.General(
                msg="Error on executing code in find_element_xpath.",
                level=50,
                exception=e
            )
        return result

    @staticmethod
    def finds_element_xpath(squirrel: Squirrel, web_element=None, xpath: str = "", **kwargs):
        """

        :param squirrel:
        :param web_element: 
        :param xpath:
        :param kwargs:
        :return: list[class:pullgerSquirrel.WebElement]
        """
        try:
            if web_element is None:
                inst = squirrel.libraries.driver
            else:
                inst = web_element

            implementation = squirrel.libraries.implementation

            result = []

            try:
                elements_list = inst.find_elements(implementation.XPATH, xpath)
            except BaseException as e:
                raise pIC_pS.connectors.selenium.General(
                    msg="Error on find element on the page by XPATH. Function: finds_element_xpath.",
                    level=50,
                    exception=e
                )

            for el in elements_list:
                result.append(WebElements(squirrel=squirrel, web_element=el))
        except BaseException as e:
            raise pIC_pS.connectors.selenium.General(
                msg="Error on executing code in finds_element_xpath.",
                level=50,
                exception=e
            )

        return result

    @staticmethod
    def text(web_element):
        try:
            result = web_element.text
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on getting text. Function: text.",
                level=50,
                exception=e
            )
        return result

    @staticmethod
    def tag_name(web_element):
        try:
            result = web_element.tag_name
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on getting tag name. Function: tag_name.",
                level=50,
                exception=e
            )
        return result

    @staticmethod
    def get_attribute(web_element, name: str):
        try:
            result = web_element.get_attribute(name)
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on getting value of attribute. Function: get_attribute.",
                level=50,
                exception=e
            )
        return result


    @staticmethod
    def close(squirrel: Squirrel, **kwargs):
        try:
            driver = squirrel.libraries.driver
            # driver.close()
            driver.quit()
        except BaseException as e:
            raise pIC_pS.connectors.selenium.PageOperation(
                msg="Error on closing selenium. Function: close.",
                level=50,
                exception=e
            )




