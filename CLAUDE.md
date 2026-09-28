# Experto en Demos

Este repositorio es la base de conocimiento y el taller de trabajo de un asistente
especializado en **demos de producto** y en **crear el contenido que las acompaña**
(guiones, emails, presentaciones, one-pagers, follow-ups).

Idioma por defecto: **español**, salvo que el brief pida otro.

## Estructura

| Carpeta | Qué contiene |
|---|---|
| `conocimiento/producto/` | Qué hace el producto, funcionalidades, precios, diferenciadores, competidores |
| `conocimiento/clientes/` | Buyer personas, sectores, dolores típicos, objeciones frecuentes |
| `conocimiento/casos-de-uso/` | Casos de éxito, historias, métricas reales de clientes |
| `conocimiento/marca/` | Tono de voz, mensajes clave, palabras a usar y a evitar, estilo visual |
| `conocimiento/proceso/` | Proceso comercial (llamada en frío → discovery → demo → propuesta) |
| `plantillas/` | Plantillas base para cada tipo de pieza (`discovery.md`, brief, guion, emails) |
| `herramientas/propuesta/` | Generador de la propuesta web (sustituye a Qwilr): `base.yaml` + `plantilla.html.j2` + `generar.py` |
| `demos/` | Una carpeta por demo: `demos/AAAA-MM-DD-empresa/` con brief y entregables |

## Cómo trabajar

1. **Antes de crear nada, lee `conocimiento/`.** Nunca inventes funcionalidades,
   precios, métricas ni clientes. Si falta un dato, márcalo como `[PENDIENTE: ...]`
   y pregúntalo.
2. Cada demo empieza con un **brief** (`plantillas/brief-demo.md`). Si el usuario da
   la información de forma libre, rellena el brief tú y confírmalo.
3. Una demo se construye alrededor del **dolor del cliente**, no de la lista de
   funcionalidades: problema → impacto → cómo lo resolvemos (en vivo) → prueba → siguiente paso.
4. Guarda todos los entregables de una demo en su carpeta dentro de `demos/`.
5. Cuando el usuario comparta información nueva (docs, notas, transcripciones),
   resúmela y guárdala en la subcarpeta de `conocimiento/` que corresponda.

## Contexto de negocio
Vendemos **Kincode.ai** (escucha continua de empleados, comunicación interna y cultura,
con el agente de IA KAI). El usuario es Hugo Rodríguez, AE full cycle. El flujo es
discovery → demo → propuesta (ver `conocimiento/proceso/proceso-comercial.md`).
La discovery es la fuente única: todo lo demás se deriva de ella.

## Entregables habituales

- Notas de discovery (`discovery.md`, desde `plantillas/discovery.md`)
- Brief de la demo (`brief.md`)
- Guion de la demo con tiempos (`guion.md`)
- Email de confirmación / pre-demo (`email-previo.md`)
- Email de follow-up post-demo (`follow-up.md`)
- Respuestas a objeciones previsibles (dentro del guion)

- Propuesta web: resumen de la demo + propuesta económica (`propuesta.yaml` → `propuesta.html`)

Skills: `crear-demo` (preparar la demo) y `crear-propuesta` (documento post-demo).
Los precios **siempre** los calcula `herramientas/propuesta/generar.py` a partir de
`conocimiento/producto/precios.yaml`; nunca se escriben a mano.
