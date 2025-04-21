import pytest
import winsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.chrome.service import Service
from pages.contact_page.contact_page import ContactPage
from pages.tensor_page.tensor_page import TensorPage
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session", autouse=True)
def play_sound_after_tests():
    yield
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    # winsound.Beep(1000, 500)


@pytest.fixture(scope="function")
def driver(request):
    # Создаем объект опций для Chrome
    chrome_options = Options()

    # Проверяем, есть ли параметр командной строки для запуска в headless режиме
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")  # Включаем безголовый режим
        chrome_options.add_argument("--disable-gpu")  # Отключаем GPU, может быть необходимо для некоторых систем
        chrome_options.add_argument("--window-size=1600,900")  # Устанавливаем размер окна

    # Инициализируем драйвер с помощью webdriver-manager
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    sleep(3)

    try:
        yield chrome_driver
    finally:
        chrome_driver.quit()  # Закрываем драйвер после завершения теста


# Добавляем опцию командной строки для headless режима
def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")


@pytest.fixture()
def contact_page(driver):
    return ContactPage(driver)


@pytest.fixture()
def tensor_page(driver):
    return TensorPage(driver)
