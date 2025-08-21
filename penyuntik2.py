import smtplib
import os
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# Fungsi untuk memuat semua file JSON di folder kerja
def load_all_json():
    json_files = [f for f in os.listdir() if f.endswith(".json")]
    configs = []
    if not json_files:
        print("⚠️ Tidak ada file .json ditemukan di folder ini.")
        return configs
    for file in json_files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                configs.append(data)
        except Exception as e:
            print(f"⚠️ Gagal membaca {file}: {e}")
    return configs

# Fungsi untuk menampilkan detail konfigurasi
def tampilkan_detail(config):
    print("\n📄 Detail Konfigurasi:")
    print(f"  Nama Config   : {config.get('name', '-')}")
    print(f"  SMTP Server   : {config.get('smtp_server', '-')}")
    print(f"  Port          : {config.get('port', '-')}")
    print(f"  Email User    : {config.get('email_user', '-')}")
    print(f"  Sender Name   : {config.get('sender_name', '-')}")
    print(f"  To            : {config.get('to', '-')}")
    print(f"  Subject       : {config.get('subject', '-')}")
    print(f"  Body          : {config.get('body', '-')}\n")

# Fungsi kirim email
def kirim_email(config):
    try:
        msg = MIMEMultipart()
        sender_name = config.get("sender_name", None)

        # Pakai nama pengirim kalau ada
        if sender_name:
            msg['From'] = formataddr((sender_name, config["email_user"]))
        else:
            msg['From'] = config["email_user"]

        msg['To'] = config["to"]
        msg['Subject'] = config["subject"]

        # Body pesan
        msg.attach(MIMEText(config["body"], "plain"))

        # Kirim via SMTP
        server = smtplib.SMTP(config["smtp_server"], config["port"])
        server.starttls()
        server.login(config["email_user"], config["email_pass"])
        server.sendmail(config["email_user"], config["to"], msg.as_string())
        server.quit()
        print(f"✅ Email terkirim ke {config['to']}")
    except Exception as e:
        print(f"❌ Gagal mengirim email: {e}")

# Fungsi countdown sebelum mulai
def countdown_timer(detikan):
    print(f"Hitung mundur sebelum mulai (detik): {detikan}")
    for sisa in range(detikan, 0, -1):
        print(f"\r⏳ Mulai dalam {sisa} detik...", end="", flush=True)
        time.sleep(1)
    print("\n📨 Mulai pengiriman email!")

# MAIN PROGRAM
if __name__ == "__main__":
    configs = load_all_json()
    if not configs:
        print("⚠️ Tidak ada config JSON valid.")
        exit()

    # Pilih config yang ditemukan
    for config in configs:
        tampilkan_detail(config)

        # Countdown (bisa ubah manual di sini)
        countdown_timer(5)  # contoh 5 detik

        # Kirim email
        kirim_email(config)
