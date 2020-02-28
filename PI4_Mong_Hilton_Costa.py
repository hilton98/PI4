from pymongo import MongoClient
from operator import itemgetter


client = MongoClient("localhost",27017)
db = client.Amazon

''' Geracao da colecao de dados
insercao e criacao do banco de dados feita no mongodb shell:
-use Amazon
-db.ini.insert * criacao de uma colecao generica para geracao da base de dados Amazon
*parser gera arquivo json: "python3 parser.py>amazon.json"
*no diretorio do arquivo json abrir terminal:
-mongoimport --db Amazon --collection produtosAmazon --file amazon.json
*geracao do collection produtosAmazon no db criado anteriormente Amazon
'''



#(a) Dado produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação

print("	5 comentários mais úteis e com maior avaliação")
value_aa =db.produtosAmazon.aggregate([{"$match":{"ASIN":"0738700797"} },{"$unwind": "$reviews"},\
 {"$sort": {"reviews.rating": -1,"reviews.helpful": -1} },\
 {"$project":{"_id":0 ,"id": "$id" ,"rating":"$reviews.rating","helpful": "$reviews.helpful"} },{"$limit": 5}])
print(list(value_aa))

print("	5 comentários mais úteis e com menor avaliação")
value_ab = db.produtosAmazon.aggregate([{"$match":{ "ASIN":"0738700797"} },{"$unwind":"$reviews"},\
	{"$sort": {"reviews.rating": 1,"reviews.helpful": -1}},\
	 {"$project":{"_id":0 ,"id": "$id","rating":"$reviews.rating", "helpful":"$reviews.helpful"}},{"$limit": 5}])
print(list(value_ab))


'''
#(b) Dado um produto, listar os produtos similares com maiores vendas do que ele
result = db.produtosAmazon.find_one( {"ASIN":"0738700797"},{"similar_items":1, "_id":0, "salesrank":1})
sales = int(result["salesrank"])

for i in range(len(result["similar_items"])):
	prods = db.produtosAmazon.find_one( {"ASIN":result["similar_items"][i]},{"ASIN":1, "_id":0, "salesrank":1, "title":1})
	if(sales > int(prods["salesrank"]) ):
		print(prods)
'''

'''
#(c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada

result = db.produtosAmazon.aggregate([{"$match":{"ASIN":"0738700797"} }, {"$unwind": "$reviews"},\
 {"$group": {"_id":"$reviews._date", "avgRating":{"$avg":"$reviews.rating"} } },\
	{"$project":{"_id":0,"data":"$_id","media":"$avgRating" }} ])

print(list(result))
'''



#(d) Listar os 10 produtos lideres de venda em cada grupo de produtos
'''
grupos = db.produtosAmazon.aggregate([{"$group": {"_id":"$group"}  } ])
grupos = list(grupos)
for i in range(len(grupos)):
	result =  db.produtosAmazon.aggregate([ {"$match":{"group":grupos[i]["_id"], "salesrank":{"$gte":'0'} } },\
	{"$group": {"_id": {"ASIN":"$ASIN", "grupo":"$group", "salesrank":"$salesrank"} } },\
	{"$sort":{"_id.salesrank":1} },{"$limit":10} ]) 
	for i in result:
		print(i)
	print()
'''

#(e) Listar os 10 produtos com a maior média de avaliações úteis positivas por grupo de produto
'''
result = db.produtosAmazon.aggregate([{"$unwind": "$reviews"},{"$group": {"_id": "$ASIN", "avgh": {"$avg": '$reviews.helpful'} } },\
 {"$project":{"_id":0,"ASIN":"$_id","avgh":1} } ,{"$sort": {"avgh": -1}},{"$limit": 10}])
print(list(result))
'''

'''
PRODUTO DE EXEMPLO

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