import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from data import *


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    # Переходим на главную страницу
    pytest.driver.get('https://mnogosna.ru/')
    yield
    pytest.driver.quit()


def search():
    pytest.driver.find_element_by_class_name('js-search-input').click()
    pytest.driver.find_element_by_id('search-input').send_keys('матрас аскона 160х200')
    pytest.driver.find_element_by_class_name('js-search-btn').click()
    time.sleep(2)


def take_screenshot(test_name):
    # Создание скриншота
    screenshot_path = f"mnogosna/screens/{test_name}_fail.png"
    highlight_element(test_name)
    pytest.driver.save_screenshot(screenshot_path)
    print(f"Скриншот сохранен: {screenshot_path}")


def highlight_element(test_name):
    element = None
    if test_name == "test_result":
        element = pytest.driver.find_elements(by=By.CLASS_NAME, value='slinks__link')[0]
    elif test_name == "test_product":
        element = pytest.driver.find_elements(by=By.CLASS_NAME, value='pop-card__name')[0]
    elif test_name == "test_photo":
        element = pytest.driver.find_elements(by=By.XPATH, value='//a[@class="pop-card__img"]/picture/img')[0]
    if element:
        # Используем ActionChains для нарисования рамки вокруг элемента
        action_chains = ActionChains(pytest.driver)
        action_chains.move_to_element(element).perform()
        pytest.driver.execute_script("arguments[0].style.border='3px solid red'", element)


def test_result():
    # Проверка результата поиска по разделам
    search()
    actual_name = pytest.driver.find_elements_by_class_name('slinks__link')[0].text
    if actual_name != expected_name:
        take_screenshot("test_result")
    assert actual_name == expected_name


def test_product():
    # Проверка первого товара
    search()
    actual_product_name = pytest.driver.find_elements_by_class_name('pop-card__name')[0].text
    if actual_product_name != expected_product_name:
        take_screenshot("test_product")
    assert actual_product_name == expected_product_name


def test_photo():
    # Проверка картинки у первого товара
    search()
    link = pytest.driver.find_elements_by_xpath('//a[@class="pop-card__img"]/picture/img')[0]
    actual_photo = link.get_attribute('src')
    if actual_photo != expected_photo:
        take_screenshot("test_photo")
    assert actual_photo == expected_photo
