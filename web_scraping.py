import requests
from bs4 import BeautifulSoup


regex = r"^\s*(\d*)\s"
lista=[]
number = 1
for number in range (1,54): 
    target = "all_targets_S{:03}".format(number)
    url = f"https://tess.mit.edu/wp-content/uploads/{target}_v1.txt"
    print (url)
    res = requests.get(url)
    nums = [x.split("\t")[0] for x in res.text.split("\n")]
    
    for n in nums:        
        try:
            toi=(int(n.strip()))            
            lista.insert(number,toi)
            print ("In the Sector ", number)
            print(" We get the TOI ",toi)
        except:
            pass 


