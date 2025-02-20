const express = require("express");
const path = require("path");
const app = express();
const port = 3000;

// Servir archivos estáticos desde la carpeta public
app.use(express.static(path.join(__dirname, "public")));

// Ruta para servir el archivo HTML generado
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "news_scraping.html"));
});

// Ruta para servir el archivo CSV
app.get("/productos.csv", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "productos.csv"));
});

// Ruta para servir el archivo JSON
app.get("/productos.json", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "productos.json"));
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
});
