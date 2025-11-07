import json
import os

data_file = "data_transport.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

def tampilkan_data(data):
    if not data:
        print("Belum ada data.")
        return
    print("\nDaftar Rute:")
    for i, d in enumerate(data, start=1):
        print(f"{i}. {d['asal']} -> {d['tujuan']} | {d['transport']} | Rp{d['biaya']}")

def tambah_data(data):
    asal = input("Asal: ")
    tujuan = input("Tujuan: ")
    transport = input("Transportasi (angkot/motor/ojek): ")
    biaya = int(input("Biaya: "))
    data.append({"asal": asal, "tujuan": tujuan, "transport": transport, "biaya": biaya})
    save_data(data)
    print("Data berhasil ditambahkan!\n")

def hapus_data(data):
    tampilkan_data(data)
    if not data:
        return
    idx = int(input("Nomor data yang ingin dihapus: ")) - 1
    if 0 <= idx < len(data):
        data.pop(idx)
        save_data(data)
        print("Data berhasil dihapus!\n")
    else:
        print("Nomor tidak valid!\n")

def ubah_data(data):
    tampilkan_data(data)
    if not data:
        return
    idx = int(input("Nomor data yang ingin diubah: ")) - 1
    if 0 <= idx < len(data):
        d = data[idx]
        d["asal"] = input(f"Asal ({d['asal']}): ") or d["asal"]
        d["tujuan"] = input(f"Tujuan ({d['tujuan']}): ") or d["tujuan"]
        d["transport"] = input(f"Transport ({d['transport']}): ") or d["transport"]
        biaya = input(f"Biaya ({d['biaya']}): ")
        if biaya:
            d["biaya"] = int(biaya)
        save_data(data)
        print("Data berhasil diubah!\n")
    else:
        print("Nomor tidak valid!\n")

def cari_data(data):
    key = input("Cari berdasarkan asal/tujuan/transport: ").lower()
    hasil = [d for d in data if key in d["asal"].lower() or key in d["tujuan"].lower() or key in d["transport"].lower()]
    tampilkan_data(hasil)

def urutkan_data(data):
    print("1. Berdasarkan Asal (A-Z)")
    print("2. Berdasarkan Biaya (termurah)")
    pilih = input("Pilih (1/2): ")
    if pilih == "1":
        data.sort(key=lambda x: x["asal"].lower())
    elif pilih == "2":
        data.sort(key=lambda x: x["biaya"])
    else:
        print("Pilihan tidak valid.")
        return
    save_data(data)
    tampilkan_data(data)

def estimasi_biaya(data):
    tampilkan_data(data)
    if not data:
        return
    idx = int(input("Pilih nomor rute untuk estimasi: ")) - 1
    if 0 <= idx < len(data):
        r = data[idx]
        total = r["biaya"] * 2
        print(f"Biaya pulang-pergi {r['asal']} <-> {r['tujuan']} : Rp{total}\n")
    else:
        print("Nomor tidak valid!\n")

def main():
    data = load_data()
    while True:
        print("\n=== Estimator Transportasi Mahasiswa SV IPB ===")
        print("1. Tampilkan Data")
        print("2. Tambah Data")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Cari Data")
        print("6. Urutkan Data")
        print("7. Estimasi Biaya Pulang Pergi")
        print("8. Keluar")

        pilih = input("Pilih menu (1-8): ")
        if pilih == "1":
            tampilkan_data(data)
        elif pilih == "2":
            tambah_data(data)
        elif pilih == "3":
            ubah_data(data)
        elif pilih == "4":
            hapus_data(data)
        elif pilih == "5":
            cari_data(data)
        elif pilih == "6":
            urutkan_data(data)
        elif pilih == "7":
            estimasi_biaya(data)
        elif pilih == "8":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()
