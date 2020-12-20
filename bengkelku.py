import os
import csv
import datetime

def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")

def int_input(note):
    try:
        return int(input(note))
    except: 
        return -1

def login():
    clearscreen()
    print(" Login ".center(30, "="))
    USERNAME = input(f"{'Username':12}: ")
    KEY = input(f"{'Password':12}: ")
    if USERNAME != "bang" or KEY != "beng":
        login()

def show():
    clearscreen()
    data = csv.DictReader(open("dataset_gudang.csv"))
    print(" Persediaan ".center(66,"="))
    print(f"| {'No':^5}", end='| ')
    print(f"{'Nama Barang':<25}", end='| ')
    print(f"{'Stok':<10}", end='| ')
    print(f"{'Harga Jual':<17}", end='|\n')
    print("="*66)
    count = 0
    for i in data: 
        count += 1
        print(f"| {(count):^5}", end='| ')
        print(f"{i['Nama Barang']:<25}", end='| ')
        print(f"{i['Stok']:<10}", end='| ')
        print(f"Rp {int(i['Harga Jual']):<14,}", end='|\n')
    print("="*66)

def sell():
    dgudang = list(csv.DictReader(open("dataset_gudang.csv")))
    dtransaksi = list(csv.DictReader(open("dataset_transaksi.csv")))
    user_input = int_input("Pilih |No| produk yang dijual: ")
    if 1 <= user_input <= len(dgudang):
        total_sold = int_input("Jumlah barang yang terjual: ")
        if 1 <= total_sold <= int(dgudang[user_input-1]["Stok"]):
            dgudang[user_input-1]["Stok"] = int(dgudang[user_input-1]["Stok"]) - total_sold
            dtransaksi.append({
            "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
            "Aktivitas":"Penjualan", 
            "Nama Barang": dgudang[user_input-1]["Nama Barang"],
            "Jumlah":total_sold, 
            "Harga": int(dgudang[user_input-1]["Harga Jual"]) * total_sold
            })
            if dgudang[user_input-1]["Stok"] == 0:
                dgudang.pop(user_input-1)

        else:
            print("Jumlah yang dimasukkan tidak sesuai")
    else: 
        print("Nomor yang anda masukkan invalid!")
        return
    write(dgudang, "dataset_gudang.csv")
    write(dtransaksi, "dataset_transaksi.csv")
    clearscreen()
    print("Berhasil Melakukan Pencatatan Penjualan")

def buy():
    dgudang = list(csv.DictReader(open("dataset_gudang.csv")))
    dtransaksi = list(csv.DictReader(open("dataset_transaksi.csv")))
    print("Masukkan [0] untuk menambah produk baru")
    user_input = int_input("Pilih |No| produk yang akan ditambah: ")

    if user_input == 0:
        name = input("Nama barang: ")
        total = int_input("Jumlah barang yang dibeli: ")
        price = int_input("Harga satuan barang ketika dijual: ")
        if total == -1 or price == -1:
            print("Harga yang anda masukkan invalid!")
            return
        dgudang.append({
            "Nama Barang": name, 
            "Stok": total, 
            "Harga Jual": price
            })
        price = int_input("Total harga Pembelian: ")

    elif 0 < user_input < len(dgudang):
        name = dgudang[user_input-1]["Nama Barang"]
        total = int_input("Jumlah barang yang dibeli: ")
        price = int_input("Total harga pembelian: ")

        dgudang[user_input-1]["Stok"] = int(dgudang[user_input-1]["Stok"]) + total
    else: 
        return
    dtransaksi.append({
        "Tanggal": datetime.date.today().strftime("%d-%m-%Y"), 
        "Aktivitas":"Pembelian", 
        "Nama Barang": name,
        "Jumlah":total, 
        "Harga": -price
        })
    write(dgudang, "dataset_gudang.csv")
    write(dtransaksi, "dataset_transaksi.csv")
    clearscreen()
    print("Berhasil Melakukan Pencatatan Pembelian")

def report():
    clearscreen()
    print("Laporan Transaksi".center(100,"="))
    dtransaksi = list(csv.DictReader(open("dataset_transaksi.csv")))
    print(f"| {'No':^5}", end='| ')
    print(f"{'Tanggal':<15}", end='| ')
    print(f"{'Aktivitas':<15}", end='| ')
    print(f"{'Nama Barang':<25}", end='| ')
    print(f"{'Jumlah':<10}", end='| ')
    print(f"{'Harga':<17}",end='|\n')
    print("="*100)
    count = 0
    for i in dtransaksi: 
        count += 1
        print(f"| {(count):^5}", end='| ')
        print(f"{i['Tanggal']:<15}", end='| ')
        print(f"{i['Aktivitas']:<15}", end='| ')
        print(f"{i['Nama Barang']:<25}", end='| ')
        print(f"{i['Jumlah']:<10}", end='| ')
        print(f"Rp {int(i['Harga']):<14,}", end='|\n')
    print("="*100)
    total_price = sum([int(price['Harga']) for price in dtransaksi])
    total_price = "Rp " + "{:,}".format(total_price)
    print(f"|{'Total Transaksi: ':>78}{total_price:^20}", end='|\n')
    print("="*100)

def write(tmp, filename):
    with open(filename, "w") as f:
        dw = csv.DictWriter(f, tmp[0].keys())
        dw.writeheader()
        dw.writerows(tmp)

login()
while True:
    clearscreen()
    print(" Menu ".center(40, "="))
    print("[1] Tampilkan Persediaan")
    print("[2] Catat Penjualan")
    print("[3] Catat Pembelian")
    print("[4] Laporan Keuangan")
    print("[0] Keluar Transaksi")
    user_input = int_input("Pilihan anda: ")
    if user_input == 1:
        show()
    elif user_input == 2:
        show()
        sell()
    elif user_input == 3:
        show()
        buy()      
    elif user_input == 4:
        report()
    elif user_input == 0: 
        print(" Program Berakhir ".center(40, "="))
        break
    input("\nTekan [Enter] untuk kembali ke menu utama...")