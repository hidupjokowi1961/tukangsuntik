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
    print("=== Detail Vaksin ===\n")

    # 1. name, smtp_server, port → tanpa jarak
    for k in ["name", "smtp_server", "port"]:
        if k in config:
            print(f"{k}: {config[k]}")

    # 2. jarak antara port dan email_user
    print()  # 1 baris kosong

    # 3. email_user, email_pass, to → tanpa jarak
    for k in ["email_user", "email_pass", "to"]:
        if k in config:
            print(f"{k}: {config[k]}")

    # 4. jarak antara to dan subject
    print()  # 1 baris kosong

    # 5. subject dengan body → tanpa jarak
    for k in ["subject", "body"]:
        if k in config:
            print(f"{k}: {config[k]}")

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
        print("\nSemua email berhasil dikirim!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengirim email: {e}")

def halaman_detail(config):
    if not test_koneksi(config):
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    tampilkan_detail(config)

    while True:
        choice = input("\nLanjut menyuntik? (Y= Lanjut / N= Menu\n): ").strip()
        if choice == "y":
            try:
                count = int(input("\nCount (1-25): "))
                delay = float(input("Delay in seconds (5-20): "))
            except ValueError:
                print("⚠️ Input harus angka. Coba lagi.")
                time.sleep(1)
                continue

            kirim_email(config, count, delay)

            # Pilihan setelah pengiriman selesai
            
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

def main():
    while True:
        clear()
        print("=== Selamat Datang di Tukang Suntik ===\n")
        configs = load_configs()
        if not configs:
            print("⚠️ Tidak ada file config JSON ditemukan.\n")
            time.sleep(2)
            return

        for i, c in enumerate(configs, 1):
            print(f"{i}. {c.get('name', c['_filename'])}")

        print("0. Keluar")
        choice = input("\nPilih config (0 untuk keluar): ").strip()

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
