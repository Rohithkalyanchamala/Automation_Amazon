import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.implicitly_wait(10) # Wait up to 10 seconds for elements to appear
driver.maximize_window()

try:
    # 1. Open Amazon
    driver.get("https://www.amazon.in")
    
    # 2. Search
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("iPhone 17 Pro", Keys.RETURN)
    time.sleep(4) # Let results load
    
    # 3. Scroll down to find the "Add to cart" buttons
    driver.execute_script("window.scrollBy(0, 400);") 
    time.sleep(2)
    
    # Locate the yellow Add to Cart buttons directly on the search results
    add_buttons = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')] | //button[contains(@id, 'a-autoid')]")
    
    # Filter to ensure we only click the actual "Add to cart" buttons
    valid_btns = [btn for btn in add_buttons if btn.is_displayed() and "add to cart" in btn.text.strip().lower()]
    
    if not valid_btns:
        with open("error_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise Exception("No 'Add to cart' buttons found directly on the search results! Saved HTML to error_page.html.")
        
    # Click the first available Add to Cart button
    add_btn = valid_btns[0]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
    time.sleep(1)
    
    try:
        add_btn.click()
    except:
        driver.execute_script("arguments[0].click();", add_btn)
        
    print("Clicked 'Add to cart' right from the search results!")
    
    # 4. Click "Go to Cart" (Right side panel or overlay)
    driver.implicitly_wait(0.5) # Prevent full 10s wait on missing fallbacks
    go_to_cart_clicked = False
    
    for _ in range(3):
        if go_to_cart_clicked: break
        try:
            side_cart_btn = driver.find_element(By.XPATH, "//span[@id='attach-sidesheet-view-cart-button']//input | //input[@aria-labelledby='attach-sidesheet-view-cart-button-announce']")
            driver.execute_script("arguments[0].click();", side_cart_btn)
            go_to_cart_clicked = True
        except:
            try:
                sw_gtc = driver.find_element(By.XPATH, "//a[@id='sw-gtc']")
                driver.execute_script("arguments[0].click();", sw_gtc)
                go_to_cart_clicked = True
            except:
                time.sleep(0.5)
                
    driver.implicitly_wait(3) # Restore nominal wait
    
    # Ultimate Fallback: The main top-right Cart icon
    if not go_to_cart_clicked:
        try:
            cart_icon = driver.find_element(By.ID, "nav-cart")
            driver.execute_script("arguments[0].click();", cart_icon)
        except: pass
            
    print("Automation Complete: Navigated to Cart!")
    
    # 5. Click Proceed to Buy
    driver.implicitly_wait(0.5) # Prevent 10s delay on exception fallback
    
    proceed_clicked = False
    for _ in range(12): # poll up to 6 seconds
        if proceed_clicked: break
        try:
            # Standard Proceed to Buy button
            proceed_btn = driver.find_element(By.NAME, "proceedToRetailCheckout")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_btn)
            time.sleep(0.5)
            proceed_btn.click()
            proceed_clicked = True
        except:
            try:
                # Fallback ID
                proceed_btn = driver.find_element(By.ID, "sc-buy-box-ptc-button")
                driver.execute_script("arguments[0].click();", proceed_btn)
                proceed_clicked = True
            except:
                time.sleep(0.5)
                
    driver.implicitly_wait(10) # Restore nominal wait
    print("Automation Complete: Proceed to Buy clicked!")
    time.sleep(5)
    
except Exception as e:
    print(f"Failed: {e}")
    driver.save_screenshot("error.png")
finally:
    driver.quit()