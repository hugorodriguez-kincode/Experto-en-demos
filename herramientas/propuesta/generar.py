#!/usr/bin/env python3
"""Genera la propuesta web (demo + propuesta económica) a partir de un propuesta.yaml.

Uso:  python3 herramientas/propuesta/generar.py demos/<carpeta>/propuesta.yaml
Salida: propuesta.html junto al yaml.
"""
import base64
import mimetypes
import re
import sys
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
PRECIOS = RAIZ / "conocimiento" / "producto" / "precios.yaml"


def fusionar(base, extra):
    """Fusión en profundidad: extra gana sobre base."""
    if isinstance(base, dict) and isinstance(extra, dict):
        out = dict(base)
        for k, v in extra.items():
            out[k] = fusionar(base.get(k), v) if k in base else v
        return out
    return extra if extra is not None else base


def eur(x, decimales=None):
    """Formato español: 1.000 € / 475,20 €."""
    if decimales is None:
        decimales = 0 if float(x).is_integer() or abs(x) >= 1000 else 2
    s = f"{x:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"


def calcular_precios(n, pol, extra):
    pol = fusionar(pol, extra.get("politica", {}))
    lista = pol["precio_lista_emp_mes"]
    integ = pol["integracion_pago_unico"]
    final = round(lista * (1 - pol["descuento_especial"]), 2)

    def fila(nombre, precio):
        mensual = round(precio * n, 2)
        anio1 = round(mensual * 12 + integ)
        return {"nombre": nombre, "precio": precio, "mensual": mensual, "anio1": anio1}

    normal = fila("Precio normal", lista)
    oferta = fila("Precio final", final)
    extras = [fila(d["nombre"], round(final * (1 - d["pct"]), 2)) for d in pol["descuentos_adicionales"]]
    for f in [oferta] + extras:
        f["ahorro"] = normal["anio1"] - f["anio1"]
        f["ahorro_pct"] = round(100 * f["ahorro"] / normal["anio1"])
    piloto = pol["piloto"]
    return {
        "n": n, "integracion": integ, "descuento_pct": round(pol["descuento_especial"] * 100),
        "normal": normal, "oferta": oferta, "extras": extras,
        "mejor": min([oferta] + extras, key=lambda f: f["precio"]),
        "piloto": {
            "personas": extra.get("piloto_personas") or f"~{round(n * piloto['porcentaje_empresa'])}",
            "pct": round(piloto["porcentaje_empresa"] * 100),
            "duracion": extra.get("piloto_duracion", piloto["duracion"]),
            "coste": piloto["coste"],
            "si_no": f"{eur(lista)}/emp/mes",
        },
        "ruta": extra.get("ruta_sugerida", ""),
        "mostrar_piloto": extra.get("mostrar_piloto", True),
    }


def archivo_a_data_uri(ruta_imagen, carpeta_base, aviso_si_falta=None):
    """Si `ruta_imagen` es un archivo local (relativo a `carpeta_base`), lo
    incrusta como data: URI para que el HTML siga siendo un único archivo
    portable. Si ya es una URL http(s) o un data:, se deja tal cual."""
    if not ruta_imagen or ruta_imagen.startswith(("http://", "https://", "data:")):
        return ruta_imagen
    ruta = (carpeta_base / ruta_imagen).resolve()
    if not ruta.is_file():
        if aviso_si_falta:
            print(f"  ⚠ {aviso_si_falta.format(ruta_imagen=ruta_imagen, ruta=ruta)}")
        return None
    mime = mimetypes.guess_type(ruta.name)[0] or "image/jpeg"
    b64 = base64.b64encode(ruta.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def normalizar_personajes(datos, carpeta_yaml):
    """Acepta tanto `nombre: Miguel` (solo texto) como
    `nombre: {nombre: Miguel, foto: fotos/miguel.jpg}` (con foto real,
    archivo local o URL). Deja siempre dicts con `nombre` y `foto` (o None)."""
    personajes = datos.get("demo", {}).get("personajes", {}) or {}
    normalizados = {}
    for clave, valor in personajes.items():
        if isinstance(valor, dict):
            nombre, foto = valor.get("nombre"), valor.get("foto")
        else:
            nombre, foto = valor, None
        foto = archivo_a_data_uri(
            foto, carpeta_yaml,
            "no se encuentra la foto '{ruta_imagen}' (se esperaba en {ruta}); se usarán iniciales")
        normalizados[clave] = {"nombre": nombre, "foto": foto}
    datos["demo"]["personajes"] = normalizados


def normalizar_logos_clientes(datos):
    """Acepta tanto `Danone` (solo texto, pastilla) como
    `{nombre: Danone, logo: logos-clientes/danone.jpeg}` (con logo real).
    Las rutas de logo son relativas a conocimiento/marca/ (se comparten entre
    todas las propuestas, no van dentro de demos/<carpeta>/)."""
    base_logos = RAIZ / "conocimiento" / "marca"
    normalizados = []
    for valor in datos.get("clientes_logos", []) or []:
        if isinstance(valor, dict):
            nombre, logo, fondo = valor.get("nombre"), valor.get("logo"), valor.get("fondo")
        else:
            nombre, logo, fondo = valor, None, None
        logo = archivo_a_data_uri(
            logo, base_logos,
            "no se encuentra el logo '{ruta_imagen}' (se esperaba en {ruta}); se mostrará solo el nombre")
        normalizados.append({"nombre": nombre, "logo": logo, "fondo": fondo})
    datos["clientes_logos"] = normalizados


def normalizar_premios(datos):
    """Igual que los logos de clientes: `imagen` es relativa a conocimiento/marca/."""
    base_logos = RAIZ / "conocimiento" / "marca"
    for pr in datos.get("premios", []) or []:
        pr["imagen"] = archivo_a_data_uri(
            pr.get("imagen"), base_logos,
            "no se encuentra la imagen del premio '{ruta_imagen}' (se esperaba en {ruta})")


def revisar(datos, texto_plano):
    """Avisos de calidad: lo que en Qwilr se escapaba a mano."""
    avisos = []
    nombre = datos["cliente"]["nombre"]
    variantes = {m for m in re.findall(re.escape(nombre), texto_plano, re.I)} - {nombre}
    if variantes:
        avisos.append(f"El nombre del cliente aparece como {sorted(variantes)}; la forma oficial es '{nombre}'.")
    for p in re.findall(r"\[PENDIENTE[^\]]*\]", texto_plano):
        avisos.append(f"Queda un pendiente: {p}")
    if re.search(r"\{\{|\}\}|\{canales\}", texto_plano):
        avisos.append("Queda algún placeholder sin rellenar.")
    faltan = [b["clave"] for b in datos["demo"]["bloques"]
              if not datos["demo"].get("personajes", {}).get(b["clave"], {}).get("nombre")]
    if faltan:
        avisos.append(f"Faltan nombres de personajes de la demo: {faltan}")
    return avisos


def main(ruta_yaml):
    ruta_yaml = Path(ruta_yaml)
    base = yaml.safe_load((AQUI / "base.yaml").read_text(encoding="utf-8"))
    prop = yaml.safe_load(ruta_yaml.read_text(encoding="utf-8"))
    datos = fusionar(base, prop)
    canales = datos["demo"].get("canales", "")
    for b in datos["demo"]["bloques"]:
        b["puntos"] = [p.replace("{canales}", canales) for p in b["puntos"]]
    normalizar_personajes(datos, ruta_yaml.parent)
    normalizar_logos_clientes(datos)
    normalizar_premios(datos)

    pol = yaml.safe_load(PRECIOS.read_text(encoding="utf-8"))
    datos["precios"] = calcular_precios(datos["cliente"]["empleados"], pol, datos.get("precios", {}))
    datos.setdefault("fecha", date.today().strftime("%d/%m/%Y"))

    env = Environment(loader=FileSystemLoader(AQUI), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    env.filters["eur"] = eur
    html = env.get_template("plantilla.html.j2").render(d=datos)

    salida = ruta_yaml.with_name("propuesta.html")
    salida.write_text(html, encoding="utf-8")
    print(f"✔ Generada {salida}")
    p = datos["precios"]
    print(f"  {p['n']} empleados · final {eur(p['oferta']['precio'])}/emp/mes · año 1 {eur(p['oferta']['anio1'])}"
          f" · mejor {eur(p['mejor']['precio'])}/emp/mes")
    texto_plano = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[\s\S]*?</\1>", "", html))
    for a in revisar(datos, texto_plano):
        print(f"  ⚠ {a}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
