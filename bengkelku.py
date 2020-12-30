import os
import csv
import datetime

def clearscreen():
    os.system("clear||cls")

def int_input(note):
    try: 
        return int(input(note))
    except: 
        return int_input(note)

def login():
    clearscreen()
    print(" Login ".center(30, "="))

    USERNAME = input(f"{'Username':12}: ")
    KEY = input(f"{'Password':12}: ")
    # invalid?
    if USERNAME != "BengkelKu" or KEY != "2021Sukses":
        login()

def show(data1):
    print(" Persediaan ".center(73,'='))
    print(f"|{'No':^6}| {'Nama Barang':<30}| {'Stok':<10}| {'Harga Jual':<19}|")
    print("="*73)

    num = 0
    for i in data1: 
        num += 1
        name, stock, price = i['Nama Barang'], i['Stok'], i['Harga Jual']
        print(f"|{num:^6}| {name:<30}| {stock:<10}|Rp {int(price):16,} |")
    print('='*73)

def sell(data1, data2):
    show(data1)
    user_input = int_input("Pilih | No | Produk Yang Terjual: ")

    # nomor valid?
    if 1 <= user_input <= len(data1):
        total_sold = int_input("Jumlah Barang Yang Terjual: ")
        stock   = int(data1[user_input-1]["Stok"])

        # stock tersedia?
        if 1 <= total_sold <= stock:
            add = int_input("Biaya Tambahan: ")
            price = int(data1[user_input-1]["Harga Jual"]) * total_sold + add
            note = input("Keterangan: ")

            data2.append({
            "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
            "Aktivitas":"Jual", 
            "Nama Barang": data1[user_input-1]["Nama Barang"],
            "Jumlah":total_sold, 
            "Harga": price,
            "Keterangan": note
            })

            data1[user_input-1]["Stok"] = stock - total_sold
            if data1[user_input-1]["Stok"] == 0:
                data1.pop(user_input-1)
            
            # catat?
            if input("Masukkan [iya] Jika Anda Yakin Ingin Melakukan Pencatatan Penjualan: ") == 'iya':
                write(data1, "dataset_gudang.csv")
                write(data2, "dataset_transaksi.csv")
                print("Berhasil Melakukan Pencatatan Penjualan".center(66, "="))

        else:
            print("Input Invalid!")
    else: 
        print("Input Invalid!")

def service(data2):
    print(" Service ".center(30, "="))
    note = input("Keterangan: ")
    price = int_input("Biaya Service: ")
     
    data2.append({
    "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
    "Aktivitas":"Service", 
    "Nama Barang": "---Service",
    "Jumlah": "---", 
    "Harga": price,
    "Keterangan": note
    })
    # catat?
    if input("Masukkan [iya] Jika Anda Yakin Ingin Melakukan Pencatatan Service: ") == 'iya':
        write(data2, "dataset_transaksi.csv")
        print("Berhasil Melakukan Pencatatan Service".center(66, "="))

def buy(data1, data2):
    show(data1)
    user_input = int_input("[0] untuk menambah produk baru\nPilih |No| produk yang akan ditambah: ")

    # Tambah barang baru?
    if user_input == 0:
        name = input("Nama Barang: ")
        total = int_input("Jumlah Barang: ")
        price_pcs = int_input("Harga Satuan Ketika Hendak Dijual: ")

        data1.append({
            "Nama Barang": name, 
            "Stok": total, 
            "Harga Jual": price_pcs
            })

    # Tambah stok?
    elif 0 < user_input <= len(data1):
        name = data1[user_input-1]["Nama Barang"]
        total = int_input("Jumlah barang yang dibeli: ")
        data1[user_input-1]["Stok"] = int(data1[user_input-1]["Stok"]) + total
    
    # input invalid?
    else: 
        print("Input Invalid!")
        return
    
    price = int_input("Total Harga Pembelian: ")
    note = input("Keterangan: ")
    data2.append({
        "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
        "Aktivitas":"Beli", 
        "Nama Barang": name,
        "Jumlah":total, 
        "Harga": -price,
        "Keterangan": note
        })

    # catat?
    if input("Masukkan [iya] Jika Anda Yakin Ingin Melakukan Pencatatan Penjualan: ") == 'iya':
        write(data1, "dataset_gudang.csv")
        write(data2, "dataset_transaksi.csv")
        print("Berhasil Melakukan Pencatatan Penjualan".center(66, "="))

def report(data2):
    print(" Laporan Transaksi ".center(114,'='))
    print(f"|{'No':^6}|{'Tanggal':^12}|{'Aktivitas':^16}|{'Nama Barang':^26}|{'Jumlah':^8}|{'Harga':^20}|{'Keterangan':^18}|")
    print("="*114)

    num = 0
    for i in data2: 
        num += 1
        dt, act, name = i['Tanggal'], i['Aktivitas'], i['Nama Barang']
        total, price, note = i['Jumlah'], i['Harga'], i['Keterangan']
        print(f"|{num:^6}|{dt:^12}| {act:<15}| {name:<25}| {total:<7}| Rp{int(price):16,} | {note:<17}|")

    print("="*114)
    total_price = sum([int(price['Harga']) for price in data2])
    print(f"|{'Total Transaksi: ':>93}Rp{total_price:16,} |")
    print("="*114)

def clear_report(data2):
    report(data2)

    # Yakin hapus data?
    if input("Masukkan [iya] jika anda yakin ingin menghapus laporan keuangan: ") == 'iya':
        date_now = datetime.date.today().strftime('%d %B %Y')
        filepath_backup = "backups/" + str(date_now)+'.csv'
        try:
            write(data2, filepath_backup)
            print("!! Lokasi Backup Data: ", filepath_backup)
        except:
            print("Data Transaksi Kosong!")
        with open("dataset_transaksi.csv", "w") as f:
            f.write("Tanggal,Aktivitas,Nama Barang,Jumlah,Harga,Keterangan")
        print("Berhasil Membersihkan Data")

def write(file, filepath):
    with open(filepath, "w") as f:
        dw = csv.DictWriter(f, file[0].keys())
        dw.writeheader()
        dw.writerows(file)

login()
while True:
    # Pemilihan menu
    clearscreen()
    print(" Menu ".center(40, "="))
    print("[1] Tampilkan Persediaan")
    print("[2] Catat Penjualan")
    print("[3] Catat Jasa Service")
    print("[4] Catat Pembelian")
    print("[5] Laporan Keuangan")
    print("[6] Bersihkan Laporan Keuangan")
    print("[0] Keluar Transaksi")
    user_input = int_input("Pilihan anda: ")

    # load data
    data1 = list(csv.DictReader(open("dataset_gudang.csv")))
    data2 = list(csv.DictReader(open("dataset_transaksi.csv")))

    clearscreen()
    if user_input == 1:
        show(data1)

    elif user_input == 2:
        sell(data1, data2)

    elif user_input == 3:
        service(data2)

    elif user_input == 4:
        buy(data1, data2)   

    elif user_input == 5:
        report(data2)

    elif user_input == 6:
        clear_report(data2)

    elif user_input == 0: 
        print(" Program Berakhir ".center(40, "="))
        break
    
    input("\nTekan [Enter] untuk kembali ke menu utama...")