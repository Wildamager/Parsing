import json
data = {
    }

def create_subcategories_list(list):
    subcategory_list=[]
    for subcategory in list:
        subcategory_list.append(
            {
            'name': subcategory[0],
            'link': subcategory[1],
            }
        )
    return subcategory_list


def create_categories(category, subcategories):
    data[category] = []
    # print(subcategories_list)
    products = []
    
    for subcategory in subcategories:
        try:
            data[category].append(
                {
                'name': subcategory[0],
                'link': subcategory[1], 
                'image': subcategory[2],
                'subcategories': subcategory[3]
                }
            )
        except TypeError:
            data[category].append(
                {
                'name': subcategory[0],
                'link': subcategory[1], 
                'image': subcategory[2],
                'subcategories': subcategory[3],
                'products':subcategory[4]
                }
            )

# def create_products(value, link, image, name, price, description):
#     value['products'].append({
#         "link": link,
#         "image": image,
#         "name": name,
#         "price": price,
#         "description": description
#     })

def json_file(data):
    with open("data_file.json", "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)

def main():
    json_file(data)
