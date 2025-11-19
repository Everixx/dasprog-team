import json
import os

DATA_FILE = r"D:\kelompok\transport.json"
REQUEST_FILE = r"D:\kelompok\request.json"

def baca_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return None

def simpan_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def baca_permintaan():
    try:
        with open(REQUEST_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Handle both old and new format
            if isinstance(data, list):
                return {"requests": data}
            return data
    except:
        return {"requests": []}

def simpan_permintaan(permintaan):
    with open(REQUEST_FILE, "w", encoding="utf-8") as file:
        json.dump(permintaan, file, indent=2, ensure_ascii=False)

# --- FUNGSI SORTING ---
def urutkan_krl_berdasarkan_nama():
    """Mengurutkan tujuan KRL berdasarkan nama (A-Z)"""
    data = baca_data()
    if not data:
        return None
    
    tujuan_terurut = sorted(data['krl_destinations'], key=lambda x: x['name'])
    return tujuan_terurut

def urutkan_krl_berdasarkan_biaya():
    """Mengurutkan tujuan KRL berdasarkan biaya (termurah dulu)"""
    data = baca_data()
    if not data:
        return None
    
    tujuan_terurut = sorted(data['krl_destinations'], key=lambda x: x['cost'])
    return tujuan_terurut

def urutkan_transport_berdasarkan_biaya():
    """Mengurutkan transportasi berdasarkan biaya (termurah dulu)"""
    data = baca_data()
    if not data:
        return None
    
    transport_terurut = sorted(data['transport_to_station'], key=lambda x: x['cost'])
    return transport_terurut

# --- FUNGSI SEARCHING ---
def cari_tujuan_krl(kata_kunci):
    """Mencari tujuan KRL berdasarkan nama"""
    data = baca_data()
    if not data:
        return None
    
    kata_kunci = kata_kunci.lower()
    hasil = []
    
    for tujuan in data['krl_destinations']:
        if kata_kunci in tujuan['name'].lower():
            hasil.append(tujuan)
    
    return hasil

def cari_transportasi(kata_kunci):
    """Mencari transportasi berdasarkan nama"""
    data = baca_data()
    if not data:
        return None
    
    kata_kunci = kata_kunci.lower()
    hasil = []
    
    for transport in data['transport_to_station']:
        if kata_kunci in transport['name'].lower():
            hasil.append(transport)
    
    return hasil

def tampilkan_info():
    data = baca_data()
    if not data:
        print("Data tidak ditemukan")
        return
    
    print("\n" + "="*50)
    print("INFORMASI TRANSPORTASI")
    print("="*50)
    
    # Tampilkan transportasi terurut berdasarkan biaya
    transport_terurut = urutkan_transport_berdasarkan_biaya()
    print("\nTransportasi ke Stasiun Bogor (Termurah -> Termahal):")
    for transport in transport_terurut:
        biaya = f"Rp {transport['cost']:,}" if transport['cost'] > 0 else "Gratis"
        print(f"- {transport['name']}: {biaya}")
    
    # Tampilkan tujuan KRL terurut berdasarkan biaya
    tujuan_terurut = urutkan_krl_berdasarkan_biaya()
    print("\nTujuan KRL dari Stasiun Bogor (Termurah -> Termahal):")
    for tujuan in tujuan_terurut:
        print(f"- {tujuan['name']}: Rp {tujuan['cost']:,}")

def hitung_biaya():
    data = baca_data()
    if not data:
        print("Data tidak ditemukan")
        return
    
    print("\n" + "="*40)
    print("HITUNG BIAYA")
    print("="*40)
    
    print("\nPilih jenis perhitungan:")
    print("1. Ke Stasiun Bogor saja")
    print("2. Perjalanan KRL lengkap")
    print("3. Cari tujuan KRL")
    
    pilihan = input("Pilihan (1-3): ")
    
    if pilihan == "1":
        print("\nPilih transportasi ke Stasiun Bogor:")
        transports = urutkan_transport_berdasarkan_biaya()  # Tampilkan terurut
        for i, transport in enumerate(transports, 1):
            biaya = f"Rp {transport['cost']:,}" if transport['cost'] > 0 else "Gratis"
            print(f"{i}. {transport['name']} - {biaya}")
        
        try:
            pilihan_transport = int(input("Pilih transportasi: ")) - 1
            if 0 <= pilihan_transport < len(transports):
                transport = transports[pilihan_transport]
                
                if transport['name'] == "Kendaraan Pribadi":
                    bensin = int(input("Biaya bensin: Rp "))
                    parkir = int(input("Biaya parkir: Rp "))
                    total = bensin + parkir
                else:
                    total = transport['cost']
                
                print(f"\nBiaya sekali jalan: Rp {total:,}")
                print(f"Biaya pulang-pergi: Rp {total * 2:,}")
                print(f"Per minggu (5x): Rp {total * 2 * 5:,}")
                print(f"Per bulan (20x): Rp {total * 2 * 20:,}")
                
        except:
            print("Input harus angka")
            
    elif pilihan == "2":
        print("\nTAHAP 1: Transportasi ke Stasiun Bogor")
        transports = urutkan_transport_berdasarkan_biaya()  # Tampilkan terurut
        for i, transport in enumerate(transports, 1):
            biaya = f"Rp {transport['cost']:,}" if transport['cost'] > 0 else "Gratis"
            print(f"{i}. {transport['name']} - {biaya}")
        
        try:
            pilihan_transport = int(input("Pilih transportasi: ")) - 1
            if not (0 <= pilihan_transport < len(transports)):
                return
                
            transport = transports[pilihan_transport]
            
            if transport['name'] == "Kendaraan Pribadi":
                bensin = int(input("Biaya bensin: Rp "))
                parkir = int(input("Biaya parkir: Rp "))
                biaya_transport = bensin + parkir
            else:
                biaya_transport = transport['cost']
            
            print("\nTAHAP 2: Tujuan KRL")
            tujuan_krl = urutkan_krl_berdasarkan_biaya()  # Tampilkan terurut
            for i, tujuan in enumerate(tujuan_krl, 1):
                print(f"{i}. {tujuan['name']} - Rp {tujuan['cost']:,}")
            
            pilihan_krl = int(input("Pilih tujuan KRL: ")) - 1
            if 0 <= pilihan_krl < len(tujuan_krl):
                tujuan = tujuan_krl[pilihan_krl]
                total = biaya_transport + tujuan['cost']
                
                print(f"\nTotal sekali jalan: Rp {total:,}")
                print(f"Total pulang-pergi: Rp {total * 2:,}")
                print(f"Per minggu (5x): Rp {total * 2 * 5:,}")
                print(f"Per bulan (20x): Rp {total * 2 * 20:,}")
                
        except:
            print("Input harus angka")
    
    elif pilihan == "3":
        # Fungsi searching
        kata_kunci = input("Masukkan nama tujuan KRL yang dicari: ")
        hasil = cari_tujuan_krl(kata_kunci)
        
        if hasil:
            print(f"\nHasil pencarian untuk '{kata_kunci}':")
            for tujuan in hasil:
                print(f"- {tujuan['name']}: Rp {tujuan['cost']:,}")
        else:
            print(f"Tidak ditemukan tujuan KRL dengan kata kunci '{kata_kunci}'")

def minta_tujuan():
    data = baca_permintaan()
    
    nama = input("Nama Anda: ")
    tujuan = input("Tujuan KRL yang diminta: ")
    
    if not nama or not tujuan:
        print("Nama dan tujuan harus diisi")
        return
    
    permintaan_baru = {
        "nama": nama,
        "tujuan": tujuan
    }
    
    data['requests'].append(permintaan_baru)
    simpan_permintaan(data)
    print("Permintaan berhasil dikirim")

def hapus_tujuan_krl():
    data = baca_data()
    if not data:
        print("Data tidak ditemukan")
        return False
    
    tujuan_krl = urutkan_krl_berdasarkan_nama()  # Tampilkan terurut berdasarkan nama
    
    if not tujuan_krl:
        print("Tidak ada tujuan KRL yang bisa dihapus")
        return False
    
    print("\nDaftar Tujuan KRL (Terurut A-Z):")
    for i, tujuan in enumerate(tujuan_krl, 1):
        print(f"{i}. {tujuan['name']} - Rp {tujuan['cost']:,}")
    
    try:
        pilihan = int(input("Pilih tujuan KRL yang akan dihapus: ")) - 1
        if 0 <= pilihan < len(tujuan_krl):
            tujuan_dihapus = tujuan_krl[pilihan]
            
            konfirmasi = input(f"Yakin hapus '{tujuan_dihapus['name']}'? (y/t): ").lower()
            if konfirmasi == 'y':
                # Hapus tujuan dari data asli (bukan yang terurut)
                for i, tujuan in enumerate(data['krl_destinations']):
                    if tujuan['name'] == tujuan_dihapus['name']:
                        data['krl_destinations'].pop(i)
                        break
                
                simpan_data(data)
                print("Tujuan KRL berhasil dihapus")
                return True
            else:
                print("Penghapusan dibatalkan")
                return False
        else:
            print("Pilihan tidak valid")
            return False
    except:
        print("Input harus angka")
        return False

def menu_admin():
    data = baca_data()
    if not data:
        print("Data tidak ditemukan")
        return
    
    password = input("Password admin: ")
    if password != data['admin_password']:
        print("Password salah")
        return
    
    while True:
        print("\n" + "="*20)
        print("MENU ADMIN")
        print("="*20)
        print("1. Lihat permintaan user")
        print("2. Tambah tujuan KRL")
        print("3. Hapus tujuan KRL")
        print("4. Cari tujuan KRL")
        print("5. Kembali")
        
        pilihan = input("Pilihan: ")
        
        if pilihan == "1":
            data_permintaan = baca_permintaan()
            requests = data_permintaan.get('requests', [])
            
            if requests:
                print("\nPermintaan User:")
                for i, permintaan in enumerate(requests, 1):
                    # Handle both old and new format
                    nama = permintaan.get('nama') or permintaan.get('name', 'Tidak ada nama')
                    tujuan = permintaan.get('tujuan') or permintaan.get('destination', 'Tidak ada tujuan')
                    print(f"{i}. {nama}: {tujuan}")
            else:
                print("Tidak ada permintaan")
                
        elif pilihan == "2":
            data = baca_data()
            if not data:
                continue
                
            nama = input("Nama tujuan KRL: ")
            try:
                biaya = int(input("Biaya KRL: Rp "))
            except:
                print("Biaya harus angka")
                continue
            
            tujuan_baru = {"name": nama, "cost": biaya}
            data['krl_destinations'].append(tujuan_baru)
            
            simpan_data(data)
            print("Tujuan berhasil ditambahkan")
        
        elif pilihan == "3":
            hapus_tujuan_krl()
                
        elif pilihan == "4":
            kata_kunci = input("Masukkan nama tujuan KRL yang dicari: ")
            hasil = cari_tujuan_krl(kata_kunci)
            
            if hasil:
                print(f"\nHasil pencarian untuk '{kata_kunci}':")
                for tujuan in hasil:
                    print(f"- {tujuan['name']}: Rp {tujuan['cost']:,}")
            else:
                print(f"Tidak ditemukan tujuan KRL dengan kata kunci '{kata_kunci}'")
                
        elif pilihan == "5":
            break

def main():
    print("=" * 50)
    print("SISTEM TRANSPORTASI KRL SV IPB")
    print("=" * 50)
    
    nama = input("Masukkan nama Anda: ")
    print(f"\nHalo, {nama}!")
    
    while True:
        print("\n" + "="*30)
        print("MENU UTAMA")
        print("="*30)
        print("1. Hitung Biaya Transportasi")
        print("2. Minta Tujuan KRL Baru") 
        print("3. Keluar")
        
        pilihan = input("Pilihan: ")
        
        if pilihan == "1":
            tampilkan_info()
            hitung_biaya()
        elif pilihan == "2":
            minta_tujuan()
        elif pilihan == "3":
            print(f"\nTerima kasih {nama}!")
            break
        elif pilihan == "0":
            menu_admin()

if __name__ == "__main__":
    main()