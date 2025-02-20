import os
import webbrowser
import feedparser

# URL del Feed RSS y ATOM (puedes cambiarlo a otro sitio de noticias)
RSS_FEED_URL = " https://www.mundodeportivo.com/"  # Fuente RSS
ATOM_FEED_URL = "https://www.mundodeportivo.com/"  # Fuente ATOM

# Obtener datos del feed RSS
rss_feed = feedparser.parse(RSS_FEED_URL)
atom_feed = feedparser.parse(ATOM_FEED_URL)

# Generar HTML
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noticias y Scraping</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>

    <div class="banner">
        <h1>Bienvenido a nuestras noticias para nada robadas de otro periodicos</h1>
        <p>Si te gustan las noticias para nada robadas de otros periodicos, este es tu sitio.</p>
    </div>

    <h2>📰 Últimas Noticias sobre tecnologia (RSS)</h2>
    <div class="news-container">
"""

# Agregar noticias RSS
for entry in rss_feed.entries[:60]:  # Solo las primeras 5 noticias
    html_content += f"""
        <div class="news-card">
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <p>{entry.summary[:100]}...</p>
        </div>
    """

html_content += """
    </div>
    <h2>🔍 Noticias de España (ATOM)</h2>
    <div class="news-container">
"""

# Agregar noticias ATOM
for entry in atom_feed.entries[:5]:  # Solo las primeras 5 noticias
    html_content += f"""
        <div class="news-card">
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <p>{entry.summary[:100]}...</p>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# Guardar el archivo HTML
file_path = "news_scraping.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Abrir automáticamente el archivo en el navegador
webbrowser.open("file://" + os.path.abspath(file_path))

print("✅ Archivo generado: news_scraping.html (se abrirá en el navegador)")
