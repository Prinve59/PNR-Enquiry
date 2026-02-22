from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_pnr_status(pnr_number):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(f"https://www.confirmtkt.com/pnr-status/{pnr_number}")
        time.sleep(5)
        
        result = {
            'pnr': pnr_number,
            'train_name': None,
            'train_number': None,
            'status': None,
            'station': None
        }
        
        # Get all text elements
        all_elements = driver.find_elements(By.XPATH, "//*[string-length(text()) > 0]")
        
        for elem in all_elements:
            text = elem.text.strip()
            
            # Train number and name (format: 12345 - Train Name)
            if text and '-' in text and text[0].isdigit() and len(text.split()[0]) >= 5:
                parts = text.split('-', 1)
                if parts[0].strip().isdigit():
                    result['train_number'] = parts[0].strip()
                    result['train_name'] = parts[1].strip() if len(parts) > 1 else None
            
            # Status (CNF, RAC, WL)
            if 'CNF' in text or 'RAC' in text or 'WL' in text:
                if not result['status'] or len(text) < len(result['status']):
                    result['status'] = text
            
            # Station codes (3-4 letter uppercase)
            if text.isupper() and 3 <= len(text) <= 4 and text.isalpha():
                if not result['station']:
                    result['station'] = text
        
        return result
    finally:
        driver.quit()

if __name__ == "__main__":
    pnr = "2510323163"
    status = get_pnr_status(pnr)
    
    print(f"PNR: {status['pnr']}")
    print(f"Train Number: {status['train_number']}")
    print(f"Train Name: {status['train_name']}")
    print(f"Status: {status['status']}")
    print(f"Station: {status['station']}")
