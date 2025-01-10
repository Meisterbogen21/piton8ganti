import csv
from datetime import datetime
import os
import streamlit as st

class RentalService:
    def __init__(self):
        self.rental_file = os.path.join(os.path.dirname(__file__), "mobil_dipakai.csv")
        self.available_file = os.path.join(os.path.dirname(__file__), "mobil_tersedia.csv")
        self.rented_cars = []
        self.available_cars = []
        self.load_rented_cars()
        self.load_available_cars()

    def load_rented_cars(self):
        """Memuat data mobil yang sedang dipakai dari file CSV."""
        try:
            with open(self.rental_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Lewati header jika ada
                for row in reader:
                    car_data = {
                        "car_name": row[0],
                        "plate_number": row[1],
                        "renter_name": row[2],
                        "start_date": datetime.strptime(row[3], '%Y-%m-%d'),
                        "end_date": datetime.strptime(row[4], '%Y-%m-%d')
                    }
                    self.rented_cars.append(car_data)
        except FileNotFoundError:
            st.error("File rental tidak ditemukan. Memulai dengan data kosong.")

    def load_available_cars(self):
        """Memuat data mobil yang tersedia dari file CSV."""
        try:
            with open(self.available_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Lewati header jika ada
                for row in reader:
                    car_data = {
                        "car_name": row[0],
                        "plate_number": row[1],
                        "status": row[2]
                    }
                    if car_data["status"].lower() == "tersedia":
                        self.available_cars.append(car_data)
        except FileNotFoundError:
            st.error("File ketersediaan mobil tidak ditemukan. Memulai dengan data kosong.")

    def display_rented_cars(self):
        """Menampilkan data mobil yang sedang dipakai."""
        st.subheader("Mobil yang sedang dipakai:")
        for car in self.rented_cars:
            st.write(f"{car['car_name']} ({car['plate_number']}) - {car['renter_name']} dari {car['start_date'].strftime('%Y-%m-%d')} sampai {car['end_date'].strftime('%Y-%m-%d')}")

    def display_available_cars(self):
        """Menampilkan mobil yang tersedia."""
        st.subheader("Mobil yang tersedia:")
        for car in self.available_cars:
            st.write(f"{car['car_name']} ({car['plate_number']}) - Status: {car['status']}")

    def replace_car(self):
        """Menggantikan mobil dari daftar tersedia."""
        if not self.available_cars:
            st.warning("Maaf, tidak ada mobil pengganti yang tersedia.")
            return None

        replacement_car = self.available_cars.pop(0)
        st.success(f"Mobil pengganti: {replacement_car['car_name']} ({replacement_car['plate_number']})")
        return replacement_car

    def return_car(self, car_name, plate_number):
        """Mengembalikan mobil ke daftar mobil yang tersedia."""
        returned_car = {
            "car_name": car_name,
            "plate_number": plate_number,
            "status": "Tersedia"
        }
        self.available_cars.append(returned_car)
        st.info(f"Mobil {car_name} ({plate_number}) telah dikembalikan dan tersedia kembali untuk disewa.")

# Streamlit Interface
if __name__ == "__main__":
    st.title("Rental Service Management")

    rental_service = RentalService()

    st.sidebar.header("Menu")
    option = st.sidebar.radio("Pilih opsi:", ["Tampilkan Mobil", "Ganti Mobil", "Kembalikan Mobil"])

    if option == "Tampilkan Mobil":
        rental_service.display_rented_cars()
        rental_service.display_available_cars()

    elif option == "Ganti Mobil":
        if st.button("Ganti Mobil"):
            rental_service.replace_car()
        rental_service.display_available_cars()

    elif option == "Kembalikan Mobil":
        car_name = st.text_input("Nama Mobil yang Dikembalikan:")
        plate_number = st.text_input("Nomor Polisi:")
        if st.button("Kembalikan Mobil"):
            rental_service.return_car(car_name, plate_number)
        rental_service.display_available_cars()
