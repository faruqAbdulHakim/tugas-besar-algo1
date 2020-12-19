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

# login()
while True:
    clearscreen()
    print(" Menu ".center(40, "="))
    print("[1] Tampilkan Persediaan")
    print("[2]")
    print("[3]")
    print("[4]")
    print("[ ] Keluar Program")
    user_input = input("Pilihan anda: ")
    if user_input == '1':
        show()
        input("\nTekan [Enter] untuk kembali ke menu utama...")
    elif user_input == '2':
        pass
    elif user_input == '3':
        pass
    elif user_input == '4':
        pass
    else: 
        print(" Program Berakhir ".center(40, "="))
        break