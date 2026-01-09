import json
import random
import os

# --- 1. ESTRUCTURA DE COSTOS DE REVENTA ---
# El precio base NO es retail, es el "Lowest Ask" de StockX.
MARGEN_GANANCIA = 1500      # Tu ganancia limpia por par (MXN)
COSTO_ENVIO_MX = 400        # Envío USA -> Tu Bodega -> Cliente
IMPUESTO_ADUANA = 0.19      # 19% (Importación Global T-MEC simplificada)
TIPO_CAMBIO = 21.50         # Dólar "Protegido" (Para cubrir volatilidad diaria)
COMISION_PASARELA = 0.05    # 5% (Comisión de cobro con tarjeta/PayPal)

# Ruta de salida
RUTA_SALIDA = 'public/inventory.json'

# --- 2. CATÁLOGO MAESTRO (PRECIOS DE MERCADO STOCKX) ---
# Los precios en 'usd' son el promedio de REVENTA actual, no el precio de tienda.
CATALOGO_STOCKX = [
    # --- JORDAN 1 HIGH (Los Santos Griales) ---
    {"name": "Jordan 1 Retro High OG", "model": "Chicago Lost & Found", "cat": "Retro 1", "usd": 440, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Chicago-Reimagined-Lost-and-Found-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Dark Mocha", "cat": "Retro 1", "usd": 510, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Dark-Mocha-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Travis Scott Mocha", "cat": "Retro 1", "usd": 1800, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Travis-Scott-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "University Blue", "cat": "Retro 1", "usd": 380, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-White-University-Blue-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Shattered Backboard 3.0", "cat": "Retro 1", "usd": 450, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Shattered-Backboard-30-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Patent Bred", "cat": "Retro 1", "usd": 240, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Patent-Bred-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Shadow 2.0", "cat": "Retro 1", "usd": 290, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Shadow-20-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Taxi (Yellow Toe)", "cat": "Retro 1", "usd": 210, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Taxi-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Palomino", "cat": "Retro 1", "usd": 230, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Palomino-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "UNC Toe", "cat": "Retro 1", "usd": 250, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-UNC-Toe-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 1 LOW (Hype Puro) ---
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Reverse Mocha", "cat": "Retro 1", "usd": 1250, "img": "https://images.stockx.com/images/Air-Jordan-1-Low-Travis-Scott-Reverse-Mocha-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Olive", "cat": "Retro 1", "usd": 900, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-SP-Travis-Scott-Olive-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Black Phantom", "cat": "Retro 1", "usd": 800, "img": "https://images.stockx.com/images/Air-Jordan-1-Low-Travis-Scott-Black-Phantom-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Fragment", "cat": "Retro 1", "usd": 1600, "img": "https://images.stockx.com/images/Air-Jordan-1-Low-fragment-design-x-Travis-Scott-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Zion Voodoo", "cat": "Retro 1", "usd": 400, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Zion-Williamson-Voodoo-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Black Toe (2023)", "cat": "Retro 1", "usd": 160, "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Black-Toe-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 3 ---
    {"name": "Jordan 3 Retro", "model": "White Cement Reimagined", "cat": "Retro 3", "usd": 310, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-White-Cement-Reimagined-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Black Cement (2018)", "cat": "Retro 3", "usd": 420, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Black-Cement-2018-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "A Ma Maniére", "cat": "Retro 3", "usd": 550, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-A-Ma-Maniere-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "J Balvin Medellín Sunset", "cat": "Retro 3", "usd": 450, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-SP-J-Balvin-Medellin-Sunset-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Fire Red (2022)", "cat": "Retro 3", "usd": 240, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Fire-Red-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Midnight Navy", "cat": "Retro 3", "usd": 220, "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Midnight-Navy-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 4 (Los más calientes) ---
    {"name": "Jordan 4 Retro", "model": "Military Black", "cat": "Retro 4", "usd": 480, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Military-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Black Cat (2020)", "cat": "Retro 4", "usd": 950, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Black-Cat-2020-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "SB Pine Green", "cat": "Retro 4", "usd": 600, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-SB-Pine-Green-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Bred Reimagined", "cat": "Retro 4", "usd": 300, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Bred-Reimagined-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "White Oreo", "cat": "Retro 4", "usd": 450, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-White-Oreo-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "University Blue", "cat": "Retro 4", "usd": 420, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-University-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Thunder (2023)", "cat": "Retro 4", "usd": 280, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Thunder-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Red Cement", "cat": "Retro 4", "usd": 260, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Red-Cement-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Midnight Navy", "cat": "Retro 4", "usd": 340, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Midnight-Navy-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Military Blue (2024)", "cat": "Retro 4", "usd": 270, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Military-Blue-2024-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Off-White Sail", "cat": "Retro 4", "usd": 1600, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Off-White-Sail-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Union Guava Ice", "cat": "Retro 4", "usd": 850, "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Union-Guava-Ice-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 5 & 6 ---
    {"name": "Jordan 5 Retro", "model": "Off-White Muslin", "cat": "Retro 5", "usd": 950, "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Off-White-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "UNC", "cat": "Retro 5", "usd": 230, "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-UNC-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Raging Bull", "cat": "Retro 5", "usd": 220, "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Raging-Bull-Red-Suede-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Travis Scott British Khaki", "cat": "Retro 6", "usd": 420, "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Travis-Scott-British-Khaki-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Travis Scott Olive", "cat": "Retro 6", "usd": 550, "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Travis-Scott-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Infrared (2019)", "cat": "Retro 6", "usd": 320, "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Black-Infrared-2019-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Carmine (2021)", "cat": "Retro 6", "usd": 240, "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Carmine-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 11 ---
    {"name": "Jordan 11 Retro", "model": "Concord (2018)", "cat": "Retro 11", "usd": 480, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Concord-2018-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Space Jam (2016)", "cat": "Retro 11", "usd": 450, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Space-Jam-2016-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Bred (2019)", "cat": "Retro 11", "usd": 400, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Playoffs-2019-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Cool Grey (2021)", "cat": "Retro 11", "usd": 320, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Cool-Grey-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Cherry", "cat": "Retro 11", "usd": 260, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Cherry-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Gratitude", "cat": "Retro 11", "usd": 230, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-DMP-Gratitude-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro Low", "model": "Cement Grey", "cat": "Retro 11", "usd": 195, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-Cement-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro Low", "model": "Legend Blue", "cat": "Retro 11", "usd": 220, "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-Legend-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 12 & 13 ---
    {"name": "Jordan 12 Retro", "model": "Flu Game", "cat": "Otros Retro", "usd": 400, "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Flu-Game-2016-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 12 Retro", "model": "Playoffs", "cat": "Otros Retro", "usd": 250, "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Playoffs-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 12 Retro", "model": "Cherry (2023)", "cat": "Otros Retro", "usd": 230, "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Cherry-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Flint (2020)", "cat": "Otros Retro", "usd": 280, "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Flint-2020-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Chicago (2017)", "cat": "Otros Retro", "usd": 320, "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Chicago-2017-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Wheat", "cat": "Otros Retro", "usd": 180, "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Wheat-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
]

def calcular_precio_mxn(precio_usd, factor_demanda=1.0):
    # Fórmula: ((Costo USD * T.Cambio) + Envío + Impuestos) + Margen + Pasarela
    costo_producto = precio_usd * TIPO_CAMBIO * factor_demanda
    base_importacion = costo_producto + COSTO_ENVIO_MX
    costo_con_aduana = base_importacion * (1 + IMPUESTO_ADUANA)
    precio_publico = (costo_con_aduana + MARGEN_GANANCIA) * (1 + COMISION_PASARELA)
    return int(round(precio_publico / 50) * 50)

def generar_precios_talla(base_usd, es_gs=False):
    pricing = {}
    
    if es_gs:
        # Tallas Junior (Más baratas base)
        tallas = ["23 MX", "23.5 MX", "24 MX", "24.5 MX", "25 MX"]
        base_usd = base_usd * 0.75 # El GS suele valer 25% menos en retail, en resale varía pero es buena regla
    else:
        # Tallas Adulto (Men's)
        tallas = ["25 MX", "25.5 MX", "26 MX", "26.5 MX", "27 MX", "27.5 MX", "28 MX", "28.5 MX", "29 MX", "30 MX"]

    for talla in tallas:
        # 1. Simular disponibilidad (No siempre hay todas las tallas)
        if random.random() > 0.15: 
            # 2. Curva de Demanda StockX: Tallas 26-28 son más caras
            factor = 1.0
            val_talla = float(talla.split()[0])
            
            if 26.5 <= val_talla <= 28.5:
                factor = 1.12 # +12% sobre el precio base por demanda
            
            # 3. Fluctuación pequeña de mercado
            factor *= random.uniform(0.98, 1.02)
            
            pricing[talla] = calcular_precio_mxn(base_usd, factor)
            
    return pricing

def ejecutar_robot():
    print("🏭 INICIANDO ROBOT DE INVENTARIO WERA STOCK...")
    print(f"💰 Dólar Base: ${TIPO_CAMBIO}")
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_public = os.path.join(directorio_actual, 'public')
    archivo_final = os.path.join(carpeta_public, 'inventory.json')

    if not os.path.exists(carpeta_public):
        os.makedirs(carpeta_public)

    lista_productos = []
    id_gen = 1000

    for item in CATALOGO_STOCKX:
        # Generar Adulto
        precios_men = generar_precios_talla(item['usd'], es_gs=False)
        if precios_men:
            prod_men = {
                "id": id_gen,
                "name": item['name'],
                "model": item['model'],
                "brand": "Jordan",
                "category": item['cat'],
                "price": min(precios_men.values()), # Precio "Desde"
                "pricing": precios_men, # Matriz de precios
                "image": item['img'],
                "badge": "MEN'S"
            }
            if item['usd'] > 600: prod_men['badge'] = "GRAIL"
            lista_productos.append(prod_men)
            id_gen += 1

        # Generar GS (Junior) - Multiplica el inventario
        precios_gs = generar_precios_talla(item['usd'], es_gs=True)
        if precios_gs:
            prod_gs = {
                "id": id_gen,
                "name": item['name'].replace("Retro", "Retro GS"),
                "model": item['model'],
                "brand": "Jordan",
                "category": item['cat'],
                "price": min(precios_gs.values()),
                "pricing": precios_gs,
                "image": item['img'], # Usamos la misma foto (suelen ser iguales visualmente)
                "badge": "GS (JUNIOR)"
            }
            lista_productos.append(prod_gs)
            id_gen += 1

    random.shuffle(lista_productos)
    
    try:
        with open(archivo_final, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=2)
        print(f"✅ ÉXITO: {len(lista_productos)} modelos cargados con precios de reventa.")
        print(f"📍 Archivo: {archivo_final}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_robot()