# 🧪 Test Automation Suite (Pytest + Selenium)

This repository contains **end-to-end automated test scripts** for validating login, vendor filtering, and favorite product features on [Testathon](https://testathon.live).  
It uses **Pytest** and **Selenium WebDriver** with support for local ChromeDriver and BrowserStack.

---

## 📂 Test Scripts Overview

### 1. `login.py` — Login Automation
Automates multiple login scenarios for different user accounts.

**Features:**
- Initializes Chrome WebDriver via a reusable `driver` fixture.
- Runs **parametrized tests** for different usernames and passwords.
- Covers:
  - ✅ Successful login + logout
  - 🔒 Locked account detection
  - ❌ Invalid username
  - ❌ Invalid password
- Uses **explicit waits** to ensure stable element interactions.

**Example Test Cases:**

| Username            | Password        | Expected Result    |
|---------------------|-----------------|--------------------|
| `demouser`          | `testingisfun99`| success            |
| `locked_user`       | `testingisfun99`| locked_account     |
| `random_user_123`   | `testingisfun99`| invalid_username   |
| `demouser`          | `wrong_password`| invalid_password   |

---

### 2. `vendor.py` — Vendor Selection & Product Filtering
Tests product filtering by vendor and highlights a known **OnePlus filtering bug**.

**Workflow:**
1. **Login Automation**
   - Navigates to login page, fills credentials, waits for dashboard.
2. **Vendor Selection & Verification**
   - Iterates over vendors (Samsung, OnePlus, Apple).
   - Selects vendor checkbox and verifies product list.
3. **OnePlus Bug Detection**
   - When selecting *OnePlus*, products from other vendors still appear → **bug flagged**.

**Robustness:**
- Explicit waits prevent flaky tests.
- Modular steps → easy debugging and extension.
- Console logs clearly indicate pass/fail scenarios.

**Purpose:**
- Detects regression issues (e.g., OnePlus bug).
- Compatible with BrowserStack for cross-browser/device testing.
- Easily extensible for new vendors.

---

### 3. `fav.py` — Favorite Products Automation
Validates the favorite products feature and highlights a **favorites display bug**.

**Workflow:**
1. **Selecting Favorites**
   - Marks multiple products as favorites via heart icon.
2. **Navigating to Favorites Tab**
   - Opens the Favorites tab to verify selected items.
3. **Observed Bug**
   - Despite selecting multiple products, only **three favorites** are displayed → inconsistent with user expectations.

**Key Notes:**
- Uses intelligent waits for reliable product interaction.
- Modular steps simplify maintenance and extension.
- Highlights UX issue: favorites do not reflect all user selections.

---

## ▶️ Running the Tests
Install dependencies:
```bash
pip install pytest selenium
