# Alcance — Web + CRM inmobiliario v1

Fuente única del alcance. Sirve **igual a los dos clientes inmobiliarios**: cambian
marca, nombre y precio, no lo que se construye.

De aquí se redacta la propuesta al cliente. Si algo no está en este documento, **no está
vendido**. Ese es el punto: en el proyecto anterior el alcance no se escribió y el equipo
acabó asumiendo extras que el cliente recordaba como prometidos.

Arquitectura: ver `arquitectura-ghl.md` y `../../docs/ghl-listado-inmobiliario.md`.
Precios: ver `scope_fase1.py` y `scope_fase2_opciones.py`.

---

## Fase 1 — alcance cerrado

### A. Páginas del sitio (7 facturables)

| # | Página | Secciones | Qué lleva |
|---|---|:--:|---|
| 1 | Inicio | 7 | Cabecera con su nombre, trayectoria, propiedades destacadas, acceso al listado, bloque "¿quieres vender?", cómo trabaja, contacto |
| 2 | Propiedades | 4 | Listado a medida: rejilla, buscador, orden y filtros por precio, zona, garaje, piscina y nº de baños |
| 3 | Ficha de propiedad | 6 | Galería, cabecera con precio y zona, bloque de características, descripción, situación, "Solicitar visita" y WhatsApp |
| 4 | Sobre mí | 4 | Su trayectoria. Es la página que resuelve el problema de fondo: que quien busque su nombre la encuentre |
| 5 | Vende tu propiedad | 6 | Captación de inventario: por qué vender con ella y formulario de valoración |
| 6 | Contacto | 3 | Formulario, WhatsApp y calendario |
| 7 | Alta de propiedad | 3 | Formulario multi-paso de alta y edición. URL no listada, bajo su dominio |

**Sin página de gracias**: la confirmación tras enviar un formulario aparece en la misma
página. **Sin carrito ni checkout**: no se usa el módulo de tienda.

**Aviso legal, política de privacidad y política de cookies** se maquetan y publican **sin
cargo de diseño**. Los textos los redacta su asesor legal, no nosotros.

Incluye **2 rondas de revisión de diseño por página**. A partir de la tercera, se cotiza.

### B. Ficha de propiedad — campos

| Campo | Tipo |
|---|---|
| `referencia` | Texto, **clave única** (es lo que permite editar) |
| `titulo` | Texto |
| `precio` | Moneda |
| **`garaje`** | Sí / No |
| **`piscina`** | Sí / No |
| **`num_banos`** | Número |
| `zona` | Desplegable |
| `tipo_inmueble` | Desplegable: piso, casa, chalet, ático, local |
| `num_habitaciones` | Número |
| `metros_construidos` | Número |
| `descripcion` | Texto largo |
| `estado` | Borrador / Publicada / Reservada / Vendida / Retirada |
| `fotos` | Subida múltiple de archivos |
| `certificado_energetico` | Texto o archivo |
| `propietario` | Asociación al contacto |
| `url_ficha` | Texto, lo escribe el sistema |

En negrita, los tres que salen textuales de la llamada. El resto se confirma en la reunión
de revisión — están listados en `hechos-y-supuestos.md` de cada cliente.

`estado` sustituye al borrado: el formulario no puede eliminar registros, y para una
inmobiliaria el histórico de lo vendido interesa.

### C. CRM

**P1 · Captación (inventario)** — Nuevo propietario → Valoración agendada → Mandato
firmado → Publicada → Vendida o perdida

**P2 · Compradores (demanda)** — Nuevo lead → Cualificado → Visita agendada → Oferta o
reserva → Cerrado

2 vistas guardadas: *Propiedades publicadas* y *Visitas de esta semana*.

### D. Automatizaciones (6)

| Código | Nombre | Se dispara con | Nodos |
|---|---|---|:--:|
| LS01 | Lead web y origen de contacto | Formulario de contacto enviado | 8 |
| LS02 | Solicitud de visita desde una ficha | Formulario de visita, con la referencia del inmueble | 8 |
| LS03 | Captación "Vende tu propiedad" | Formulario de valoración enviado | 8 |
| LS04 | Prospección manual de particulares | Etiqueta `prospecto-particular` añadida | 10 |
| AP01 | Alta, actualización y retirada de propiedad | Formulario de alta enviado | 8 |
| SP01 | Visita agendada: confirmación y recordatorios | Cita agendada en el calendario | 10 |

### E. Formularios, calendarios e integración

- **F01** Contacto · **F02** Solicitar visita (lleva oculta la referencia del inmueble) ·
  **F03** Vende tu propiedad / valoración
- **S01** Alta y edición de propiedad — multi-paso, con lógica condicional
- **C01** Visitas (la ubicación es la dirección del inmueble) · **C02** Valoración a domicilio
- **1 integración**: n8n con la API de GHL. WhatsApp y correo entran en el setup de
  subcuenta y no se cobran dos veces.

### F. Plantillas de mensaje (4)

Confirmación de visita · Ficha de propiedad por email · Resultado de valoración ·
Secuencia de prospección.

### G. Formación

**2 sesiones de 2 horas**: (1) subir, editar y marcar como vendida una propiedad —
el uso que va a hacer cada semana; (2) CRM, pipelines, WhatsApp y calendarios.

Durante la sesión 1 se cargan **las 5 primeras propiedades**. El resto las carga ella.

### H. Criterios de aceptación

Se da por entregada la Fase 1 cuando:

1. Las 7 páginas están publicadas en su dominio con certificado SSL.
2. Hay 5 propiedades cargadas y visibles en el listado, con sus fotos.
3. Ella da de alta una sexta propiedad por sí misma durante la sesión de formación.
4. Los 6 workflows se han probado de punta a punta.
5. Las 2 sesiones de formación se han impartido.

---

## Fuera de alcance

No entra en el precio cerrado. Cualquiera de estas cosas se cotiza aparte.

**Portales y sindicación** — publicación o feed a Idealista, Fotocasa o Habitaclia · MLS
e IDX · extracción automatizada de anuncios de particulares (ver `docs/`: las condiciones
de uso lo prohíben y hay implicaciones de RGPD).

**Contenido** — fotografía, vídeo, tour virtual, planos, home staging · redacción de las
descripciones de las propiedades · redacción de los textos legales · traducción y
multi-idioma · certificado energético.

**Funcionalidad** — firma electrónica de mandatos y contratos · matching automático
comprador-propiedad (Fase 2-A) · reseñas (Fase 2-B) · campañas de pago y dashboards
(Fase 2-C) · migración de datos históricos · área privada de propietarios · app móvil ·
integración contable o de facturación · pasarela de pago y cobros online.

**Marketing** — gestión de campañas, creatividades e **inversión publicitaria** · SEO de
contenidos continuo y link building.

**Operación** — carga de más de 5 propiedades por nuestra parte · soporte fuera del
horario acordado · cambios de diseño a partir de la tercera ronda por página.

---

## Cómo se pide un cambio

1. Se pide **por escrito**.
2. Se responde con estimación de precio y de impacto en la fecha **en 48 horas hábiles**.
3. Se ejecuta **cuando hay aprobación escrita**.
4. Un cambio aprobado puede mover la fecha de entrega, y se dice en la estimación.

No se cobra desde cero: se cobra el cambio.

---

## Responsabilidades del cliente

Sin esto el proyecto se para, y conviene que esté escrito antes de empezar:

- Logo y marca en formato editable.
- Fotografías de las propiedades.
- Descripciones de las propiedades.
- Textos legales redactados por su asesor.
- Dominio contratado y acceso al panel de DNS.
- Cuenta de WhatsApp Business y correo corporativo.
- Una persona de contacto que valide y responda en plazo.

## Suscripciones a cargo del cliente

No están en el precio de implementación: subcuenta de GoHighLevel · dominio · n8n ·
WhatsApp y telefonía · envío de email.

Se dice explícitamente para que "todo incluido" no signifique lo que no significa.
