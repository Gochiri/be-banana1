# Cómo montar un listado inmobiliario sobre GoHighLevel

Análisis reutilizable, no específico de un cliente. Nace de la pregunta de la llamada
del 2026-09-02: *"probablemente tengamos que indagar tipo tienda en lugar de custom
objects porque va a ser más sencillo si lo hacemos por el shop"*.

**Nivel de evidencia.** El proxy de salida de la sesión bloqueó el acceso directo a
`help.gohighlevel.com` y `marketplace.gohighlevel.com`. Todo lo marcado `[DOC]` viene
de resúmenes de buscador atribuidos a esas páginas de documentación, no de la página
leída de principio a fin. Lo marcado `[VALIDAR]` hay que comprobarlo dentro de la
cuenta antes de firmar alcance. Nada de esto se afirma como verificado en primera
persona.

---

## Veredicto

**Custom Object `Propiedad` como fuente única + listado y ficha a medida alimentados
por n8n desde la API v2. Sin módulo Tienda.**

La intuición de partida (tienda) y la de Sonia (custom objects) no eran alternativas
excluyentes: eran dos capas distintas, la de datos y la de render. La decisión real es
**quién pinta el listado**, y ahí hay un intercambio limpio:

| | Tienda pinta el listado | Render a medida |
|---|---|---|
| Coste | ~$490 menos | ~$490 más |
| Filtro por garaje / piscina / nº baños | **No es posible de forma nativa** | Sí |
| Carrito, checkout y página de gracias | GHL los crea; hay que ocultarlos | No existen |
| Galería, buscador, SEO, orden | Ya resueltos | Hay que construirlos |

Para una inmobiliaria el filtro por atributos no es un extra: es la forma en que la
gente busca casa. Por eso el render a medida gana pese a costar más.

---

## El hallazgo que ordena la decisión

- **Un formulario o encuesta de GHL crea Y ACTUALIZA registros de Custom Object de
  forma nativa**, con mapeo de campos y deduplicación por email, teléfono o **una clave
  personalizada** `[DOC 155000006384]`. Con `referencia` declarada campo único
  `[DOC 155000006668]`, el mismo formulario sirve de alta y de edición. Eso es
  exactamente la página de carga que se pedía, y no cuesta desarrollo.
- **Un formulario NO puede crear un Producto de tienda.** Eso exige API v2
  (`POST /products`, `POST /products/:id/price`, `POST /medias/upload-file`). Es decir,
  **n8n hacía falta en las dos arquitecturas**. El Custom Object no añade un sistema.
- **Los Productos no admiten campos personalizados arbitrarios.** Los *product custom
  values* son un set cerrado (nombre, descripción, tipo, precio, SKU, stock, envío) y
  `[DOC]` solo resuelven en la ficha de producto, no en el listado ni en otras páginas.
  Garaje, piscina y nº de baños acabarían siendo texto dentro de la descripción.
- **Los Custom Objects están en todos los planes** desde octubre de 2025, con 10 objetos
  por subcuenta `[DOC 155000006631]`, y tienen **triggers y acciones nativos de workflow**
  `[DOC 155000004389]`.

---

## Comparativa

| Criterio | Tienda / Productos | Custom Objects solos | Blogs | Objeto + render a medida |
|---|---|---|---|---|
| Render público nativo | Sí, 5 páginas automáticas | **No encontré ninguno** | Sí | No, se construye |
| Ficha de detalle | Plantilla única + fichas personalizadas 1:1 | — | Cuerpo del post | Total control |
| Galería multi-imagen | Sí, estilo único para toda la tienda | — | En el cuerpo | A medida |
| Atributos estructurados | **No** | **Sí, tipados** | No | **Sí** |
| Filtro público | Solo disponibilidad y rango de precio `[DOC 155000003046]` | — | Por categoría | **Cualquiera** |
| Buscador | Sí, título y descripción | — | Solo en el blog | A medida |
| SEO / slug | Sí, handle propio por producto | — | Sí | A medida |
| Alta por la clienta | UI de Productos, o formulario + n8n | **Formulario nativo, alta y edición** | Editor de blog | **Formulario nativo** |
| Triggers de workflow | Limitados, orientados a pedido | **Sí, nativos** | No | **Sí, nativos** |
| Carrito | Se crea y hay que ocultarlo | No aplica | No | **No existe** |

**Descartados.** *Blogs*: sin atributos estructurados y sin filtro por precio; cada ficha
sería mantenimiento manual. *Fuente externa* (Sheets, Airtable, Supabase): saca el
inventario del CRM, añade una suscripción más y no aporta nada que el objeto no dé por
debajo de ~40 fichas.

---

## Arquitectura recomendada

```
  Irene rellena la encuesta de alta          (página GHL, su dominio, URL no listada)
                 │
                 ▼
  Custom Object "Propiedad"                  FUENTE ÚNICA DE VERDAD
   · campos tipados: garaje, piscina, baños, zona, precio, estado
   · clave única "referencia" -> el mismo formulario edita
   · asociación nativa al contacto propietario
                 │  trigger nativo de registro
                 ▼
  Workflow AP01  ──webhook──►  n8n
                                │ · redimensiona las fotos      <- IMPRESCINDIBLE
                                │ · publica el feed JSON
                                │ · escribe de vuelta url_ficha
                                ▼
  Listado y ficha a medida                   RENDER
   · filtros en el navegador: precio, zona, garaje, piscina, baños
   · sin carrito, sin checkout, sin página de gracias
```

Sincronización en un solo sentido. La verdad vive en el CRM, junto al propietario, el
mandato y la comisión.

**A menos de 40 propiedades el filtrado va en el navegador**, sobre el feed completo.
Sin backend, sin paginación, sin índice. Por encima de ~100 fichas hay que replantearlo.

---

## Dos trampas que hay que resolver en el build

**1. El límite de subida de fotos no cuadra consigo mismo.** El formulario acepta
archivos de hasta 50 MB, pero Media Storage acepta 25 MB `[DOC 48001216629]`. Una foto
de móvil de una agente inmobiliaria **pasa el formulario y revienta al publicarse**. El
nodo de redimensionado en n8n no es opcional; es lo que hace que el sistema funcione en
manos reales.

**2. GHL no espera la respuesta del webhook.** No se puede encadenar "llama a n8n y
sigue con lo que devuelva". n8n tiene que **escribir de vuelta** `url_ficha` en el
registro, y el workflow continúa con un trigger de campo actualizado.

---

## Acceso a la página de alta

**GHL no tiene protección por contraseña ni login nativo para páginas de sitio o
embudo.** Hay varias peticiones de esa función abiertas en su portal de ideas, lo que es
buena señal de que no existe. Los trucos de JavaScript que circulan **no son seguridad** y
no se deben vender como tal.

Lo que sí hay:

- **URL no listada bajo su dominio** — `sudominio.es/gestion-a7f3k2`, fuera del menú,
  `noindex`, con token oculto que n8n valida. Cumple literalmente "una página en GHL
  dentro de su mismo dominio". **Recomendado por defecto.**
- **Client Portal con dominio propio** `[DOC 155000002561]` — login real con magic link
  y contraseña. Es montar una membresía para un solo usuario: se cotiza como opción.
- **Que use la app de GHL con su usuario** — lo más seguro y cero build, pero no es
  "su dominio".

---

## Portales inmobiliarios: por qué no se promete sindicación

**Idealista prohíbe expresamente el scraping** en sus condiciones: no se permite *"use,
copy, monitor (for example, spider, scrape), display, download, save or reproduce the
content… for any commercial or competitive activity without our prior written
permission"*. Su API no tiene precio público y el acceso es por solicitud de partner.

Y si lo que se extrae son **nombres y teléfonos de particulares** que publican su casa,
eso es dato personal: RGPD, base legal para el contacto en frío, y derecho *sui generis*
de base de datos del titular del portal.

Conclusión operativa: **la extracción automatizada no entra en un alcance cerrado.** Lo
que sí se puede vender, y es donde está el valor real, es el **seguimiento**: pipeline de
captación y secuencia automática de contacto alimentada manualmente por la agente, con
opt-out en cada mensaje. Y el canal sostenible de verdad son las **campañas a vendedores**.

Cuando un tercero cobra 50 €/mes por "buscar particulares en Idealista y escribirles", lo
que se está comprando sobre todo es que el riesgo técnico y legal lo asuma otro.

---

## Checklist de validación en la cuenta

Comprobar **antes** de firmar alcance. Los marcados 🔴 bloquean la arquitectura.

| # | Validar | Bloquea |
|---|---|---|
| V01 | Plan de la subcuenta y objetos disponibles | Todo |
| V02 | 🔴 Que un formulario **actualice** un registro existente por clave única | Edición de propiedad |
| V03 | 🔴 Que el Custom Object admita **campo de subida de archivos** para las fotos | Fotos |
| V04 | 🔴 Scopes del token: `objects/records.write`, `medias.write` | n8n |
| V05 | Que la página de alta sirva bajo el dominio del cliente y se pueda `noindex` | Acceso |
| V06 | Máximo de imágenes por registro, orden y foto de portada | Fotos |
| V07 | Que las URLs de archivo del formulario sean accesibles desde n8n sin auth | Fotos |
| V08 | Comportamiento real del redimensionado: 50 MB entra, 25 MB publica | Fotos |
| V09 | Trigger de registro creado/actualizado y su latencia | AP01 |
| V10 | Que el feed JSON se pueda servir con CORS desde el dominio del sitio | Render |
| V11 | Buscador con acentos y ñ (Málaga, baños) | Búsqueda |
| V12 | Banner de cookies RGPD nativo o de tercero | Legal |
| V13 | Que un formulario con campos de objeto se pueda clonar a otra subcuenta | Segundo cliente |

V13 importa más de lo que parece: la documentación menciona limitaciones al compartir
formularios con campos de custom object entre subcuentas. Si no se pueden clonar, el
segundo cliente lleva rehacer el formulario, no copiarlo — y eso es tiempo a presupuestar.

---

## Fuentes

Documentación de HighLevel (vía resúmenes de buscador, no leídas directamente):
[Custom Objects en formularios y encuestas](https://help.gohighlevel.com/support/solutions/articles/155000006384-custom-objects-and-company-objects-in-forms-surveys-quizzes) ·
[Campos únicos en Custom Objects](https://help.gohighlevel.com/support/solutions/articles/155000006668-custom-objects-unique-fields-support) ·
[Custom Objects en todos los planes](https://help.gohighlevel.com/support/solutions/articles/155000006631-custom-objects-in-all-plans-higher-limit) ·
[Custom Objects en workflows](https://help.gohighlevel.com/support/solutions/articles/155000004389-using-custom-objects-in-workflow-actions-and-triggers) ·
[Orden y filtro del listado de productos](https://help.gohighlevel.com/support/solutions/articles/155000003046-how-to-sort-and-filter-products-in-highlevel-ecommerce-site-builder) ·
[Colecciones manuales e inteligentes](https://help.gohighlevel.com/support/solutions/articles/155000006616-products-manual-and-smart-collections) ·
[Fichas de producto personalizadas](https://help.gohighlevel.com/support/solutions/articles/155000006238-custom-product-details-page-for-e-commerce-stores) ·
[Montar una tienda](https://help.gohighlevel.com/support/solutions/articles/155000001157-how-to-set-up-an-e-commerce-online-store-websites-) ·
[Dominios whitelabel y Client Portal](https://help.gohighlevel.com/support/solutions/articles/155000002561-setting-up-whitelabel-domain-api-domain-email-sending-domain-sites-domain-client-portal-domain-) ·
[Límites de Media Storage](https://help.gohighlevel.com/support/solutions/articles/48001216629-media-storage-file-upload-limits) ·
[API de productos](https://marketplace.gohighlevel.com/docs/ghl/products/create-product/) ·
[API de subida de media](https://marketplace.gohighlevel.com/docs/ghl/medias/upload-media-content/) ·
[API de registros de objeto](https://marketplace.gohighlevel.com/docs/ghl/objects/search-object-records/)

Otras: [Condiciones de uso de idealista](https://www.idealista.com/ayuda/articulos/legal-statement/?lang=en) ·
[Nodo de HighLevel en n8n](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.highlevel/) ·
[Textos legales obligatorios en webs españolas](https://protecciondatos-lopd.com/empresas/textos-legales-web/)
