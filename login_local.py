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
    # Option 1: If chromedriver is in PATH
    # driver = webdriver.Chrome()
    
    # Option 2: If you need to specify the path to chromedriver
    service = Service(executable_path='C:\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected_result", [
    ("demouser", "testingisfun99", "success"),
    ("image_not_loading_user", "testingisfun99", "success"),
    ("existing_orders_user", "testingisfun99", "success"),
    ("fav_user", "testingisfun99", "success"),
    ("locked_user", "testingisfun99", "locked_account"),
    ("random_user_123", "testingisfun99", "invalid_username"),
    ("demouser", "wrong_password", "invalid_password")
])
def test_login_scenarios(driver, username, password, expected_result):
    """
    Test login scenarios locally using Chrome browser
    """
    try:
        # Open the sign-in page
        driver.get("https://testathon.live/signin")
        
        
        # Use WebDriverWait to wait for the username field to be clickable
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        username_field = wait.until(EC.element_to_be_clickable((By.ID, "react-select-2-input")))
        
        username_field.send_keys(username)
        time.sleep(1)  # Wait for 1 second after typing
        username_field.send_keys(Keys.ENTER)
        time.sleep(1)  # Wait for 1 second after pressing enter

        # Use WebDriverWait to wait for the password field to be clickable
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "react-select-3-input")))

        password_field.send_keys(password)
        time.sleep(1)  # Wait for 1 second after typing
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)  # Wait for 1 second after pressing enter

        # Find the form and submit it
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            form.submit()
        except:
            # Fallback to clicking the button if form submission fails or no form is found
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'LOG IN')]")))
            driver.execute_script("arguments[0].click();", login_button)

        time.sleep(5)  # Increased wait for login to complete and page to redirect

        if expected_result == "success":
            # Verify successful login
            assert driver.current_url == "https://testathon.live/?signin=true"

            # Logout
            logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'LOG OUT')] | //a[contains(text(), 'LOG OUT')] | //*[contains(@id, 'logout')] | //*[contains(@class, 'logout')] ")))
            logout_button.click()
            time.sleep(2)  # Wait for logout to complete

            # Verify logout (e.g., by checking if redirected back to signin page or a welcome page)
            assert driver.current_url == "https://testathon.live/signin" or driver.current_url == "https://testathon.live/"
        elif expected_result == "locked_account":
            # Assert that the current URL is still the sign-in page
            assert driver.current_url == "https://testathon.live/signin"
            # Assert that the error message is present
            error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Your account has been locked.')]")))
            assert error_message.is_displayed()
        elif expected_result == "invalid_username":
            # Assert that the current URL is still the sign-in page
            assert driver.current_url == "https://testathon.live/signin"
            # Assert that the error message is present
            error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Invalid Username')]")))
            assert error_message.is_displayed()
        elif expected_result == "invalid_password":
            # Assert that the current URL is still the sign-in page
            assert driver.current_url == "https://testathon.live/signin"
            # Assert that the error message is present
            error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Invalid Password')]")))
            assert error_message.is_displayed()

        print(f"✓ Local test passed for {username} with expected result: {expected_result}")

    except AssertionError as e:
        print(f"✗ Local test failed for {username}: {str(e)}")
        raise  # Re-raise the assertion error to mark the pytest test as failed

    except Exception as e:
        print(f"✗ Local test error for {username}: {str(e)}")
        raise  # Re-raise the exception to mark the pytest test as failed