import ephem
from datetime import datetime, timezone, timedelta
import geocoder

def hitung_hilal(tanggal, lat, lon, elevasi=0, kriteria='mabims'):
    # Set lokasi pengamat
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = elevasi
    observer.date = tanggal

    # Tentukan waktu matahari terbenam (sunset)
    sun = ephem.Sun()
    sun.compute(observer)
    
    # Cari waktu matahari terbenam terdekat
    sunset = observer.next_setting(sun)
    observer.date = sunset
    
    # Hitung posisi bulan dan matahari pada saat sunset
    sun.compute(observer)
    moon = ephem.Moon()
    moon.compute(observer)
    
    # Hitung sudut elongasi (jarak bulan-matahari)
    elongasi = ephem.separation((sun.ra, sun.dec), (moon.ra, moon.dec))
    elongasi_derajat = elongasi * 180 / 3.14159265
    
    # Konversi radian ke derajat
    azimuth_sun = sun.az * 180 / 3.14159265
    altitude_sun = sun.alt * 180 / 3.14159265
    azimuth_moon = moon.az * 180 / 3.14159265
    altitude_moon = moon.alt * 180 / 3.14159265
    
    print(f"Tanggal/Waktu: {sunset}")
    print(f"Lokasi: Latitude {lat}, Longitude {lon}")
    print(f"Ketinggian Matahari: {altitude_sun:.2f}°")
    print(f"Ketinggian Bulan (Hilal): {altitude_moon:.2f}°")
    print(f"Elongasi: {elongasi}")
    print(f"Elongasi: {elongasi * 180 / 3.14159265:.2f}°")
    print("-----------------------------------------------------------------------")
    
    # # Logika sederhana penentuan hilal (contoh: kriteria MABIMS)
    # if altitude_moon > 3 and elongasi * 180 / 3.14159265 > 6.4:
    #     print("Hilal kemungkinan besar terlihat.")
    # else:
    #     print("Hilal kemungkinan tidak terlihat.")

    if kriteria == 'mabims':
        if altitude_moon >= 3 and elongasi * 180 / 3.14159265 >= 6.4:
            print("Hilal kemungkinan besar terlihat (Kriteria MABIMS)")
        elif altitude_moon > 0 and elongasi * 180 / 3.14159265 > 3:
            print("Hilal sulit terlihat, membutuhkan kondisi ideal")
        else:
            print("Hilal tidak terlihat")
    elif kriteria == 'wujudul':
        if altitude_moon > 0 and elongasi * 180 / 3.14159265 > 0:
            print("Hilal terlihat (Kriteria Wujudul Hilal)")
        else:
            print("Hilal tidak terlihat (Kriteria Wujudul Hilal)")
    elif kriteria == 'odeh':
        # Hitung lebar sabit (W) dalam arcmenit
        # W = (ARCL/2) - (ARCL^2 / 7200)
        arcl = elongasi  # elongasi = ARCL
        W = (arcl / 2) - (arcl ** 2 / 7200)

        # ARCV = beda ketinggian bulan dan matahari
        arcv = altitude_moon - altitude_sun

        if altitude_moon > 0:
            if W >= 0.216 and arcv >= 5.65:
                print('Hilal terlihat dengan mata telanjang (Odeh)')
            elif W >= 0.066 and arcv >= 2.0:
                print('Hilal terlihat dengan alat optik (Odeh)')
            else:
                print('Hilal tidak terlihat (Odeh)')
        else:
            print('Hilal di bawah ufuk (Odeh)')


# def get_datetime_wita(timezone_offset):
#     datetime_utc = datetime.now()
#     timezone_wita = timezone(timedelta(hours=timezone_offset))
#     return datetime_utc.astimezone(timezone_wita).strftime('%Y-%m-%d %H:%M:%S %Z')

def location():
    g = geocoder.ip('me')
    return (g.lat, g.lng)

input_kriteria = input("1 : MABIMS (Nahdatul Ulama)" \
"\n2 : Wujudul (Muhammadiyah)" \
"\n3 : Odeh " \
"\nMasukkan kriteria penentuan hilal: "
).strip().lower()

print("-----------------------------------------------------------------------")

input_tanggal = input("Masukkan tanggal (YYYY-MM-DD) atau tekan Enter untuk tanggal hari ini: ").strip()
if input_tanggal:
    try:
        tanggal = datetime.strptime(input_tanggal, '%Y-%m-%d')
    except ValueError:
        print("Format tanggal tidak valid. Menggunakan tanggal hari ini.")
        tanggal = datetime.now()
else:
    tanggal = datetime.now()

if input_kriteria == "1":
    input_kriteria = "mabims"
    print(f"kriteria: {input_kriteria}")
elif input_kriteria == "2":
    input_kriteria = "wujudul"
    print(f"kriteria: {input_kriteria}")
elif input_kriteria == "3":
    input_kriteria = "odeh"
    print(f"kriteria: {input_kriteria}")
else:
    print("ERROR: Kriteria tidak valid, menggunakan default MABIMS (Nahdatul Ulama)")
    input_kriteria = "mabims"

print("-----------------------------------------------------------------------")

hitung_hilal(tanggal, *location(), kriteria=input_kriteria)