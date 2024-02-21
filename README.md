First things first, we will have to call the libraries that we are going to use. These being:
```
import matplotlib.pyplot as plt  # Data visualization \n
import requests
from bs4 import BeautifulSoup  # Data extraction 
```
Now that we have the necessary libraries called, the first thing we are going to do is collect the information from a website. The website I am going to use is [books.toscrap.com](https://books.toscrape.com/).
However, we are not interested in the visual aspect of the website. What we really need is the html side of things.
Thankfully we have everything we need in a convenient form.
Now to slowly take apart the website to extract our data.
```
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
```
This code extracts data from the website, but it's important to note that it only scrapes until the nth page. It is crucial to change the variable n to a specific value; otherwise, the code will not work. Here is the loop for context:
```
for page_number in range(1, n): # change n to the desired value
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    data_scrap(url)
```
Now that we have all the data we require, time to put said data in a good formal so that we have easy access to it. To do so we are going to open a .txt file named book_data and store everything in a  {book_name}| {book_price[1::]}| {book_rating} form.
To use the data in our program I have decided to make a matrix which stores n matrices, each with the previously mentioned structure.	To do so I used:
```
data = []
with open('book_data.txt', 'r', encoding='utf-8') as text:
    for line in text:
        data.append(line.strip().split("| "))
```
Now to visualize the data I have decided to clean stuff up a little.
To do so I am making 3 arrays, each will store names, prices and ratings.
```
names = []
price = []
rating = []
for _ in range(len(data)):
    names.append(data[_][0][0:6])
    price.append(float(data[_][1][1::]))
    rating.append(int(data[_][2]))
```
Now to the interesting part where we visualize the data.
First we initialize a plot where we will be having data visualized. To do so:
```
fig, ax1 = plt.subplots(figsize=(15, 8))
```
Now to create a 3 variable graph I have chosen to do 2 graph overlapping. First with the data at hand I create a bar graph which represents the price related to the names. Like this:
```
# Bar graph
ax1.bar(names, price, color="blue")
ax1.set_xlabel("Book names")
ax1.set_ylabel("Price (£)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
```
Now a scatter graph representing the ratings related to names.
```
# Scatter graph
ax2 = ax1.twinx()
ax2.scatter(names, rating, color="red", marker='o')
ax2.set_ylabel("Ratings (1-5)", color="red")
ax2.set_yticks(constant_ratings_order)
```
And finally we overlap and show the final graph.
```
print(f"{names}\n{price}\n{rating}")
print(f"{len(names)}\n{len(price)}\n{len(rating)}")

ax1.set_xticks(names)
ax1.set_xticklabels(names, rotation=90, ha='right')
plt.show()
```
If we were to run the provided code, the code will analyze the first 2 pages and give us the following graph:
