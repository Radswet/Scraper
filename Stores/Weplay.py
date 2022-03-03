from bs4 import BeautifulSoup
import requests
from utils import remove_words


def discover():
    page = 1
    product_urls = []

    website = 'https://www.weplay.cl/figuras-y-juguetes/funko-pop.html?p={}'

    while True:
        print("page ", page)
        url = website.format(page)
        result = requests.get(url)
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')

        products = soup.findAll('a', class_='product-item-link')

        if not products:
            break

        for product in products:
            product_urls.append(product['href'])

        page += 1

    return product_urls


def products(url):
    
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')

    try:
        sku = soup.find('div', {'itemprop': 'sku'}).text
        name = soup.find('span', {'itemprop': 'name'}).text.strip()
        price = remove_words(soup.find('span', {'class': 'price'}).text)

        table = soup.find(
            'table', {'style': 'border-collapse: collapse; width: 100%; height: auto;'})
        table_body = table.find('tbody')

        rows = table_body.findAll('tr')
        data = []

        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        PremiumOutlet = PlazaNorte = False
        for i in data:
            if len(i) == 2 and i[1] != 'Agotado':
                if i[0] == 'Premium Outlet':
                    PremiumOutlet = True
                if i[0] == 'Plaza Norte':
                    PlazaNorte = True
        if PlazaNorte or PremiumOutlet:
            product = {"name": name, "price": price,
                    "sku": sku, "url": url, "Premium Outlet": PremiumOutlet, "Plaza Norte": PlazaNorte}
            return product
    except:
        print("error 404")
    