import os
import re
import urllib.request
import urllib.error

STATIC_DIR = r"c:\xampp\htdocs\python_django_project\myproject\static"
VENDOR_DIR = os.path.join(STATIC_DIR, "vendor")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

os.makedirs(VENDOR_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_file(url, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if os.path.exists(destination) and os.path.getsize(destination) > 0:
        print(f"[EXISTS] {destination}")
        return True
    print(f"[DOWNLOADING] {url} -> {destination}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response, open(destination, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[SUCCESS] Saved {destination} ({os.path.getsize(destination)} bytes)")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to download {url}: {e}")
        return False

# 1. Download Vendor Assets
vendor_files = {
    # Bootstrap CSS & JS
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css":
        os.path.join(VENDOR_DIR, "bootstrap", "css", "bootstrap.min.css"),
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js":
        os.path.join(VENDOR_DIR, "bootstrap", "js", "bootstrap.bundle.min.js"),
    
    # Bootstrap Icons CSS & Font files
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css":
        os.path.join(VENDOR_DIR, "bootstrap-icons", "bootstrap-icons.min.css"),
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2":
        os.path.join(VENDOR_DIR, "bootstrap-icons", "fonts", "bootstrap-icons.woff2"),
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff":
        os.path.join(VENDOR_DIR, "bootstrap-icons", "fonts", "bootstrap-icons.woff"),

    # AOS
    "https://unpkg.com/aos@2.3.4/dist/aos.css":
        os.path.join(VENDOR_DIR, "aos", "aos.css"),
    "https://unpkg.com/aos@2.3.4/dist/aos.js":
        os.path.join(VENDOR_DIR, "aos", "aos.js"),

    # Leaflet
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css":
        os.path.join(VENDOR_DIR, "leaflet", "leaflet.css"),
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js":
        os.path.join(VENDOR_DIR, "leaflet", "leaflet.js"),
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png":
        os.path.join(VENDOR_DIR, "leaflet", "images", "marker-icon.png"),
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png":
        os.path.join(VENDOR_DIR, "leaflet", "images", "marker-icon-2x.png"),
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png":
        os.path.join(VENDOR_DIR, "leaflet", "images", "marker-shadow.png"),
    "https://unpkg.com/leaflet@1.9.4/dist/images/layers.png":
        os.path.join(VENDOR_DIR, "leaflet", "images", "layers.png"),
    "https://unpkg.com/leaflet@1.9.4/dist/images/layers-2x.png":
        os.path.join(VENDOR_DIR, "leaflet", "images", "layers-2x.png"),
}

for url, dest in vendor_files.items():
    download_file(url, dest)

# 2. Download Google Fonts Inter
inter_css_url = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
try:
    print("[DOWNLOADING] Google Font Inter stylesheet...")
    req = urllib.request.Request(inter_css_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        css_text = resp.read().decode('utf-8')
    
    inter_dir = os.path.join(VENDOR_DIR, "inter")
    fonts_dir = os.path.join(inter_dir, "fonts")
    os.makedirs(fonts_dir, exist_ok=True)

    font_url_matches = re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', css_text)
    print(f"Found {len(font_url_matches)} font files for Inter")
    for idx, f_url in enumerate(font_url_matches):
        filename = f"inter_{idx}_{os.path.basename(f_url.split('?')[0])}"
        f_dest = os.path.join(fonts_dir, filename)
        if download_file(f_url, f_dest):
            css_text = css_text.replace(f_url, f"fonts/{filename}")

    inter_css_dest = os.path.join(inter_dir, "inter.css")
    with open(inter_css_dest, 'w', encoding='utf-8') as fp:
        fp.write(css_text)
    print(f"[SUCCESS] Inter font localized to {inter_css_dest}")
except Exception as e:
    print(f"[ERROR] Failed to localize Google Fonts Inter: {e}")

# 3. Download All Unsplash Images
unsplash_images = {
    # Hero / Auth
    "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1920&q=80": "hero-bg.jpg",
    "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80": "auth-bg.jpg",
    
    # Food categories / listings
    "https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=900&q=80": "food-sourdough.jpg",
    "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=900&q=80": "food-fruits.jpg",
    "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=900&q=80": "food-meals.jpg",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80": "food-produce.jpg",
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80": "food-bakery.jpg",
    "https://images.unsplash.com/photo-1595854341625-f33ee10dbf94?auto=format&fit=crop&w=900&q=80": "food-dairy.jpg",
    
    # Impact section
    "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?auto=format&fit=crop&w=900&q=80": "impact-distribution.jpg",
    "https://images.unsplash.com/photo-1488459716781-31db52582fe9?auto=format&fit=crop&w=900&q=80": "impact-community.jpg",
    "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=900&q=80": "impact-environment.jpg",
    
    # Community & Story Gallery
    "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=900&q=80": "gallery-1.jpg",
    "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=900&q=80": "gallery-2.jpg",
    "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?auto=format&fit=crop&w=900&q=80": "gallery-3.jpg",
    "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?auto=format&fit=crop&w=900&q=80": "gallery-4.jpg",
    "https://images.unsplash.com/photo-1498579397066-22750a3cb424?auto=format&fit=crop&w=900&q=80": "gallery-5.jpg",
    "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?auto=format&fit=crop&w=900&q=80": "gallery-6.jpg",
    "https://images.unsplash.com/photo-1607349913338-fca6f742960f?auto=format&fit=crop&w=900&q=80": "gallery-7.jpg",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=80": "gallery-8.jpg",
    
    # Avatars (track.html)
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80": "avatar-1.jpg",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80": "avatar-2.jpg",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80": "avatar-3.jpg",
}

for url, filename in unsplash_images.items():
    dest = os.path.join(IMAGES_DIR, filename)
    download_file(url, dest)

print("\n--- ALL ASSETS DOWNLOADED SUCCESSFULLY ---")
