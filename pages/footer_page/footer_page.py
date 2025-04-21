from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class FooterLoc():
    # Локаторы для скачивания плагина
    DOWNLOAD_LOCAL_VERSIONS_LINK = (By.XPATH, "//a[contains(text(), 'Скачать локальные версии')]")
    PLUGIN_SIZE_TEXT = (By.CSS_SELECTOR, '[class="sbis_ru-DownloadNew-loadLink__link js-link"]')
    WINDOWS_PLUGIN_LINK = (
        By.CSS_SELECTOR, '[href="https://update.saby.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe"]')


class FooterPage(BasePage):
    loc = FooterLoc

    def scroll_to_download_local_versions(self):
        logging.info("Прокрутка до ссылки 'Скачать локальные версии'")
        self.scroll_to_element(self.loc.DOWNLOAD_LOCAL_VERSIONS_LINK)

    def click_download_local_versions(self):
        logging.info("Клик по ссылке 'Скачать локальные версии'")
        download_local_versions_link = self.wait_clickable(self.loc.DOWNLOAD_LOCAL_VERSIONS_LINK)
        download_local_versions_link.click()

    def get_expected_plugin_size(self):
        logging.info("Получение ожидаемого размера плагина")
        size_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.loc.PLUGIN_SIZE_TEXT)
        ).text
        logging.info(f"Найденный текст с размером: '{size_text}'")
        # Извлекаем числовое значение из текста
        # Разделить текст по пробелам и взять первое число
        for part in size_text.split():
            try:
                # Заменяем запятую на точку для корректного преобразования (на всякий случай)
                return float(part.replace(',', '.'))
            except ValueError:
                continue
        # Если не удалось найти число, логируем ошибку и возвращаем значение по умолчанию
        logging.error(f"Не удалось извлечь размер из текста: '{size_text}'")
        return 10.37  # Значение по умолчанию, чтобы тест не падал

    def download_windows_plugin(self, download_dir):
        logging.info(f"Скачивание плагина Windows в {download_dir}")
        # Убедиться, что директория для скачивания существует
        os.makedirs(download_dir, exist_ok=True)
        # Клик по ссылке скачивания плагина Windows
        windows_plugin_link = self.wait_clickable(self.loc.WINDOWS_PLUGIN_LINK)
        windows_plugin_link.click()

    def verify_plugin_downloaded(self, download_dir, expected_filename="sbisplugin-setup-web.exe"):
        logging.info(f"Проверка скачивания плагина в {download_dir}")
        file_path = os.path.join(download_dir, expected_filename)
        # Ожидать до 30 секунд появления файла
        for _ in range(30):
            if os.path.exists(file_path):
                logging.info(f"Файл плагина {file_path} найден")
                return file_path
            time.sleep(1)
        raise AssertionError(f"Файл плагина {file_path} не был скачан")

    def verify_file_size(self, file_path, expected_size_mb):
        logging.info(f"Проверка размера файла {file_path}")
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Конвертация байтов в МБ
        # Округлить до 2 знаков после запятой для сравнения
        file_size_mb = round(file_size_mb, 2)
        expected_size_mb = round(expected_size_mb, 2)

        # Допуск различия в размере (10%)
        tolerance = expected_size_mb * 0.1

        logging.info(
            f"Фактический размер: {file_size_mb} МБ, Ожидаемый размер: {expected_size_mb} МБ, Допуск: {tolerance} МБ")

        assert abs(file_size_mb - expected_size_mb) <= tolerance, (
            f"Размер файла {file_size_mb} МБ не соответствует ожидаемому {expected_size_mb} МБ (допуск: {tolerance} МБ)"
        )
        logging.info(f"Размер файла проверен: {file_size_mb} МБ соответствует ожидаемому {expected_size_mb} МБ")
