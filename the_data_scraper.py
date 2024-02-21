import matplotlib.pyplot as plt 
import requests
from bs4 import BeautifulSoup

constant_ratings_order = [1, 2, 3, 4, 5]
rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def data_scrap(url):
    with open('book_data.txt', 'w') as file:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('h3')
        ratings = soup.select('.star-rating')
        prices = soup.select('.price_color')

        for title, price, rating in zip(titles, prices, ratings):
            book_name = title.a['title']
            book_price = price.get_text(strip=True)
            word_rating = rating['class'][1]
            book_rating = rating_dict[word_rating]
            with open("book_data.txt", 'a', encoding='utf-8') as f:
                f.write(f"{book_name}| {book_price[1::]}| {book_rating}\n")

# Update the loop to make requests to each page
for page_number in range(1, 2):
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    data_scrap(url)

data = []
with open('book_data.txt', 'r', encoding='utf-8') as text:
    for line in text:
        data.append(line.strip().split("| "))

names = []
price = []
rating = []

for _ in range(len(data)):
    names.append(data[_][0][0:6])
    price.append(float(data[_][1][1::]))
    rating.append(int(data[_][2]))

fig, ax1 = plt.subplots(figsize=(15, 8))

# Bar graph
ax1.bar(names, price, color="blue")
ax1.set_xlabel("Book names")
ax1.set_ylabel("Price (£)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Scatter graph
ax2 = ax1.twinx()
ax2.scatter(names, rating, color="red", marker='o')
ax2.set_ylabel("Ratings (1-5)", color="red")
ax2.set_yticks(constant_ratings_order)

print(f"{names}\n{price}\n{rating}")
print(f"{len(names)}\n{len(price)}\n{len(rating)}")

ax1.set_xticks(names)
ax1.set_xticklabels(names, rotation=90, ha='right')
plt.show()
