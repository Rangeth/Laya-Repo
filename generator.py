import os
import zipfile
import hashlib

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                arcname = os.path.relpath(fp, os.path.dirname(folder_path))
                zipf.write(fp, arcname)

repo_dir = "C:\\Users\\Rangeth\\Laya-Repo"
zips_dir = os.path.join(repo_dir, "zips")

# Erstelle zips Verzeichnis falls nicht existent
os.makedirs(zips_dir, exist_ok=True)

# Addons verpacken
addons = ["repository.laya", "plugin.video.layatv"]

for addon in addons:
    addon_path = os.path.join(repo_dir, addon)
    # Beachte Groß-/Kleinschreibung falls Ordner anders heißt
    if not os.path.exists(addon_path) and addon == "plugin.video.layatv":
        addon_path = os.path.join(repo_dir, "plugin.video.Layatv")
        addon = "plugin.video.Layatv"
        
    if os.path.exists(addon_path):
        addon_zip_dir = os.path.join(zips_dir, addon.lower())
        os.makedirs(addon_zip_dir, exist_ok=True)
        zip_name = f"{addon.lower()}-1.0.0.zip"
        zip_folder(addon_path, os.path.join(addon_zip_dir, zip_name))
        print(f"Erfolgreich verpackt: {zip_name}")

print("Fertig! Alle ZIP-Dateien wurden im Ordner 'zips' erstellt.")
