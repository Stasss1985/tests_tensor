import time
import pytest
import logging


def test_02_check_region(contact_page):
    logging.info("Старт проверки регионов")
    contact_page.open_page()
    contact_page.take_screenshot()
    # Переход в контакты
    contact_page.go_to_contacts()
    contact_page.take_screenshot()
    # Проверка своего региона
    contact_page.verify_my_region()
    contact_page.take_screenshot()
    # Проверка списка партнеров своего региона
    contact_page.verify_partners_list_does_not_empty_krasnodar()
    contact_page.take_screenshot()
    # Смена региона на Камчатку
    contact_page.change_region_to_kamchatka()
    contact_page.take_screenshot()
    # Проверка, что регион сменился на Камчатский край
    time.sleep(2)
    contact_page.verify_region_changed()
    contact_page.take_screenshot()
    # Проверка списка партнеров региона Камчатка и что список изменился
    contact_page.verify_partners_list_does_not_empty_kamchatka()
    contact_page.take_screenshot()
    # Проверка заголовка региона Камчатский край
    contact_page.verify_title_contains_region()
    contact_page.take_screenshot()
    # Проверка, что URL содержит Камчатский край
    contact_page.verify_url_region_kamchatka()
    contact_page.take_screenshot()
    logging.info("Проверка регионов завершена успешно")
