# 🌐 Configuración DNS para baggage-go.com → GitHub Pages

Para que **baggage-go.com** muestre la web (alojada en GitHub Pages), hay que entrar en el
panel DNS de **donde compraste el dominio** y poner estos registros.

## 1) Registros A (dominio raíz: baggage-go.com)
Borra el registro A actual (apunta a 80.58.61.250, el parking) y añade estos **4 registros A**:

| Tipo | Nombre / Host | Valor |
|------|---------------|-------|
| A | @ (o vacío) | 185.199.108.153 |
| A | @ (o vacío) | 185.199.109.153 |
| A | @ (o vacío) | 185.199.110.153 |
| A | @ (o vacío) | 185.199.111.153 |

## 2) Registro CNAME (para www.baggage-go.com)
| Tipo | Nombre / Host | Valor |
|------|---------------|-------|
| CNAME | www | decoxibiza-code.github.io |

## 3) (Opcional) Registros AAAA para IPv6
| Tipo | Nombre | Valor |
|------|--------|-------|
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |

## Después
- La propagación tarda de **15 minutos a unas horas** (a veces hasta 24-48 h).
- Cuando resuelva, la web estará en **https://baggage-go.com**.
- Entonces se activa **"Enforce HTTPS"** (candado/SSL) en GitHub → Settings → Pages.

## Datos del hosting
- Repo: https://github.com/decoxibiza-code/baggage-go
- GitHub Pages: rama `main`, carpeta raíz. Dominio en el fichero `CNAME`.
- Cada vez que se regenera la web (`python _generador/build.py`) y se hace `git push`, la web se actualiza sola.
