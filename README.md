vendor.py

Automation Overview: Vendor Selection and Product Filtering Test

This automation script is designed to log in to the application, select vendors, and verify product filtering. It specifically highlights a known issue (the "OnePlus bug") where products are not correctly filtered when OnePlus is selected.

Workflow:

Login Automation

The script automatically navigates to the login page.

It fills in the username and password fields and submits the login form.

After login, it waits until the dashboard or vendor selection section is fully loaded to ensure the application is ready for further actions.

Vendor Selection and Product Verification

The automation iterates over a predefined list of vendors (e.g., Samsung, OnePlus, Apple).

For each vendor, it selects the corresponding checkbox to filter products.

Instead of using fixed delays, the script waits intelligently for elements to become interactable and for products to load.

It then captures the list of displayed products for verification.

Highlighting the OnePlus Bug

When the "OnePlus" vendor is selected, the script checks if the products displayed are correctly filtered.

If products from other vendors appear alongside OnePlus products, the script highlights this issue, signaling the bug.

Robustness Features

Explicit waits ensure elements are loaded and interactable, reducing flaky test failures.

Each test step is modular and independent, making debugging and maintenance easier.

The automation provides clear console outputs for both successful actions and detected issues.

Purpose and Benefits:

Detecting Regression Bugs: The script efficiently highlights issues like the OnePlus product filtering bug.

Cross-Browser/Platform Testing: Designed to be compatible with BrowserStack, allowing testing on multiple browsers and devices.

Reusable and Extensible: Additional vendors or new test scenarios can be easily added without major changes.

Documentation-Ready: The workflow, expected results, and bug detection are clearly documented for team reference or open-source sharing.

fav.py

Favorite Products Automation Test

This automation tests the favorite products feature in the application, highlighting a known bug where selected favorites are not displayed correctly.

Workflow:

Selecting Favorite Products

The script selects multiple products by clicking the alternative heart icon, which marks them as favorites.

This action is performed for several products to simulate a typical user behavior of adding multiple favorites.

Navigating to the Favorites Tab

After marking products as favorites, the script navigates to the Favorites tab to verify that all selected products appear.

Observed Bug

Despite selecting multiple products as favorites, only three products are displayed in the Favorites tab.

This behavior occurs even when more products were marked, indicating a functional bug in the favorite products feature.

Purpose of Automation

Detects inconsistencies in favorite product display.

Helps the QA team identify issues in product selection and tabular display logic.

Can be extended to test favorite functionality across different devices and browsers (BrowserStack compatible).

Key Notes:

The automation uses intelligent waits to ensure that products are fully loaded before interacting with the heart icons.

Each product selection and verification step is modular, making it easy to maintain and extend.

This test highlights critical UX issues where users expect all selected favorites to appear but see only a subset.




