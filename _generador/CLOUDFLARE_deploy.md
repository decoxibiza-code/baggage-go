# ☁️ Publicar BaggageGo en Cloudflare Pages (recomendado)

Como el dominio **baggage-go.com** ya está en Cloudflare, usamos **Cloudflare Pages**:
hosting gratis, HTTPS automático, dominio automático y redepliegue en cada `git push`.

## Pasos (panel de Cloudflare, ~5 min)

1. Entra en **dash.cloudflare.com** → menú lateral **"Workers y Pages"** (Compute).
2. Botón **"Create" / "Crear aplicación"** → pestaña **"Pages"** → **"Connect to Git" / "Conectar a Git"**.
3. Autoriza a Cloudflare el acceso a tu **GitHub** (una sola vez) y elige el repositorio **`baggage-go`**.
4. Configuración de compilación (build):
   - **Framework preset / Preset de framework:** `None` (Ninguno)
   - **Build command / Comando de compilación:** *(déjalo VACÍO)*
   - **Build output directory / Directorio de salida:** `/`  *(o déjalo por defecto)*
   - La web ya viene generada en HTML; no hace falta compilar nada.
5. **"Save and Deploy" / "Guardar e implementar"**. En ~1 min tendrás una URL de prueba
   tipo **baggage-go.pages.dev** ya funcionando.
6. En el proyecto → pestaña **"Custom domains" / "Dominios personalizados"** →
   **"Set up a custom domain"** → escribe **baggage-go.com** → **Continuar/Activar**.
   - Como el dominio está en Cloudflare, crea el DNS automáticamente.
   - Repite para **www.baggage-go.com** si quieres que el www también funcione.
7. **HTTPS:** automático (Cloudflare emite el certificado). No hay que hacer nada más.

## Resultado
- **https://baggage-go.com** sirviendo la web, con SSL.
- Cada `git push` al repo → Cloudflare Pages **redepliega solo**.

## Nota sobre GitHub Pages
Ya habíamos activado GitHub Pages como alternativa. Con Cloudflare Pages no hace falta;
puedes dejarlo (es inofensivo) o desactivarlo en GitHub → repo → Settings → Pages.
El fichero `CNAME` del repo es solo para GitHub Pages; Cloudflare Pages lo ignora.

## Alternativa por CLI (opcional, técnica)
Con Wrangler (CLI de Cloudflare):
```bash
npm i -g wrangler
wrangler login
wrangler pages deploy "." --project-name baggage-go
```
