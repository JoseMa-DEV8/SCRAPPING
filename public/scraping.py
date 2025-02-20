import csv
import json
import webbrowser
import os
import feedparser
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configurar Selenium con Chrome en modo headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=options)
url = "https://topflex-web.com/"
browser.get(url)
soup = BeautifulSoup(browser.page_source, "html.parser")
browser.quit()

# Extraer imágenes, títulos y precios
images = [img["src"] for img in soup.find_all("img", class_="attachment-woocommerce_thumbnail")]
titles = [title.get_text(strip=True) for title in soup.find_all("h2", class_="woocommerce-loop-product__title")]
prices = [price.get_text(strip=True) for price in soup.find_all("bdi")]

# Crear lista de productos
productos = [{"Imagen": images[i], "Título": titles[i], "Precio": prices[i]} for i in range(min(len(images), len(titles), len(prices)))]

# Guardar en CSV
csv_file = "productos.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Imagen", "Título", "Precio"])
    writer.writeheader()
    writer.writerows(productos)

# Guardar en JSON
json_file = "productos.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(productos, f, indent=4, ensure_ascii=False)

# Obtener noticias desde feeds RSS y ATOM
RSS_FEED_URL = "https://www.mundodeportivo.com/rss/futbol.xml"
rss_feed = feedparser.parse(RSS_FEED_URL)
ATOM_FEED_URL = "https://www.nbamaniacs.com/feed/atom/"
atom_feed = feedparser.parse(ATOM_FEED_URL)

# Generar HTML
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noticias y Productos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: url('./champions.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            width: 300px;
        }
        .card img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }
        h1 {
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            color: green;
        }
        /* Estilo para el contenedor de noticias */
        .news-container {
            display: flex;
            flex-wrap: wrap; /* Permite múltiples filas si no caben en una sola */
            gap: 20px;
            justify-content: center;
        }
        .news-card {
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 10px;
            width: 300px; /* Ancho fijo para cada tarjeta */
            text-align: left;
        }
        .news-card h3 {
            font-size: 18px;
        }
        .news-card p {
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>TopFlex - Noticias y Productos</h1>
    
    <div class="container">
"""
# Agregar productos
for producto in productos:
    html_content += f"""
        <div class="card">
            <img src="{producto['Imagen']}" alt="{producto['Título']}">
            <h3>{producto['Título']}</h3>
            <p><strong>{producto['Precio']}</strong></p>
        </div>
    """
html_content += """
    </div>
    <h2>📰 Últimas Noticias (RSS)</h2>
    <div class="news-container">
"""
# Agregar noticias RSS con imágenes
for entry in rss_feed.entries[:5]:
    img_url = None
    if "media_content" in entry and entry.media_content:
        img_url = entry.media_content[0]['url']
    elif "enclosures" in entry and entry.enclosures:
        img_url = entry.enclosures[0]['href']
    elif "summary" in entry:
        match = re.search(r'<img.*?src=["\'](.*?)["\']', entry.summary)
        if match:
            img_url = match.group(1)
    html_content += f"""
        <div class="card">
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            {'<img src="' + img_url + '" alt="Imagen Noticia" style="width:100%;border-radius:10px;">' if img_url else ''}
            <p>{entry.summary[:100]}...</p>
        </div>
    """
# Agregar noticias ATOM con el mismo formato que las RSS
html_content += """
    </div>
    <h2>📰 Últimas Noticias (ATOM)</h2>
    <div class="news-container">
"""
for entry in atom_feed.entries[:5]:
    img_url = None
    if "media_content" in entry and entry.media_content:
        img_url = entry.media_content[0]['url']
    elif "enclosures" in entry and entry.enclosures:
        img_url = entry.enclosures[0]['href']
    elif "summary" in entry:
        match = re.search(r'<img.*?src=["\'](.*?)["\']', entry.summary)
        if match:
            img_url = match.group(1)
    html_content += f"""
        <div class="card">
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            {'<img src="' + img_url + '" alt="Imagen Noticia" style="width:100%;border-radius:10px;">' if img_url else ''}
            <p>{entry.summary[:100]}...</p>
        </div>
    """
html_content += """
    </div>

html_content += """
    <div id="mapa" class="mapa">
        
        <iframe 
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3306.033277403239!2d-118.26982902448391!3d34.043017473160404!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x80c2c7b85dea2a93%3A0x1ff47c3ceb7bb2d5!2sCrypto.com%20Arena!5e0!3m2!1ses!2ses!4v1740074619673!5m2!1ses!2ses" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </iframe>
    </div>"""

# Guardar y abrir el HTML
temp_html = "news_scraping.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)
webbrowser.open("file://" + os.path.abspath(temp_html))
print("✅ Página generada: news_scraping.html (se abrirá en el navegador)")
