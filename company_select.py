
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)
import time

# CONFIG
SIGNIN_URL = "https://testathon.live/signin"
USERNAME = "demouser"
PASSWORD = "testingisfun99"
# vendors from your screenshot
VENDORS = ["Apple", "Samsung", "Google", "OnePlus"]
CLICK_WAIT_SECONDS = 10
GLOBAL_TIMEOUT = 20

# --- Helpers (robust to React re-renders) ---
def robust_select_react_select(driver, wait, container_css, value_text, timeout=GLOBAL_TIMEOUT):
    """Open react-select container, type value, try to pick the option (robust/retrying)."""
    end = time.time() + timeout
    container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, container_css)))
    try:
        container.click()
    except Exception:
        driver.execute_script("arguments[0].click();", container)

    while time.time() < end:
        try:
            input_sel = f"{container_css} input"
            input_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_sel)))
            input_el.clear()
            input_el.send_keys(value_text)
            time.sleep(0.3)
        except (StaleElementReferenceException, TimeoutException):
            # re-open container and retry
            try:
                container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, container_css)))
                driver.execute_script("arguments[0].click();", container)
            except Exception:
                pass
            continue

        # Attempt various xpaths for matching option
        option_xpaths = [
            f"//div[contains(@class,'menu')]//div[normalize-space()='{value_text}']",
            f"//div[contains(@class,'option') or contains(@class,'options')]//div[normalize-space()='{value_text}']",
            f"//div[normalize-space()='{value_text}']",
            f"//span[normalize-space()='{value_text}']",
            f"//li[normalize-space()='{value_text}']",
        ]
        for xp in option_xpaths:
            try:
                opt = driver.find_element(By.XPATH, xp)
                if not opt.is_displayed():
                    continue
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                    time.sleep(0.1)
                    opt.click()
                    return True
                except StaleElementReferenceException:
                    break
                except Exception:
                    try:
                        driver.execute_script("arguments[0].click();", opt)
                        return True
                    except Exception:
                        break
            except NoSuchElementException:
                continue

        # Fallback: press Enter in input (re-find to avoid stale)
        try:
            input_el = driver.find_element(By.CSS_SELECTOR, f"{container_css} input")
            input_el.send_keys(Keys.ENTER)
            return True
        except Exception:
            time.sleep(0.2)
            continue

    return False


def click_vendor_checkbox(driver, wait, vendor_name, timeout=GLOBAL_TIMEOUT):
    """
    Click the vendor checkbox/label/span to toggle selection.
    Returns True if a click action was performed.
    """
    end = time.time() + timeout
    xpaths = [
        f"//input[@type='checkbox' and normalize-space(@value)='{vendor_name}']",
        f"//label[.//span[normalize-space()='{vendor_name}']]",
        f"//div[contains(@class,'filters-available-size')]//span[normalize-space()='{vendor_name}']",
        f"//div[normalize-space()='{vendor_name}']",
    ]
    while time.time() < end:
        for xp in xpaths:
            try:
                el = driver.find_element(By.XPATH, xp)
                if not el.is_displayed():
                    continue
                tag = el.tag_name.lower()
                try:
                    if tag == "input":
                        # click ancestor label if exists (safer)
                        try:
                            label = el.find_element(By.XPATH, "./ancestor::label[1]")
                            driver.execute_script("arguments[0].scrollIntoView(true);", label)
                            driver.execute_script("arguments[0].click();", label)
                            return True
                        except Exception:
                            driver.execute_script("arguments[0].click();", el)
                            return True
                    else:
                        driver.execute_script("arguments[0].scrollIntoView(true);", el)
                        driver.execute_script("arguments[0].click();", el)
                        return True
                except StaleElementReferenceException:
                    break
                except Exception:
                    try:
                        el.click()
                        return True
                    except Exception:
                        try:
                            driver.execute_script("arguments[0].click();", el)
                            return True
                        except Exception:
                            break
            except NoSuchElementException:
                continue
        time.sleep(0.2)
    return False


def is_vendor_selected(driver, vendor_name):
    """
    Try to detect if vendor checkbox is currently selected.
    Returns True if selected, False otherwise or unknown.
    """
    try:
        inp = driver.find_element(By.XPATH, f"//input[@type='checkbox' and normalize-space(@value)='{vendor_name}']")
        # .is_selected() works for input elements
        return inp.is_selected()
    except Exception:
        # try to infer from class on label/span (if site marks selected via class)
        try:
            el = driver.find_element(By.XPATH, f"//label[.//span[normalize-space()='{vendor_name}']]")
            cls = el.get_attribute("class") or ""
            return "checked" in cls.lower() or "active" in cls.lower() or "selected" in cls.lower()
        except Exception:
            return False


# --- Main ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, GLOBAL_TIMEOUT)

try:
    driver.get(SIGNIN_URL)
    print("Opened signin page.")

    # Login using the robust react-select helper (username + password)
    if not robust_select_react_select(driver, wait, "#username", USERNAME):
        raise Exception("Failed to select username.")
    print("Username selected.")

    if not robust_select_react_select(driver, wait, "#password", PASSWORD):
        raise Exception("Failed to select password.")
    print("Password entered.")

    # Click Login
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
    except TimeoutException:
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'log in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'login')]")
        ))
    driver.execute_script("arguments[0].click();", login_btn)
    print("Clicked Login.")
    wait.until(EC.presence_of_element_located((By.ID, "logout")))
    print("✅ Logged in successfully.")

    # Ensure vendor page visible
    if "/?signin=true" not in driver.current_url:
        driver.get("https://kolkata.bugbash.live/?signin=true")
        time.sleep(1)

    # For each vendor: select -> wait -> unselect -> continue
    for vendor in VENDORS:
        print(f"--- Processing vendor: {vendor} ---")

        clicked = click_vendor_checkbox(driver, wait, vendor)
        if not clicked:
            print(f"⚠ Could not click/select vendor '{vendor}', skipping.")
            continue

        # optionally verify selected
        time.sleep(0.5)
        sel = is_vendor_selected(driver, vendor)
        print(f"Selected = {sel} (may be inferred). Waiting {CLICK_WAIT_SECONDS}s...")
        time.sleep(CLICK_WAIT_SECONDS)

        # Unselect by toggling the same element
        # Prefer clicking the checkbox input's ancestor label if present
        unclicked = click_vendor_checkbox(driver, wait, vendor)
        if not unclicked:
            print(f"⚠ Could not unselect vendor '{vendor}'.")
        else:
            # small pause to allow UI to update
            time.sleep(0.5)
            sel_after = is_vendor_selected(driver, vendor)
            print(f"After unselect, Selected = {sel_after}")

    print("✅ Done toggling all vendors.")

finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.") 
