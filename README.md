# BaggageGo — Web

Sitio web estático de **BaggageGo Mallorca**: entrega de equipaje, transporte de mercancías y mudanzas en Mallorca.

- **Dominio:** https://baggage-go.com
- **Idiomas:** Español (raíz), English (`/en/`), Deutsch (`/de/`)
- **90 páginas** optimizadas para SEO (hreflang, canonical, Open Graph, JSON-LD, sitemap).

## Estructura
- `index.html` — página principal
- `servicios/` · `zonas/` · `guias/` — páginas de servicio, zona (SEO local) y blog
- `en/` · `de/` — versiones en inglés y alemán
- `styles.css` · `main.js` — estilos y scripts
- `sitemap.xml` · `robots.txt` · `CNAME` — SEO técnico y dominio
- `_generador/build.py` — **motor que genera TODAS las páginas** (Python). No editar los `.html` a mano.

## Regenerar la web
```bash
cd _generador
python build.py
```

## Hosting
GitHub Pages (rama `main`, carpeta raíz) con dominio personalizado `baggage-go.com` (ver fichero `CNAME`).

## Pendiente
- Sustituir teléfono/WhatsApp, email y precios reales (variables `WA`, `EMAIL`, `PHONE_DISPLAY` en `_generador/build.py`).
