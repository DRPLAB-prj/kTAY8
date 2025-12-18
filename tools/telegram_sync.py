import requests
import os
import time
import json

# --- CONFIGURAZIONE ---
# Configurazione Bot Telegram
# Inserire il token fornito da BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# ID Utente Telegram autorizzato (solo i messaggi da questo ID verranno processati)
# Puoi ottenerlo scrivendo a @userinfobot su Telegram
TRUSTED_USER_ID = 000000000 
# Cartella dove salvare le immagini RAW (percorso assoluto o relativo corretto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR, "data", "raw")
# ----------------------

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def download_photo(file_id, save_path):
    # 1. Get File Path
    url_info = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    resp = requests.get(url_info).json()
    
    if not resp.get('ok'):
        print(f"Errore info file: {resp}")
        return False
        
    file_path = resp['result']['file_path']
    
    # 2. Download Content
    url_content = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    img_data = requests.get(url_content).content
    
    with open(save_path, 'wb') as f:
        f.write(img_data)
    return True

def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERRORE: Configurazione mancante. Inserire il BOT_TOKEN nello script.")
        return
        
    if TRUSTED_USER_ID == 000000000:
        print("⚠️  ATTENZIONE: TRUSTED_USER_ID non impostato. Lo script accetterà immagini da CHIUNQUE.")
        print("   Per sicurezza, imposta il tuo ID Telegram in tools/telegram_sync.py")
        time.sleep(3)

    os.makedirs(SAVE_DIR, exist_ok=True)
    print(f"📡 In ascolto su Telegram... Salvataggio in: {SAVE_DIR}")
    
    offset = None
    
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get("ok"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" not in update:
                        continue
                        
                    message = update["message"]
                    sender_id = message.get("from", {}).get("id")
                    
                    # Filtro Sicurezza: Controlla chi manda il messaggio
                    if TRUSTED_USER_ID != 000000000 and sender_id != TRUSTED_USER_ID:
                        print(f"⛔ Messaggio ignorato da utente non autorizzato: {sender_id}")
                        continue
                    
                    # Controlla se c'è una foto
                    if "photo" in message:
                        # Telegram manda diverse risoluzioni, l'ultima è la più alta
                        photo = update["message"]["photo"][-1]
                        file_id = photo["file_id"]
                        
                        timestamp = int(time.time())
                        filename = f"telegram_{timestamp}_{file_id[:5]}.jpg"
                        save_path = os.path.join(SAVE_DIR, filename)
                        
                        print(f"📥 Scaricamento foto: {filename}...")
                        if download_photo(file_id, save_path):
                            print("   ✅ Salvato.")
                        else:
                            print("   ❌ Errore download.")
                            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🛑 Stop.")
            break
        except Exception as e:
            print(f"⚠️ Errore: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
