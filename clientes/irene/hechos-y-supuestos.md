# Irene — hechos y supuestos

Origen: llamada del equipo del **2026-09-02**. Irene no estuvo en esa llamada; todo lo de
aquí es lo que Sonia contó sobre ella.

Los hechos se numeran para poder citarlos desde la propuesta. **La propuesta no puede
afirmar nada que no esté en la tabla de hechos.** Todo lo demás va en supuestos y se
cierra en la reunión de revisión con ella.

Sin datos personales en este repo: ni apellido, ni teléfono, ni email, ni dirección.

---

## Hechos

| # | Hecho |
|---|---|
| H01 | Lleva unos 20 años en el sector, siempre trabajando para otras agencias. Acaba de montar la suya. |
| H02 | Sus antiguos clientes la buscan **a ella**, no a la agencia. Ha habido casos de clientes que llamaron a agencias donde ya no trabaja y no se les redirigió; uno compró una casa que habría querido comprar con ella. |
| H03 | Está cerrando su marca y quiere la dirección web en sus tarjetas de visita. Es lo que necesita con urgencia. |
| H04 | Tiene pocas propiedades. Estimación de Sonia: no más de 10. |
| H05 | Atributos de propiedad mencionados textualmente: **garaje sí/no, piscina sí/no y número de baños**. Y una **ficha** por vivienda. |
| H06 | No trabaja con Idealista. Idealista cobra unos 500 €/mes por publicar 5 casas, sin gestionar los leads. |
| H07 | Iba a pagar 50 €/mes a un tercero por una automatización que busca particulares que publican en Idealista y les escribe. |
| H08 | **Tiene compradores; lo que le falta es inventario.** |
| H09 | La comisión en su zona es del 10-12% del valor de la vivienda, y la paga quien vende. |
| H10 | En su zona no hay ninguna vivienda por debajo de 400.000 €. |
| H11 | Ha vendido una casa que firma en noviembre. Otras dos las vendió estando en otra agencia, y de esas se lleva alrededor del 2% de los 12; el resto va a la agencia. |
| H12 | No hace campañas de publicidad. Las querrá más adelante. |
| H13 | Sonia le factura por porcentaje de venta más un mínimo mensual. Las suscripciones las paga Irene. |
| H14 | Hay un **segundo cliente**, conocido suyo y de otra agencia, que quiere lo mismo a precio completo. Ambos saben que se les presenta el mismo proyecto. |
| H15 | Otro cliente inmobiliario del equipo hace campañas **solo para captar inventario**: cualifica en detalle a quien quiere vender y deriva directamente a un asesor a quien solo quiere comprar o alquilar. Le funciona. |

### Aritmética admisible en la propuesta

De H09 y H10, y **solo** de ahí: una sola venta al mínimo de su zona son **40.000 a
48.000 € de comisión** (400.000 € × 10-12%).

Es aritmética sobre cifras que ella dio. Cualquier otra métrica —conversiones, plazos de
venta, retorno esperado— sería inventada y **no puede aparecer**.

### Contradicción sin resolver

En la llamada se dice también que "está vendiendo unas tres casas al mes", que no encaja
con H11 (tres ventas en total, y una firma en noviembre). **No usar ninguna de las dos
cifras en la propuesta** hasta aclararlo con ella.

---

## Supuestos

Todo esto está sin confirmar. Va marcado como tal en el mapa de alcance y se cierra en la
reunión de revisión.

| # | Supuesto | Impacto si falla |
|---|---|---|
| S01 | Zona geográfica concreta en la que opera | Los desplegables de zona del listado |
| S02 | Campos de ficha más allá de garaje, piscina y baños: tipo de inmueble, habitaciones, metros, certificado energético | Estructura del objeto y del formulario de alta |
| S03 | El sitio va solo en español | Multi-idioma es un módulo entero |
| S04 | Entre 8 y 15 fotos por propiedad | Dimensionado del redimensionado y del almacenamiento |
| S05 | Soporte en horario laboral, sin guardias | Precio del soporte mensual |
| S06 | Trabaja venta, no alquiler. El alquiler solo aparece en el contexto de las campañas | Haría falta un tercer pipeline |
| S07 | Ella misma cargará las propiedades, con formulario de autoservicio | La alternativa es servicio gestionado y cambia la cuota mensual |
| S08 | Nombre y marca del segundo cliente | Su propuesta no se puede renderizar todavía |

---

## Preguntas para la reunión de revisión

1. Confirmar S01 a S07.
2. ¿Cuántas propiedades tiene ahora mismo y cuántas espera tener en un año?
3. ¿Quién hace las fotos? El sitio vive o muere por ellas y no están en alcance.
4. ¿Tiene ya el dominio contratado? ¿Y el logo en formato editable?
5. ¿Quién le redacta los textos legales?
6. La fecha real de "urgente": ¿cuándo manda a imprimir las tarjetas?
7. Aclarar la contradicción sobre el ritmo de ventas.
