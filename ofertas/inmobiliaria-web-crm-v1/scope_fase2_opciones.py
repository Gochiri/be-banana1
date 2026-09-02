"""
Opciones de Fase 2 — precios MARGINALES sobre una Fase 1 ya construida.

Marginal significa que las bases de módulo (Workflows $350, Integraciones $300,
Documentos $200, Sitio web) ya están pagadas en Fase 1, así que aquí solo se cobra
lo que escala: workflows extra, nodos extra, plantillas extra, páginas extra.

Vender estas opciones a precio standalone sería cobrar dos veces la misma base.

    python3 scope_fase2_opciones.py

Nota: el buscador con filtros por garaje/piscina/baños NO aparece aquí. Con la
arquitectura sin tienda entra en Fase 1 por construcción.
"""

# Factores de escala de tabla_precios.md
WF_EXTRA = 70
NODO_EXTRA = 12
NODOS_BASE = 8
PLANTILLA_EXTRA = 50
INTEGRACION_EXTRA = 300
INTEGRACION_MENSUAL = 50
CHATBOT_BASE = 400
CHATBOT_NODOS_BASE = 10
CHATBOT_NODO_EXTRA = 15
CHATBOT_IA_AVANZADA = 150
CHATBOT_MENSUAL = 80
REPORTES = 250
REPORTES_MENSUAL = 60
CAPACITACION_SESION = 200
PAGINA_EXTRA = 200  # línea nueva "Sitio web multipágina"


def coste_workflows(wfs):
    """Coste marginal de N workflows: todos son extra, más sus nodos por encima de 8."""
    total = len(wfs) * WF_EXTRA
    for _, nodos in wfs:
        total += max(0, nodos - NODOS_BASE) * NODO_EXTRA
    return total


OPCIONES = {}

# ─── A · Matching comprador <-> propiedad ────────────────────────────────────
# El motor de "tiene compradores, le falta inventario".
_a_wfs = [
    ("SP02 · Seguimiento post-visita", 11),
    ("SP03 · Alerta de nueva propiedad a compradores con criterio compatible", 10),
    ("SP04 · Nurture del comprador sin match", 12),
]
OPCIONES["A · Matching comprador ↔ propiedad"] = {
    "workflows": _a_wfs,
    "setup": coste_workflows(_a_wfs),
    "mensual": 0,
    "porque": "Ella tiene compradores de 20 años. Esto los reactiva sola cada vez "
              "que entra una propiedad que encaja con lo que pidieron.",
}

# ─── B · Reseñas y reputación ────────────────────────────────────────────────
_b_wfs = [
    ("PS01 · Solicitud de reseña tras la firma", 8),
    ("PS02 · Reseña recibida: aviso y publicación", 8),
]
OPCIONES["B · Reseñas y reputación"] = {
    "workflows": _b_wfs,
    "setup": coste_workflows(_b_wfs) + 2 * PLANTILLA_EXTRA,
    "mensual": 0,
    "porque": "Refuerza justo su problema de origen: que quien busque su nombre "
              "la encuentre a ella y con prueba social.",
}

# ─── C · Campañas Meta de captación de inventario ────────────────────────────
# El canal sostenible que sustituye la idea de raspar Idealista.
_c_wfs = [
    ("LS05 · Lead de Meta Lead Ads", 10),
    ("LS06 · Cualificación dura de vendedor", 16),
    ("LS07 · Ruteo de comprador/alquiler a asesor", 9),
    ("AP04 · Recuperación de no cualificados", 12),
]
_c_chatbot = coste_workflows([]) + CHATBOT_BASE + \
    max(0, 12 - CHATBOT_NODOS_BASE) * CHATBOT_NODO_EXTRA + CHATBOT_IA_AVANZADA
OPCIONES["C · Campañas Meta de captación"] = {
    "workflows": _c_wfs,
    "setup": (coste_workflows(_c_wfs) + _c_chatbot + INTEGRACION_EXTRA
              + PAGINA_EXTRA + REPORTES + CAPACITACION_SESION),
    "mensual": INTEGRACION_MENSUAL + CHATBOT_MENSUAL + REPORTES_MENSUAL,
    "porque": "Lo que le funciona al otro cliente inmobiliario del equipo: anunciar "
              "a quien QUIERE VENDER, no a quien quiere comprar. Cualifica duro al "
              "vendedor y deriva directo al asesor al comprador y al de alquiler.",
    "nota": "NO incluye la inversión publicitaria. Esa la pone ella y va aparte.",
}


if __name__ == "__main__":
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from scope_fase1 import eur, precio_cliente_final, MARGEN_SONIA

    print("=" * 68)
    print("  FASE 2 — opciones, precio marginal sobre Fase 1")
    print("=" * 68)
    tot_s = tot_m = 0
    for nombre, o in OPCIONES.items():
        print(f"\n  {nombre}")
        for wf, nodos in o["workflows"]:
            print(f"      {wf} ({nodos} nodos)")
        extra = o.get("nota")
        if extra:
            print(f"      ! {extra}")
        linea = f"      -> nosotros: {eur(o['setup']):,} EUR"
        if o["mensual"]:
            linea += f" + {eur(o['mensual'], 5):,} EUR/mes"
        linea += f"   |  Irene (ref.): {precio_cliente_final(o['setup']):,} EUR"
        if o["mensual"]:
            linea += f" + {precio_cliente_final(o['mensual'], 5):,} EUR/mes"
        print(linea)
        tot_s += o["setup"]
        tot_m += o["mensual"]
    print("\n" + "=" * 68)
    print(f"  Las tres juntas -> nosotros: {eur(tot_s):,} EUR + {eur(tot_m, 5):,} EUR/mes")
    print(f"  {'':>17} Irene (ref.): {precio_cliente_final(tot_s):,} EUR"
          f" + {precio_cliente_final(tot_m, 5):,} EUR/mes")
    print(f"  (margen de Sonia {MARGEN_SONIA:.0%})")
    print("=" * 68)
