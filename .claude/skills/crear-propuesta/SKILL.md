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

Ya no es un scroll de documento como Qwilr: es un **deck de diapositivas a pantalla
completa** (13 diapositivas fijas, una idea por pantalla, con scroll-snap), pensado para
sentirse como un producto propio y no como un contrato largo:

- Se navega con scroll/swipe (una diapositiva "engancha" en cada pantalla), con las
  flechas ‹ › de abajo, con las flechas del teclado o con el índice (☰ arriba a la
  izquierda) para saltar directo a una sección.
- Fondos de color con degradados (indigo/navy/dark) que rotan diapositiva a diapositiva
  para dar ritmo, en vez de un fondo blanco continuo.
- **Personajes de la demo** y **Piloto/Implementación/condición comercial** se navegan
  con pestañas dentro de su diapositiva (100 % CSS, sin depender de JavaScript).
- Contador "03 / 13", barra de progreso arriba y botón "Hablar con {{autor}}" siempre visibles.
- Al imprimir/exportar a PDF, las diapositivas pasan a maquetarse en vertical (una tras
  otra) y se fuerza a mostrar todo el contenido de las pestañas, para que no falte nada
  en el PDF que se envía por email.

Las 13 diapositivas están para razones de estructura (portada, objetivo, oportunidad,
los 3 dolores, solución, insight→acción, demo, propuesta económica, próximos pasos,
seguridad, integraciones, clientes, contacto). Si el cliente pide cambiar el diseño
(colores, orden, más o menos diapositivas), edita `plantilla.html.j2`; no hace falta
tocar `generar.py` salvo que cambie qué datos se calculan.
