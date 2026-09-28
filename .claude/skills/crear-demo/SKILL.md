---
name: crear-demo
description: Genera el paquete completo de una demo de producto (brief, guion con tiempos, email previo, follow-up y objeciones) a partir de la información de un cliente. Úsala cuando el usuario pida preparar, crear o planificar una demo.
---

# Crear demo

1. Lee todo `conocimiento/` (producto, clientes, casos de uso, marca).
2. Reúne del usuario los datos del brief (`plantillas/brief-demo.md`). Si faltan
   datos críticos (asistentes, dolor principal, duración, objetivo), pregúntalos
   de una vez; el resto márcalo como `[PENDIENTE: ...]`.
3. Crea `demos/AAAA-MM-DD-empresa/` y genera, a partir de las plantillas:
   - `brief.md`
   - `guion.md` — ajusta los tiempos a la duración real; máx. 3 momentos "wow",
     cada uno ligado a un dolor del brief; incluye objeciones y plan B.
   - `email-previo.md`
   - `follow-up.md` — borrador para completar tras la demo.
4. Usa el tono de `conocimiento/marca/`. No inventes datos del producto ni métricas
   de clientes: cita solo lo que está en `conocimiento/`.
5. Termina con un resumen corto: qué se ha generado y qué queda pendiente.
