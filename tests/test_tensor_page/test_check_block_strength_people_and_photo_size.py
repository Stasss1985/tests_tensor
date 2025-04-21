import allure
import pytest
import logging


@pytest.mark.smoke('smoke test')
def test_01_check_block_strength_people_and_photo_size(contact_page, tensor_page):
    logging.info("Старт 1-ого сценария")
    contact_page.open_page()
    contact_page.take_screenshot()
    # Переход в контакты
    contact_page.go_to_contacts()
    contact_page.take_screenshot()
    # Найти баннер Тензор, кликнуть по нему
    contact_page.click_tensor_banner()
    contact_page.take_screenshot()
    # Найти баннер Сила в людях
    tensor_page.find_banner_strong_people()
    tensor_page.take_screenshot()
    # Найти "Подробнее" и кликнуть по нему
    tensor_page.click_details()
    tensor_page.take_screenshot()
    # Проверка URL адреса
    tensor_page.check_url_about()
    tensor_page.take_screenshot()
    # Проверка размера фотографий
    tensor_page.check_images_in_work_block()
    tensor_page.take_screenshot()
    logging.info("Перый сценарий зевершен успешно")
