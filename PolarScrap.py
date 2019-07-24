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
	return s.replace("'"," ").replace("&"," ").replace("ñ","n")		

my_url = ['https://www.lapolar.cl/moda/ropa-hombre/chaquetas-parkas/','https://www.lapolar.cl/moda/ropa-mujer/chaquetas-parkas/',]

filename = "tablas/Polar.csv"

f = open(filename,"w")

headers = "item_id,categoria,nombre_de_producto,precio_de_producto,descuento,url_producto \n"

f.write(headers)

contador = 0

for i in my_url:

	uClient = uReq(i)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html,"html.parser")

	#recoje cada producto
	containers = page_soup.findAll("div",{"class":"product-tile__wrapper"})	



	for container in containers:

		item_id = container["data-pid"]

		title_container = container.find("div",{"class":"pdp-link"})

		product_name = title_container.a["data-product-name"]

		product_name = normalize(product_name)

		product_price = container.findAll("span",{"class":"price-value"})[0].text.strip()

		try:
			precio_normal = container.findAll("span",{"class":"price-value"})[1].text.strip()
		except IndexError:
			precio_normal = product_price	

		numeroPrecio = 	int(product_price.replace('$','').replace('.',''))
		normalPrecio = int(precio_normal.replace('$','').replace('.',''))
		numeroDescuento = normalPrecio - numeroPrecio

		descuento = '$'+str(int((numeroDescuento-numeroDescuento%1000)/1000))+'.'

		if str(int(numeroDescuento%1000))=='0' and numeroDescuento!=0:
			descuento = descuento + '000'
		elif str(int(numeroDescuento%1000))!='0':
			descuento = descuento+str(int(numeroDescuento%1000))
		elif numeroDescuento==0:
			descuento = '$'+str(numeroDescuento)

		product_url = 'https://www.lapolar.cl' + title_container.a["href"]
		
		image_url = container.find("a",{"class":"image-link"}).img["src"]

		if contador == 0:
			categoriaId = "PH"
		elif contador == 1:
			categoriaId = "PM"
		elif contador == 2:
			categoriaId =""
		elif contador ==3:
			categoriaId = ""
		elif contador == 4:
			categoriaId = ""
		elif contador ==5:
			categoriaId = ""
		elif contador == 6:
			categoriaId =""
		
		categoria = ""
		if contador == 0:
			categoria = "Parkas Hombre"
		elif contador == 1:
			categoria = "Parkas Mujer"
		elif contador == 2:
			categoria =""
		elif contador ==3:
			categoria = ""
		elif contador == 4:
			categoria = ""
		elif contador ==5:
			categoria = ""
		elif contador == 6:
			categoria =""	

		dl_jpg(image_url,'/home/shiru/Escritorio/pruebas raras/Scrap/Scraping/img_polar/',item_id+categoriaId)

		f.write(item_id+categoriaId + ","+categoria+","+product_name + "," + product_price + "," + descuento +","+ product_url + "\n")
	contador += 1	
f.close()		
