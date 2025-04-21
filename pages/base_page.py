import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import allure

logging.basicConfig(
    filename='test_execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class BasePage:
    base_url = 'https://sbis.ru/'
    page_url = None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        driver.maximize_window()
        self.wait = WebDriverWait(driver, 30)  # Добавляем ожидание

    def open_page(self):
        logging.info("Open SBIS")
        self.driver.get("https://sbis.ru/")

    def find(self, locator: tuple):
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            logging.error(f"Element with locator {locator} not found.")
            return None

    def find_all(self, locator: tuple):
        return self.driver.find_elements(*locator)

    def send_keys(self, locator: tuple, text: str):
        try:
            self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)
        except TimeoutException:
            logging.error(f"Element with locator {locator} not visible.")

    def click(self, locator: tuple):
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException:
            logging.error(f"Element with locator {locator} not clickable.")

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def scroll_to_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def scroll_by(self, pixels: int):
        """Прокрутка страницы на заданное количество пикселей."""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def scroll_to_top(self):
        """Прокрутка страницы вверх до самого верха."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_down(self, scroll_pause_time=2):
        """Прокрутка страницы вниз до самого низа."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Прокрутка вниз
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ждем, чтобы страница загрузилась
            time.sleep(scroll_pause_time)

            # Получаем новую высоту страницы после прокрутки
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # Если высота не изменилась, значит достигли низа страницы
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_in_modal(self, modal_locator: tuple):
        """Прокрутка внутри всплывающего окна."""
        modal_window = self.wait.until(EC.visibility_of_element_located(modal_locator))
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_window)

    def scroll_in_modal_by(self, modal_locator: tuple, pixels: int):
        """Прокрутка внутри всплывающего окна на заданное количество пикселей."""
        modal_window = self.wait.until(EC.visibility_of_element_located(modal_locator))
        self.driver.execute_script(f"arguments[0].scrollTop += {pixels};", modal_window)

    def close_driver(self):
        self.driver.quit()

    def check_expected_url(self, expected_url):
        """
        Проверяет, что текущий URL соответствует ожидаемому.
        :param expected_url: Ожидаемый URL.
        """
        current_url = self.driver.current_url
        assert current_url == expected_url, \
            f"Текущий URL не соответствует ожидаемому. Ожидалось: '{expected_url}', Фактически: '{current_url}'"

    def take_screenshot(self):
        screenshot_path = "screenshot.png"
        self.driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)

    def wait_for_element_visibility(self, locator: tuple, timeout: int = 30):
        """Ожидает появления элемента на странице."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logging.error(f"Element with locator {locator} not visible after {timeout} seconds.")
            return None

    def wait_for_element_presence(self, locator: tuple, timeout: int = 30):
        """Ожидает присутствия элемента на странице."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logging.error(f"Element with locator {locator} not present after {timeout} seconds.")
            return None

    def wait_clickable(self, locator: tuple, timeout: int = 30):
        """Ожидает, пока элемент не станет кликабельным."""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logging.error(f"Element with locator {locator} not clickable after {timeout} seconds.")
            return None

    def wait_for_elements(self, locator: tuple, timeout: int = 30):
        """Ожидает появления всех элементов на странице."""
        try:
            return self.wait.until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            logging.error(f"Elements with locator {locator} not visible after {timeout} seconds.")
            return []

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 30):
        """Ожидает исчезновения элемента со страницы."""
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logging.error(f"Element with locator {locator} still visible after {timeout} seconds.")
            return False

    @allure.step("Сравнение текста элемента с ожидаемым текстом")
    def compare_text(self, locator, expected_text):
        # Ожидание появления элемента и получение его текста
        actual_text = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(locator)
        ).text

        assert actual_text == expected_text, f"Текст не совпадает. Ожидаемый: {expected_text}, Фактический: {actual_text}"
        allure.attach(f"Ожидаемый текст: {expected_text}\nФактический текст: {actual_text}", name="Сравнение текста",
                      attachment_type=allure.attachment_type.TEXT)
