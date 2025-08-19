import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Bersihkan layar (biar rapi)
def clear():
    os.system("clear" if os.name == "posix" else "cls")

# Ambil daftar file JSON
def list_config():
    return [f for f in os.listdir() if f.endswith(".json")]

# Tampilkan detail config
def tampilkan_config(path):
    with open(path, "r") as f:
        data = json.load(f)
    print("=== Detail Config ===")
    for k, v in data.items():
        print(f"{k}: {v}")
    return data

# Kirim email
def kirim_email(config):
    try:
        smtp_server = config["smtp_server"]
        smtp_port = config["smtp_port"]
        email_user = config["email_user"]
        email_pass = config["email_pass"]
        tujuan = config["to"]
        subjek = config["subject"]
        isi = config["body"]

        # Buat pesan
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = tujuan
        msg["Subject"] = subjek
        msg.attach(MIMEText(isi, "plain"))

        print("\n📤 Mengirim email...")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, tujuan, msg.as_string())

        print("✅ Email berhasil terkirim ke:", tujuan)

    except Exception as e:
        print("❌ Gagal kirim email:", e)

    input("\nTekan ENTER untuk kembali ke menu utama...")

# Menu utama
def menu():
    while True:
        clear()
        print("=== Menu Utama - Pilih Config JSON ===")
        configs = list_config()

        if not configs:
            print("⚠️ Tidak ada file config JSON ditemukan.")
            input("\nTambahkan file JSON lalu tekan ENTER...")
            continue

        for i, c in enumerate(configs, 1):
            print(f"{i}. {c}")

        print("0. Keluar")
        pilihan = input("\nPilih nomor config: ")

        if pilihan == "0":
            break
        if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(configs):
            input("❌ Pilihan tidak valid! Tekan ENTER...")
            continue

        # Ambil config terpilih
        file_config = configs[int(pilihan) - 1]
        clear()
        config = tampilkan_config(file_config)

        # Tanya apakah mau lanjut
        lanjut = input("\nApakah mau lanjut kirim email? (y/n): ").lower()
        if lanjut == "y":
            kirim_email(config)
        else:
            input("↩️ Tekan ENTER untuk kembali ke menu utama...")

if __name__ == "__main__":
    menu()
