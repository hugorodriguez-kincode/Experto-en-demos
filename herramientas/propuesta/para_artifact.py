#!/usr/bin/env python3
"""Adapta el HTML autocontenido (generar.py) a lo que admite el visor de Artifacts.

El visor de Artifacts corre en un iframe con permisos limitados: no se pueden
incrustar iframes de otras webs (los vídeos de Loom), los mailto: no son
fiables para todo el mundo, y el propio Artifact ya pone su <!doctype>/<head>/
<body>, así que el archivo publicado no debe traer los suyos.

Uso:  python3 herramientas/propuesta/para_artifact.py demos/<carpeta>/propuesta.html
Salida: demos/<carpeta>/propuesta.artifact.html, listo para publicar con la
herramienta Artifact (file_path=esa ruta, sin volver a envolverlo).
"""
import base64
import mimetypes
import re
import sys
import urllib.request
from pathlib import Path


def inline_images(html):
    """Descarga toda <img src="http..."> y la sustituye por un data: URI.

    El CSP del visor solo deja pasar imágenes propias, de Google Fonts o de
    data:/blob:, así que cualquier imagen en un CDN externo (el mascota KAI,
    un logo de cliente) hay que incrustarla o se queda en blanco.
    """
    def repl(m):
        url = m.group(1)
        if url.startswith('data:'):
            return m.group(0)
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                data = r.read()
                ctype = r.headers.get_content_type() or mimetypes.guess_type(url)[0] or 'image/jpeg'
        except Exception as e:
            print(f"  ⚠ no se pudo descargar {url}: {e}; la imagen quedará rota en el Artifact")
            return m.group(0)
        b64 = base64.b64encode(data).decode()
        return m.group(0).replace(url, f'data:{ctype};base64,{b64}')

    return re.sub(r'<img[^>]+src="(https?://[^"]+)"', repl, html)


def video_cards(html):
    """Cambia cada <iframe> de Loom por una tarjeta que enlaza fuera: el visor
    de Artifacts no permite incrustar sitios de terceros."""
    pat = re.compile(
        r'<div><div class="video"><iframe src="[^"]+"[^>]*></iframe></div>\s*'
        r'<p[^>]*><a href="([^"]+)"[^>]*>▶ Ver el vídeo en Loom</a></p></div>',
        re.S,
    )

    def repl(m):
        href = m.group(1)
        return (f'<a class="video-card" href="{href}" target="_blank" rel="noopener">'
                f'<span class="play">▶</span><span>Ver el vídeo de la demo en Loom<br>'
                f'<small>Se abre en una pestaña nueva</small></span></a>')

    return pat.subn(repl, html)


def clickable_email_chip(html):
    """El botón "Hablar con ___" pasa de <a mailto> a un botón que copia el
    email: los enlaces mailto: no funcionan para buena parte de quien vea un
    Artifact compartido."""
    m = re.search(r'<a id="talkBtn"[^>]*href="mailto:([^"?]+)\?[^"]*"[^>]*>(.*?)</a>', html, re.S)
    if not m:
        return html, False
    email, inner = m.group(1), m.group(2)
    new_btn = (f'<button id="talkBtn" class="chrome-btn" type="button" data-email="{email}" '
               f'onclick="copyEmail(this)">{inner}</button>')
    return html[:m.start()] + new_btn + html[m.end():], True


def copy_buttons_on_ctas(html):
    """Añade un botón "Copiar email" junto a cada CTA mailto: del cuerpo,
    como alternativa al enlace (que puede no hacer nada para el viewer)."""
    pat = re.compile(r'(<a class="cta" href="mailto:([^"?]+)\?[^"]*">.*?</a>)', re.S)

    def repl(m):
        return (m.group(1) + f' <button type="button" class="copy-mini" data-email="{m.group(2)}" '
                f'onclick="copyEmail(this)" aria-label="Copiar email de contacto">Copiar email</button>')

    return pat.subn(repl, html)


EXTRA_STYLE = """
<style>
.video-card{display:flex;align-items:center;gap:16px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);
  border-radius:16px;padding:18px 22px;text-decoration:none;color:inherit;transition:.15s;max-width:420px}
.theme-light .video-card,.theme-tint .video-card{background:var(--soft);border-color:var(--line)}
.video-card:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,0,0,.18)}
.video-card .play{flex:0 0 auto;width:44px;height:44px;border-radius:50%;background:#fff;color:var(--indigo);
  display:grid;place-items:center;font-size:16px}
.video-card small{opacity:.7;font-weight:400}
.copy-mini{margin-left:10px;background:none;border:1.5px solid currentColor;opacity:.7;color:inherit;
  border-radius:999px;padding:6px 14px;font-size:13px;font-weight:600;cursor:pointer;vertical-align:middle}
.copy-mini:hover{opacity:1}
#talkBtn{cursor:pointer}
</style>
"""

EXTRA_SCRIPT = """
<script>
function copyEmail(btn){
  const email=btn.dataset.email, original=btn.innerHTML;
  const done=ok=>{ btn.innerHTML = ok ? '✓ Email copiado' : email; setTimeout(()=>btn.innerHTML=original,1600); };
  try{ navigator.clipboard.writeText(email).then(()=>done(true)).catch(()=>done(false)); }
  catch(e){ done(false); }
}
</script>
"""


def main(ruta_html):
    ruta = Path(ruta_html)
    src = ruta.read_text(encoding='utf-8')

    title = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
    # Nombre corto para la pestaña/galería del Artifact: "nombre de producto",
    # no "Propuesta de colaboración · Cliente". Ajusta a mano si hace falta.
    title = re.sub(r'^Propuesta de colaboraci[oó]n\s*[·:-]\s*', 'Propuesta ', title)

    head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
    body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
    styles = re.findall(r'<style>.*?</style>', head, re.S)
    font_links = [l for l in re.findall(r'<link[^>]+>', head) if 'font' in l or 'preconnect' in l]

    body, n = video_cards(body)
    print(f"  vídeos convertidos a tarjeta de enlace: {n}")
    body, ok = clickable_email_chip(body)
    if not ok:
        print("  ⚠ no se encontró el botón 'Hablar con...' para convertirlo")
    body, n2 = copy_buttons_on_ctas(body)
    print(f"  botones de copiar email añadidos: {n2}")
    body = inline_images(body)

    out = f"<title>{title}</title>\n" + "\n".join(font_links) + "\n" + "\n".join(styles) + EXTRA_STYLE + \
        "\n" + body + "\n" + EXTRA_SCRIPT + "\n"

    salida = ruta.with_suffix('').with_suffix('.artifact.html')
    salida.write_text(out, encoding='utf-8')
    print(f"✔ Generado {salida}")
    print("  Publícalo con la herramienta Artifact: file_path apuntando a ese archivo,")
    print("  sin volver a envolverlo en <html>/<head>/<body> (el Artifact ya lo hace).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
