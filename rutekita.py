import json
import os

DATA_FILE = "data_transport.json"
REQUEST_FILE = "request_tujuan.json"
ADMIN_NAME = "admin"

def load_data():
    """Membaca data dari file JSON"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Jika file tidak ada atau rusak, buat data default
        default_data = [
            {
                "kota": "Laladon",
                "transportasi": [
                    {"nama": "Angkot", "biaya": 4000, "jarak_km": 3.2, "waktu_menit": 10},
                    {"nama": "Gojek", "biaya": 9000, "jarak_km": 3.2, "waktu_menit": 8}
                ]
            }
        ]
        save_data(default_data)
        return default_data

def save_data(data):
    """Menyimpan data ke file JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_requests():
    """Membaca data request dari file JSON"""
    try:
        with open(REQUEST_FILE, "r", encoding="utf-8") as f:
            requests = json.load(f)
        return requests
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_requests(requests):
    """Menyimpan data request ke file JSON"""
    with open(REQUEST_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)

def find_city(data, nama_kota):
    """Mencari kota dalam data"""
    for kota in data:
        if kota["kota"].lower() == nama_kota.lower():
            return kota
    return None

# ========================
# Menu User
# ========================
def menu_tujuan(data):
    """Menu 1: Lihat tujuan dan transportasi"""
    print("\n" + "="*50)
    print("DAFTAR TUJUAN DAN TRANSPORTASI")
    print("="*50)
    
    if not data:
        print("❌ Belum ada data tujuan")
        return
    
    for i, kota in enumerate(data, 1):
        print(f"\n{i}. 🏙️  {kota['kota']}")
        for j, transport in enumerate(kota["transportasi"], 1):
            print(f"   {j}. {transport['nama']} - Rp{transport['biaya']:,} - {transport['jarak_km']} km - {transport['waktu_menit']} menit")
    
    # Pilih untuk estimasi biaya
    try:
        pilihan = input("\nPilih nomor tujuan untuk estimasi biaya (atau 0 untuk kembali): ").strip()
        if pilihan == "0":
            return
        
        idx_kota = int(pilihan) - 1
        if 0 <= idx_kota < len(data):
            kota = data[idx_kota]
            print(f"\nPilih transportasi di {kota['kota']}:")
            for j, transport in enumerate(kota["transportasi"], 1):
                print(f"   {j}. {transport['nama']} - Rp{transport['biaya']:,}")
            
            pilihan_transport = input("Pilih nomor transportasi: ").strip()
            idx_transport = int(pilihan_transport) - 1
            
            if 0 <= idx_transport < len(kota["transportasi"]):
                transport = kota["transportasi"][idx_transport]
                print("\n" + "="*40)
                print("ESTIMASI BIAYA")
                print("="*40)
                sekali = transport["biaya"]
                pp = sekali * 2
                minggu = pp * 5
                bulan = minggu * 4
                print(f"Transportasi          : {transport['nama']}")
                print(f"Biaya sekali jalan   : Rp{sekali:,}")
                print(f"Pulang-pergi         : Rp{pp:,}")
                print(f"Per minggu (5 hari)  : Rp{minggu:,}")
                print(f"Per bulan (4 minggu) : Rp{bulan:,}")
                print("="*40)
            else:
                print("❌ Pilihan transportasi tidak valid")
        else:
            print("❌ Pilihan tujuan tidak valid")
    except ValueError:
        print("❌ Masukkan angka yang valid")

def menu_request_tujuan():
    """Menu 2: Request tujuan baru"""
    print("\n" + "="*40)
    print("REQUEST TUJUAN BARU")
    print("="*40)
    
    tujuan_baru = input("Masukkan nama tujuan yang ingin ditambahkan: ").strip()
    
    if not tujuan_baru:
        print("❌ Nama tujuan tidak boleh kosong!")
        return
    
    # Simpan request ke file
    requests = load_requests()
    
    # Cek apakah request sudah ada
    for req in requests:
        if req["tujuan"].lower() == tujuan_baru.lower():
            print(f"❌ Request untuk tujuan '{tujuan_baru}' sudah ada!")
            return
    
    requests.append({"tujuan": tujuan_baru, "status": "pending"})
    save_requests(requests)
    
    print(f"✅ Request tujuan '{tujuan_baru}' berhasil dikirim!")

def menu_rekap_pengeluaran(data):
    """Menu 3: Rekap pengeluaran mingguan dan bulanan"""
    print("\n" + "="*50)
    print("REKAP PENGELUARAN MINGGUAN & BULANAN")
    print("="*50)
    
    if not data:
        print("❌ Belum ada data tujuan")
        return
    
    # Pilih tujuan
    print("\nPilih tujuan:")
    for i, kota in enumerate(data, 1):
        print(f"{i}. {kota['kota']}")
    
    try:
        pilihan_kota = int(input("Pilih nomor tujuan: ")) - 1
        if not (0 <= pilihan_kota < len(data)):
            print("❌ Pilihan tidak valid")
            return
        
        kota = data[pilihan_kota]
        
        # Pilih transportasi
        print(f"\nPilih transportasi di {kota['kota']}:")
        for i, transport in enumerate(kota["transportasi"], 1):
            print(f"{i}. {transport['nama']} - Rp{transport['biaya']:,}")
        
        pilihan_transport = int(input("Pilih nomor transportasi: ")) - 1
        if not (0 <= pilihan_transport < len(kota["transportasi"])):
            print("❌ Pilihan tidak valid")
            return
        
        transport = kota["transportasi"][pilihan_transport]
        
        # Input frekuensi
        try:
            hari_per_minggu = int(input("Berapa hari per minggu? (1-7): "))
            if not (1 <= hari_per_minggu <= 7):
                print("❌ Masukkan angka 1-7")
                return
        except ValueError:
            print("❌ Masukkan angka yang valid")
            return
        
        # Hitung rekap
        print("\n" + "="*50)
        print("REKAP PENGELUARAN")
        print("="*50)
        
        sekali = transport["biaya"]
        pp = sekali * 2
        per_hari = pp * hari_per_minggu
        per_minggu = per_hari
        per_bulan = per_minggu * 4
        
        print(f"Tujuan          : {kota['kota']}")
        print(f"Transportasi    : {transport['nama']}")
        print(f"Hari per minggu : {hari_per_minggu}")
        print(f"Biaya per hari  : Rp{per_hari:,}")
        print(f"Biaya per minggu: Rp{per_minggu:,}")
        print(f"Biaya per bulan : Rp{per_bulan:,}")
        print("="*50)
        
    except ValueError:
        print("❌ Masukkan angka yang valid")

# ========================
# Menu Admin (Tersembunyi)
# ========================
def menu_admin_lihat_request():
    """Menu Admin 1: Lihat request tujuan dari user"""
    print("\n" + "="*40)
    print("REQUEST TUJUAN DARI USER (ADMIN)")
    print("="*40)
    
    requests = load_requests()
    
    if not requests:
        print("❌ Tidak ada request tujuan")
        return
    
    print("\nDaftar request tujuan:")
    for i, request in enumerate(requests, 1):
        print(f"{i}. {request['tujuan']} - Status: {request['status']}")

def menu_admin_tambah_tujuan(data):
    """Menu Admin 2: Tambah data tujuan"""
    print("\n" + "="*40)
    print("TAMBAH DATA TUJUAN (ADMIN)")
    print("="*40)
    
    kota_nama = input("Masukkan nama tujuan/kota: ").strip()
    if not kota_nama:
        print("❌ Nama tujuan tidak boleh kosong!")
        return data
    
    # Cek apakah kota sudah ada
    if find_city(data, kota_nama):
        print(f"❌ Tujuan '{kota_nama}' sudah ada!")
        return data
    
    # Buat kota baru
    kota_baru = {"kota": kota_nama, "transportasi": []}
    data.append(kota_baru)
    
    # Tambah transportasi
    while True:
        print(f"\nTambah transportasi untuk {kota_nama}:")
        nama_transport = input("Nama transportasi (atau 'selesai' untuk berhenti): ").strip()
        
        if nama_transport.lower() == 'selesai':
            break
        
        if not nama_transport:
            print("❌ Nama transportasi tidak boleh kosong!")
            continue
        
        try:
            biaya = int(input("Biaya sekali jalan (Rp): "))
            jarak = float(input("Jarak (km): "))
            waktu = int(input("Waktu tempuh (menit): "))
        except ValueError:
            print("❌ Input harus angka!")
            continue
        
        kota_baru["transportasi"].append({
            "nama": nama_transport,
            "biaya": biaya,
            "jarak_km": jarak,
            "waktu_menit": waktu
        })
        
        print(f"✅ Transportasi '{nama_transport}' berhasil ditambahkan!")
    
    save_data(data)
    print(f"✅ Tujuan '{kota_nama}' berhasil ditambahkan!")
    return data

def menu_admin_hapus_tujuan(data):
    """Menu Admin 3: Hapus data tujuan"""
    print("\n" + "="*40)
    print("HAPUS DATA TUJUAN (ADMIN)")
    print("="*40)
    
    if not data:
        print("❌ Tidak ada data tujuan")
        return data
    
    print("\nDaftar tujuan:")
    for i, kota in enumerate(data, 1):
        print(f"{i}. {kota['kota']} ({len(kota['transportasi'])} transportasi)")
    
    try:
        pilihan = int(input("Pilih nomor tujuan yang akan dihapus: ")) - 1
        if not (0 <= pilihan < len(data)):
            print("❌ Pilihan tidak valid")
            return data
        
        kota = data[pilihan]
        konfirmasi = input(f"Yakin hapus tujuan '{kota['kota']}'? (y/n): ").lower()
        
        if konfirmasi == 'y':
            data.remove(kota)
            save_data(data)
            print(f"✅ Tujuan '{kota['kota']}' berhasil dihapus!")
        else:
            print("❌ Penghapusan dibatalkan")
    
    except ValueError:
        print("❌ Masukkan angka yang valid")
    
    return data

def menu_admin(data):
    """Menu admin tersembunyi"""
    while True:
        print("\n" + "="*40)
        print("MENU ADMIN")
        print("="*40)
        print("1. Lihat request tujuan")
        print("2. Tambah data tujuan")
        print("3. Hapus data tujuan")
        print("0. Kembali ke menu utama")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            menu_admin_lihat_request()
        elif pilihan == "2":
            data = menu_admin_tambah_tujuan(data)
        elif pilihan == "3":
            data = menu_admin_hapus_tujuan(data)
        elif pilihan == "0":
            break
        else:
            print("❌ Pilihan tidak valid")
    
    return data

# ========================
# Program utama
# ========================
def main():
    print("="*50)
    print("SELAMAT DATANG DI SV GOEST")
    print("="*50)
    
    # Input nama user
    nama = input("Masukkan nama Anda: ").strip()
    if not nama:
        nama = "Pengguna"
    
    print(f"\nHalo, {nama}! 👋")
    
    # Load data
    data = load_data()
    
    # Cek jika admin
    is_admin = nama.lower() == ADMIN_NAME.lower()
    if is_admin:
        print("👑 Mode Admin diaktifkan")
    
    # Menu utama
    while True:
        print("\n" + "="*40)
        print("MENU UTAMA SV GOEST")
        print("="*40)
        print("1. 🎯 Tujuan")
        print("2. 📝 Request Tujuan")
        print("3. 💰 Rekap Pengeluaran")
        if is_admin:
            print("9. 🔧 Menu Admin (Tersembunyi)")
        print("0. ❌ Keluar")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            menu_tujuan(data)
        elif pilihan == "2":
            menu_request_tujuan()
        elif pilihan == "3":
            menu_rekap_pengeluaran(data)
        elif pilihan == "9" and is_admin:
            data = menu_admin(data)
        elif pilihan == "0":
            print("\n" + "="*50)
            print("Terima kasih telah menggunakan SV GOEST! 👋")
            print("="*50)
            break
        else:
            print("❌ Pilihan tidak valid")

if __name__ == "__main__":
    main()