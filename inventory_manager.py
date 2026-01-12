import json
import random
import os
import urllib.request
import time

# --- 1. CONFIGURACIÓN FINANCIERA (Regla de los $2,500) ---
AUMENTO_FIJO = 2500.00      # Cubre Logística, Aduana, Pasarela y Tu Ganancia.
TIPO_CAMBIO = 21.00         # Dólar Protección

# Rutas
RUTA_JSON = 'public/inventory.json'
RUTA_IMAGENES = 'public/images'

# --- 2. CATÁLOGO MAESTRO (100+ Modelos) ---
CATALOGO_JORDAN = [
    # JORDAN 4
    {"name": "Jordan 4 Retro", "model": "Bred Reimagined", "cat": "Retro 4", "usd": 220, "sku": "FV5029-006", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Bred-Reimagined-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Military Black", "cat": "Retro 4", "usd": 380, "sku": "DH6927-111", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Military-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "SB Pine Green", "cat": "Retro 4", "usd": 480, "sku": "DR5415-103", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-SB-Pine-Green-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Thunder (2023)", "cat": "Retro 4", "usd": 240, "sku": "DH6927-017", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Thunder-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Red Cement", "cat": "Retro 4", "usd": 210, "sku": "DH6927-161", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Red-Cement-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Midnight Navy", "cat": "Retro 4", "usd": 290, "sku": "DH6927-140", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Midnight-Navy-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Military Blue (2024)", "cat": "Retro 4", "usd": 220, "sku": "FV5029-141", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Military-Blue-2024-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Black Cat (2020)", "cat": "Retro 4", "usd": 850, "sku": "CU1110-010", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Black-Cat-2020-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "White Oreo", "cat": "Retro 4", "usd": 380, "sku": "CT8527-100", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-White-Oreo-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "University Blue", "cat": "Retro 4", "usd": 360, "sku": "CT8527-400", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-University-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Infrared", "cat": "Retro 4", "usd": 230, "sku": "DH6927-061", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Infrared-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Lightning", "cat": "Retro 4", "usd": 220, "sku": "CT8527-700", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Lightning-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Frozen Moments", "cat": "Retro 4", "usd": 280, "sku": "AQ9129-001", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Frozen-Moments-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Seafoam", "cat": "Retro 4", "usd": 260, "sku": "AQ9129-103", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Seafoam-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Canvas Black", "cat": "Retro 4", "usd": 290, "sku": "DH7138-006", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Black-Canvas-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Craft Photon Dust", "cat": "Retro 4", "usd": 240, "sku": "DV3742-021", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-SE-Craft-Photon-Dust-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Off-White Sail", "cat": "Retro 4", "usd": 1300, "sku": "CV9388-100", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Off-White-Sail-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Union Guava Ice", "cat": "Retro 4", "usd": 750, "sku": "DC9533-800", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Union-Guava-Ice-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Union Off Noir", "cat": "Retro 4", "usd": 650, "sku": "DC9533-001", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Union-Off-Noir-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Taupe Haze", "cat": "Retro 4", "usd": 350, "sku": "DB0732-200", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Taupe-Haze-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Tour Yellow", "cat": "Retro 4", "usd": 300, "sku": "CT8527-700", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Tour-Yellow-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Shimmer", "cat": "Retro 4", "usd": 320, "sku": "DJ0675-200", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Shimmer-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Canyon Purple", "cat": "Retro 4", "usd": 210, "sku": "AQ9129-500", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Canyon-Purple-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Cool Grey", "cat": "Retro 4", "usd": 350, "sku": "308497-007", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Cool-Grey-2019-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 4 Retro", "model": "Fire Red (2020)", "cat": "Retro 4", "usd": 300, "sku": "DC7770-160", "img": "https://images.stockx.com/images/Air-Jordan-4-Retro-Fire-Red-2020-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    
    # --- JORDAN 1 HIGH ---
    {"name": "Jordan 1 Retro High OG", "model": "Chicago Lost & Found", "cat": "Retro 1", "usd": 380, "sku": "DZ5485-612", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Chicago-Reimagined-Lost-and-Found-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Dark Mocha", "cat": "Retro 1", "usd": 420, "sku": "555088-105", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Dark-Mocha-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "University Blue", "cat": "Retro 1", "usd": 320, "sku": "555088-134", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-White-University-Blue-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Patent Bred", "cat": "Retro 1", "usd": 200, "sku": "555088-063", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Patent-Bred-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Taxi", "cat": "Retro 1", "usd": 180, "sku": "555088-711", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Taxi-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Shadow 2.0", "cat": "Retro 1", "usd": 260, "sku": "555088-035", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Shadow-20-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Royal Reimagined", "cat": "Retro 1", "usd": 140, "sku": "DZ5485-042", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Royal-Reimagined-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Palomino", "cat": "Retro 1", "usd": 210, "sku": "DZ5485-020", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Palomino-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "UNC Toe", "cat": "Retro 1", "usd": 220, "sku": "DZ5485-400", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-UNC-Toe-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Lucky Green", "cat": "Retro 1", "usd": 160, "sku": "DZ5485-031", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Lucky-Green-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Green Glow", "cat": "Retro 1", "usd": 150, "sku": "DZ5485-130", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Green-Glow-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Satin Bred", "cat": "Retro 1", "usd": 140, "sku": "FD4810-061", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Satin-Bred-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "White Cement", "cat": "Retro 1", "usd": 170, "sku": "DZ5485-052", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-White-Cement-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Washed Black", "cat": "Retro 1", "usd": 190, "sku": "DZ5485-051", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Washed-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Spider-Man", "cat": "Retro 1", "usd": 200, "sku": "DV1748-601", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Spider-Man-Across-the-Spider-Verse-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Heritage", "cat": "Retro 1", "usd": 130, "sku": "555088-161", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Heritage-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Brotherhood", "cat": "Retro 1", "usd": 140, "sku": "555088-706", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Brotherhood-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Bordeaux", "cat": "Retro 1", "usd": 180, "sku": "555088-611", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Bordeaux-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Pollen", "cat": "Retro 1", "usd": 170, "sku": "555088-701", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Pollen-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Electro Orange", "cat": "Retro 1", "usd": 160, "sku": "555088-180", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Electro-Orange-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Light Smoke Grey", "cat": "Retro 1", "usd": 250, "sku": "555088-126", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Light-Smoke-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Volt Gold", "cat": "Retro 1", "usd": 160, "sku": "555088-118", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Volt-Gold-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Bio Hack", "cat": "Retro 1", "usd": 260, "sku": "555088-201", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Bio-Hack-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "J Balvin", "cat": "Retro 1", "usd": 350, "sku": "DC3481-900", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-J-Balvin-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro High OG", "model": "Court Purple", "cat": "Retro 1", "usd": 300, "sku": "555088-500", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-High-Court-Purple-White-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    
    # --- JORDAN 1 LOW ---
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Reverse Mocha", "cat": "Retro 1", "usd": 1050, "sku": "DM7866-162", "img": "https://images.stockx.com/images/Air-Jordan-1-Low-Travis-Scott-Reverse-Mocha-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Olive", "cat": "Retro 1", "usd": 800, "sku": "DZ4137-106", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-SP-Travis-Scott-Olive-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Black Phantom", "cat": "Retro 1", "usd": 700, "sku": "DM7866-001", "img": "https://images.stockx.com/images/Air-Jordan-1-Low-Travis-Scott-Black-Phantom-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Travis Scott Fragment", "cat": "Retro 1", "usd": 1400, "sku": "DM7866-140", "img": "https://images.stockx.com/images/Air-Jordan-1-Low-fragment-design-x-Travis-Scott-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Black Toe", "cat": "Retro 1", "usd": 140, "sku": "CZ0790-106", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Black-Toe-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Starfish", "cat": "Retro 1", "usd": 180, "sku": "CZ0790-801", "img": "https://images.stockx.com/images/Air-Jordan-1-Low-Starfish-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Zion Voodoo", "cat": "Retro 1", "usd": 320, "sku": "DZ7292-200", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Zion-Williamson-Voodoo-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Neutral Grey", "cat": "Retro 1", "usd": 260, "sku": "CZ0790-100", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Neutral-Grey-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Atmosphere Grey", "cat": "Retro 1", "usd": 130, "sku": "CZ0790-101", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Atmosphere-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Year of the Dragon", "cat": "Retro 1", "usd": 380, "sku": "FN3727-100", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Year-of-the-Dragon-2024-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Powder Blue", "cat": "Retro 1", "usd": 170, "sku": "CZ0790-104", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Powder-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Mystic Navy", "cat": "Retro 1", "usd": 140, "sku": "CZ0790-041", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Mystic-Navy-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Bleached Coral", "cat": "Retro 1", "usd": 160, "sku": "CZ0790-061", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Bleached-Coral-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Shadow", "cat": "Retro 1", "usd": 140, "sku": "CZ0790-003", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Shadow-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 1 Retro Low OG", "model": "Trophy Room", "cat": "Retro 1", "usd": 500, "sku": "FN0432-063", "img": "https://images.stockx.com/images/Air-Jordan-1-Retro-Low-OG-Trophy-Room-Away-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 3 ---
    {"name": "Jordan 3 Retro", "model": "White Cement Reimagined", "cat": "Retro 3", "usd": 270, "sku": "DN3707-100", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-White-Cement-Reimagined-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Black Cement (2018)", "cat": "Retro 3", "usd": 360, "sku": "854262-001", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Black-Cement-2018-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "J Balvin Medellín", "cat": "Retro 3", "usd": 400, "sku": "FN0344-901", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-SP-J-Balvin-Medellin-Sunset-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Midnight Navy", "cat": "Retro 3", "usd": 190, "sku": "CT8532-140", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Midnight-Navy-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Fire Red", "cat": "Retro 3", "usd": 220, "sku": "DN3707-160", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Fire-Red-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Fear Pack", "cat": "Retro 3", "usd": 210, "sku": "CT8532-080", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Fear-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "A Ma Maniére", "cat": "Retro 3", "usd": 480, "sku": "DH3434-110", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-A-Ma-Maniere-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Wizards", "cat": "Retro 3", "usd": 200, "sku": "CT8532-148", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Washington-Wizards-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Craft Ivory", "cat": "Retro 3", "usd": 220, "sku": "FJ9479-100", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Craft-Ivory-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Desert Elephant", "cat": "Retro 3", "usd": 190, "sku": "CT8532-008", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Desert-Elephant-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Cardinal Red", "cat": "Retro 3", "usd": 230, "sku": "CT8532-126", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Cardinal-Red-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Pine Green", "cat": "Retro 3", "usd": 250, "sku": "CT8532-030", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Pine-Green-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Racer Blue", "cat": "Retro 3", "usd": 240, "sku": "CT8532-145", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Racer-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Patchwork", "cat": "Retro 3", "usd": 170, "sku": "DO1830-200", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Patchwork-Camo-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 3 Retro", "model": "Palomino", "cat": "Retro 3", "usd": 210, "sku": "CT8532-102", "img": "https://images.stockx.com/images/Air-Jordan-3-Retro-Palomino-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # --- JORDAN 5, 6, 11, 12, 13 ---
    {"name": "Jordan 5 Retro", "model": "UNC", "cat": "Retro 5", "usd": 220, "sku": "DV4982-400", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-UNC-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"}, 
    {"name": "Jordan 5 Retro", "model": "Off-White Muslin", "cat": "Retro 5", "usd": 950, "sku": "CT8480-001", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Off-White-Black-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Raging Bull", "cat": "Retro 5", "usd": 200, "sku": "DD0587-600", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Raging-Bull-Red-Suede-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Green Bean", "cat": "Retro 5", "usd": 170, "sku": "DM9014-003", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Green-Bean-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Concord", "cat": "Retro 5", "usd": 190, "sku": "DD0587-141", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Concord-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Aqua", "cat": "Retro 5", "usd": 200, "sku": "DD0587-047", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Aqua-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Shattered Backboard", "cat": "Retro 5", "usd": 220, "sku": "DC1060-100", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Shattered-Backboard-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 5 Retro", "model": "Moonlight", "cat": "Retro 5", "usd": 230, "sku": "CT4838-011", "img": "https://images.stockx.com/images/Air-Jordan-5-Retro-Moonlight-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Travis Scott British Khaki", "cat": "Retro 6", "usd": 380, "sku": "DH0690-200", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Travis-Scott-British-Khaki-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Infrared", "cat": "Retro 6", "usd": 280, "sku": "384664-060", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Black-Infrared-2019-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Travis Scott Olive", "cat": "Retro 6", "usd": 480, "sku": "CN1084-200", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Travis-Scott-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Carmine", "cat": "Retro 6", "usd": 220, "sku": "CT8529-106", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Carmine-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Midnight Navy", "cat": "Retro 6", "usd": 190, "sku": "CT8529-141", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Midnight-Navy-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Cool Grey", "cat": "Retro 6", "usd": 200, "sku": "CT8529-100", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Cool-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "UNC Home", "cat": "Retro 6", "usd": 220, "sku": "CT8529-410", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-UNC-Home-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Georgetown", "cat": "Retro 6", "usd": 210, "sku": "CT8529-012", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Georgetown-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 6 Retro", "model": "Toro Bravo", "cat": "Retro 6", "usd": 240, "sku": "CT8529-600", "img": "https://images.stockx.com/images/Air-Jordan-6-Retro-Toro-Bravo-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # JORDAN 11
    {"name": "Jordan 11 Retro", "model": "Concord", "cat": "Retro 11", "usd": 450, "sku": "378037-100", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Concord-2018-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Space Jam", "cat": "Retro 11", "usd": 420, "sku": "378037-003", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Space-Jam-2016-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Bred", "cat": "Retro 11", "usd": 380, "sku": "378037-061", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Playoffs-2019-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"}, 
    {"name": "Jordan 11 Retro", "model": "Cool Grey", "cat": "Retro 11", "usd": 300, "sku": "CT8012-005", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Cool-Grey-2021-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Cherry", "cat": "Retro 11", "usd": 240, "sku": "CT8012-116", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Cherry-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Gratitude", "cat": "Retro 11", "usd": 210, "sku": "CT8012-170", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-DMP-Gratitude-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Jubilee", "cat": "Retro 11", "usd": 270, "sku": "CT8012-011", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Jubilee-25th-Anniversary-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro", "model": "Neapolitan", "cat": "Retro 11", "usd": 190, "sku": "AR0715-101", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Neapolitan-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro Low", "model": "Cement Grey", "cat": "Retro 11", "usd": 180, "sku": "AV2187-140", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-Cement-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"}, 
    {"name": "Jordan 11 Retro Low", "model": "Legend Blue", "cat": "Retro 11", "usd": 210, "sku": "AV2187-117", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-Legend-Blue-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro Low", "model": "72-10", "cat": "Retro 11", "usd": 220, "sku": "AV2187-001", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-72-10-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 11 Retro Low", "model": "Yellow Snakeskin", "cat": "Retro 11", "usd": 200, "sku": "AH7860-107", "img": "https://images.stockx.com/images/Air-Jordan-11-Retro-Low-Yellow-Snakeskin-W-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},

    # J12 - J13
    {"name": "Jordan 12 Retro", "model": "Flu Game", "cat": "Otros Retro", "usd": 320, "sku": "130690-002", "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Flu-Game-2016-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 12 Retro", "model": "Playoffs", "cat": "Otros Retro", "usd": 240, "sku": "CT8013-006", "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Playoffs-2022-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 12 Retro", "model": "Royalty", "cat": "Otros Retro", "usd": 250, "sku": "CT8013-170", "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Royalty-Taxi-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 12 Retro", "model": "Cherry", "cat": "Otros Retro", "usd": 220, "sku": "CT8013-116", "img": "https://images.stockx.com/images/Air-Jordan-12-Retro-Cherry-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Flint", "cat": "Otros Retro", "usd": 260, "sku": "414571-404", "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Flint-2020-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Chicago", "cat": "Otros Retro", "usd": 300, "sku": "414571-122", "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Chicago-2017-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Wheat", "cat": "Otros Retro", "usd": 190, "sku": "414571-171", "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Wheat-2023-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"},
    {"name": "Jordan 13 Retro", "model": "Wolf Grey", "cat": "Otros Retro", "usd": 200, "sku": "414571-160", "img": "https://images.stockx.com/images/Air-Jordan-13-Retro-Wolf-Grey-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"}
]

def obtener_imagen_stockx(slug):
    # La imagen ya está en el catálogo, pero esta función puede servir de fallback
    return slug

def descargar_imagen(url, nombre_archivo):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://stockx.com/'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(nombre_archivo, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        # Silenciosamente fallar, la web usará el link remoto
        return False

def calcular_precio_mxn(precio_usd, factor_demanda=1.0):
    # FÓRMULA SIMPLIFICADA: (USD * TIPO_CAMBIO) + $2,500
    costo_producto = precio_usd * TIPO_CAMBIO * factor_demanda
    precio_publico = costo_producto + AUMENTO_FIJO
    return int(round(precio_publico / 50) * 50)

def generar_precios_talla(base_usd, es_gs=False):
    pricing = {}
    
    if es_gs:
        # Tallas Junior (Más baratas base)
        tallas = ["23 MX", "23.5 MX", "24 MX", "24.5 MX", "25 MX"]
        base_usd_ajustado = base_usd * 0.75 
    else:
        # Tallas Adulto (Men's)
        tallas = ["25 MX", "25.5 MX", "26 MX", "26.5 MX", "27 MX", "27.5 MX", "28 MX", "28.5 MX", "29 MX", "30 MX"]
        base_usd_ajustado = base_usd

    for talla in tallas:
        # 1. Simular disponibilidad (No siempre hay todas las tallas)
        if random.random() > 0.05: 
            # 2. Curva de Demanda StockX: Tallas 26-28 son más caras
            factor = 1.0
            val_talla = float(talla.split()[0])
            
            if 26.5 <= val_talla <= 28.5:
                factor = 1.12 # +12% sobre el precio base por demanda
            
            # 3. Fluctuación pequeña de mercado
            factor *= random.uniform(0.98, 1.02)
            
            pricing[talla] = calcular_precio_mxn(base_usd_ajustado, factor)
            
    return pricing

def buscar_imagen_local(sku, carpeta_imagenes):
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        nombre = f"{sku}{ext}"
        if os.path.exists(os.path.join(carpeta_imagenes, nombre)):
            return f"/images/{nombre}"
    return None

def ejecutar_robot():
    print("🏭 INICIANDO ROBOT DE INVENTARIO WERA STOCK...")
    print(f"💰 Dólar Base: ${TIPO_CAMBIO}")
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_public = os.path.join(directorio_actual, 'public')
    carpeta_imagenes = os.path.join(carpeta_public, 'images')
    archivo_final = os.path.join(carpeta_public, 'inventory.json')

    if not os.path.exists(carpeta_public):
        os.makedirs(carpeta_public)
        
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    lista_productos = []
    id_gen = 1000

    for item in CATALOGO_JORDAN:
        # 1. Prioridad: ¿Ya existe la foto en tu carpeta?
        url_final_web = buscar_imagen_local(item['sku'], carpeta_imagenes)
        
        # 2. Si no existe, intentar descargar de StockX
        if not url_final_web:
            # Usar la URL directa que definimos en el catálogo
            url_imagen = item['img']
            nombre_archivo = f"{item['sku']}.jpg"
            ruta_local = os.path.join(carpeta_imagenes, nombre_archivo)
            
            print(f"   Descargando: {item['model']}...")
            if descargar_imagen(url_imagen, ruta_local):
                url_final_web = f"/images/{nombre_archivo}"
            else:
                # 3. Si falla la descarga, usamos la URL remota directamente (no respaldo local)
                # Esto asegura que la imagen se vea aunque no se descargue
                url_final_web = url_imagen

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
                "image": url_final_web,
                "badge": "MEN'S"
            }
            if item['usd'] > 600: prod_men['badge'] = "GRAIL"
            lista_productos.append(prod_men)
            id_gen += 1

        # Generar GS (Junior)
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
                "image": url_final_web, # Misma foto
                "badge": "GS (JUNIOR)"
            }
            lista_productos.append(prod_gs)
            id_gen += 1

    random.shuffle(lista_productos)
    
    try:
        with open(archivo_final, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=2)
        print(f"✅ ÉXITO: {len(lista_productos)} modelos cargados con precios de reventa.")
        print(f"📍 Archivo guardado en: {archivo_final}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")

if __name__ == "__main__":
    ejecutar_robot()