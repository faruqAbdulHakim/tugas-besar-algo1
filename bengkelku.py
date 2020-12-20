import os
import csv

def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")
def login():
    clearscreen()
    USERNAME = input(f"{'Username':12}: ")
    KEY = input(f"{'Password':12}: ")
    if USERNAME != "bang" or KEY != "beng":
        login()
def int_input(note):
    try:
        return int(input(note))
    except: 
        return -1

def show():
    clearscreen()
    data = csv.DictReader(open("dataset_gudang.csv"))
    print(" Persediaan ".center(66,"="))
    print(f"| {'No':^5}", end='| ')
    print(f"{'Nama Barang':<25}", end='| ')
    print(f"{'Stok':<10}", end='| ')
    print(f"{'Harga Satuan':<17}", end='|\n')
    print("="*66)
    count = 0
    for i in data: 
        count += 1
        print(f"| {(count):^5}", end='| ')
        print(f"{i['Nama Barang']:<25}", end='| ')
        print(f"{i['Stok']:<10}", end='| ')
        print(f"Rp {int(i['Harga Satuan']):<14,}", end='|\n')
    print("="*66)

def sell():
    data = list(csv.DictReader(open("dataset_gudang.csv")))
    user_input = int_input("Pilih |No| produk yang dijual: ")
    if 1 <= user_input <= len(data):
        total_sold = int_input("Jumlah barang yang terjual: ")
        if 1 <= total_sold <= int(data[user_input-1]["Stok"]):
            data[user_input-1]["Stok"] = int(data[user_input-1]["Stok"]) - total_sold
            write(data, "dataset_gudang.csv")
        else:
            print("Jumlah yang dimasukkan tidak sesuai")
    else: 
        print("Barang belum tersedia")

def buy():
    data = list(csv.DictReader(open("dataset_gudang.csv")))
    print("Masukkan [0] untuk menambah produk baru")
    user_input = int_input("Pilih |No| produk yang akan ditambah: ")
    if user_input == 0:
        name = input("Masukkan nama barang: ")
        total_buy = input("Masukkan jumlah barang yang dibeli: ")
        price = int_input("Masukkan harga satuan barang: ")
        tmp_dict = {"Nama Barang": name, "Stok": total_buy, "Harga Satuan":price}
        data.append(tmp_dict)
    elif 0 < user_input < len(data):
        total_buy = int_input("Masukkan jumlah barang yang dibeli: ")
        price = int_input("Masukkan total harga satuan barang: ")
        data[user_input-1]["Stok"] = int(data[user_input-1]["Stok"]) + total_buy
    write(data, "dataset_gudang.csv")

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
    print("[0] Keluar Program")
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
        pass
    elif user_input == 0: 
        print(" Program Berakhir ".center(40, "="))
        break
    input("\nTekan [Enter] untuk kembali ke menu utama...")