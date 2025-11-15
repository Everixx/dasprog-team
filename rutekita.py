import json
import os

DATA_FILE = r"D:\dasprog\data_transport.json"
REQUEST_FILE = r"D:\dasprog\request_tujuan.json"
ADMIN_NAME = "admin"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_requests():
    try:
        with open(REQUEST_FILE, "r", encoding="utf-8") as f:
            requests = json.load(f)
        return requests
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_requests(requests):
    with open(REQUEST_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)

def find_city(data, nama_kota): #searching
    for kota in data:
        if kota["kota"].lower() == nama_kota.lower():
            return kota
    return None

def sort_by_cheapest(data):
    """Fungsi untuk mengurutkan data berdasarkan biaya termurah"""
    # Filter out KRL configuration
    data_tujuan = [kota for kota in data if kota.get("kota") != "KONFIGURASI_KRL" and kota.get("kota") != "KONFIGURASI_BISKITA"]
    
    # Urutkan berdasarkan biaya transportasi termurah di setiap kota
    sorted_data = sorted(data_tujuan, key=lambda x: min(t["biaya"] for t in x["transportasi"]))
    
    return sorted_data

def hitung_krl_dari_sv_ipb(data): #searching
    # Cari konfigurasi KRL dalam data
    konfig_krl = None
    for item in data:
        if item.get("kota") == "KONFIGURASI_KRL":
            konfig_krl = item
            break
    
    if not konfig_krl:
        print("❌ Konfigurasi KRL tidak ditemukan dalam data")
        return None

    print("\n" + "="*60)
    print("🚆 RUTE KRL DARI SV IPB - DENGAN TRANSPORTASI PENUNJANG")
    print("="*60)
    
    try:
        # Tahap 1: Ke Stasiun Bogor
        print("\n📍 TAHAP 1: DARI SV IPB KE STASIUN BOGOR")
        print("Pilih transportasi ke stasiun:")
        for i, transport in enumerate(konfig_krl["transportasi_ke_stasiun"], 1):
            print(f"{i}. {transport['nama']} - Rp {transport['biaya']:,}")
        print(f"{len(konfig_krl['transportasi_ke_stasiun']) + 1}. Custom (masukkan manual)")
        
        pilihan1 = input(f"Pilih transportasi ke stasiun (1-{len(konfig_krl['transportasi_ke_stasiun']) + 1}): ").strip()
        
        if pilihan1 == str(len(konfig_krl['transportasi_ke_stasiun']) + 1):
            biaya_ke_stasiun = int(input("Masukkan biaya ke stasiun: Rp "))
            nama_tahap1 = input("Jenis transportasi: ")
        elif pilihan1.isdigit() and 1 <= int(pilihan1) <= len(konfig_krl['transportasi_ke_stasiun']):
            idx = int(pilihan1) - 1
            biaya_ke_stasiun = konfig_krl["transportasi_ke_stasiun"][idx]["biaya"]
            nama_tahap1 = konfig_krl["transportasi_ke_stasiun"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
            
        # Tahap 2: KRL
        print(f"\n📍 TAHAP 2: KRL DARI STASIUN BOGOR")
        print("Pilih tujuan KRL:")
        for i, tujuan in enumerate(konfig_krl["tujuan_krl"], 1):
            print(f"{i}. {tujuan['nama']} - Rp {tujuan['biaya']:,}")
        print(f"{len(konfig_krl['tujuan_krl']) + 1}. Custom (masukkan manual)")
        
        pilihan2 = input(f"Pilih tujuan KRL (1-{len(konfig_krl['tujuan_krl']) + 1}): ").strip()
        
        if pilihan2 == str(len(konfig_krl['tujuan_krl']) + 1):
            biaya_krl = int(input("Masukkan biaya KRL: Rp "))
            tujuan_krl = input("Tujuan KRL: ")
        elif pilihan2.isdigit() and 1 <= int(pilihan2) <= len(konfig_krl['tujuan_krl']):
            idx = int(pilihan2) - 1
            biaya_krl = konfig_krl["tujuan_krl"][idx]["biaya"]
            tujuan_krl = konfig_krl["tujuan_krl"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
            
        # Tahap 3: Dari Stasiun Tujuan
        print(f"\n📍 TAHAP 3: DARI STASIUN TUJUAN KE LOKASI AKHIR")
        print("Pilih transportasi dari stasiun tujuan:")
        for i, transport in enumerate(konfig_krl["transportasi_dari_stasiun"], 1):
            print(f"{i}. {transport['nama']} - Rp {transport['biaya']:,}")
        print(f"{len(konfig_krl['transportasi_dari_stasiun']) + 1}. Custom (masukkan manual)")
        
        pilihan3 = input(f"Pilih transportasi (1-{len(konfig_krl['transportasi_dari_stasiun']) + 1}): ").strip()
        
        if pilihan3 == str(len(konfig_krl['transportasi_dari_stasiun']) + 1):
            biaya_dari_stasiun = int(input("Masukkan biaya dari stasiun: Rp "))
            nama_tahap3 = input("Jenis transportasi: ")
        elif pilihan3.isdigit() and 1 <= int(pilihan3) <= len(konfig_krl['transportasi_dari_stasiun']):
            idx = int(pilihan3) - 1
            biaya_dari_stasiun = konfig_krl["transportasi_dari_stasiun"][idx]["biaya"]
            nama_tahap3 = konfig_krl["transportasi_dari_stasiun"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
        
        # Hitung total
        total_sekali = biaya_ke_stasiun + biaya_krl + biaya_dari_stasiun
        
        # Tampilkan rincian
        print("\n" + "="*50)
        print("💰 RINCIAN BIAYA PERJALANAN KRL DARI SV IPB")
        print("="*50)
        print(f"1. {nama_tahap1:<20} : Rp{biaya_ke_stasiun:,}")
        print(f"2. KRL ke {tujuan_krl:<15} : Rp{biaya_krl:,}")
        print(f"3. {nama_tahap3:<20} : Rp{biaya_dari_stasiun:,}")
        print("-" * 50)
        print(f"TOTAL SEKALI JALAN              : Rp{total_sekali:,}")
        print(f"PULANG-PERGI                    : Rp{total_sekali * 2:,}")
        
        # Estimasi mingguan/bulanan
        print("\n" + "="*30)
        print("📅 ESTIMASI REGULER")
        print("="*30)
        print(f"Per minggu (5x PP) : Rp{total_sekali * 2 * 5:,}")
        print(f"Per bulan (20x PP) : Rp{total_sekali * 2 * 20:,}")
        print("="*50)
        
        return {
            "jenis": "KRL_MULTIMODA",
            "rincian": {
                "tahap1": {"nama": nama_tahap1, "biaya": biaya_ke_stasiun},
                "tahap2": {"nama": f"KRL ke {tujuan_krl}", "biaya": biaya_krl},
                "tahap3": {"nama": nama_tahap3, "biaya": biaya_dari_stasiun}
            },
            "total_sekali": total_sekali,
            "tujuan_krl": tujuan_krl
        }
        
    except ValueError:
        print("❌ Input harus angka!")
        return None

def hitung_biskita_dari_sv_ipb(data): #searching
    # Cari konfigurasi BISKITA dalam data
    konfig_biskita = None
    for item in data:
        if item.get("kota") == "KONFIGURASI_BISKITA":
            konfig_biskita = item
            break
    
    if not konfig_biskita:
        print("❌ Konfigurasi BISKITA tidak ditemukan dalam data")
        return None

    print("\n" + "="*60)
    print("🚌 RUTE BISKITA DARI SV IPB - DENGAN TRANSPORTASI PENUNJANG")
    print("="*60)
    
    try:
        # Tahap 1: Ke Halte Biskita
        print("\n📍 TAHAP 1: DARI SV IPB KE HALTE BISKITA")
        print("Pilih transportasi ke halte:")
        for i, transport in enumerate(konfig_biskita["transportasi_ke_halte"], 1):
            print(f"{i}. {transport['nama']} - Rp {transport['biaya']:,}")
        print(f"{len(konfig_biskita['transportasi_ke_halte']) + 1}. Custom (masukkan manual)")
        
        pilihan1 = input(f"Pilih transportasi ke halte (1-{len(konfig_biskita['transportasi_ke_halte']) + 1}): ").strip()
        
        if pilihan1 == str(len(konfig_biskita['transportasi_ke_halte']) + 1):
            biaya_ke_halte = int(input("Masukkan biaya ke halte: Rp "))
            nama_tahap1 = input("Jenis transportasi: ")
        elif pilihan1.isdigit() and 1 <= int(pilihan1) <= len(konfig_biskita['transportasi_ke_halte']):
            idx = int(pilihan1) - 1
            biaya_ke_halte = konfig_biskita["transportasi_ke_halte"][idx]["biaya"]
            nama_tahap1 = konfig_biskita["transportasi_ke_halte"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
            
        # Tahap 2: BISKITA
        print(f"\n📍 TAHAP 2: BISKITA DARI HALTE")
        print("Pilih tujuan BISKITA:")
        for i, tujuan in enumerate(konfig_biskita["tujuan_biskita"], 1):
            print(f"{i}. {tujuan['nama']} - Rp {tujuan['biaya']:,}")
        print(f"{len(konfig_biskita['tujuan_biskita']) + 1}. Custom (masukkan manual)")
        
        pilihan2 = input(f"Pilih tujuan BISKITA (1-{len(konfig_biskita['tujuan_biskita']) + 1}): ").strip()
        
        if pilihan2 == str(len(konfig_biskita['tujuan_biskita']) + 1):
            biaya_biskita = int(input("Masukkan biaya BISKITA: Rp "))
            tujuan_biskita = input("Tujuan BISKITA: ")
        elif pilihan2.isdigit() and 1 <= int(pilihan2) <= len(konfig_biskita['tujuan_biskita']):
            idx = int(pilihan2) - 1
            biaya_biskita = konfig_biskita["tujuan_biskita"][idx]["biaya"]
            tujuan_biskita = konfig_biskita["tujuan_biskita"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
            
        # Tahap 3: Dari Halte Tujuan
        print(f"\n📍 TAHAP 3: DARI HALTE TUJUAN KE LOKASI AKHIR")
        print("Pilih transportasi dari halte tujuan:")
        # Menggunakan transportasi_ke_halte yang sama untuk tahap 3
        for i, transport in enumerate(konfig_biskita["transportasi_ke_halte"], 1):
            print(f"{i}. {transport['nama']} - Rp {transport['biaya']:,}")
        print(f"{len(konfig_biskita['transportasi_ke_halte']) + 1}. Custom (masukkan manual)")
        
        pilihan3 = input(f"Pilih transportasi (1-{len(konfig_biskita['transportasi_ke_halte']) + 1}): ").strip()
        
        if pilihan3 == str(len(konfig_biskita['transportasi_ke_halte']) + 1):
            biaya_dari_halte = int(input("Masukkan biaya dari halte: Rp "))
            nama_tahap3 = input("Jenis transportasi: ")
        elif pilihan3.isdigit() and 1 <= int(pilihan3) <= len(konfig_biskita['transportasi_ke_halte']):
            idx = int(pilihan3) - 1
            biaya_dari_halte = konfig_biskita["transportasi_ke_halte"][idx]["biaya"]
            nama_tahap3 = konfig_biskita["transportasi_ke_halte"][idx]["nama"]
        else:
            print("❌ Pilihan tidak valid")
            return None
        
        # Hitung total
        total_sekali = biaya_ke_halte + biaya_biskita + biaya_dari_halte
        
        # Tampilkan rincian
        print("\n" + "="*50)
        print("💰 RINCIAN BIAYA PERJALANAN BISKITA DARI SV IPB")
        print("="*50)
        print(f"1. {nama_tahap1:<20} : Rp{biaya_ke_halte:,}")
        print(f"2. BISKITA ke {tujuan_biskita:<12} : Rp{biaya_biskita:,}")
        print(f"3. {nama_tahap3:<20} : Rp{biaya_dari_halte:,}")
        print("-" * 50)
        print(f"TOTAL SEKALI JALAN              : Rp{total_sekali:,}")
        print(f"PULANG-PERGI                    : Rp{total_sekali * 2:,}")
        
        # Estimasi mingguan/bulanan
        print("\n" + "="*30)
        print("📅 ESTIMASI REGULER")
        print("="*30)
        print(f"Per minggu (5x PP) : Rp{total_sekali * 2 * 5:,}")
        print(f"Per bulan (20x PP) : Rp{total_sekali * 2 * 20:,}")
        print("="*50)
        
        return {
            "jenis": "BISKITA_MULTIMODA",
            "rincian": {
                "tahap1": {"nama": nama_tahap1, "biaya": biaya_ke_halte},
                "tahap2": {"nama": f"BISKITA ke {tujuan_biskita}", "biaya": biaya_biskita},
                "tahap3": {"nama": nama_tahap3, "biaya": biaya_dari_halte}
            },
            "total_sekali": total_sekali,
            "tujuan_biskita": tujuan_biskita
        }
        
    except ValueError:
        print("❌ Input harus angka!")
        return None

def menu_tujuan(data):
    """Menu 1: Lihat tujuan dan transportasi dengan fitur sorting biaya termurah"""
    print("\n" + "="*50)
    print("🎯 DAFTAR TUJUAN DAN TRANSPORTASI")
    print("="*50)
    
    # Filter data untuk mengecualikan konfigurasi KRL dan BISKITA
    data_tujuan = [kota for kota in data if kota.get("kota") != "KONFIGURASI_KRL" and kota.get("kota") != "KONFIGURASI_BISKITA"]
    
    if not data_tujuan:
        print("❌ Belum ada data tujuan")
        return
    
    # Tampilkan opsi sorting
    print("\n📊 OPSI TAMPILAN:")
    print("1. Tampilkan semua tujuan")
    print("2. Urutkan berdasarkan biaya termurah")
    
    try:
        sort_choice = input("Pilih opsi tampilan (1-2): ").strip()
        
        if sort_choice == "2":
            data_tampil = sort_by_cheapest(data)
            print("\n✅ Data diurutkan berdasarkan biaya termurah")
        else:
            data_tampil = data_tujuan
            print("\n📋 Menampilkan semua tujuan")
    except:
        data_tampil = data_tujuan
        print("\n📋 Menampilkan semua tujuan")
    
    # Tampilkan data
    print("\n" + "="*50)
    print(f"🏙️  DAFTAR TUJUAN ({len(data_tampil)} hasil)")
    print("="*50)
    
    for i, kota in enumerate(data_tampil, 1):
        print(f"\n{i}. 🏙️  {kota['kota']}")
        # Urutkan transportasi berdasarkan biaya (termurah ke termahal)
        transportasi_sorted = sorted(kota["transportasi"], key=lambda x: x["biaya"])
        for j, transport in enumerate(transportasi_sorted, 1):
            print(f"   {j}. {transport['nama']} - Rp{transport['biaya']:,} - {transport['jarak_km']} km - {transport['waktu_menit']} menit")
    
    # Tambahkan opsi KRL dan BISKITA khusus
    print(f"\n{len(data_tampil) + 1}. 🚆 KRL (Dari SV IPB dengan transportasi penunjang)")
    print(f"{len(data_tampil) + 2}. 🚌 BISKITA (Dari SV IPB dengan transportasi penunjang)")
    
    # Pilih untuk estimasi biaya
    try:
        pilihan = input(f"\nPilih nomor tujuan untuk estimasi biaya (1-{len(data_tampil) + 2}) atau 0 untuk kembali: ").strip()
        if pilihan == "0":
            return
        
        pilihan_int = int(pilihan)
        
        # Jika memilih opsi KRL khusus
        if pilihan_int == len(data_tampil) + 1:
            hasil_krl = hitung_krl_dari_sv_ipb(data)
            return
        
        # Jika memilih opsi BISKITA khusus
        if pilihan_int == len(data_tampil) + 2:
            hasil_biskita = hitung_biskita_dari_sv_ipb(data)
            return
        
        idx_kota = pilihan_int - 1
        if 0 <= idx_kota < len(data_tampil):
            kota = data_tampil[idx_kota]
            print(f"\nPilih transportasi di {kota['kota']}:")
            # Tampilkan transportasi yang sudah diurutkan dari termurah
            transportasi_sorted = sorted(kota["transportasi"], key=lambda x: x["biaya"])
            for j, transport in enumerate(transportasi_sorted, 1):
                print(f"   {j}. {transport['nama']} - Rp{transport['biaya']:,}")
            
            pilihan_transport = input("Pilih nomor transportasi: ").strip()
            idx_transport = int(pilihan_transport) - 1
            
            if 0 <= idx_transport < len(transportasi_sorted):
                transport = transportasi_sorted[idx_transport]
                
                print("\n" + "="*40)
                print("💰 ESTIMASI BIAYA")
                print("="*40)
                
                sekali = transport["biaya"]
                pp = sekali * 2
                minggu = pp * 5
                bulan = minggu * 4
                
                print(f"Transportasi          : {transport['nama']}")
                print(f"Tujuan               : {kota['kota']}")
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
    print("📝 REQUEST TUJUAN BARU")
    print("="*40)
    
    tujuan_baru = input("Masukkan nama tujuan yang ingin ditambahkan: ").strip()
    
    if not tujuan_baru:
        print("❌ Nama tujuan tidak boleh kosong!")
        return
    
    requests = load_requests()
    
    for req in requests:
        if req["tujuan"].lower() == tujuan_baru.lower():
            print(f"❌ Request untuk tujuan '{tujuan_baru}' sudah ada!")
            return
    
    requests.append({"tujuan": tujuan_baru, "status": "pending"})
    save_requests(requests)
    
    print(f"✅ Request tujuan '{tujuan_baru}' berhasil dikirim!")

def menu_admin_lihat_request():
    """Menu Admin 1: Lihat request tujuan dari user"""
    print("\n" + "="*40)
    print("👀 REQUEST TUJUAN DARI USER (ADMIN)")
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
    print("➕ TAMBAH DATA TUJUAN (ADMIN)")
    print("="*40)
    
    kota_nama = input("Masukkan nama tujuan/kota: ").strip()
    if not kota_nama:
        print("❌ Nama tujuan tidak boleh kosong!")
        return data
    
    if find_city(data, kota_nama):
        print(f"❌ Tujuan '{kota_nama}' sudah ada!")
        return data
    
    kota_baru = {"kota": kota_nama, "transportasi": []}
    data.append(kota_baru)
    
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
    print("🗑️  HAPUS DATA TUJUAN (ADMIN)")
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
        konfirmasi = input(f"Yakin hapus tujuan '{kota['kota']}'? (y/t): ").lower()
        
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
        print("🔧 MENU ADMIN")
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

def main():
    print("="*50)
    print("🌟 SELAMAT DATANG DI SV GOEST 🌟")
    print("="*50)
    
    nama = input("Masukkan nama Anda: ").strip()
    if not nama:
        nama = "Pengguna"
    
    print(f"\nHalo, {nama}! 👋")
    
    data = load_data()
    
    is_admin = nama.lower() == ADMIN_NAME.lower()
    if is_admin:
        print("👑 Mode Admin diaktifkan")
    
    while True:
        print("\n" + "="*40)
        print("🏠 MENU UTAMA SV GOEST")
        print("="*40)
        print("1. 🎯 Tujuan & Transportasi")
        print("2. 📝 Request Tujuan") 
        if is_admin:
            print("3. 🔧 Menu Admin (Tersembunyi)")
        print("0. ❌ Keluar")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            menu_tujuan(data)
        elif pilihan == "2":
            menu_request_tujuan()
        elif pilihan == "3" and is_admin:
            data = menu_admin(data)
        elif pilihan == "0":
            print("\n" + "="*50)
            print("🙏 Terima kasih telah menggunakan SV GOEST! 👋")
            print("="*50)
            break
        else:
            print("❌ Pilihan tidak valid")

if __name__ == "__main__":
    main()