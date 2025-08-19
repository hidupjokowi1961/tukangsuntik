import smtplib
import time
import json
import os

def load_config(config_file):
    with open(config_file, "r") as f:
        return json.load(f)

def send_email(config):
    sender = config["sender_email"]
    password = config["app_password"]
    receiver = config["receiver_email"]
    subject = config["subject"]
    message = config["message"]
    count = config.get("count", 1)
    delay = config.get("delay", 1)

    email_message = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        for i in range(count):
            try:
                server.sendmail(sender, receiver, email_message)
                print(f"✅ Email {i+1}/{count} terkirim ke {receiver}")
            except Exception as e:
                print(f"❌ Email {i+1} gagal: {e}")

            if i < count - 1:
                time.sleep(delay)

        server.quit()
        print("\n📌 Selesai: Semua proses pengiriman email sudah dicoba.\n")

    except Exception as e:
        print(f"❌ Gagal menghubungkan ke server SMTP: {e}")

def main():
    while True:
        print("\n=== Menu Utama - Pilih Config JSON ===")
        # ✅ Perbaikan: semua file .json, gak harus diawali 'config'
        configs = [f for f in os.listdir() if f.lower().endswith(".json")]

        if not configs:
            print("⚠️ Tidak ada file config JSON ditemukan.")
            return

        for i, cfg in enumerate(configs, 1):
            print(f"{i}. {cfg}")
        print("0. Keluar")

        choice = input("Pilih nomor config: ")

        if choice == "0":
            print("👋 Keluar dari program.")
            break

        try:
            config_file = configs[int(choice) - 1]
        except (IndexError, ValueError):
            print("⚠️ Pilihan tidak valid.")
            continue

        config = load_config(config_file)

        # Preview isi config
        print("\n=== Detail Config Dipilih ===")
        print(f"📧 Pengirim : {config['sender_email']}")
        print(f"📩 Penerima : {config['receiver_email']}")
        print(f"📝 Subjek   : {config['subject']}")
        print(f"💬 Pesan    : {config['message']}")
        print(f"#️⃣ Jumlah  : {config.get('count', 1)}")
        print(f"⏱️ Delay    : {config.get('delay', 1)} detik")
        print("=============================")

        confirm = input("Apakah config sudah sesuai? (y/n): ").lower()
        if confirm == "y":
            send_email(config)
            back = input("Mau kembali ke menu utama? (y/n): ").lower()
            if back != "y":
                print("👋 Keluar dari program.")
                break
        else:
            print("↩️ Kembali ke menu utama...")

if __name__ == "__main__":
    main()
