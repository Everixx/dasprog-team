import json

DATA_FILE = "transport.json"
REQUEST_FILE = "request.json"

def load_data(filename): #read
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if filename == REQUEST_FILE and isinstance(data, list):
                return {"requests": data}
            return data
    except:
        if filename == REQUEST_FILE:
            return {"requests": []}
        return None

def save_data(data, filename): #create
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def sort_data(data, key): #sorting
    return sorted(data, key=lambda x: x[key])

def search_data(data, keyword, field='name'): #searching
    keyword = keyword.lower()
    return [item for item in data if keyword in item[field].lower()]

def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def display_info():
    data = load_data(DATA_FILE)
    if not data:
        print("❌ Data tidak ditemukan")
        return
    print("\n" + "="*50)
    print("🚊 INFO TRANSPORTASI")
    print("="*50)
    
    transports = sort_data(data['transport_to_station'], 'cost')
    print("\n🚗 Ke Stasiun Bogor:")
    for t in transports:
        cost = format_rupiah(t['cost']) if t['cost'] > 0 else "🆓 Gratis"
        print(f"  • {t['name']}: {cost}")
    
    transports = sort_data(data['transport_from_destination'], 'cost')
    print("\n🚕 Dari Stasiun Tujuan:")
    for t in transports:
        cost = format_rupiah(t['cost']) if t['cost'] > 0 else "🆓 Gratis"
        print(f"  • {t['name']}: {cost}")
    
    destinations = sort_data(data['krl_destinations'], 'cost')
    print("\n🎯 Tujuan KRL:")
    for d in destinations:
        print(f"  • {d['name']}: {format_rupiah(d['cost'])}")

def calculate_cost():
    data = load_data(DATA_FILE)
    if not data:
        print("❌ Data tidak ditemukan")
        return
    
    print("\n💰 HITUNG BIAYA TRANSPORTASI")
    print("1. 🚗  Transportasi ke Stasiun")
    print("2. 🚊  Perjalanan KRL lengkap (dari SV IPB University/rumah ke tujuan akhir)")
    print("3. 🔍  Cari Tujuan KRL")
    
    choice = input("Pilihan: ")
    
    if choice == "1":
        transport = select_transport("KE STASIUN", data['transport_to_station'])
        if transport:
            cost = get_transport_cost(transport)
            show_cost_breakdown(cost, "Transportasi ke Stasiun")
    
    elif choice == "2":
        transport1 = select_transport("KE STASIUN", data['transport_to_station'])
        if not transport1: return
        cost1 = get_transport_cost(transport1)

        dest = select_krl_destination(data['krl_destinations'])
        if not dest: return
        cost2 = dest['cost']
        
        transport2 = select_transport("DARI STASIUN", data['transport_from_destination'])
        if not transport2: return
        cost3 = get_transport_cost(transport2)
        
        total = cost1 + cost2 + cost3
        print(f"\n📊 Total Sekali Jalan: {format_rupiah(total)}")
        show_cost_breakdown(total, "Perjalanan Lengkap")
    
    elif choice == "3":
        keyword = input("Cari tujuan: ")
        results = search_data(data['krl_destinations'], keyword)
        if results:
            print(f"\n✅ Ditemukan {len(results)} hasil:")
            for item in results:
                print(f"  • {item['name']}: {format_rupiah(item['cost'])}")
        else:
            print("❌ Tidak ditemukan")

def select_transport(title, transport_list):
    transports = sort_data(transport_list, 'cost')
    print(f"\n{title}:")
    for i, t in enumerate(transports, 1):
        cost = format_rupiah(t['cost']) if t['cost'] > 0 else "Gratis"
        print(f"  {i}. {t['name']} - {cost}")
    
    try:
        choice = int(input("Pilih: ")) - 1
        return transports[choice] if 0 <= choice < len(transports) else None
    except:
        return None

def select_krl_destination(destinations):
    dests = sort_data(destinations, 'name')
    print(f"\n🎯 TUJUAN KRL:")
    for i, d in enumerate(dests, 1):
        print(f"  {i}. {d['name']} - {format_rupiah(d['cost'])}")
    
    try:
        choice = int(input("Pilih: ")) - 1
        return dests[choice] if 0 <= choice < len(dests) else None
    except:
        return None

def get_transport_cost(transport):
    if transport['name'] == "Kendaraan Pribadi":
        try:
            fuel = int(input("⛽  Biaya bensin: Rp "))
            parking = int(input("🅿️  Biaya parkir: Rp "))
            return fuel + parking
        except:
            return 0
    return transport['cost']

def show_cost_breakdown(cost, title):
    print(f"\n📊 {title}:")
    print(f"  💰 Sekali jalan: {format_rupiah(cost)}")
    print(f"  🔄 Pulang-pergi: {format_rupiah(cost * 2)}")
    print(f"  📅 Per minggu(5x): {format_rupiah(cost * 2 * 5)}")
    print(f"  📅 Per bulan(20x): {format_rupiah(cost * 2 * 20)}")

def request_destination():
    data = load_data(REQUEST_FILE)
    
    print("\n💡 MINTA TUJUAN BARU")
    name = input("Nama: ")
    destination = input("Tujuan: ")
    
    if name and destination:
        data['requests'].append({"nama": name, "tujuan": destination})
        save_data(data, REQUEST_FILE)
        print("✅ Permintaan terkirim!")

def admin_menu(): #update
    data = load_data(DATA_FILE)
    if not data:
        print("❌ Data tidak ditemukan")
        return
    
    if input("🔒 Password: ") != data['admin_password']:
        print("❌ Password salah!")
        return
    
    while True:
        print("\n👨‍💼 MENU ADMIN")
        print("1. 👥  Lihat Permintaan")
        print("2. ➕  Tambah Tujuan KRL")
        print("3. 🗑️  Hapus Tujuan KRL")
        print("4. ↩️  Kembali")
        
        choice = input("Pilihan: ")
        
        if choice == "1":
            request_data = load_data(REQUEST_FILE)
            requests = request_data.get('requests', [])
            
            if requests:
                print(f"\n📋 {len(requests)} Permintaan:")
                for req in requests:
                    nama = req.get('nama', req.get('name', 'Tidak ada nama'))
                    tujuan = req.get('tujuan', req.get('destination', 'Tidak ada tujuan'))
                    print(f"  👤 {nama}: {tujuan}")
            else:
                print("ℹ️ Tidak ada permintaan")
        
        elif choice == "2":
            name = input("Nama tujuan: ")
            try:
                cost = int(input("Biaya: Rp "))
                data['krl_destinations'].append({"name": name, "cost": cost})
                save_data(data, DATA_FILE)
                print("✅ Tujuan ditambahkan!")
            except:
                print("❌ Biaya harus angka")
        
        elif choice == "3":
            if delete_krl_destination():
                save_data(data, DATA_FILE)
        
        elif choice == "4":
            break

def delete_krl_destination(): #Delete
    data = load_data(DATA_FILE)
    if not data:
        return False
    
    destinations = sort_data(data['krl_destinations'], 'name')
    print("\n🗑️ HAPUS TUJUAN KRL:")
    for i, d in enumerate(destinations, 1):
        print(f"  {i}. {d['name']} - {format_rupiah(d['cost'])}")
    
    try:
        choice = int(input("Pilih: ")) - 1
        if 0 <= choice < len(destinations):
            deleted = destinations[choice]
            if input(f"Hapus '{deleted['name']}'? (y/t): ").lower() == 'y':
                data['krl_destinations'] = [d for d in data['krl_destinations'] if d['name'] != deleted['name']]
                print("✅ Tujuan dihapus!")
                return True
    except:
        pass
    
    return False

def main():
    print("=" * 40)
    print("🚊 ESTIMATOR BIAYA TRANSPORTASI KRL SV IPB")
    print("=" * 40)
    
    name = input("👤 Nama Anda: ")
    print(f"\n🎉 Halo, {name}! Selamat datang di Estimator Biaya Transportasi KRL SV IPB!")
    
    while True:
        print("\n🏠 MENU UTAMA")
        print("1. 💰 Hitung Biaya Transportasi ke stasiun")
        print("2. 💡 Minta Tujuan")
        print("3. ❌ Keluar")
        
        choice = input("Pilihan: ")
        
        if choice == "1":
            display_info()
            calculate_cost()
        elif choice == "2":
            request_destination()
        elif choice == "3":
            print(f"\n👋 Terima kasih {name}!")
            break
        elif choice == "0":
            admin_menu()

if __name__ == "__main__":
    main()