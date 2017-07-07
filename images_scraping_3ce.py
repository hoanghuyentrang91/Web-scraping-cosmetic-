# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 21:35:13 2017

@author: kara

README:
    - Remember to change to corresponding BASE_URL and directory
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import sleep # be nice
import os
import csv
import string

# This function is used to parse html file to lxml file
def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")

#============================= Change part ====================================
BASE_URL = "http://stylenanda.com/product/list.html?cate_no=496"
os.chdir('C:\\Users\\min\\Desktop\\karacos\\product\\tool\\others\\3ce')
prefixId = '3CEToolOthers'
dir_name = prefixId
brand = "CE"
#==============================================================================
    
    
soup = make_soup(BASE_URL)  

# Write info to .csv file. Info are name, price, image url of product
info_imageurl = []
info_name = []
info_price = []

# Write info to .txt file
info = []
n=0
#============================= Change part ====================================
# Fixed variables: name, price, imageurl
#==============================================================================
checkPart = soup.find("ul","prdList column3")
for item in checkPart.findAll("li"):
    
    # Get product's image url
    img = item.find("img")
    imageurl = 'http:' + str(img.get("src")) 
  
        
    # Get name of product    
    namepart = item.find("p",class_="name")
    if (namepart is not None):
        nametemp = str(namepart.text)
        # Check if there is any special characters in nametemp, change that character to "_"
        invalidChars = set(string.punctuation.replace("_", ""))
        for i in range(0,len(nametemp)):
            if (nametemp[i] == '\n'):
                nametemp = nametemp[0:(i-1)]
                for i in range(0,len(nametemp)):
                    if (nametemp[i] in invalidChars):
                        nametemp = nametemp.replace(nametemp[i],'_',1)
                break
        name = nametemp   
    else:
        break

    
    # Get price of product
    prc = item.find("p",class_="price")
    if (prc is not None):
        price = prc.text
    else:
        break

    
    #=========================== Fixed part ===================================    
    # Download images and store it in the corresponding folder:
    imagefile = open(prefixId + str(n+1) + ".gif","wb")
    n = n+1;
    imagefile.write(urlopen(imageurl).read())
    imagefile.close()
    
    # # Write info to .csv file  
    info_name.append(name)
    info_price.append(price)
    info_imageurl.append(imageurl)
    
    # Write info to .txt file
    info.append(name)
    info.append(price)
    info.append(imageurl)
    
    sleep(0.1)


#=============================== Fixed part ===================================

# Write info to .csv file 
with open(dir_name + ".csv",  'w', encoding='euc-kr', newline='') as csvfile:
    fieldnames = ['Name', 'Price', 'Image URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for i in range(0,len(info_name)):
        writer.writerow({'Name': info_name[i],'Price': info_price[i], 'Image URL': info_imageurl[i]})

 
# Write info to .txt file
infofile = open(dir_name + ".txt","w")
for each in info:
    infofile.write(each)
    infofile.write('\n\n')
infofile.close()


# Write info to .xml file 
import xml.etree.cElementTree as ET

root = ET.Element("ALL")
brandElement = ET.SubElement(root, brand)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

for i in range(0,len(info_name)):
  itemElement = ET.SubElement(brandElement, "ITEM")
  ET.SubElement(itemElement, "ID").text = prefixId + str(i+1)
  ET.SubElement(itemElement, "NAME").text = info_name[i]
  ET.SubElement(itemElement, "PRICE").text = info_price[i]
  ET.SubElement(itemElement, "IMAGE").text = prefixId + str(i+1) + ".gif"

tree = ET.ElementTree(root)
indent(root)
tree.write(dir_name + ".xml", encoding="utf-8", xml_declaration=True)

   
   
    
    
    
    
    
    
    