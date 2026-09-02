# Arquitectura — Web + CRM inmobiliario v1

Cómo se monta por dentro. Documento interno: nada de esto va a la propuesta del cliente.

El porqué de las decisiones está en `../../docs/ghl-listado-inmobiliario.md`. Aquí está
el cómo.

---

## Piezas

```
  ENCUESTA S01 "Alta de propiedad"          página GHL, dominio del cliente,
        │                                    URL no listada + noindex
        │  escritura nativa, sin código
        ▼
  CUSTOM OBJECT "Propiedad"                 FUENTE ÚNICA DE VERDAD
        │  campos tipados · clave única "referencia" · asociación al propietario
        │
        │  trigger nativo: registro creado o actualizado
        ▼
  WORKFLOW AP01                             orquesta
        │
        │  webhook (GHL no espera respuesta)
        ▼
  n8n                                       PUBLICACIÓN
        │  1. descarga las fotos del formulario
        │  2. REDIMENSIONA Y COMPRIME        <- sin esto, el sistema se rompe
        │  3. sube a Media Storage
        │  4. regenera el feed JSON del listado
        │  5. escribe de vuelta url_ficha en el registro
        ▼
  LISTADO + FICHA a medida                  RENDER
        filtros en el navegador sobre el feed completo
```

## Contrato del feed

n8n publica un único JSON con las propiedades en estado `Publicada`. El listado y la
ficha lo consumen en el navegador; a este volumen no hace falta backend ni paginación.

```json
{
  "generado": "2026-09-02T10:00:00Z",
  "propiedades": [
    {
      "referencia": "REF-0001",
      "titulo": "Piso · 3 hab · 2 baños · Garaje · Piscina · [Zona]",
      "precio": 425000,
      "zona": "…",
      "tipo_inmueble": "piso",
      "num_habitaciones": 3,
      "num_banos": 2,
      "garaje": true,
      "piscina": true,
      "metros_construidos": 118,
      "descripcion": "…",
      "fotos": ["https://…/1.jpg", "https://…/2.jpg"],
      "portada": "https://…/1.jpg",
      "url_ficha": "https://…/propiedades/ref-0001"
    }
  ]
}
```

Los filtros de garaje, piscina y nº de baños se resuelven contra estos campos. Es
justo lo que el módulo de tienda no permite hacer.

---

## Las dos trampas conocidas

**1. Fotos: 50 MB entran, 25 MB publican.** El formulario acepta archivos de hasta 50 MB
pero Media Storage acepta 25 MB. Una foto de móvil sin comprimir **pasa el formulario y
falla al publicarse**, y el fallo ocurre lejos de donde la clienta lo provocó. El paso de
redimensionado en n8n no es un refinamiento: es lo que hace que funcione en manos reales.
Comprobar en V08.

**2. GHL no espera la respuesta del webhook.** No se puede hacer "llama a n8n y sigue con
lo que devuelva". Por eso n8n **escribe de vuelta** `url_ficha` en el registro y AP01
continúa con un trigger de campo actualizado. Cualquier diseño que asuma respuesta
síncrona va a fallar en producción.

## Manejo de errores

- Si falla la subida de una foto: el registro queda en `Borrador`, y se avisa por email
  interno con la referencia y el motivo. Nunca se publica una ficha a medias.
- Si falla la regeneración del feed: se conserva el feed anterior. El sitio sigue en pie
  mostrando lo último bueno, en lugar de quedarse en blanco.
- Toda ejecución de n8n queda registrada con la referencia del inmueble, para poder
  reconstruir qué pasó con cada alta.

## Acceso a la página de alta

Por defecto, **URL no listada** bajo su dominio: fuera del menú, con `noindex`, y un token
oculto en el formulario que n8n valida. GHL no tiene contraseña ni login nativo para
páginas de sitio, y los trucos de JavaScript que circulan no son seguridad — no se venden
como tal.

Si el cliente pide login de verdad, la opción es el Client Portal con dominio propio, y se
cotiza aparte.

## Segundo cliente

El alcance es idéntico. Lo que hay que verificar antes de prometer plazo es **V13**: si un
formulario con campos de custom object se puede clonar entre subcuentas. La documentación
menciona limitaciones. Si no se puede, el segundo cliente lleva **rehacer** el formulario,
no copiarlo, y eso es tiempo que hay que presupuestar.

## Validaciones

La lista completa V01–V13 está en `../../docs/ghl-listado-inmobiliario.md`. Las que
bloquean la arquitectura entera: **V02** (que el formulario actualice por clave única),
**V03** (campo de fotos en el objeto) y **V04** (scopes del token).
