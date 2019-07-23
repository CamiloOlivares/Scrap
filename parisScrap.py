from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve 


#inicio de definicion de funcines
def dl_jpg(url,file_path,file_name):
	full_path = file_path+file_name+'.jpg'
	return urlretrieve(url,full_path)

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

my_url= ['https://www.paris.cl/mujer/moda-juvenil/chaquetas-parkas/','https://www.paris.cl/hombre/moda-juvenil/camisas/','https://www.paris.cl/hombre/moda-juvenil/jeans/','https://www.paris.cl/hombre/ropa-interior/boxers/','https://www.paris.cl/mujer/moda-juvenil/chaquetas-parkas/','https://www.paris.cl/mujer/moda-juvenil/jeans/','https://www.paris.cl/mujer/ropa-interior/calzones/']

#Creo un documento vacio
filename = "tablas/Paris.csv"

f = open(filename,"w")

headers = "item_id,categoria,nombre_de_producto,precio_de_producto,precio_normal,url_producto \n"

f.write(headers)
# abriendo una conexión, obteniendo la página web
contador = 0
for i in my_url:
	uClient = uReq(i)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html,"html.parser")

	#recoje cada pregunto
	containers = page_soup.findAll("div",{"class":"product-tile"})



	for container in containers:


		item_id=container["data-itemid"]
		#name selection
		title_container = container.find("a",{"class":"thumb-link js-product-layer"}) 
		product_name = normalize(title_container["title"])

		#product price
		try:
			price_container = container.findAll("div",{"class":"item-price offer-price price-tc default-price"})
			product_price = price_container[0].text.strip()
			product_discount = ""
		except IndexError:
			price_container = container.findAll("div",{"class":"item-price offer-price price-tc cencosud-price"})
			product_price = price_container[0].text.strip()		
		
		try:
			precioNormal = container.find("span",{"itemprop":"price"}).text.strip()
		except AttributeError:
			precioNormal = '$0' 					
		#product_url
		url_container = container.find("a",{"class":"js-product-layer"})
		product_url = url_container["href"]

		imageContainer = container.find("div",{"class":"box-image-product"})

		imageContainer=imageContainer.find("img",{"class":"img-prod lazy"})

		image_url=imageContainer["data-src"]
		descargaExitosa = ('','')
		categoriaId = ""
		if contador == 0:
			categoriaId = "PH"
		elif contador == 1:
			categoriaId = "CH"
		elif contador == 2:
			categoriaId ="JH"
		elif contador ==3:
			categoriaId = "BH"
		elif contador == 4:
			categoriaId = "PM"
		elif contador ==5:
			categoriaId = "JM"
		elif contador == 6:
			categoriaId ="Cal"
		descargaExitosa = dl_jpg(image_url,'/home/shiru/Escritorio/pruebas raras/Scrap/Scraping/img_paris/',item_id+categoriaId)


		#print("product_name" + product_name)
		#print("product_price" + product_price)
		#print("product_url" + product_url)

		categoria = ""
		if contador == 0:
			categoria = "Parkas Hombre"
		elif contador == 1:
			categoria = "Camisas Hombre"
		elif contador == 2:
			categoria ="Jeans Hombre"
		elif contador ==3:
			categoria = "Boxers Hombre"
		elif contador == 4:
			categoria = "Parkas Mujer"
		elif contador ==5:
			categoria = "Jeans Mujer"
		elif contador == 6:
			categoria ="Calzones"			
					
		if product_price != "N/A" and descargaExitosa[1]!='':
			f.write(item_id+categoriaId + ","+categoria+","+product_name + "," + product_price + "," + precioNormal +","+ product_url + "\n")
	contador += 1		
f.close()

 



