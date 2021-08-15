import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

def run_caribarang(inp): 
    inp = inp.replace(' ', '%20')

    r = requests.get(f"https://www.tokopedia.com/search?st=product&q={inp}", timeout=10, headers=headers)
    src = r.content

    soup = BeautifulSoup(src, "html.parser")

    links = soup.find_all("a", class_="pcv3__info-content css-1qnnuob")

    link_tokopedia = None
    nama_tokopedia = None
    harga_tokopedia = None

    for link in links:
        link_tokopedia = link['href']
        nama_tokopedia = link.find('div', class_="css-1f4mp12").text
        harga_tokopedia = link.find('div', class_="css-rhd610").text
        break
    
    return nama_tokopedia, harga_tokopedia, link_tokopedia
