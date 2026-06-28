import sys
import re
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

# Basis-URLs festlegen
HANDLE = int(sys.argv[1])
BASE_URL = "https://tamildhool.tech"

def get_shows():
    """Ruft die Webseite auf und listet die verfügbaren Shows auf."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        html = response.text
        
        # Sucht nach Links zu den einzelnen Shows (z.B. Super Singer)
        # Regex sucht nach: <a href="LINK">TITEL</a> innerhalb der Show-Kategorie
        matches = re.findall(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', html)
        
        # Einzigartige Shows filtern, um Dopplungen zu vermeiden
        seen = set()
        for url, title in matches:
            if "vijay-tv" in url and title.strip() and url not in seen:
                seen.add(url)
                # Nur relevante Einträge anzeigen (z.B. keine Startseiten-Links)
                if len(title) > 3 and "Home" not in title:
                    add_directory_item(title.strip(), url, is_folder=True)
                    
    except Exception as e:
        xbmcgui.Dialog().notification('LayaTV Fehler', str(e), xbmcgui.NOTIFICATION_ERROR, 5000)

def add_directory_item(name, url, is_folder=True):
    """Hilfsfunktion, um Einträge in der Kodi-Liste anzuzeigen."""
    list_item = xbmcgui.ListItem(label=name)
    # Wenn es ein Ordner ist, wird beim Klicken die nächste Ebene geladen
    # Wenn nicht, wird es als Video abgespielt
    url_param = f"{sys.argv[0]}?url={urllib.parse.quote_plus(url)}&mode={'folder' if is_folder else 'play'}"
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url_param, listitem=list_item, isFolder=is_folder)

# Hauptlogik des Add-ons steuern
params = urllib.parse.parse_qs(sys.argv[2][1:])
url_arg = params.get('url', [None])[0]
mode_arg = params.get('mode', [None])[0]

if url_arg is None:
    # Hauptmenü: Zeige alle Vijay TV Shows an
    get_shows()
    xbmcplugin.endOfDirectory(HANDLE)
else:
    # Hier wird später die Logik für die einzelnen Folgen eingebaut
    xbmcgui.Dialog().ok("LayaTV", f"Öffne Show-Link:\n{url_arg}\n\n(Folgen-Auswahl wird im nächsten Schritt finalisiert)")
    xbmcplugin.endOfDirectory(HANDLE)
