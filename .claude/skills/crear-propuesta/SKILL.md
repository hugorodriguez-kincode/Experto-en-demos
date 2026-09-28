---
name: crear-propuesta
description: Genera la propuesta web interactiva de Kincode (resumen de la demo + propuesta económica, lo que antes se hacía en Qwilr) a partir de las notas de la discovery y la demo. Úsala cuando el usuario pida una propuesta, un presupuesto, una propuesta económica o el documento post-demo para un cliente.
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

## Cómo es la plantilla (herramientas/propuesta/plantilla.html.j2)

No es un scroll estático como Qwilr: es interactiva, sin necesidad de JavaScript para
lo esencial (funciona igual si el cliente lo abre o lo imprime a PDF):

- **Personajes de la demo**: se seleccionan con pestañas (Empleado / Manager / People / CEO)
  en vez de cuatro secciones seguidas; cada una enseña sus puntos y su vídeo.
- **Propuesta económica**: pestañas Piloto / Implementación completa, y dentro de
  implementación, pestañas por condición comercial (precio final, -10 % firma anual,
  -20 % firma anual + pago anticipado) con tarjetas de cifras que cambian al instante.
  Debajo se mantiene la tabla completa de referencia.
- Barra de progreso de lectura, menú lateral que se resalta solo, botón flotante
  "Hablar con {{autor}}" con mailto pre-rellenado, y CTAs en precios y próximos pasos.
- Menú en cajón (☰) en móvil.
- Al imprimir/exportar a PDF se muestran TODAS las pestañas a la vez (nadie se queda
  contenido oculto en el PDF que se envía por email).

Si el cliente pide cambiar el diseño (colores, orden de secciones, más o menos
interactividad), edita `plantilla.html.j2`; no hace falta tocar `generar.py` salvo que
cambie qué datos se calculan.
