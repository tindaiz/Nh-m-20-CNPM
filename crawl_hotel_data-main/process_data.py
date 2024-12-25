import pandas as pd 
import re

# def rebrand_location(location):
#     match = re.search(r'(\d+,\d+|\d+)(km|m)', location)
#     if match:
#         distance = match.group(1).replace(',', '')
#         unit = match.group(2)

#         if unit == "km":
#             return int(distance) * 1000  # Convert kilometers to meters
#         elif unit == "m":
#             return int(distance)

def format_score(score):
    # Handle cases with a comma
    score = re.sub(r'Đạt điểm\s*(\d{1,2}),(\d)', r'\1.\2', score)
    # Handle cases without a comma
    score = re.sub(r'Đạt điểm\s*(\d{1,2})\b', r'\1.0', score)
    return score

# reviews = {
#     'Xuất sắc' : 5,
#     'Tuyệt hảo' : 4,
#     'Tuyệt vời' : 3,
#     'Rất tốt' : 2,
#     'Tốt' : 1,
#     'Điểm đánh giá' : 0,
# }

# def rebrand_review(review):
#     for letter, number in reviews.items():
#         if letter in review:
#             review = int(re.sub(r'.+', str(number), review))
#             break
#     return review

# type_of_properties = {
#     1 : ['hotel', 'inn'],
#     2 : ['homestay', 'guest house', 'bnb', 'bed and breakfast'],
#     3 : ['resort', 'villa', 'spa', 'beach resort'],
#     #Ambious will also clarify as 1
# }

# def clarify_type(hotel):
#     hotel = hotel.lower()
#     for hotel_type, keywords in type_of_properties.items():
#         for keyword in keywords:
#             if keyword in hotel:
#                 return hotel_type
#     return 1

def main():
    data = pd.read_csv('hotels_list.csv')
    data['price'] = data['price'].apply(lambda x: int(re.sub(r'\D', '', x)))
    # data['address'] = data['address'].apply(lambda x: x.split(',')[-1].strip())
    # data['location'] = data['location'].apply(rebrand_location)
    data['score'] = data['score'].apply(lambda x: re.sub('\n.*', '', x))
    data['score'] = data['score'].apply(format_score)
    # data['avg review'] = data['avg review'].apply(rebrand_review)
    # data['reviews count'] = data['reviews count'].apply(lambda x: x.replace('No info', '0'))
    # data['reviews count'] = data['reviews count'].apply(lambda x: int(x) if '.' not in x else int(x.replace('.', '')))
    # data['type'] = data['hotel'].apply(clarify_type)
    # data['note'] = data['note'].apply(lambda x: x.type())
    data['avg review'] = data['avg review'].apply(lambda x: -1 if x == 'No info'  else x)
    data['score'] = data['score'].apply(lambda x: -1 if x == 'No info'  else x)
    data['reviews count'] = data['reviews count'].apply(lambda x: -1 if x == 'No info' else x)
    data['note'] = data['note'].apply(lambda x: 0 if pd.isna(x)  else 1)
    data = data.rename(columns={'note': 'beach'})
    data.drop('location', inplace=True, axis=1) 
    data.to_csv('processed_data.csv', index = False)

if __name__ == '__main__':
    main()
