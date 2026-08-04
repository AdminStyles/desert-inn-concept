# -*- coding: utf-8 -*-
"""
es_translations.py -- Spanish (es) copy for Desert Inn Sports Bar & Grill's
bilingual toggle. Parallel structure to brand_config.py / build_*.py content;
edit facts in brand_config.py, edit Spanish wording here. Keys mirror the
English strings emitted by site_common.py and build_homepage.py/build_menu_items.py.
Filled in 2026-08-03.
"""

NAV_ES = {
    "MENU": "MENÚ",
    "SPECIALS": "PROMOCIONES",
    "Specials": "Promociones",
    "FIND US": "UBICACIÓN",
    "Find Us": "Ubicación",
}

ORDER_LABEL_ES = "LLAMAR PARA ORDENAR"
CALL_LABEL_ES = "LLAMAR"
FOLLOW_ES = "Síguenos"

# ---------------------------------------------------------------------------
# Hero (Hero 4 -- stacked photo collage)
# ---------------------------------------------------------------------------
HERO_BADGE_ES = "BAR DEPORTIVO Y PARRILLA &middot; METOLIUS, OR"
HERO_HEADING_ES = 'Tu destino para<br><span class="accent">deportes y diversión</span>'
HERO_SUB_ES = ("Comida para cenar adentro, afuera o para llevar en Metolius. Bar completo, "
               "cobertura total de los partidos, y un menú con la comida que realmente "
               "quieres después del último silbatazo.")
HERO_MENU_BTN_ES = "Ver el menú completo"

# ---------------------------------------------------------------------------
# Trust strip
# ---------------------------------------------------------------------------
TRUST_ES = [
    ("Música en Vivo y Eventos", "Entretenimiento"),
    ("Cerveza, Vino y Licor", "Bar Completo"),
    ("Interior y Exterior", "Para comer o llevar"),
    ("Acepta Mascotas", "Terraza para mascotas"),
]

# ---------------------------------------------------------------------------
# Features (favorites() falls back to this icon-card layout -- no FAVORITES set)
# ---------------------------------------------------------------------------
FEATURES_ES = [
    ("Día de juego, todos los días",
     "Múltiples televisores en todo el local para fútbol americano, básquetbol, "
     "béisbol, hockey y más."),
    ("Bar completo",
     "Una amplia selección de cerveza, vino y licor &mdash; algo para todos."),
    ("Ambiente familiar y para mascotas",
     "Comedor interior y exterior, para llevar, y una terraza que acepta mascotas."),
]

# ---------------------------------------------------------------------------
# Weekly specials (Scroll 4 -- horizontal scroll-snap add-on)
# ---------------------------------------------------------------------------
EVENTS_SNAP_TAG_ES = "PROMOCIONES SEMANALES"
EVENTS_SNAP_TITLE_ES = "Siempre hay algo especial"
EVENTS_SNAP_ES = [
    ("Martes de Tacos", "3 tacos &mdash; $9.99"),
    ("Miércoles de Alitas", "10 alitas &mdash; $12.99"),
    ("Viernes de Pescado Frito", "$14.99"),
    ("Plato para el Día del Juego", "$26.99 &mdash; hecho para compartir"),
]

# ---------------------------------------------------------------------------
# Story (photo-beside-text pattern -- STORY_IMAGE is set)
# ---------------------------------------------------------------------------
STORY_TAG_ES = "NUESTRA HISTORIA"
STORY_TITLE_ES = "Más que un bar deportivo"
STORY_BODY_ES = ("Desert Inn Sports Bar &amp; Grill es el destino vecinal de Metolius para "
                  "buena comida, bebidas refrescantes y un ambiente deportivo emocionante. "
                  "Con televisores en todo el local, disfruta de fútbol americano, "
                  "básquetbol, béisbol, hockey y más mientras comes. Es un lugar "
                  "para que amigos, familias, compañeros de trabajo y visitantes se "
                  "relajen, celebren, y lo conviertan en una parada habitual.")

# ---------------------------------------------------------------------------
# CTA band
# ---------------------------------------------------------------------------
CTA_TITLE_ES = "Ven a ver el partido"
CTA_SUB_ES = "385 Jefferson Ave, Metolius, OR &middot; Llama con anticipación para el horario de hoy"
CTA_BUTTON_ES = "VER MENU"

# ---------------------------------------------------------------------------
# Find us
# ---------------------------------------------------------------------------
FIND_US_TITLE_ES = "Encuéntranos"
DIRECTIONS_ES = "Cómo llegar &rarr;"

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
# FOLLOW_ES defined above

# ---------------------------------------------------------------------------
# Menu section titles (keyed by anchor, matches brand_config.MENU_SECTIONS)
# ---------------------------------------------------------------------------
MENU_SECTION_TITLES_ES = {
    "appetizers": "Aperitivos",
    "burgers": "Hamburguesas",
    "sandwiches": "Sándwiches y Wraps",
    "pizza": "Pizza",
    "baskets": "Canastas",
    "salads": "Ensaladas",
    "wings": "Alitas",
    "sides": "Acompañamientos",
    "desserts": "Postres",
    "beverages": "Bebidas",
}

MENU_INTRO_ES = ""

# ---------------------------------------------------------------------------
# Menu items -- keyed by anchor, list of (name_es_or_None, desc_es_or_None) in
# the exact order they appear in brand_config.MENU_SECTIONS. None = pass
# through the English value unchanged (proper dish name reads naturally as-is).
# ---------------------------------------------------------------------------
MENU_ITEMS_ES = {
    "appetizers": [
        ("Palitos de Mozzarella", None),
        ("Aros de Cebolla", None),
        ("Nachos Cargados", None),
        ("Pepinillos Fritos", None),
        ("Jalapeños Rellenos", None),
        ("Quesadilla de Pollo", None),
        ("Cáscaras de Papa Rellenas", None),
        ("Totopos con Salsa", None),
    ],
    "burgers": [
        ("Hamburguesa con Queso Clásica", None),
        ("Hamburguesa con Tocino y Queso", None),
        ("Hamburguesa de Champiñones y Queso Suizo", None),
        ("Hamburguesa BBQ", None),
        ("Hamburguesa con Jalapeño", None),
        ("Hamburguesa Doble", None),
        ("Hamburguesa Western", None),
        (None, None),  # Patty Melt -- proper dish name, reads fine as-is
    ],
    "sandwiches": [
        ("Sándwich de Pollo a la Parrilla", None),
        (None, None),  # Philly Cheesesteak
        ("Sándwich BLT", None),
        ("Sándwich Club", None),
        ("Wrap de Pollo Buffalo", None),
        ("Wrap de Pavo", None),
        (None, None),  # French Dip
        ("Sándwich de Cerdo Desmenuzado BBQ", None),
    ],
    "pizza": [
        ("Pizza de Queso", None),
        ("Pizza de Pepperoni", None),
        ("Pizza Amantes de la Carne", None),
        ("Pizza Suprema", None),
        ("Pizza de Pollo BBQ", None),
        ("Pizza Hawaiana", None),
        ("Pizza Vegetariana", None),
        ("Pizza Personalizada", None),
    ],
    "baskets": [
        ("Canasta de Pescado con Papas", None),
        ("Canasta de Tiras de Pollo", None),
        ("Canasta de Camarones", None),
        ("Canasta de Popcorn de Pollo", None),
        ("Canasta de Pescado Crujiente", None),
        ("Canasta de Alitas de Pollo", None),
    ],
    "salads": [
        ("Ensalada de la Casa", None),
        ("Ensalada César", None),
        ("Ensalada del Chef", None),
        ("Ensalada de Pollo a la Parrilla", None),
        ("Ensalada de Pollo Crujiente", None),
        ("Ensalada de Taco", None),
    ],
    "wings": [
        ("6 Alitas", None),
        ("10 Alitas", None),
        ("15 Alitas", None),
        ("20 Alitas", None),
        ("Alitas Sin Hueso", None),
    ],
    "sides": [
        ("Papas Fritas", None),
        ("Croquetas de Papa", None),
        ("Ensalada de Col", None),
        ("Ensalada Pequeña", None),
        ("Aros de Cebolla", None),
        ("Papas Fritas de Camote", None),
    ],
    "desserts": [
        ("Pastel de Chocolate", None),
        ("Pastel de Queso", None),
        ("Copa de Helado", None),
        ("Brownie con Helado", None),
        ("Pastel de Manzana", None),
    ],
    "beverages": [
        ("Refresco", None),
        ("Té Helado", None),
        ("Limonada", None),
        ("Café", None),
        ("Té Caliente", None),
        ("Agua Embotellada", None),
    ],
    # Full specials page (build_specials_page.py) -- same order as
    # brand_config.SPECIALS_LIST.
    "specials": [
        ("Especial de Almuerzo Diario", None),
        ("Especial de Hamburguesa y Papas Fritas", None),
        ("Martes de Tacos", "3 tacos"),
        ("Miércoles de Alitas", "10 alitas"),
        ("Viernes de Pescado Frito", None),
        ("Especial de Noche de Bistec", None),
        ("Cena de Costillas BBQ", None),
        ("Especial de Costilla Prime", None),
        ("Especial de Bistec Empanizado", None),
        ("Especial de Salmón a la Parrilla", None),
        ("Especial de Pizza Familiar", None),
        ("Bandeja para el Día del Juego", None),
        ("Combo de Aperitivos Happy Hour", None),
        ("Combo de Sopa y Sándwich", None),
        ("Especial de Canasta de Tiras de Pollo", None),
        ("Especial de Nachos Cargados", None),
        ("Combo de Sándwich de Cerdo Deshebrado", None),
        ("Combo de Dos Hamburguesas con Queso", None),
        ("Especial de Canasta de Camarones", None),
        ("Especial de Desayuno de Fin de Semana", None),
    ],
}

SPECIALS_PAGE_INTRO_ES = "Algo bueno cada día de la semana &mdash; aquí está la lista completa."
