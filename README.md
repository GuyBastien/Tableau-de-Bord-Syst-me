# 🖥️ Parrot OS — Web Dashboard

Dashboard sistem an tan reyèl pou Parrot OS. Bèl entèfas cyberpunk ki montre CPU, RAM, disk, rezo ak proses.

## ⚡ Lanse rapid

```bash
chmod +x start.sh
./start.sh
```

Ouvri browser ou sou **http://localhost:5000**

---

## 📊 Sa li montre

| Seksyon | Detay |
|---------|-------|
| **CPU** | % itilizasyon, frekans, nòm kœurs, chak kœur |
| **RAM** | % itilizasyon, espas itilize/total, SWAP |
| **Stockage** | Tout patiksyon, % plen |
| **Réseau** | Bytes voye/resevwa, entèfas ak IP |
| **Processus** | Top 10 proses pa CPU |
| **Système** | OS, kernel, arch, tanperati, uptime |

## ⚙️ Prérequis

```bash
pip3 install flask flask-cors psutil --break-system-packages
```

## 🔄 Rafraîchissement

Dashboard aktualize chak **2 secondes** otomatikman.

## ⚠️ Alertes automatiques

- CPU > 85% → alèt wouj
- RAM > 90% → alèt kritik
