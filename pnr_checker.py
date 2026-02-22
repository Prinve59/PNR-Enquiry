from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

import re

def get_pnr_status(pnr_number):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/google-chrome'
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(f"https://www.confirmtkt.com/pnr-status/{pnr_number}")
        time.sleep(10)
        
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        print(f"DEBUG: Page text length: {len(page_text)}")
        print(f"DEBUG: First 500 chars: {page_text[:500]}")
        
        result = {
            'pnr': pnr_number,
            'train_name': None,
            'train_number': None,
            'origin_station': None,
            'origin_code': None,
            'dest_station': None,
            'dest_code': None,
            'date': None,
            'status': None,
            'coach': None,
            'seat': None
        }
        
        # Train number and name
        train_match = re.search(r'(\d{5})\s*-\s*([A-Z\s]+EXPRESS|[A-Z\s]+)', page_text)
        if train_match:
            result['train_number'] = train_match.group(1)
            result['train_name'] = train_match.group(2).strip()
        
        # Origin station
        origin_match = re.search(r'([A-Za-z\s]+)\s*-\s*([A-Z]{3,4}),\s*\d{2}:\d{2}', page_text)
        if origin_match:
            result['origin_station'] = origin_match.group(1).strip()
            result['origin_code'] = origin_match.group(2)
        
        # Destination station
        dest_match = re.search(r'([A-Za-z\s]+Junction|[A-Za-z\s]+)\s*-\s*([A-Z]{3,4}),\s*\d{2}:\d{2}', page_text)
        if dest_match:
            matches = re.findall(r'([A-Za-z\s]+(?:Junction)?)\s*-\s*([A-Z]{3,4}),\s*\d{2}:\d{2}', page_text)
            if len(matches) >= 2:
                result['dest_station'] = matches[1][0].strip()
                result['dest_code'] = matches[1][1]
        
        # Date
        date_match = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*(\d{1,2}\s+[A-Za-z]{3})', page_text)
        if date_match:
            result['date'] = date_match.group(2)
        
        # Status, Coach, Seat
        status_match = re.search(r'(CNF|RAC|WL)\s+([A-Z]\d+)\s+(\d+)', page_text)
        if status_match:
            result['status'] = status_match.group(1)
            result['coach'] = status_match.group(2)
            result['seat'] = status_match.group(3)
        
        return result
    finally:
        driver.quit()

if __name__ == "__main__":
    pnr = "2510323163"
    status = get_pnr_status(pnr)
    
    print(f"PNR: {status['pnr']}")
    print(f"Train: {status['train_number']} - {status['train_name']}")
    print(f"From: {status['origin_station']} ({status['origin_code']})")
    print(f"To: {status['dest_station']} ({status['dest_code']})")
    print(f"Date: {status['date']}")
    print(f"Status: {status['status']}")
    print(f"Coach: {status['coach']}")
    print(f"Seat: {status['seat']}")
