import re
import json
#from pymongo import MongoClient

#quantidade de produtos: 548,552

#Id:   0
#ASIN: 0771044445
#  discontinued product

#client = MongoClient("localhost",27017)

#	teste
#print(client.list_database_names())

print("Gerando os produtos...")
file = open("amazon-meta.txt","r") 
produtos = ""
for linha in file:
	produtos = produtos+linha
produtos = re.split(r'ASIN:',produtos)
file.close()

print("Gerando dados JSON...")

prod = []
for i in range(1,len(produtos)-1):
	id_v = len(produtos[i].split("\n") )
	
	if(re.search("discontinued", produtos[i].split("\n")[1] ) ):
		value = json.dumps({"Id": int((produtos[i].split("\n")[id_v-2]).split()[1])-1,
		"ASIN":  ( produtos[i].split("\n")[0] ).split(" ")[1]})
		prod.append(value)
	else:
		qtdS = len( (produtos[i].split("\n")[4]).split() )			#quantidade de similares
		qtdC = int((produtos[i].split("\n")[5]).split()[1] )		#quantidade de categorias
		qtdr = int((produtos[i].split("\n")[5+qtdC+1]).split()[2]) #quantidade de reviews

		#similar
		sim = []
		for j in range(qtdS-2):
			sim.append( (produtos[i].split("\n")[4]).split()[j+2] )
		
		#categorias
		cat = []
		for j in range(5+1,5+qtdC):
			cat.append( produtos[i].split("\n")[j] )

		#reviews
		reviews = []
		rev = re.split(r'reviews:',produtos[i])
		for j in range(1,len(rev[1].split("\n"))-4 ):
			reviews.append(rev[1].split("\n")[j])


		value = json.dumps({"Id": int((produtos[i].split("\n")[id_v-2]).split()[1])-1,
		"ASIN":  ( produtos[i].split("\n")[0] ),
		"title": ( produtos[i].split("\n")[1] ),
		"group": ( produtos[i].split("\n")[2] ).split()[1],
		"salesrank": int( ( produtos[i].split("\n")[3] ).split()[1] ),
		"similar": sim,
		"categories": int(( produtos[i].split("\n")[5] ).split()[1]),
		"categorias": cat,
		"reviews": reviews})
		prod.append(value)

print(prod[2])



'''
Id:   2
ASIN: 0738700797
  title: Candlemas: Feast of Flames
  group: Book
  salesrank: 168596
  similar: 5  0738700827  1567184960  1567182836  0738700525  0738700940
  categories: 2
   |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Earth-Based Religions[12472]|Wicca[12484]
   |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Earth-Based Religions[12472]|Witchcraft[12486]
  reviews: total: 12  downloaded: 12  avg rating: 4.5
    2001-12-16  cutomer: A11NCO6YTE4BTJ  rating: 5  votes:   5  helpful:   4
    2002-1-7  cutomer:  A9CQ3PLRNIR83  rating: 4  votes:   5  helpful:   5
    2002-1-24  cutomer: A13SG9ACZ9O5IM  rating: 5  votes:   8  helpful:   8
    2002-1-28  cutomer: A1BDAI6VEYMAZA  rating: 5  votes:   4  helpful:   4
    2002-2-6  cutomer: A2P6KAWXJ16234  rating: 4  votes:  16  helpful:  16
    2002-2-14  cutomer:  AMACWC3M7PQFR  rating: 4  votes:   5  helpful:   5
    2002-3-23  cutomer: A3GO7UV9XX14D8  rating: 4  votes:   6  helpful:   6
    2002-5-23  cutomer: A1GIL64QK68WKL  rating: 5  votes:   8  helpful:   8
    2003-2-25  cutomer:  AEOBOF2ONQJWV  rating: 5  votes:   8  helpful:   5
    2003-11-25  cutomer: A3IGHTES8ME05L  rating: 5  votes:   5  helpful:   5
    2004-2-11  cutomer: A1CP26N8RHYVVO  rating: 1  votes:  13  helpful:   9
    2005-2-7  cutomer:  ANEIANH0WAT9D  rating: 5  votes:   1  helpful:   1
'''