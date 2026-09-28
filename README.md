# Experto en Demos

Base de conocimiento y automatización para preparar demos de producto y todo su
contenido (guiones, emails, follow-ups, objeciones).

- Añade la información del producto, clientes, casos de uso y marca en `conocimiento/`.
- Pide una demo nueva describiendo al cliente; se generará en `demos/`.
- Las instrucciones del asistente están en [`CLAUDE.md`](CLAUDE.md).

## Generar una propuesta (sustituye a Qwilr)

```bash
pip install -r requirements.txt
python3 herramientas/propuesta/generar.py demos/2026-09-golive/propuesta.yaml
```

Rellena un `propuesta.yaml` por cliente (o pídele a Claude que lo haga a partir de la
discovery). Los precios, los descuentos y los ahorros se calculan solos desde
`conocimiento/producto/precios.yaml`, y el script avisa de nombres mal escritos,
placeholders sin rellenar y pendientes. La salida es un único `propuesta.html` que puedes
compartir o exportar a PDF (Imprimir → Guardar como PDF).
