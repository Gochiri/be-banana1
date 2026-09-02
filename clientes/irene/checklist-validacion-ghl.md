# Irene — validación en la cuenta de GHL

Comprobar **antes de firmar el alcance**. Los 🔴 bloquean la arquitectura entera: si
alguno falla, hay que replantear antes de prometer plazo o precio.

Detalle y fuentes: `../../docs/ghl-listado-inmobiliario.md`.

## Bloqueantes

- [ ] **V02** 🔴 Un formulario con campo de custom object **actualiza** un registro
      existente usando `referencia` como clave única. No solo lo crea.
      *Si falla:* no hay edición de propiedades por autoservicio; hay que ir a n8n para
      todo y el formulario pasa a ser solo un disparador.
- [ ] **V03** 🔴 El Custom Object admite **campo de subida de archivos** para las fotos.
      *Si falla:* las fotos van por otra vía (contacto, o paso aparte), y el flujo de
      alta se complica.
- [ ] **V04** 🔴 El token tiene los scopes `objects/records.write` y `medias.write`.
      *Si falla:* n8n no puede publicar.

## Arquitectura

- [ ] **V01** Plan de la subcuenta y cuántos objetos personalizados quedan disponibles.
- [ ] **V05** La página de alta sirve bajo el dominio del cliente y se puede marcar
      `noindex` y sacar del menú.
- [ ] **V09** El trigger de "registro creado o actualizado" dispara, y con qué latencia.
- [ ] **V10** El feed JSON se puede servir con CORS desde el dominio del sitio.

## Fotos — donde más probable es que se rompa

- [ ] **V06** Máximo de imágenes por registro, orden y cuál queda de portada.
- [ ] **V07** Las URLs de archivo que devuelve el formulario son accesibles desde n8n
      sin autenticación.
- [ ] **V08** Confirmar el desajuste: el formulario acepta 50 MB pero Media Storage
      acepta 25 MB. **Subir una foto de móvil sin comprimir y ver dónde falla.**
      Es lo que va a pasar en manos de la clienta el primer día.

## Detalles que muerden tarde

- [ ] **V11** El buscador encuentra con acentos y ñ: probar "Málaga" y "baños".
- [ ] **V12** Banner de cookies: nativo o de tercero, y cuál cumple RGPD.
- [ ] **V13** Un formulario con campos de custom object **se puede clonar a otra
      subcuenta**. La documentación menciona limitaciones.
      *Si falla:* el segundo cliente lleva **rehacer** el formulario, no copiarlo.
      Eso es tiempo que hay que presupuestar antes de prometerle plazo.

---

## Antes de mandarle la cotización a Sonia

- [ ] Confirmar los $1.200 de "listado y ficha a medida" — mueve todos los importes.
- [ ] Rellenar `PON_AQUI_URL_LOGO` y `PON_AQUI_LINK_CALENDARIO`.
- [ ] Releer el bloque "Qué no incluye" pensando en lo que Irene podría dar por supuesto:
      es la sección que evita el conflicto, y solo funciona si es específica de ella.

Precios y voz del documento ya están cerrados: es la cotización de Profit Technology a
Be Banana, en euros, sin el margen de Sonia dentro.
