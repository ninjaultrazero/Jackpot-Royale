# 🎰 Jackpot Royale

Benvenuto in **Jackpot Royale**, un'applicazione di casinò virtuale sviluppata in Python con `customtkinter`. Il programma offre tre giochi: **Roulette, Slot Machine e Blackjack**, il tutto con un'interfaccia accattivante e animazioni fluide! 💰

---

## 🚀 Installazione
Per eseguire il programma, segui questi passi:

### 1⃣ Clona il repository
```bash
git clone https://github.com/tuo-repo/jackpot-royale.git
cd jackpot-royale
```

### 2⃣ Crea un ambiente virtuale (opzionale ma consigliato)
```bash
python -m venv venv
source venv/bin/activate  # Su macOS/Linux
venv\Scripts\activate  # Su Windows
```

### 3⃣ Installa le dipendenze richieste
```bash
pip install -r requirements.txt
```

### 4⃣ Avvia il programma
```bash
cd python\login_and_main
python login.py
```

---

## 🕹️ Giochi disponibili

### 🌁 Roulette
> Clicca sul pulsante **Roulette** per avviare il gioco della roulette. In questo gioco puoi piazzare scommesse sui numeri, sul rosso/nero, sul pari/dispari, o sui gruppi di numeri. La ruota gira e, al termine del giro, il numero vincente verrà annunciato!

**Dettagli del gioco:**
- **Ruota della Roulette**: Una ruota con numeri da 0 a 36. I numeri sono alternati tra **rosso** e **nero**, con il **0** in verde.
- **Puntate**: Puoi piazzare scommesse sui singoli numeri (esempio: 7), oppure su **colore** (rosso o nero), **pari/dispari**, e **bassi/ alti** (1-18 o 19-36).
- **Vincite**: Se indovini il numero, la vincita sarà di **35 volte la tua scommessa**. Le scommesse sui colori o su pari/dispari pagano **2 volte la puntata**.

### 🎰 Slot Machine
> Entra nel mondo delle slot con un semplice click sul pulsante **Slot Machine**.

### ♠️ Blackjack
> Metti alla prova la tua strategia con il **Blackjack**.

---

## 🎨 Funzionalità principali

✅ **Interfaccia Moderna**: Design elegante con `customtkinter`.<br>
✅ **Animazioni**: Monete che cadono per un effetto visivo coinvolgente.<br>
✅ **Gestione delle Monete**: Mostra il saldo disponibile in alto a destra.<br>
✅ **Facile Navigazione**: Pulsanti interattivi con immagini personalizzate.<br>
✅ **Effetti Sonori**: Suoni realistici per un'esperienza di gioco coinvolgente.<br>

---

## 🎰 Roulette - Dettagli

La **Roulette** offre una versione digitale interattiva e divertente del classico gioco da casinò:

- **Numeri**: La ruota è composta da numeri da 0 a 36, con numeri alternati tra **rosso** e **nero**. Lo **0** è verde.
- **Scommesse**:
  - **Numero singolo**: Scommetti su un singolo numero per vincere **35 volte la puntata**.
  - **Rosso/Nero**: Scommetti sul colore del numero estratto. Se indovini, vinci **2 volte la puntata**.
  - **Pari/Dispari**: Scommetti se il numero estratto sarà pari o dispari. Se indovini, vinci **2 volte la puntata**.
  - **Bassi/Alti**: Scommetti sui numeri da 1 a 18 (bassi) o da 19 a 36 (alti). La vincita è **2 volte la puntata**.
- **Animazione**: La ruota della roulette gira con una transizione fluida e realistico effetto visivo.
- **Suoni**: Effetti sonori aggiunti per migliorare l’esperienza del gioco.
- **Puntata iniziale**: Il saldo di partenza è **5000 FUN**.

**Come giocare:**
1. Clicca su un numero o una scommessa speciale (rosso, nero, pari, dispari, etc.).
2. Seleziona la puntata usando le fiches disponibili (1, 5, 10, 25, 50, 100 FUN).
3. Clicca sul pulsante **Gira** per avviare la ruota.
4. Dopo che la ruota si ferma, verrà mostrato il numero vincente.
5. Se hai vinto, il saldo verrà aggiornato con le tue vincite!

--- 

## 🛠️ Dipendenze
Il progetto utilizza:
- `customtkinter`
- `PIL` (Pillow)
- `os`, `random`, `subprocess`
- `pygame` per effetti sonori

Installa tutto con:
```bash
pip install customtkinter pillow pygame
```

## 📌 Note aggiuntive
- Assicurati di avere **Python 3.8+** installato.
- Se un'immagine non viene caricata, verifica il percorso nel codice.
- La cartella delle immagini deve contenere `casino_bg.png`, `roulette.png`, `slot.png` e `jack.png`.
- I file audio richiesti per la Slot Machine (`spin.mp3` e `win.mp3`) devono trovarsi nella cartella principale.

--- 

## 🤝 Contributi
Vuoi migliorare il progetto? Sentiti libero di:
1. **Forkare** il repository
2. Creare un **branch** con le tue modifiche
3. Inviare una **pull request** 🚀

--- 

## 🐝 Licenza
Questo progetto è distribuito sotto la licenza **MIT**.

Buon divertimento con **Jackpot Royale**! 🎲🎰💵

---
