"""
Scope de Fase 1 para la oferta "Web + CRM inmobiliario v1".

Sirve tal cual a Irene y al segundo cliente: el alcance es idéntico, solo cambian
marca y precio final. Se alimenta a calcular_cotizacion() de la skill ghl-cotizador.

    python3 scope_fase1.py

IMPORTANTE — dos líneas del presupuesto NO salen de tabla_precios.md y por eso van
aparte, en LINEAS_FUERA_DE_TABLA:

  1. "Sitio web multipágina" sustituye al módulo 7 (Landing Pages). La regla de
     +$300 por página extra se escribió para embudos de 1-3 páginas; aplicada a un
     sitio de 7 daba $2.410, el 51% del proyecto. Tramo acordado: $1.500 base hasta
     6 páginas + $200 por página adicional.
  2. "Listado y ficha a medida" no tiene línea en la tabla: es desarrollo front-end
     real (feed JSON desde n8n + render + filtros por atributos en el navegador).
     Nace de la decisión de NO usar el módulo Tienda. Cifra propuesta, a confirmar.

Por eso landing_pages va vacío en el scope: si se dejara, el cotizador volvería a
aplicar la regla vieja y contaría el sitio dos veces.
"""

SCOPE_FASE1 = {
    "cliente": "Web + CRM inmobiliario — Fase 1",
    # Agencia nueva: dominio, correo y WhatsApp se montan desde cero.
    "setup_subcuenta": "completo",
    "pipelines": [
        # 5 etapas cada uno = dentro del límite base, sin extras.
        {"nombre": "P1 · Captación (inventario)", "etapas": 5},
        {"nombre": "P2 · Compradores (demanda)", "etapas": 5},
    ],
    "vistas_filtros": 2,  # Propiedades publicadas + Visitas de esta semana
    "workflows": [
        {"nombre": "LS01 · Lead web y origen de contacto", "nodos": 8},
        {"nombre": "LS02 · Solicitud de visita desde ficha", "nodos": 8},
        {"nombre": "LS03 · Captación 'Vende tu propiedad'", "nodos": 8},
        {"nombre": "LS04 · Prospección manual de particulares", "nodos": 10},
        {"nombre": "AP01 · Alta / actualización / retirada de propiedad", "nodos": 8},
        {"nombre": "SP01 · Visita agendada: confirmación y recordatorios", "nodos": 10},
    ],
    "integraciones": 1,  # n8n <-> GHL API v2 (objects/records, medias)
    "plantillas": 4,     # confirmación de visita, ficha por email, valoración, prospección
    "calendarios": True, # C01 Visitas + C02 Valoración a domicilio
    "landing_pages": [], # ver docstring: el sitio se cobra en LINEAS_FUERA_DE_TABLA
    "reportes": False,   # la transcripción nunca menciona reporting -> Fase 2-C
    "sesiones_capacitacion": 2,
    "soporte": True,
    "pago_anual_soporte": False,
}

# Páginas reales del sitio. Se cuentan aquí, no en el scope del cotizador.
PAGINAS_SITIO = [
    ("Inicio", 7),
    ("Propiedades (listado)", 4),
    ("Ficha de propiedad", 6),
    ("Sobre mí", 4),
    ("Vende tu propiedad", 6),
    ("Contacto", 3),
    ("Alta de propiedad (URL no listada)", 3),
]
# Aviso legal, privacidad y cookies se maquetan sin cargo de diseño.

SITIO_BASE = 1500        # incluye hasta 6 páginas
SITIO_PAGS_INCLUIDAS = 6
SITIO_PAG_EXTRA = 200
DESARROLLO_LISTADO_FICHA = 1200  # propuesto, a confirmar

USD_A_EUR = 0.87  # declarado en la propuesta. A 2026-09-02 el spot era 0,8631.


def precio_sitio(paginas=PAGINAS_SITIO):
    extra = max(0, len(paginas) - SITIO_PAGS_INCLUIDAS)
    return SITIO_BASE + extra * SITIO_PAG_EXTRA


def lineas_fuera_de_tabla():
    return [
        (f"Sitio web multipágina ({len(PAGINAS_SITIO)} págs)", precio_sitio()),
        ("Listado y ficha a medida (a confirmar)", DESARROLLO_LISTADO_FICHA),
    ]


def eur(usd, redondeo=50):
    """Convierte a euros redondeando al alza al múltiplo indicado."""
    import math
    return int(math.ceil(usd * USD_A_EUR / redondeo) * redondeo)


if __name__ == "__main__":
    import sys
    sys.path.insert(
        0,
        "/root/.claude/skills/synced/de67ae3e-d8ff-43c5-84c4-263db8b09f22"
        "_24b47049-24e1-40fb-a8ea-cc102e3d7139/ghl-cotizador/scripts",
    )
    from ghl_cotizador import calcular_cotizacion

    r = calcular_cotizacion(SCOPE_FASE1)
    carte = r["a_la_carte"]

    print("=" * 62)
    print("  FASE 1 — desglose")
    print("=" * 62)
    for m in carte["desglose"]:
        print(f"  {m['modulo']:.<46} ${m['setup']:>8,.0f}")
        for d in m["detalle"]:
            print(f"      · {d}")
    print("-" * 62)
    subtotal_tabla = carte["setup"]
    print(f"  {'Subtotal según tabla de precios':.<46} ${subtotal_tabla:>8,.0f}")
    print()
    for nombre, importe in lineas_fuera_de_tabla():
        print(f"  {nombre:.<46} ${importe:>8,.0f}")
    total = subtotal_tabla + sum(i for _, i in lineas_fuera_de_tabla())
    print("=" * 62)
    print(f"  {'TOTAL SETUP':.<46} ${total:>8,.0f}")
    print(f"  {'TOTAL MENSUAL':.<46} ${carte['mensual']:>8,.0f}")
    print("=" * 62)
    print(f"  En euros a {USD_A_EUR}: {eur(total):,} EUR setup / {eur(carte['mensual'], 5):,} EUR mes")
    print()
    mejor = r["mejor_paquete"]
    print("  Paquetes (comparados solo sobre lo que sí cubre la tabla):")
    print("   ", "ninguno ahorra -> À LA CARTE" if not mejor else "mejor: " + mejor["paquete"])
    for p in r["todos_paquetes"]:
        print(f"    {p['paquete']:<12} setup ${p['setup_total']:>7,.0f}"
              f"  mes ${p['mensual_total']:>5,.0f}"
              f"  ahorro 1er año ${p['ahorro_total_primer_año']:>8,.0f}")
