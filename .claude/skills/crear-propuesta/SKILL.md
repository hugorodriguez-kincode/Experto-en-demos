---
name: crear-propuesta
description: Genera la propuesta web interactiva de Kincode (resumen de la demo + propuesta económica, lo que antes se hacía en Qwilr) a partir de las notas de la discovery y la demo, y puede publicarla como un Artifact con enlace para compartir. Úsala cuando el usuario pida una propuesta, un presupuesto, una propuesta económica o el documento post-demo para un cliente.
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
     Si la discovery trae foto de alguno (columna "Foto"), usa la forma larga
     `empleado: {nombre: Miguel, foto: fotos/miguel.jpg}` en vez de solo el nombre:
     guarda el archivo en `demos/<carpeta>/fotos/` (el generador lo incrusta solo)
     o pon directamente una URL https. Sin foto, el personaje se queda con un
     avatar de iniciales; no inventes ni descargues fotos de otras personas.
   - `precios`: `piloto_personas`, `ruta_sugerida` y, si hay condiciones especiales,
     `politica:` para sobrescribir lo que haga falta de `precios.yaml` (p. ej. `descuento_especial`).
     Pon `mostrar_piloto: false` si no se ofrece piloto.
   - `proximos_pasos`: incluye el HRIS concreto del cliente.
   - Quita `portada.imagen` y `cliente.logo` si no hay imágenes de ese cliente.
   - `clientes_logos` y `premios` (logos de clientes que confían en Kincode y
     reconocimientos como el HR Innovation Summit 2025) viven en `base.yaml`,
     no en el yaml del cliente: son los mismos en todas las propuestas. Las
     imágenes van en `conocimiento/marca/logos-clientes/` y
     `conocimiento/marca/premios/` (rutas relativas a `conocimiento/marca/`).
     Si un logo es blanco/claro, añádele `fondo: oscuro` para que se vea.
     Solo tócalos si el usuario pide añadir un cliente o premio nuevo.
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

## Publicarla como Artifact (enlace para compartir)

Si el usuario quiere un enlace en vez de (o además de) el archivo `propuesta.html`:

1. `python3 herramientas/propuesta/para_artifact.py demos/<carpeta>/propuesta.html`
   — genera `propuesta.artifact.html`. Este paso adapta el HTML a las reglas del
   visor de Artifacts (que no son las de un navegador normal):
   - Convierte el botón "Hablar con ___" y añade un botón "Copiar email" junto
     a cada CTA, porque los enlaces `mailto:` no son fiables dentro del visor.
   - Descarga e incrusta como `data:` cualquier imagen externa (el visor
     bloquea imágenes que no sean propias, de Google Fonts o data:/blob:).
   - Quita `<!doctype>/<html>/<head>/<body>`: el Artifact ya pone los suyos.
   (Los vídeos de Loom ya son una tarjeta de enlace desde la propia plantilla,
   no un `<iframe>` — nunca los incrustes, el visor de Artifacts los bloquea y
   además fallan bastante como iframe en un navegador normal.)
2. Publica con la herramienta Artifact: `file_path` apuntando a ese
   `.artifact.html`, un `title` corto (2-4 palabras, sin explicación tras un
   guion — el propio `<title>` del HTML manda si no coincide, actualízalo ahí),
   una `description` de una frase e `icon` (p. ej. `presentation`).
3. Antes de publicar, comprueba con un screenshot local que las tarjetas de
   vídeo y el botón de copiar funcionan, y que no queda ninguna `<img>` con
   `src="http..."` sin incrustar (el aviso de la propia herramienta Artifact
   lo dice si se cuela alguna).

El archivo `propuesta.html` (el original, con mailtos) sigue siendo el que se
envía por email o se sube a Drive/HubSpot; el `.artifact.html` es solo para
cuando el destino es un enlace de Artifact.
