import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

@pytest.fixture(scope="function")
def driver():
    """
    Initialize the Chrome driver for local testing
    Make sure chromedriver is in your PATH or update the executable_path
    """
    service = Service(executable_path=r'C:\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_to_favourites_and_verify(driver):
    """
    Test adding an item to favourites and verifying its presence in the favourites page.
    """
    try:
        # 1. Login
        driver.get("https://testathon.live/signin")
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.element_to_be_clickable((By.ID, "react-select-2-input")))
        username_field.send_keys("fav_user")
        time.sleep(1)
        username_field.send_keys(Keys.ENTER)
        time.sleep(1)

        password_field = wait.until(EC.element_to_be_clickable((By.ID, "react-select-3-input")))
        password_field.send_keys("testingisfun99")
        time.sleep(1)
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)

        try:
            form = driver.find_element(By.TAG_NAME, "form")
            form.submit()
        except:
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'LOG IN')]")))
            driver.execute_script("arguments[0].click();", login_button)
        time.sleep(5)

        assert driver.current_url == "https://testathon.live/?signin=true" or driver.current_url == "https://testathon.live/"

        # 2. Navigate to Home Page (if not already there)
        driver.get("https://testathon.live/")
        time.sleep(2)

        # 3. Click Favorite Button for a specific product (e.g., iPhone 12, id="1")
        # Assuming iPhone 12 is the first product with id="1"
        product_id = "1"
        product_title = "iPhone 12" # This should match the alt text or title of the product

        # Locate the favorite button for the product
        # The button is inside a div with class "shelf-stopper" within the product's shelf-item div
        favourite_button_xpath = f"//div[@id='{product_id}']//button[@aria-label='delete']"
        favourite_button = wait.until(EC.element_to_be_clickable((By.XPATH, favourite_button_xpath)))
        favourite_button.click()
        time.sleep(2) # Give time for the favourite action to register

        # 4. Navigate to Favourites Page
        favourites_link = wait.until(EC.element_to_be_clickable((By.ID, "favourites")))
        favourites_link.click()
        time.sleep(3) # Wait for the favourites page to load

        # 5. Verify Favorited Item is present
        # Assuming the product title will be visible on the favourites page
        # You might need to adjust this XPath based on the actual structure of the favourites page
        favourited_item_xpath = f"//*[contains(text(), '{product_title}')]"
        favourited_item = wait.until(EC.presence_of_element_located((By.XPATH, favourited_item_xpath)))
        assert favourited_item.is_displayed(), f"Favorited item '{product_title}' not found on favourites page."
        print(f"✓ Favorited item '{product_title}' successfully found on favourites page.")

        # 6. Logout
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'LOG OUT')] | //a[contains(text(), 'LOG OUT')] | //*[contains(@id, 'logout')] | //*[contains(@class, 'logout')] ")))
        logout_button.click()
        time.sleep(2)
        assert driver.current_url == "https://testathon.live/signin" or driver.current_url == "https://testathon.live/"
        print("✓ Logout successful.")

    except AssertionError as e:
        print(f"✗ Test failed: {str(e)}")
        raise
    except Exception as e:
        print(f"✗ An unexpected error occurred: {str(e)}")
        raise
