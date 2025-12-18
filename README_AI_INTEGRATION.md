# Integrazione AI (YOLOv8) in kTAY8

Questa versione di kTAY8 è stata modificata per supportare il rilevamento ugelli tramite Intelligenza Artificiale (YOLOv8), mantenendo la compatibilità con il sistema originale.

## 🚀 Come Funziona
Il sistema cerca automaticamente un modello AI nella cartella `server/`.
1.  Se trova `best.tflite` (Consigliato per Orange Pi) o `best.onnx`, usa l'AI.
2.  Se non trova nulla o l'AI fallisce, usa il vecchio metodo "Blob Detector" (cerchi).

## 🛠️ Installazione su Orange Pi

1.  **Copia i file**:
    Copia tutto il contenuto di questa cartella sul tuo Orange Pi (sovrascrivendo l'installazione esistente di kTAY8 se presente).

2.  **Installa le dipendenze**:
    ```bash
    pip install -r requirements.txt
    # Se tflite-runtime da errore, prova:
    # pip install tflite-runtime --extra-index-url https://google-coral.github.io/py-repo/
    ```

3.  **Carica il Modello**:
    Dopo aver addestrato il modello col notebook, prendi il file `best.tflite` (o `.onnx`) e copialo nella cartella `server/` dell'Orange Pi.

4.  **Riavvia**:
    Riavvia il servizio kTAY8:
    ```bash
    sudo systemctl restart ktay8
    ```

## 🔍 Verifica
Controlla i log per vedere se il modello è stato caricato:
```bash
tail -f /home/pi/kTAY8/server/logs/ktay8_server.log
```
Dovresti vedere: `*** AI Model loaded successfully.`
