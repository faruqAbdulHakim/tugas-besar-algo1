import os
import csv
import datetime

def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")

def int_input(note):
    try:
        x = int(input(note))
        return x
    except: 
        return int_input(note)

def login():
    clearscreen()
    print(" Login ".center(30, "="))
    USERNAME = input(f"{'Username':12}: ")
    KEY = input(f"{'Password':12}: ")
    if USERNAME != "BengkelKu" or KEY != "2021Sukses":
        login()

def show(data1):
    # Print Header tabel
    print(" Persediaan ".center(66,"="))
    print(f"| {'No':^5}", end='| ')
    print(f"{'Nama Barang':<25}", end='| ')
    print(f"{'Stok':<10}", end='| ')
    print(f"{'Harga Jual':<17}", end='|\n')
    print("="*66)
    # Print isi Tabel
    count = 0
    for i in data1: 
        count += 1
        print(f"| {(count):^5}", end='| ')
        print(f"{i['Nama Barang']:<25}", end='| ')
        print(f"{i['Stok']:<10}", end='| ')
        print(f"Rp {int(i['Harga Jual']):<14,}", end='|\n')
    print("="*66)

def sell(data1, data2):

    # Menampilkan persediaan
    show(data1)
    # Memilih barang yang akan dijual
    user_input = int_input("Pilih |No| produk yang dijual: ")

    # Apakah nomor barang yang dimasukkan valid?
    if 1 <= user_input <= len(data1):
        # Jumlah barang yang akan dijual
        total_sold = int_input("Jumlah barang yang terjual: ")
        stock = int(data1[user_input-1]["Stok"])

        # Apakah jumlah barang sesuai dengan stock yang tersedia?
        if 1 <= total_sold <= stock:
            # Menentukan biaya jasa
            services = int_input("Besar biaya jasa: ")
            # Menghitung total biaya
            price = int(data1[user_input-1]["Harga Jual"]) * total_sold + services
            # Mengubah stock persediaan dengan mengurangi jumlah barang yang terjual
            data1[user_input-1]["Stok"] = stock - total_sold

            # Mencatat pada daftar transaksi
            data2.append({
            "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
            "Aktivitas":"Jual", 
            "Nama Barang": data1[user_input-1]["Nama Barang"],
            "Jumlah":total_sold, 
            "Harga": price
            })

            # Menghapus barang di data persediaan jika stock barang habis
            if data1[user_input-1]["Stok"] == 0:
                data1.pop(user_input-1)

    # Keluar jika terdapat input invalid pada inputan nomor / stock barang
        else:
            print("Input Invalid!")
            return
    else: 
        print("Input Invalid!")
        return
    
    # Mencatat ulang pada data gudang dan data transaksi
    write(data1, "dataset_gudang.csv")
    write(data2, "dataset_transaksi.csv")
    print("Berhasil Melakukan Pencatatan Penjualan".center(66, "="))

def buy(data1, data2):
    # Memilih barang yang akan di beli(restock) atau menambahkan barang baru pada daftar
    show(data1)
    user_input = int_input("[0] untuk menambah produk baru\nPilih |No| produk yang akan ditambah: ")

    # Jika menambahkan barang baru
    if user_input == 0:
        name = input("Nama barang: ")
        total = int_input("Jumlah barang yang dibeli: ")
        price = int_input("Harga satuan barang ketika dijual: ")
        # Mencatat pada daftar gudang
        data1.append({
            "Nama Barang": name, 
            "Stok": total, 
            "Harga Jual": price
            })
        # Total biaya yang dikeluarkan
        price = int_input("Total harga Pembelian: ")

    # Jika menambahkan barang yang sudah ada
    elif 0 < user_input <= len(data1):
        name = data1[user_input-1]["Nama Barang"]
        total = int_input("Jumlah barang yang dibeli: ")
        # Total biaya yang dikeluarkan
        price = int_input("Total harga pembelian: ")
        # Menambahkan stock barang
        data1[user_input-1]["Stok"] = int(data1[user_input-1]["Stok"]) + total
    
    # Jika inputan invalid
    else: 
        print("Input Invalid!")
        return
    # Menambahkan data transaksi baru
    data2.append({
        "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
        "Aktivitas":"Beli", 
        "Nama Barang": name,
        "Jumlah":total, 
        "Harga": -price
        })
    # Mencatat ulang pada data gudang dan data transaksi
    write(data1, "dataset_gudang.csv")
    write(data2, "dataset_transaksi.csv")
    print("Berhasil Melakukan Pencatatan Pembelian".center(66, "="))

def report(data2):
    # Print header tabel
    print("Laporan Transaksi".center(100,"="))
    print(f"| {'No':^5}", end='| ')
    print(f"{'Tanggal':<15}", end='| ')
    print(f"{'Aktivitas':<15}", end='| ')
    print(f"{'Nama Barang':<25}", end='| ')
    print(f"{'Jumlah':<10}", end='| ')
    print(f"{'Harga':<17}",end='|\n')
    print("="*100)
    # Print isi tabel
    count = 0
    for i in data2: 
        count += 1
        print(f"| {(count):^5}", end='| ')
        print(f"{i['Tanggal']:<15}", end='| ')
        print(f"{i['Aktivitas']:<15}", end='| ')
        print(f"{i['Nama Barang']:<25}", end='| ')
        print(f"{i['Jumlah']:<10}", end='| ')
        print(f"Rp {int(i['Harga']):<14,}", end='|\n')
    print("="*100)
    total_price = sum([int(price['Harga']) for price in data2])
    total_price = "Rp " + "{:,}".format(total_price)
    print(f"|{'Total Transaksi: ':>78}{total_price:^20}", end='|\n')
    print("="*100)

def clear_report(data2):
    report(data2)
    isContinue = input("Apakah anda yakin ingin menghapus laporan keuangan? (y/t)").lower()
    # Memutuskan apakah akan menghapus data?
    if isContinue != 'y' and isContinue != 't':
        clearscreen()
        clear_report(data2)
    elif isContinue == 'y':
        date_now = datetime.date.today().strftime('%d %B %Y')
        file_loc = "backups/" + str(date_now)+'.csv'
        try:
            write(data2, file_loc)
            print("Lokasi Backup Data: ", file_loc)
        except:
            print("Data Transaksi Kosong!")
        with open("dataset_transaksi.csv", "w") as f:
            f.write("Tanggal,Aktivitas,Nama Barang,Jumlah,Harga")

def write(tmp, filename):
    with open(filename, "w") as f:
        dw = csv.DictWriter(f, tmp[0].keys())
        dw.writeheader()
        dw.writerows(tmp)

# login()
while True:
    clearscreen()
    print(" Menu ".center(40, "="))
    print("[1] Tampilkan Persediaan")
    print("[2] Catat Penjualan")
    print("[3] Catat Pembelian")
    print("[4] Laporan Keuangan")
    print("[5] Bersihkan Laporan Keuangan")
    print("[0] Keluar Transaksi")
    user_input = int_input("Pilihan anda: ")

    clearscreen()
    data1 = list(csv.DictReader(open("dataset_gudang.csv")))
    data2 = list(csv.DictReader(open("dataset_transaksi.csv")))

    if user_input == 1:
        show(data1)

    elif user_input == 2:
        sell(data1, data2)

    elif user_input == 3:
        buy(data1, data2)   

    elif user_input == 4:
        report(data2)

    elif user_input == 5:
        clear_report(data2)

    elif user_input == 0: 
        print(" Program Berakhir ".center(40, "="))
        break
    
    input("\nTekan [Enter] untuk kembali ke menu utama...")