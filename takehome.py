import copy

class Product:
	numProds = 0

	def __init__(self, prodName, manu, model, family, date):
		self.prodName = prodName
		self.manu = manu
		self.model = model
		self.family = family
		self.date = date
		Product.numProds += 1

	def printProd(self):
		print("{\"product_name\":\"" + self.prodName + "\",\"manufacturer\":\"" + self.manu + "\",\"model\":\"" + self.model + "\",\"family\":\"" + self.family + "\",\"announced-date\":\"" + self.date + "\"}")

class Listing:
	numListings = 0

	def __init__(self, title, manu, curr, price):
		self.title = title
		self.manu = manu
		self.curr = curr
		self.price = price
		Listing.numListings += 1

	def printListing(self):
		print("{\"title\":\"" + self.title + "\",\"manufacturer\":\"" + self.manu + "\",\"currency\":\"" + self.curr + "\",\"price\":\"" + self.price + "\"}")

# Reads products and Listings from there files
def readProdsAndListings():
	with open("products.txt", "r") as productsFile:
		for line in productsFile:
			line = line.strip()
			line = line[1:-1]         # remove curly braces on the begining and end of lines
			fields  = line.split(",")

			prodName = ""
			manu = ""
			model = ""
			family = ""
			date = ""

			for field in fields:
				item = field.split(":", 1)
				name = item[0][1:-1]          # removes quotes
				value = item[1][1:-1]

				if name == "product_name":
					prodName = value
				elif name == "manufacturer":
					manu = value
				elif name == "model":
					model = value
				elif name == "family":
					family = value
				elif name == "announced-date":
					date = value

			product = Product(prodName, manu, model, family, date)
			if manu.lower() not in manufacturers:
				manufacturers.append(manu.lower())
			#product.printProd()
			products.append(copy.deepcopy(product))

	with open("listings.txt", "r") as listingsFile:
		for line in listingsFile:
			line = line.strip()
			line = line[1:-1]
			fields  = line.split("\",\"")

			title = ""
			manu = ""
			curr = ""
			price = ""

			for field in fields:
				item = field.split(":", 1)
				name = item[0]
				value = item[1]
				
				#removes trailing and preceding quotes
				if (name[0] == '"' and name[len(name)-1] == '"' and name[len(name)-2] != '\\'):
					name = name[1:-1]
				elif (name[len(name)-1] == '"' and name[len(name)-2] != '\\'):
					name = name[:-1]

				if (value[0] == '"' and value[len(value)-1] == '"' and value[len(value)-2] != '\\'):
					value = value[1:-1]
				elif (value[0] == '"'):
					value = value[1:]

				if name == "title":
					title = value
				elif name == "manufacturer":
					manu = value
				elif name == "currency":
					curr = value
				elif name == "price":
					price = value

			listing = Listing(title, manu, curr, price)
			#listing.printListing()
			listings.append(copy.deepcopy(listing))
			
			# store listings in a dictionary by valid manufacturer
			for validManu in manufacturers:
				if validManu in manu.lower():
					if validManu not in relevantListings:
						newListingsByManu = [listing]
						relevantListings[validManu] = newListingsByManu
						break
					else:
						listingsByManu = relevantListings[validManu]
						listingsByManu.append(listing)
						relevantListings[validManu] = listingsByManu
						break



# Used to write products back to a file in the same format as the original text file
# so I can dif them and make sure I parsed the info correctly
def writeProdFile():
	o = open("output.txt", "w")
	for i in range(0, Product.numProds):
		if products[i].family == "":
			o.write("{\"product_name\":\"" + products[i].prodName + "\",\"manufacturer\":\"" + products[i].manu + "\",\"model\":\"" + products[i].model + "\",\"announced-date\":\"" + products[i].date + "\"}\n")
		else:
			o.write("{\"product_name\":\"" + products[i].prodName + "\",\"manufacturer\":\"" + products[i].manu + "\",\"model\":\"" + products[i].model + "\",\"family\":\"" + products[i].family + "\",\"announced-date\":\"" + products[i].date + "\"}\n")
	o.close()

def writeListFile():
	o = open("output.txt", "w")
	for i in range(0, Listing.numListings):
		o.write("{\"title\":\"" + listings[i].title + "\",\"manufacturer\":\"" + listings[i].manu + "\",\"currency\":\"" + listings[i].curr + "\",\"price\":\"" + listings[i].price + "\"}\n")
	o.close()

# used to see the difference in format of manufacturers in listings and products
def printAllManus():
	prodManus = {}
	listManus = {}
	for prod in products:
		if prod.manu not in prodManus:
			prodManus[prod.manu] = 1;
		else:
			prodManus[prod.manu] = prodManus[prod.manu] + 1;

	for listing in listings:
		if listing.manu not in listManus:
			listManus[listing.manu] = 1;
		else:
			listManus[listing.manu] = listManus[listing.manu] + 1;

	prodFile = open("productManufacturers.txt", "w")
	listFile = open("listingManufacturers.txt", "w")

	for key, value in prodManus.items():
		prodFile.write(key + "\n")

	for key, value in listManus.items():
		listFile.write(key + "\n")

	prodFile.close()
	listFile.close()

# matches products to listings
def match():
	for prod in products:
		if prod.manu.lower() in relevantListings:
			listings = relevantListings[prod.manu.lower()]

			for listing in listings:
				if (prod.model != "" and prod.model.lower() in listing.title.lower()) and (prod.family != "" and prod.family.lower()):
					if prod.prodName not in results:
						resultsForProd = [listing]
						results[prod.prodName] = resultsForProd
					else:
						resultsForProd = results[prod.prodName]
						resultsForProd.append(listing)
						results[prod.prodName] = resultsForProd

def printResults():
	o = open("results.txt", "w")

	for prodName, listings in results.items():
		o.write("{\"product_name\": \"" + prodName + "\", \"listings\": [")
		for i, listing in enumerate(listings):
			if i == len(listings) - 1:
				o.write("{\"title\": \"" + listing.title + "\", \"manufacturer\": \"" + listing.manu + "\", \"currency\": \"" + listing.curr + "\", \"price\": \"" + listing.price + "\"}")
			else:
				o.write("{\"title\": \"" + listing.title + "\", \"manufacturer\": \"" + listing.manu + "\", \"currency\": \"" + listing.curr + "\", \"price\": \"" + listing.price + "\"}, ")

		o.write("]}\n")
	o.close()


# Start #
products = []             # List of all products
listings = []             # List of all listings
relevantListings = {}     # Dictionary that holds a list of listings with key as manufacturer
manufacturers = []        # List of manufacturers
results = {}

readProdsAndListings()
match()
printResults()


