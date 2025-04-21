import allure
import pytest
import logging
import os


@allure.title("Проверка скачивания и размера плагина SBIS")
def test_03_check_plugin_download_and_size(download_footer_page):
    logging.info("Старт - проверка скачивания и размера плагина")
    # Определение фиксированной директории для скачивания
    download_dir = r"C:\Users\Stass\tests_tensor\tests\test_footer_page"
    # Открыть главную страницу SBIS
    download_footer_page.open_page()
    download_footer_page.take_screenshot()
    # Прокрутить до ссылки "Скачать локальные версии" и кликнуть по ней
    download_footer_page.scroll_to_download_local_versions()
    download_footer_page.take_screenshot()
    download_footer_page.click_download_local_versions()
    download_footer_page.take_screenshot()
    # Получить ожидаемый размер плагина
    expected_size_mb = download_footer_page.get_expected_plugin_size()
    logging.info(f"Ожидаемый размер плагина: {expected_size_mb} МБ")
    # Скачать плагин для Windows
    download_footer_page.download_windows_plugin(download_dir)
    download_footer_page.take_screenshot()
    # Проверить, что плагин был скачан
    file_path = download_footer_page.verify_plugin_downloaded(download_dir)
    logging.info(f"Файл плагина скачан: {file_path}")
    # Проверить размер файла
    download_footer_page.verify_file_size(file_path, expected_size_mb)
    download_footer_page.take_screenshot()
    logging.info("Сценарий проверки скачивания и размера плагина завершен успешно")
