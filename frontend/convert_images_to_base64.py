#!/usr/bin/env python3
"""
Script para convertir imágenes a Base64 y actualizar el HTML
"""
import base64
import re
from pathlib import Path

def image_to_base64(image_path):
    """Convierte una imagen a Base64"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def main():
    # Rutas
    frontend_dir = Path(__file__).parent
    images_dir = frontend_dir / 'imagenes'
    html_path = frontend_dir / 'presentacion_defensa.html'
    
    # Convertir imágenes a Base64
    print("📷 Convirtiendo imágenes a Base64...")
    fondo1_b64 = image_to_base64(images_dir / 'fondo1.png')
    logo_b64 = image_to_base64(images_dir / 'logo.png')
    grafica_b64 = image_to_base64(images_dir / 'grafica_corelaciones.jpg')
    
    print(f"✅ fondo1.png: {len(fondo1_b64)} caracteres")
    print(f"✅ logo.png: {len(logo_b64)} caracteres")
    print(f"✅ grafica_corelaciones.jpg: {len(grafica_b64)} caracteres")
    
    # Leer HTML
    print(f"\n📄 Leyendo {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Reemplazar rutas relativas por Base64
    print("\n🔄 Reemplazando rutas por imágenes Base64...")
    
    # 1. Reemplazar fondo1.png en #portada::before
    html_content = re.sub(
        r"background-image: url\('imagenes/fondo1\.png'\);",
        f"background-image: url('data:image/png;base64,{fondo1_b64}');",
        html_content
    )
    
    # 2. Reemplazar logo.png en section:not(#portada)::after
    html_content = re.sub(
        r"background-image: url\('imagenes/logo\.png'\);",
        f"background-image: url('data:image/png;base64,{logo_b64}');",
        html_content
    )
    
    # 3. Reemplazar grafica_corelaciones.jpg en img src
    html_content = re.sub(
        r'<img src="imagenes/grafica_corelaciones\.jpg"',
        f'<img src="data:image/jpeg;base64,{grafica_b64}"',
        html_content
    )
    
    # Guardar HTML actualizado
    print(f"\n💾 Guardando HTML actualizado...")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ ¡Listo! Imágenes incrustadas en {html_path}")
    print("📦 El HTML ahora es completamente autónomo y funcionará en Docker")

if __name__ == '__main__':
    main()
