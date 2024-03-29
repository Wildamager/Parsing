import json
data = {
    }

def create_categories(category, link):
    data[category] = {'link':link,
                      'products':[]}

def create_products(value, link, image, name, price, description):
    value['products'].append({
        "link": link,
        "image": image,
        "name": name,
        "price": price,
        "description": description
    })

def json_file(data):
    with open("data_file.json", "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)

def main():
    json_file(data)