# Amazon Automation Bot 🛒 🤖

## Description
A robust, highly optimized Python Selenium script designed to automate the checkout flow on Amazon. 

This script searches for a predefined product, instantly identifies and clicks the localized "Add to cart" button from the search results, seamlessly bypasses intermediate overlays to jump to the cart, and automatically proceeds to the checkout stage.

### Key Features
- **Dynamic Layout Handlers**: Uses multiple layered XPaths to successfully find buttons even when Amazon runs random A/B tests on button tags and classes.
- **Optimized Polling**: Temporarily disables Selenium's `implicitly_wait` locks during branching, replacing them with ultra-fast polling loops. This pushes the execution speed to an absolute minimum instead of hanging for 10 seconds whenever a fallback button isn't found.
- **Fail-safe Debugging**: Instantly captures and dumps the HTML source code to `error_page.html` if Amazon triggers an invisible anti-bot CAPTCHA wall.
- **JavaScript Click Intercepts**: Forcefully overrides Amazon's floating DOM headers to successfully land clicks underneath elements when traditional clicks fail.

## Setup & Execution

### Prerequisites
Make sure you have Google Chrome installed on your machine. The script uses Selenium's built-in web-driver manager (Selenium 4.6+) so no manual ChromeDriver download is needed.

### Installation
1. Clone the repository
2. Install the Required modules:
```bash
pip install selenium
```

### Running the Automation
Run the file directly. Watch the magic happen.
```bash
python test.py
```

*Note: Depending on your region, you may need to adjust the `AMAZON_URL` or product query inside `test.py`.*
