# Irene — mapa de alcance y costeo

Documento **interno**. No se manda al cliente.

Alcance completo en `../../ofertas/inmobiliaria-web-crm-v1/alcance.md`. Hechos citables y
supuestos en `hechos-y-supuestos.md`. Aquí está el mapa de implementación y los números.

---

## Mapa de implementación

Nomenclatura estándar: **LS** origen de lead · **SP** pipeline de venta · **AP** proyecto
activo · **PS** reseñas. Numeración secuencial por orden lógico del proceso.

```
[ORÍGENES DE LEAD — AZUL]
├─ LS01 · Lead web y origen de contacto                              8 nodos
│   ├─ Disparador: formulario de contacto enviado / contacto creado
│   ├─ Captura de UTMs en campos propios (GHL no los guarda solo)
│   ├─ Etiqueta de origen + fecha de primer contacto
│   ├─ Crea oportunidad en P2 · Compradores
│   └─ Aviso interno + autorespuesta
├─ LS02 · Solicitud de visita desde una ficha                        8 nodos
│   ├─ Disparador: F02 enviado, con ref_propiedad oculta
│   ├─ Vincula el contacto con la propiedad de interés
│   ├─ Crea oportunidad en P2, etapa Cualificado
│   └─ Aviso a Irene con la referencia + enlace a agendar
├─ LS03 · Captación "Vende tu propiedad"                             8 nodos
│   ├─ Disparador: F03 valoración enviado
│   ├─ Crea oportunidad en P1 · Captación
│   ├─ Aviso prioritario: esto es inventario (H08)
│   └─ Envía enlace del calendario de valoración
└─ LS04 · Prospección manual de particulares                        10 nodos
    ├─ Disparador: etiqueta prospecto-particular añadida
    ├─ Versión conforme de la idea de Idealista (H07):
    │   Irene aporta el contacto, el sistema hace el seguimiento
    ├─ Secuencia de contacto con opt-out en cada mensaje
    ├─ Decisión: ¿responde? -> P1 Captación / descarte
    └─ Reintento espaciado

[PIPELINE DE VENTA — VERDE]
└─ SP01 · Visita agendada: confirmación y recordatorios              10 nodos
    ├─ Disparador: cita agendada en C01
    ├─ Confirmación por email + SMS
    ├─ Recordatorio 24 h antes / 2 h antes
    ├─ Envía la ficha de la propiedad
    └─ Aviso interno el día de la visita

[PROYECTO ACTIVO — ROJO]
└─ AP01 · Alta, actualización y retirada de propiedad                 8 nodos
    ├─ Disparador: encuesta S01 enviada
    ├─ Escribe/actualiza el registro por clave única "referencia"
    ├─ Webhook a n8n: fotos, feed, publicación
    ├─ Espera a que n8n escriba url_ficha de vuelta
    └─ Decisión por estado: Publicada / Reservada / Vendida / Retirada

[PIPELINES]
P1 · Captación   Nuevo propietario > Valoración agendada > Mandato firmado > Publicada > Vendida/Perdida
P2 · Compradores Nuevo lead > Cualificado > Visita agendada > Oferta/Reserva > Cerrado

[FORMULARIOS]  F01 Contacto · F02 Solicitar visita · F03 Valoración
[ENCUESTA]     S01 Alta y edición de propiedad (multi-paso)
[CALENDARIOS]  C01 Visitas · C02 Valoración a domicilio
[INTEGRACIÓN]  n8n <-> API v2 de GHL
```

### Campos personalizados

**Contacto** — `origen_contacto`, `utm_source`, `utm_medium`, `utm_campaign`,
`fecha_primer_contacto`, `tipo_cliente`, `zona_interes`, `presupuesto_max`,
`habitaciones_min`, `banos_min`, `necesita_garaje`, `necesita_piscina`,
`ref_propiedad_interes`, `consentimiento_comercial`.

**Oportunidad de captación** — `referencia_inmueble`, `precio_publicacion`, `url_ficha`,
`comision_pct`.

**Objeto Propiedad** — ver `alcance.md`, sección B.

`fecha_primer_contacto` es un campo propio a propósito: la fecha de creación nativa del
contacto no es fiable para atribución.

---

## Costeo

Reproducible: `python3 ../../ofertas/inmobiliaria-web-crm-v1/scope_fase1.py`

### Fase 1

| Módulo | Setup USD | Mensual USD |
|---|---:|---:|
| Setup de subcuenta (completo) | 250 | — |
| CRM & Pipelines | 250 | — |
| Automatizaciones & Workflows (6 wf, 52 nodos) | 608 | — |
| Integraciones externas (n8n ↔ API v2) | 300 | 50 |
| Documentos & Templates (4 plantillas) | 300 | — |
| Calendarios & Citas | 180 | — |
| *Subtotal según tabla de precios* | *2.288* | *50* |
| **Sitio web multipágina (7 págs)** — línea nueva | **1.700** | — |
| **Listado y ficha a medida** — línea nueva, **a confirmar** | **1.200** | — |
| Capacitación (2 sesiones) | 400 | — |
| Soporte | — | 150 |
| **TOTAL EQUIPO** | **5.188** | **200** |

**En euros a 1 USD = 0,87: 4.550 € de implementación / 175 € al mes.**

Ningún paquete ahorra con este alcance (Starter −$100, Pro −$1.672, Enterprise −$4.212
en el primer año) → **à la carte**.

### Las dos líneas que no salen de la tabla

**Sitio web multipágina — $1.700.** Sustituye al módulo 7. La regla de +$300 por página
extra se escribió para embudos de 1 a 3 páginas; aplicada a un sitio de 7 daba $2.410, el
51% del proyecto. Tramo acordado: **$1.500 base hasta 6 páginas + $200 por página
adicional**. Con 7 páginas: 1.500 + 200 = 1.700. *Este tramo sirve también para Mura,
Sara y Moncho — conviene incorporarlo a `tabla_precios.md`.*

**Listado y ficha a medida — $1.200, sin confirmar.** No hay línea en la tabla para
desarrollo front-end. Nace de la decisión de no usar el módulo Tienda: hay que construir
el render, el feed y los filtros por atributos. Es una cifra propuesta, no un dato de la
tabla. **Confirmar antes de dar precio final.**

Nota honesta: la arquitectura sin tienda cuesta **~$490 más** que haber usado el módulo
Tienda ($2.900 frente a $2.410). Lo que se compra con esa diferencia es el filtro por
garaje, piscina y nº de baños —la forma en que la gente busca casa— y que no exista un
carrito en ningún rincón del sitio.

### Fase 2 — opciones, precio marginal

Reproducible: `python3 ../../ofertas/inmobiliaria-web-crm-v1/scope_fase2_opciones.py`

| Opción | Setup USD | Mensual | EUR |
|---|---:|---:|---:|
| A · Matching comprador ↔ propiedad | 318 | — | 300 € |
| B · Reseñas y reputación | 240 | — | 250 € |
| C · Campañas Meta de captación (sin inversión publicitaria) | 1.990 | +190 | 1.750 € |

Marginal quiere decir sobre una Fase 1 ya construida: las bases de módulo ya están
pagadas. Venderlas a precio standalone sería cobrar dos veces la misma base.

---

## Nuestro precio y el de Sonia

Dos documentos distintos, y conviene no mezclarlos:

- **`cotizacion-para-be-banana.html`** — lo que Profit Technology le cobra a Be Banana.
  Es el que está construido y el que se envía. Va con marca Profit Technology.
- **La propuesta de Sonia a Irene** — la monta ella, con su marca y su margen. No está en
  este repo, y este documento no se le reenvía a Irene tal cual.

**Margen de Sonia: 90%** (confirmado). Se aplica sobre el USD y se convierte y redondea una
sola vez; redondear a euros y multiplicar después inflaría el precio por doble redondeo.

| Concepto | USD | **Nosotros → Be Banana** | Irene (referencia) |
|---|---:|---:|---:|
| Fase 1 · implantación | 5.188 | **4.550 €** | 8.600 € |
| Fase 1 · mantenimiento | 200 | **175 €/mes** | 335 €/mes |
| Opción A · Matching | 318 | **300 €** | 550 € |
| Opción B · Reseñas | 240 | **250 €** | 400 € |
| Opción C · Campañas | 1.990 | **1.750 €** | 3.300 € |
| Opción C · mantenimiento | 190 | **170 €/mes** | 315 €/mes |

Reproducible: `python3 ../../ofertas/inmobiliaria-web-crm-v1/scope_fase1.py` imprime las dos
columnas. La constante es `MARGEN_SONIA` en ese mismo archivo.

La columna de Irene es **solo referencia nuestra**: sirve para saber de qué cifras se está
hablando cuando ella lo comente, no para ponerla en ningún documento.

### El segundo cliente

Mismo alcance y mismo precio nuestro. Lo que cambie por encima es cosa de Sonia. Los dos
clientes saben que se les presenta el mismo proyecto, así que si a ella le pone precios
distintos conviene que la diferencia tenga una razón que se pueda decir en voz alta.

Su cotización no está renderizada: falta su nombre y su marca.

### Pendiente que mueve todos estos números

Los **1.200 $ de «listado y ficha a medida»** siguen sin confirmar y van dentro de los
5.188 $. Si se ajusta esa línea, se ajusta toda la tabla de arriba.
