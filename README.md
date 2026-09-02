# be-banana1

Trabajo de cliente de **Be Banana** (Sonia) con **Profit Technology** como equipo de
implementación: mapeo de procesos, presupuestos e implementaciones sobre GoHighLevel
y n8n.

## Cómo está organizado

```
docs/        conocimiento reutilizable, no atado a un cliente
ofertas/     un producto empaquetado que se vende a varios clientes
clientes/    lo que cambia de un cliente a otro: hechos, precio, propuesta
```

La separación importa: **el alcance se escribe una vez en `ofertas/`** y los clientes lo
referencian. Así presentar el mismo proyecto a dos clientes es cambiar marca y precio, no
copiar y pegar el alcance y que se desincronicen.

## Estado

| Cliente | Oferta | Estado |
|---|---|---|
| Irene | `inmobiliaria-web-crm-v1` | Propuesta redactada. Pendiente: precios finales y reunión de revisión con ella |
| Segundo cliente | `inmobiliaria-web-crm-v1` | En espera de nombre y marca |

## Reglas

1. **Hechos y supuestos van separados.** Cada cliente tiene su `hechos-y-supuestos.md`
   con hechos numerados. La propuesta no puede afirmar nada que no salga de ahí. Cero
   métricas, URLs o datos de contacto inventados; lo que falte va como `PON_AQUI_*`.
2. **Sin datos personales.** Ni apellidos, ni teléfonos, ni emails, ni direcciones de
   clientes finales. Estamos en la UE.
3. **Los precios salen del cotizador**, no a mano. Si hace falta una línea que la tabla
   no tiene, va aparte y marcada como tal.
4. **Toda propuesta lleva su cláusula de alcance** — ver `docs/clausula-alcance-maestra.md`.
   No es burocracia: es lo que evita repetir el proyecto en el que el alcance no se
   escribió y el equipo acabó asumiendo la diferencia.
5. El HTML que va a GHL sigue el estándar `ghl-html-wide`: reset del builder, clases con
   prefijo `pt-`, tokens de color y tipografía, sin hex sueltos.

## Reproducir los números

```bash
python3 ofertas/inmobiliaria-web-crm-v1/scope_fase1.py
python3 ofertas/inmobiliaria-web-crm-v1/scope_fase2_opciones.py
```
