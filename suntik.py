import os
import json
import time

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def load_configs():
    files = [f for f in os.listdir() if f.endswith(".json")]
    configs = []
    for f in files:
        try:
            with open(f, "r") as file:
                configs.append(json.load(file))
        except:
            pass
    return configs

def tampilkan_detail(config):
    clear()
    print("=== Detail Config ===")
    for k, v in config.items():
        print(f"{k}: {v}")
    print("=====================\n")

def test_koneksi(config):
    print("\n🔌 Menguji koneksi SMTP...")
    time.sleep(1.5)
    # simulasi sukses/gagal
    if str(config.get("port")) in ["587", "465"]:
        print("✅ Koneksi SMTP berhasil!\n")
        return True
    else:
        print("❌ Gagal koneksi ke SMTP server!\n")
        return False

def kirim_email(config, count, delay):
    print("\n📨 Simulasi pengiriman email...")
    for i in range(1, count+1):
        print(f"   Mengirim email ke-{i}...")
        time.sleep(delay)
    print("✅ Semua email sudah disimulasikan terkirim.\n")

def halaman_detail(config):
    # otomatis test koneksi dulu
    sukses = test_koneksi(config)
    if not sukses:
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    while True:
        tampilkan_detail(config)
        try:
            count = int(input("Masukkan jumlah email (count): "))
            delay = int(input("Masukkan jeda antar email (detik): "))
        except ValueError:
            print("⚠️ Input harus angka. Coba lagi.")
            time.sleep(1)
            continue

        kirim_email(config, count, delay)

        print("=== Setelah Selesai ===")
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
            print(f"{i}. {c.get('name', 'Config tanpa nama')}")

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
