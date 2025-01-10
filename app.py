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
                        "car_type": row[1],
                        "plate_number": row[2],
                        "renter_name": row[3],
                        "start_date": datetime.strptime(row[4], '%Y-%m-%d'),
                        "end_date": datetime.strptime(row[5], '%Y-%m-%d')
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
                        "car_type": row[1],
                        "plate_number": row[2],
                        "status": row[3]
                    }
                    if car_data["status"].lower() == "tersedia":
                        self.available_cars.append(car_data)
        except FileNotFoundError:
            st.error("File ketersediaan mobil tidak ditemukan. Memulai dengan data kosong.")

    def save_rented_cars(self):
        """Menyimpan data mobil yang sedang dipakai ke file CSV."""
        with open(self.rental_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Jenis Mobil", "Tipe Mobil", "Nomor Polisi", "Penyewa", "Tanggal Sewa", "Tanggal Kembali"])
            for car in self.rented_cars:
                writer.writerow([
                    car["car_name"],
                    car["car_type"],
                    car["plate_number"],
                    car["renter_name"],
                    car["start_date"].strftime('%Y-%m-%d'),
                    car["end_date"].strftime('%Y-%m-%d')
                ])

    def save_available_cars(self):
        """Menyimpan data mobil yang tersedia ke file CSV."""
        with open(self.available_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Jenis Mobil", "Tipe Mobil", "Nomor Polisi", "Status"])
            for car in self.available_cars:
                writer.writerow([car["car_name"], car["car_type"], car["plate_number"], car["status"]])

    def display_rented_cars(self):
        """Menampilkan data mobil yang sedang dipakai."""
        st.subheader("Mobil yang sedang dipakai:")
        for car in self.rented_cars:
            st.write(f"{car['car_name']} ({car['plate_number']}) - {car['renter_name']} dari {car['start_date'].strftime('%Y-%m-%d')} sampai {car['end_date'].strftime('%Y-%m-%d')} - Tipe: {car['car_type']}")

    def display_available_cars(self):
        """Menampilkan mobil yang tersedia."""
        st.subheader("Mobil yang tersedia:")
        for car in self.available_cars:
            st.write(f"{car['car_name']} ({car['plate_number']}) - Status: {car['status']} - Tipe: {car['car_type']}")

    def replace_car(self, rented_plate, replacement_plate):
        """Menggantikan mobil yang disewa dengan mobil pengganti."""
        rented_car = next((car for car in self.rented_cars if car["plate_number"] == rented_plate), None)
        replacement_car = next((car for car in self.available_cars if car["plate_number"] == replacement_plate), None)

        if not rented_car:
            st.error("Mobil yang ingin diganti tidak ditemukan.")
            return

        if not replacement_car:
            st.error("Mobil pengganti tidak tersedia.")
            return

        # Lakukan penggantian
        self.available_cars.remove(replacement_car)
        self.available_cars.append({
            "car_name": rented_car["car_name"],
            "car_type": rented_car["car_type"],
            "plate_number": rented_car["plate_number"],
            "status": "Rusak/Mekanik"
        })
        rented_car["car_name"] = replacement_car["car_name"]
        rented_car["car_type"] = replacement_car["car_type"]
        rented_car["plate_number"] = replacement_car["plate_number"]

        self.save_rented_cars()
        self.save_available_cars()

        st.success(f"Mobil {rented_car['car_name']} ({rented_car['plate_number']}) telah diganti dengan {replacement_car['car_name']} ({replacement_car['plate_number']}).")

# Streamlit Interface
if __name__ == "__main__":
    st.title("Rental Service Management")

    rental_service = RentalService()

    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Pilih menu:", ["Tampilkan Mobil", "Ganti Mobil"])

    if menu == "Tampilkan Mobil":
        rental_service.display_rented_cars()
        rental_service.display_available_cars()

    elif menu == "Ganti Mobil":
        rental_service.display_rented_cars()
        rental_service.display_available_cars()

        rented_plate = st.selectbox("Pilih nomor polisi mobil yang ingin diganti:", [car["plate_number"] for car in rental_service.rented_cars])
        rented_car_type = next((car["car_type"] for car in rental_service.rented_cars if car["plate_number"] == rented_plate), None)

        available_replacements = [car["plate_number"] for car in rental_service.available_cars if car["car_type"] == rented_car_type]

        replacement_plate = st.selectbox("Pilih nomor polisi mobil pengganti:", available_replacements)

        if st.button("Ganti Mobil"):
            rental_service.replace_car(rented_plate, replacement_plate)
