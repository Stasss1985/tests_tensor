from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TensorLoc():
    BANNERS = (By.XPATH, "//*[contains(text(), 'Сила в людях')]")
    READ_MORE_HREF = (By.CSS_SELECTOR, '[href="/about"]')
    BLOCK_IMAGES = (By.CSS_SELECTOR, ".tensor_ru-About__block3-image-wrapper img")


class TensorPage(BasePage):
    loc = TensorLoc

    def find_banner_strong_people(self):
        logging.info("Найти баннер Сила в людях")
        WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))
        # Поиск всех окон
        windows = self.driver.window_handles
        # Переключение на последнее из тех, что открылось
        self.driver.switch_to.window(windows[-1])
        time.sleep(5)
        self.scroll_to_down()
        # "Сила в людях"
        self.scroll_to_element(self.loc.BANNERS)
        # Убедитесь, что элемент виден
        self.wait_for_element_visibility(self.loc.BANNERS)
        assert "Сила в людях" in self.get_text(self.loc.BANNERS)

    def click_details(self):
        logging.info("Найти Подробнее и кликнуть по нему")
        time.sleep(3)
        self.find(self.loc.READ_MORE_HREF)
        self.click(self.loc.READ_MORE_HREF)
        time.sleep(3)

    def check_url_about(self):
        logging.info("Проверка URL адреса")
        self.check_expected_url("https://tensor.ru/about")

    def check_images_in_work_block(self):
        logging.info("Проверка размера фотографий")
        images = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.loc.BLOCK_IMAGES)
        )
        self.scroll_to_element(self.loc.BLOCK_IMAGES)
        if not images:
            raise AssertionError("Нет фотографий в блоке Работаем")
        first_image = images[0]
        first_width = first_image.get_attribute("width")
        first_height = first_image.get_attribute("height")

        for image in images[1:]:
            width = image.get_attribute("width")
            height = image.get_attribute("height")
            assert width == first_width, f"Ширина фото {width} не ровна ширине 1-ого фото {first_width}"
            assert height == first_height, f"Высота фото {height} не ровна высоте 1-ого фото {first_height}"
