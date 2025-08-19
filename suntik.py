import os
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def load_configs():
    files = [f for f in os.listdir() if f.endswith(".json")]
    configs = []
    for f in files:
        try:
            with open(f, "r") as file:
                data = json.load(file)
                data["_filename"] = f
                configs.append(data)
        except Exception as e:
            print(f"⚠️ Gagal membaca {f}: {e}")
    return configs

def tampilkan_detail(config):
    clear()
    print("=== Detail Config ===")
    for k, v in config.items():
        if k != "_filename":
            print(f"{k}: {v}")
    print("=====================\n")

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
        print("\n📨 Mulai pengiriman email...\n")

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
        print("\n🎉 Semua email berhasil dikirim!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengirim email: {e}")

def halaman_detail(config):
    if not test_koneksi(config):
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    while True:
        tampilkan_detail(config)
        try:
            count = int(input("Masukkan jumlah email (count): "))
            delay = float(input("Masukkan jeda antar email (detik): "))
        except ValueError:
            print("⚠️ Input harus angka. Coba lagi.")
            time.sleep(1)
            continue

        kirim_email(config, count, delay)

        print("\n=== Pilihan Setelah Pengiriman ===")
        print("1. Kembali ke Halaman Utama")
        print("2. Gunakan config ini lagi")
        print("3. Test koneksi SMTP ulang")
        choice = input("Pilih (1/2/3): ").strip()

        if choice == "1":
            break
        elif choice == "2":
            continue
        elif choice == "3":
            test_koneksi(config)
        else:
            print("⚠️ Pilihan tidak valid. Kembali ke detail config.")
            time.sleep(1)

def main():
    while True:
        clear()
        print("=== Menu Utama - Pilih Config JSON ===")
        configs = load_configs()
        if not configs:
            print("⚠️ Tidak ada file config JSON ditemukan.\n")
            time.sleep(2)
            return

        for i, c in enumerate(configs, 1):
            print(f"{i}. {c.get('name', c['_filename'])}")

        print("0. Keluar")
        choice = input("Pilih config (0 untuk keluar): ").strip()

        if choice == "0":
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(configs):
                halaman_detail(configs[idx])
            else:
                print("⚠️ Pilihan tidak valid.")
                time.sleep(1)
        except ValueError:
            print("⚠️ Input harus angka.")
            time.sleep(1)

if __name__ == "__main__":
    main()
