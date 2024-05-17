from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.redbull.com/tr-tr/athletes")
    page.goto("https://www.redbull.com/tr-tr/athletes?filter.countryCode=TR")
    page.get_by_role("button", name="Tümünü Reddet").click()
    page.get_by_label("Reset country Button").click()
    page.get_by_role("button", name="Daha fazlasını yükle").click()

    sayac = 0
    links = set()

    while True:
        try:
            # Playwright ile sayfa içeriğini alma
            page_content = page.content()
            
            # BeautifulSoup kullanarak HTML içeriğini analiz etme
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Hedef <li> etiketlerini bul
            target_class = "card-list__item"
            target_li_tags = soup.find_all('li', class_=target_class)
            
            # Her <li> etiketinin içindeki <a> etiketlerini bul
            for li_tag in target_li_tags:
                a_tags = li_tag.find_all('a')
                for a_tag in a_tags:
                    href = a_tag.get('href')  # href özelliğini al
                    if href:
                        links.add(href)
            
            # Sayfayı aşağı kaydır
            if sayac != 150:
                page.get_by_role("button", name="Daha fazlasını yükle").click()
                sayac += 1
                time.sleep(2)
            else:
                break
        except Exception as e:
            print("hata moruk")
            break

    # Linkleri link.txt dosyasına yazdır
    with open("link.txt", "w") as file:
        for link in links:
            file.write(link + "\n")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
