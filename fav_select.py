

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException,
)
import time

# === CONFIG ===
DO_LOGIN = True                     # True -> script logs in; False -> assumes already signed in
SIGNIN_URL = "https://testathon.live/signin"
START_URL = "https://testathon.live/?signin=true"
USERNAME = "demouser"
PASSWORD = "testingisfun99"

CLICK_WAIT_SECONDS = 0.5            # short pause between clicks
GLOBAL_TIMEOUT = 15
START_OFFSET = 0                    # 0 -> click 1st, 2nd skip; 1 -> start from second

# === Helpers ===
def select_react_select(wait, driver, container_css, value_text):
    """Robust small helper for react-select style controls (#username / #password)."""
    container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, container_css)))
    try:
        container.click()
    except Exception:
        driver.execute_script("arguments[0].click();", container)

    input_selector = f"{container_css} input"
    input_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_selector)))
    input_el.clear()
    input_el.send_keys(value_text)
    time.sleep(0.2)
    # try clicking visible option, else Enter
    try:
        opt = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            f"//div[contains(@class,'menu') or contains(@class,'options')]//div[normalize-space()='{value_text}']"
        )), timeout=2)
        driver.execute_script("arguments[0].click();", opt)
    except Exception:
        try:
            input_el.send_keys(Keys.ENTER)
        except Exception:
            pass
    time.sleep(0.25)


def find_heart_buttons(driver):
    """
    Return clickable ancestor elements for heart icons found on page.
    Matches <span class="MuiIconButton-label"><svg class="MuiSvgIcon-root Icon">...</svg></span>
    """
    spans = driver.find_elements(By.CSS_SELECTOR, "span.MuiIconButton-label svg.MuiSvgIcon-root.Icon")
    buttons = []
    for svg in spans:
        try:
            ancestor = None
            for tag in ("button", "label", "a", "div"):
                try:
                    ancestor = svg.find_element(By.XPATH, f"./ancestor::{tag}[1]")
                    if ancestor:
                        break
                except NoSuchElementException:
                    ancestor = None
            if ancestor:
                buttons.append(ancestor)
            else:
                buttons.append(svg.find_element(By.XPATH, "./.."))
        except StaleElementReferenceException:
            continue
        except Exception:
            continue
    return buttons

def click_vendor_checkbox(driver, wait, vendor_name):
    """Not used in this version but left for compatibility if needed."""
    pass

# === Main ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # keep Chrome open after script ends
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, GLOBAL_TIMEOUT)

try:
    # Optional login
    if DO_LOGIN:
        driver.get(SIGNIN_URL)
        select_react_select(wait, driver, "#username", USERNAME)
        select_react_select(wait, driver, "#password", PASSWORD)
        # click login button robustly
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
        except TimeoutException:
            login_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'log in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'login')]")
            ))
        driver.execute_script("arguments[0].click();", login_btn)
        # wait for login to be confirmed by presence of logout
        wait.until(EC.presence_of_element_located((By.ID, "logout")))

    # navigate to listing page (where hearts are)
    driver.get(START_URL)
    time.sleep(1)

    print("Locating heart/favorite controls on the page...")

    # Alternate clicking: indices START_OFFSET, START_OFFSET+2, ...
    index = START_OFFSET
    while True:
        hearts = find_heart_buttons(driver)
        if index >= len(hearts):
            break

        el = hearts[index]
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(0.15)
            driver.execute_script("arguments[0].click();", el)
            print(f"Clicked heart at index {index} (1-based #{index+1})")
            time.sleep(CLICK_WAIT_SECONDS)
        except StaleElementReferenceException:
            print(f"Stale element at index {index} — retrying same index...")
            time.sleep(0.2)
            continue
        except Exception as e:
            print(f"Failed to click heart at index {index}: {e}")

        index += 2

    print("✅ Done clicking alternate hearts. Now clicking the navbar Favourites link...")

    # --- CLICK THE NAVBAR 'Favourites' LINK (do NOT navigate by URL) ---
    try:
        fav_link = wait.until(EC.element_to_be_clickable((By.ID, "favourites")))
        driver.execute_script("arguments[0].scrollIntoView(true);", fav_link)
        time.sleep(0.15)
        driver.execute_script("arguments[0].click();", fav_link)
        print("Clicked navbar Favourites link.")
    except Exception as e:
        print("Could not find/click navbar Favourites link by id='favourites':", e)

    # Wait for the favourites page to load by checking a page element (shelf-container)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shelf-container")))
        print("Favourites page loaded (shelf-container present).")
    except TimeoutException:
        # fallback: just wait for body
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Favourites page loaded (fallback).")

    print("Browser left open for inspection (detach=True).")

except Exception as e:
    print("Error during run:", e)

# end — do NOT quit driver; browser remains open
