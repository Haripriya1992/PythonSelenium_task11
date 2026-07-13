from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

# test data
home_url = "https://www.guvi.in/"
login_url = "https://www.guvi.in/sign-in/?sourceUri=http%3A%2F%2Fwww.guvi.in%2F"

valid_username = "haripriyamadhavaraj@gmail.com"
valid_password = "Hari@1992"

invalid_username = "wrong_user@example.com"
invalid_password = "wrongpass123"


# this runs before every test - opens a fresh browser
# and after every test - closes it
@pytest.fixture()
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    yield drv
    drv.quit()


def click_login(drv):
    drv.get(home_url)
    time.sleep(2)
    drv.find_element(By.ID, "login-btn").click()
    time.sleep(2)


# ------------------ POSITIVE TEST CASES ------------------

def test_positive_login_button_url(driver):
    click_login(driver)
    current_url = driver.current_url
    print("URL after clicking Login:", current_url)
    assert current_url.startswith(login_url)


def test_positive_username_password_fields_visible(driver):
    driver.get(login_url)
    time.sleep(2)

    email_box = driver.find_element(By.ID, "email")
    password_box = driver.find_element(By.ID, "password")

    assert email_box.is_displayed() and email_box.is_enabled()
    assert password_box.is_displayed() and password_box.is_enabled()


def test_positive_submit_button_working(driver):
    driver.get(login_url)
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys(valid_username)
    driver.find_element(By.ID, "password").send_keys(valid_password)

    submit_button = driver.find_element(By.ID, "login-btn")
    assert submit_button.is_enabled()
    submit_button.click()
    time.sleep(3)

    print("URL after login:", driver.current_url)
    assert not driver.current_url.startswith(login_url)


# ------------------ NEGATIVE TEST CASES ------------------

def test_negative_login_url_should_not_be_homepage(driver):
    click_login(driver)
    current_url = driver.current_url
    assert not current_url.startswith(home_url + "?") and current_url != home_url


def test_negative_login_with_wrong_credentials(driver):
    driver.get(login_url)
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys(invalid_username)
    driver.find_element(By.ID, "password").send_keys(invalid_password)
    driver.find_element(By.ID, "login-btn").click()
    time.sleep(3)

    current_url = driver.current_url
    print("URL after wrong login:", current_url)
    assert current_url.startswith(login_url)


def test_negative_submit_with_empty_fields(driver):
    driver.get(login_url)
    time.sleep(2)

    submit_button = driver.find_element(By.ID, "login-btn")
    submit_button.click()
    time.sleep(2)

    print("URL after empty submit:", driver.current_url)
    assert driver.current_url.startswith(login_url)