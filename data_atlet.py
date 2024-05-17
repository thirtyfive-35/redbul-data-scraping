import re
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import time

def run(playwright) -> None:
    data_atlet = []
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    sayac = 0
    with open("link.txt",'r',encoding='latin-1') as file:
        for line in file:
            sayac += 1
            line = "https://www.redbull.com" + line.strip()
            page.goto(line)
            page.wait_for_load_state('load')  # Sayfanın yüklenmesini bekleyin
            time.sleep(1.5)
            print(sayac)
            
            page_content = page.content()
            soup = BeautifulSoup(page_content, 'html.parser')

            target_class_table = "facts__table"
            target_table = soup.find('table', class_=target_class_table)

            if target_table is None:
                data_atlet.append("-")
                print("Hedef tablo bulunamadı.")
                continue

            target_tr = target_table.find_all('tr')

            target_element_name = soup.find('cosmos-title-7-9-0', class_="person-hero-view__name")

            cosmos_element = soup.find('cosmos-title-7-9-0', class_="person-hero-view__name")

            if cosmos_element:
                # Cosmos elementinin içeriğini alıyoruz
                content = cosmos_element.get_text(separator=" ")
                
                # İçeriği <br> etiketine göre ayırma
                names = content.split("<br>")
                
                # İsimleri yazdırma
                for name in names:
                    fullname = name.strip()  # Metindeki boşlukları kaldırmak için strip() kullanıyoruz
            else:
                print("Hedef element bulunamadı.")
                data_atlet.append("-")
                continue
            #print(fullname)

            input_text= ""

            for tr_tag in target_tr:
                th_tag = tr_tag.find('th')
                td_tag = tr_tag.find('td')

                if th_tag is not None and td_tag is not None:
                    input_text += th_tag.get_text(strip=True) + ":" + td_tag.get_text(strip=True) + ","

            input_text = input_text + "fullname:" + fullname
            data_atlet.append(input_text)
            
            #print(input_text)
    
    with open("data.txt", "w",encoding="utf-8") as file:
        for link in data_atlet:
            file.write(link + "\n")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
