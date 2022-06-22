import requests
from bs4 import BeautifulSoup


regex = r"^\s*(\d*)\s"
lista=[]
number = 2

site="http://192.168.50.10:8080/memq/server/queues/lista/enqueue/"



#for number in range (1,2): 
#target = "all_targets_S{:03}".format(number)
target = "all_targets_S{:03}".format(number)
url = f"https://tess.mit.edu/wp-content/uploads/{target}_v1.txt"
print (url)
res = requests.get(url)
nums = [x.split("\t")[0] for x in res.text.split("\n")]
        
for n in nums:                    
    try:
        toi=(int(n.strip()))            
        lista.insert(number,toi)
        resposta = requests.post(site,str(toi))
        print(resposta.text)

    except:
        print("Bad Format")

