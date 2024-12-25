from playwright.sync_api import sync_playwright
import pandas as pd
import time
import json

def load_cookies(context):
    with open('cookies.json', "r") as f:
        cookies = json.load(f)
        context.add_cookies(cookies)

def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2025-01-10'
        checkout_date = '2025-01-11'
        locations = ['Hội An']
        locations = ["An Giang", "Bà Rịa - Vũng Tàu", "Bạc Liêu", "Bắc Kạn", "Bắc Giang", 
                "Bắc Ninh", "Bến Tre", "Bình Dương", "Bình Định", "Bình Phước", 
                "Bình Thuận", "Cà Mau", "Cao Bằng", "Cần Thơ", "Đà Nẵng", 
                "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", 
                "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh", 
                "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", 
                "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", 
                "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", 
                "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", 
                "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", 
                "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa", 
                "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", 
                "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]
        hotels_list = []

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        load_cookies(context)

        for location in locations:
            print(f'Fetching for {location}')
        
            page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=VND&ss={location}&ssne={location}&ssne_untouched={location}&lang=vi&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

            page = context.new_page()            
            page.goto(page_url, timeout=6000)

            time.sleep(5)

            

            scroll_pause_time = 5 
            
            last_height = page.evaluate("document.body.scrollHeight")

            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            load_more = 8

            for i in range(load_more):

                hotels = page.locator('//div[@data-testid="property-card"]').all()

                print(f'{(i + 1) * 75} hotels')

                for hotel in hotels:
                    try:
                        hotel_dict = {}
                        hotel_dict['hotel'] = hotel.locator('div[data-testid="title"]').inner_text()
                        # print('0')
                        h3_element = hotel.locator('h3.aab71f8e4e')
                        hotel_url = h3_element.locator('a').get_attribute('href')
                        hotel_dict['url'] = hotel_url
                        try:
                            hotel_dict['image_url'] = hotel.locator('img').get_attribute('src')
                        except:
                            hotel_dict['image_url'] = 'None'
                        # print('1')
                        hotel_dict['price'] = hotel.locator('span[data-testid="price-and-discounted-price"]').inner_text()
                        # print('2')
                        hotel_dict['address'] = hotel.locator('span[data-testid="address"]').inner_text()
                        # print('3')
                        hotel_dict['location'] = hotel.locator('span[data-testid="distance"]').inner_text() if hotel.locator('span[data-testid="distance"]').is_visible() else 'None'
                        # print('4')
                        hotel_dict['note'] = hotel.locator('span.abf093bdfe.b058f54b9a').inner_text() if hotel.locator('span.abf093bdfe.b058f54b9a').is_visible() else 'None'
                        # print('5')
                        hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text() if hotel.locator('//div[@data-testid="review-score"]/div[1]').is_visible() else 'No info'
                        # print('6')
                        hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text() if hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').is_visible() else 'No info'
                        # print('7')
                        hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0] if hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').is_visible() else 'No info'
                        # print('8')
                        hotel_dict['property'] = hotel.locator('div[class="abf093bdfe"]').inner_text() if hotel.locator('div[class="abf093bdfe"]').is_visible() else 'No info'
                        # print('9')
                        hotels_list.append(hotel_dict)

                    except Exception as e:
                        print(f"Error extracting data for a hotel: {e}")
                        continue
                
                print('Done! Next batch or end.')


                load_more_button = page.locator('button:has-text("Tải thêm kết quả")')
                if load_more_button.is_visible():
                    load_more_button.click()
                    time.sleep(5)

                    last_height = page.evaluate("document.body.scrollHeight")

                    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time)
                else:
                    break

            page.close()
                

            
            
            # print(f'There are: {len(hotels)} hotels in {location}.')
        browser.close()

        
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        
        
            
if __name__ == '__main__':
    main()