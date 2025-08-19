import os
import json
import time

# -----------------------------
# Fungsi utilitas
# -----------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_configs():
    files = [f for f in os.listdir() if f.endswith(".json")]
    return files

def tampilkan_config(file_config):
    with open(file_config, "r") as f:
        config = json.load(f)

    print(f"\n=== Detail Config: {file_config} ===")
    for k, v in config.items():
        print(f"{k}: {v}")
    return config

def kirim_email(config, count=1, delay=1):
    # Data dasar dari config
    server = config.get("smtp_server")
    port = config.get("smtp_port")
    user = config.get("email_user")
    password = config.get("email_pass")
    to_addr = config.get("to")
    subject = config.get("subject")
    body = config.get("body")

    # Simulasi kirim email
    for i in range(count):
        print(f"\n📨 ({i+1}/{count}) Mengirim email ke {to_addr}...")
        time.sleep(delay)
    print("\n✅ Semua email berhasil (simulasi)!")


# -----------------------------
# Main Program
# -----------------------------
while True:
    clear()
    print("=== Menu Utama - Pilih Config JSON ===")

    configs = load_configs()
    if not configs:
        print("⚠️ Tidak ada file config JSON ditemukan.")
        break

    for idx, f in enumerate(configs, start=1):
        print(f"{idx}. {f}")

    pilihan = input("\nPilih config (angka) atau 'q' untuk keluar: ").strip()
    if pilihan.lower() == "q":
        break

    if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(configs):
        input("⚠️ Pilihan tidak valid! Tekan ENTER untuk lanjut...")
        continue

    # Ambil config terpilih
    file_config = configs[int(pilihan) - 1]
    clear()
    config = tampilkan_config(file_config)

    # Input manual count & delay
    try:
        count = int(input("\nMasukkan jumlah email yang mau dikirim: "))
        delay = float(input("Masukkan jeda antar email (detik): "))
    except ValueError:
        input("⚠️ Input tidak valid! Tekan ENTER untuk kembali...")
        continue

    # Tanya aksi
    print("\nApa yang mau kamu lakukan?")
    print("1. Lanjut kirim email")
    print("2. Kembali ke menu utama")

    aksi = input("\nPilih (1/2): ").strip()
    if aksi == "1":
        kirim_email(config, count, delay)
        input("\n↩️ Tekan ENTER untuk kembali ke menu utama...")
    else:
        continue
