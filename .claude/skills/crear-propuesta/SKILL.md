---
name: crear-propuesta
description: Genera la propuesta web de Kincode (resumen de la demo + propuesta económica, lo que antes se hacía en Qwilr) a partir de las notas de la discovery y la demo. Úsala cuando el usuario pida una propuesta, un presupuesto, una propuesta económica o el documento post-demo para un cliente.
---

# Crear propuesta

1. Lee `conocimiento/` (sobre todo `producto/kincode.md`, `producto/precios.yaml` y
   `marca/estilo-propuestas.md`) y la discovery del cliente (`demos/<carpeta>/discovery.md`),
   si existe, o la transcripción o las notas que te pase el usuario.
2. Copia `demos/2026-09-golive/propuesta.yaml` como punto de partida en
   `demos/AAAA-MM-DD-empresa/propuesta.yaml` y reescribe **todo** el contenido del cliente:
   - Nombre oficial del cliente (siempre igual en todo el texto), nº de empleados, país, stack y contacto.
   - `portada`, `objetivo`, `oportunidad` (realidad, desafío, 3 pains con la cifra
     o la frase literal del cliente, insight), `solucion.pilares` (adapta los puntos a su
     stack: Teams/Slack/WhatsApp, SharePoint, HRIS) y `solucion.cita`.
   - `demo.personajes`: nombres reales de los personajes que se usaron en la demo.
   - `precios`: `piloto_personas`, `ruta_sugerida` y, si hay condiciones especiales,
     `politica:` para sobrescribir lo que haga falta de `precios.yaml` (p. ej. `descuento_especial`).
     Pon `mostrar_piloto: false` si no se ofrece piloto.
   - `proximos_pasos`: incluye el HRIS concreto del cliente.
   - Quita `portada.imagen` y `cliente.logo` si no hay imágenes de ese cliente.
3. **Nunca** escribas precios a mano: los calcula el generador.
4. Ejecuta `python3 herramientas/propuesta/generar.py demos/<carpeta>/propuesta.yaml`,
   corrige todos los avisos ⚠ que salgan y vuelve a generarla.
5. Envía `propuesta.html` al usuario para revisarla y resume: precio final, año 1, mejor
   condición y los datos marcados como `[PENDIENTE]`.
