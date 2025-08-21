import os
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------ Fungsi ------------------
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def load_config():
    file = "vaksin.json"
    if not os.path.exists(file):
        print("⚠️ File vaksin.json tidak ditemukan.")
        return None
    try:
        with open(file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Gagal membaca vaksin.json: {e}")
        return None

def tampilkan_detail(config):
    clear()
    print("=== Detail Vaksin ===\n")

    # Tentukan key yang ingin ditampilkan dan lebarnya
    sections = [
        (["name", "smtp_server", "port"], 12),
        (["email_user", "email_pass", "to"], 12),
        (["subject", "body"], 12)
    ]

    for keys, width in sections:
        for k in keys:
            if k in config:
                print(f"{k.ljust(width)}: {config[k]}")
        print()  # jarak antar section

def test_koneksi(config):
    print("\n🔌 Test koneksi SMTP...")
    try:
        server = smtplib.SMTP(config["smtp_server"], config["port"], timeout=10)
        server.starttls()
        server.login(config["email_user"], config["email_pass"])
        server.quit()
        print("✅ Koneksi SMTP berhasil!\n")
        return True
    except Exception as e:
        print(f"❌ Gagal koneksi SMTP: {e}\n")
        return False

def kirim_email(config, count, delay):
    try:
        server = smtplib.SMTP(config["smtp_server"], config["port"])
        server.starttls()
        server.login(config["email_user"], config["email_pass"])

        for i in range(1, count+1):
            msg = MIMEMultipart()
            msg["From"] = config["email_user"]
            msg["To"] = config["to"]
            msg["Subject"] = config["subject"]
            msg.attach(MIMEText(config["body"], "plain"))

            server.sendmail(config["email_user"], config["to"], msg.as_string())
            print(f"✅ ({i}/{count}) Email terkirim ke {config['to']}")
            time.sleep(delay)

        server.quit()
        print("\nSemua email berhasil dikirim!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengirim email: {e}")

# ------------------ Halaman Detail ------------------
def halaman_detail(config):
    if not test_koneksi(config):
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    tampilkan_detail(config)

    while True:
        choice = input("\nLanjut menyuntik? (Y= Lanjut / N= Menu): ").strip().lower()
        if choice == "y":
            try:
                count = int(input("\nCount (1-25): "))
                delay = float(input("Delay in seconds: "))
                countdown = int(input("Countdown in seconds: "))
                if countdown < 0:
                    countdown = 0
            except ValueError:
                print("⚠️ Input harus angka. Coba lagi.")
                time.sleep(1)
                continue

            # Animasi countdown
            for i in range(countdown, 0, -1):
                print(f"\r⏳ Mulai dalam {i} detik...", end="", flush=True)
                time.sleep(1)
            print("\n\n📨 Mulai pengiriman email...")

            kirim_email(config, count, delay)

            print("\n1. Kembali ke Halaman Utama")
            print("2. Gunakan config ini lagi")
            post_choice = input("Pilih (1/2): ").strip()
            if post_choice == "1":
                break
            elif post_choice == "2":
                tampilkan_detail(config)
                continue
            else:
                print("⚠️ Pilihan tidak valid, kembali ke menu utama.")
                break

        elif choice == "n":
            break
        else:
            print("⚠️ Pilihan tidak valid, coba lagi.")

# ------------------ Menu Utama ------------------
def main():
    while True:
        clear()
        print("=== Selamat Datang di Tukang Suntik ===\n")
        config = load_config()
        if not config:
            print("⚠️ Tidak ada config vaksin.json.\n")
            time.sleep(2)
            return

        print("1. Gunakan vaksin.json")
        print("0. Keluar")
        choice = input("\nPilih (0 untuk keluar): ").strip()

        if choice == "0":
            break
        elif choice == "1":
            halaman_detail(config)
        else:
            print("⚠️ Pilihan tidak valid.")
            time.sleep(1)

if __name__ == "__main__":
    main()
