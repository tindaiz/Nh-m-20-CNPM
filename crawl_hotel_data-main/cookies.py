import json
import time
from playwright.sync_api import sync_playwright

COOKIE_FILE = "cookies.json"

def save_cookies(context):
    cookies = context.cookies()
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f)
    print("Cookies saved to file.")

def main():
    
    with sync_playwright() as p:

        checkin_date = '2024-12-01'
        checkout_date = '2024-12-02'
        location = 'Hà Nội'

        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=VND&ss={location}&ssne={location}&ssne_untouched={location}&lang=vi&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(page_url, timeout=60000)

        time.sleep(15)

        save_cookies(context)
        browser.close()

if __name__ == '__main__':
    main()

