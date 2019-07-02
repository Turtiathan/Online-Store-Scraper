import urllib.request
from bs4 import BeautifulSoup
import csv

class Scraper:
	def __init__(self, site):
		self.site = site
		self.products_info = {}

	def scrape_product_info(self, product_url):
		"""
		Takes the url to a product's page and scrapes its information.
		Output is a dictionary containing the product's name as the key and the price and
		description as the value.
		"""
		r = urllib.request.urlopen(product_url)
		soup = BeautifulSoup(r.read(), "html.parser")
		product_name = soup.find("h1").text
		product_price = soup.find("span", {"class": "Z1WEo3w"}).text
		product_description = soup.select(".WlVrD > div")[0].text # The div containing the description is nested under another div.

		self.products_info[product_name] = [product_price, product_description]

	def scrape_store(self):
		"""
		Scrapes an online store's product listings.
		It takes each product's own url link one by one and sends it to the function, scrape_product_info(), to get that product's info.
		"""
		r = urllib.request.urlopen(self.site)
		html = r.read()
		parser = "html.parser"
		sp = BeautifulSoup(html, parser)
		for a in sp.find_all("a", href=True):
			link = a["href"]
			if "Z1craAD tm40B rNJmn" in str(a):
				self.scrape_product_info("https://shop.nordstrom.com" + link)

	def write_to_csv(self):
		"""
		Takes the self.products_info dictionary, that contains the products' information, and uploads the data to a csv file.
		The csv file has all the scraped products' names, prices, and descriptions.
		"""
		with open("products.csv", 'w', newline='') as f:
			write = csv.writer(f)
			write.writerow(["Name", "Price", "Description"])

			for product, info in self.products_info.items():
				write.writerow([product, info[0], info[1]])

	def search_product(self, product_name):
		"""
		Performs a search for the target product to see if it's in the csv file.
		If the product exists, this function returns information relating to that product.
		"""
		with open("products.csv") as file:
			reader = csv.reader(file)

			for row in reader:
				if row[0] == product_name:	
					print(product_name + ": " + row[1] + " " + row[2])
					return
					
		print(product_name + " does not exist.")
		return

scrape = Scraper("https://shop.nordstrom.com/c/all-bed-bath-home-decor?campaign=0610hpcathome&jid=oj010436-9473&cid=4q63w&cm_sp=merch-_-corp_9473_oj010436-_-hp_corp_p10_shop&")
scrape.scrape_store()
scrape.write_to_csv()
scrape.search_product("Wallet Card Tracker")
scrape.search_product("I don't exist. Bwahahahaha!")


