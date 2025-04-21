from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ContactLoc():
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    OPEN_ALL_CONTACTS_LINK = (By.CSS_SELECTOR, '[href="/contacts"]')
    LOGO_TENSOR_HREF = (By.CSS_SELECTOR, '[href="https://tensor.ru/"]')
    REGION_SELECTOR = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")
    REGION_OPTION = (By.XPATH, "//span[@title='Камчатский край']")
    PARTNERS_LIST = (By.CSS_SELECTOR,
                     '[class="controls-ListView__itemV-relative controls-ListView__itemV controls-ListView__item_default controls-ListView__item_contentWrapper js-controls-ListView__editingTarget  controls-ListView__itemV_cursor-pointer  controls-ListView__item_showActions js-controls-ListView__measurableContainer controls-ListView__item__unmarked_default controls-ListView__item_highlightOnHover controls-hover-background-default controls-Tree__item"]')
    REGION_TITLE = (By.CSS_SELECTOR, ".sbis_ru-Contacts__title")


class ContactPage(BasePage):
    loc = ContactLoc

    def go_to_contacts(self):
        logging.info("Переход в секцию контакты")
        # Переход к контактам
        contacts_link = self.wait_clickable(self.loc.CONTACTS_LINK)
        contacts_link.click()
        # Открыть все контакты
        open_all_contacts_link = self.wait_for_element_presence(self.loc.OPEN_ALL_CONTACTS_LINK)
        open_all_contacts_link.click()

    def click_tensor_banner(self):
        logging.info("Найти баннер Тензор, кликнуть по нему")
        logo_tensor_href = self.find(self.loc.LOGO_TENSOR_HREF)
        logo_tensor_href.click()

    def verify_my_region(self):
        logging.info("Проверка своего региона")
        region_text = self.wait_for_element_presence(self.loc.REGION_SELECTOR).text
        assert "Краснодарский край" in region_text, f"Expected region: Краснодарский край, but got {region_text}"

    def verify_partners_list_does_not_empty_krasnodar(self):
        logging.info("Проверка списка партнеров своего региона")
        partners = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.loc.PARTNERS_LIST)
        )
        assert len(partners) > 0, "Partners list is empty"
        self.partner_1_krasnodar = partners[0].text
        print(self.partner_1_krasnodar)

    def change_region_to_kamchatka(self):
        logging.info("Смена региона на Камчатку")
        region_selector = self.wait_clickable(self.loc.REGION_SELECTOR)
        region_selector.click()
        region_option = self.wait_clickable(self.loc.REGION_OPTION)
        region_option.click()

    def verify_region_changed(self):
        logging.info("Проверка, что регион сменился на Камчатский край")
        region_text = self.wait_for_element_presence(self.loc.REGION_SELECTOR).text
        assert "Камчатский край" in region_text, f"Expected region: Камчатский край, but got {region_text}"

    def verify_partners_list_does_not_empty_kamchatka(self):
        logging.info("Проверка списка партнеров региона Камчатка и что список изменился")
        partners = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.loc.PARTNERS_LIST)
        )
        assert len(partners) > 0, "Нет списка партнеров"
        partner_1_kamchatka = partners[0].text
        print(partner_1_kamchatka)
        assert self.partner_1_krasnodar != partner_1_kamchatka

    def verify_title_contains_region(self):
        logging.info("Проверка заголовка региона Камчатский край")
        title = self.driver.title
        assert "Камчатский край" in title, f"Expected 'Камчатский край' in title, but got {title}"

    def verify_url_region_kamchatka(self):
        logging.info("Проверка, что URL содержит Камчатский край")
        self.check_expected_url('https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients')
