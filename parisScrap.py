from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve 


#inicio de definicion de funcines
def dl_jpg(url,file_path,file_name):
	full_path = file_path+file_name+'.jpg'
	urlretrieve(url,full_path)

def normalize(s):
	replacements = (
			("á","a"),
			("é","e"),
			("í","i"),
			("ó","o"),
			("ú","u"),
		)
	for a,b in replacements:
		s = s.replace(a,b).replace(a.upper(),b.upper())
	return s.replace("'"," ").replace("&"," ")		

#termino de definicion de funciones

my_url='https://www.paris.cl/mujer/moda-juvenil/chaquetas-parkas/'

# abriendo una conexión, obteniendo la página web
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html,"html.parser")

#recoje cada pregunto
containers = page_soup.findAll("div",{"class":"product-tile"})

filename = "tablas/parkasM.csv"

f = open(filename,"w")

headers = "item_id,categoria,nombre_de_producto,precio_de_producto,url_producto \n"

f.write(headers)

for container in containers:


	item_id=container["data-itemid"]
	#name selection
	title_container = container.find("a",{"class":"thumb-link js-product-layer"}) 
	product_name = normalize(title_container["title"])

	#product price
	try:
		price_container = container.findAll("div",{"class":"item-price offer-price price-tc default-price"})
		product_price = price_container[0].text.strip()
	except IndexError:
		price_container = container.findAll("div",{"class":"item-price offer-price price-tc cencosud-price"})
		product_price = price_container[0].text.strip()		
			

	

	#product_url
	url_container = container.find("a",{"class":"js-product-layer"})
	product_url = url_container["href"]

	imageContainer = container.find("div",{"class":"box-image-product"})

	imageContainer=imageContainer.find("img",{"class":"img-prod lazy"})

	image_url=imageContainer["data-src"]

	dl_jpg(image_url,'/home/shiru/Escritorio/pruebas raras/Scrap/Scraping/img_paris_parkasM/',item_id)


	#print("product_name" + product_name)
	#print("product_price" + product_price)
	#print("product_url" + product_url)

	if product_price != "N/A" :
		f.write(item_id + ","+"Parkas Mujer"+","+product_name + "," + product_price + "," + product_url + "\n")

f.close()

 



