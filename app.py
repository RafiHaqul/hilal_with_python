from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ephem
from datetime import datetime, timezone, timedelta
import math
import os

app = Flask(__name__, static_folder='static')
CORS(app)

def hitung_hilal(tanggal_str, lat, lon, elevasi=0, kriteria='mabims'):
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = float(elevasi)

    date_obj = datetime.strptime(tanggal_str, '%Y-%m-%d')
    observer.date = date_obj

    sun = ephem.Sun()
    sun.compute(observer)

    # Cari waktu matahari terbenam
    sunset = observer.next_setting(sun)
    observer.date = sunset

    # Hitung posisi bulan dan matahari pada saat sunset
    sun.compute(observer)
    moon = ephem.Moon()
    moon.compute(observer)

    # Elongasi (jarak sudut bulan-matahari)
    elongasi_rad = ephem.separation((sun.ra, sun.dec), (moon.ra, moon.dec))
    elongasi_deg = float(elongasi_rad) * 180 / math.pi

    azimuth_sun  = float(sun.az)  * 180 / math.pi
    altitude_sun = float(sun.alt) * 180 / math.pi
    azimuth_moon  = float(moon.az)  * 180 / math.pi
    altitude_moon = float(moon.alt) * 180 / math.pi
    illuminasi    = float(moon.phase)

    # Umur bulan sejak konjungsi (new moon)
    prev_new = ephem.previous_new_moon(sunset)
    umur_bulan_jam = (float(sunset) - float(prev_new)) * 24

    arcv = altitude_moon - altitude_sun

    # --- Penentuan berdasarkan kriteria ---
    if kriteria == 'mabims':
        if altitude_moon >= 3 and elongasi_deg >= 6.4:
            verdict = 'terlihat'
            keterangan = 'Hilal kemungkinan besar terlihat (Kriteria MABIMS)'
        elif altitude_moon >= 0 and elongasi_deg >= 3:
            verdict = 'mungkin'
            keterangan = 'Hilal sulit terlihat, membutuhkan kondisi ideal'
        else:
            verdict = 'tidak'
            keterangan = 'Hilal tidak terlihat'

    elif kriteria == 'wujudul':
        if altitude_moon >= 0 and elongasi_deg >= 0:
            verdict = 'terlihat'
            keterangan = 'Hilal wujud di atas ufuk (Kriteria Wujudul Hilal)'
        else:
            verdict = 'tidak'
            keterangan = 'Hilal tidak wujud (di bawah ufuk)'

    elif kriteria == 'odeh':
        # Hitung lebar sabit (W) dalam arcmenit
        # W = (ARCL/2) - (ARCL^2 / 7200)
        arcl = elongasi_deg  # elongasi = ARCL
        W = (arcl / 2) - (arcl ** 2 / 7200)

        # ARCV = beda ketinggian bulan dan matahari
        arcv = altitude_moon - altitude_sun

        if altitude_moon > 0:
            if W >= 0.216 and arcv >= 5.65:
                verdict = 'terlihat'
                keterangan = f'Hilal terlihat dengan mata telanjang (Odeh) — W={W:.3f}\', ARCV={arcv:.2f}°'
            elif W >= 0.066 and arcv >= 2.0:
                verdict = 'mungkin'
                keterangan = f'Hilal terlihat dengan alat optik (Odeh) — W={W:.3f}\', ARCV={arcv:.2f}°'
            else:
                verdict = 'tidak'
                keterangan = f'Hilal tidak terlihat (Odeh) — W={W:.3f}\', ARCV={arcv:.2f}°'
        else:
            verdict = 'tidak'
            keterangan = 'Hilal di bawah ufuk (Odeh)'

    # Konversi waktu sunset ke string UTC
    sunset_dt = ephem.Date(sunset).datetime()
    sunset_utc_str = sunset_dt.strftime('%Y-%m-%d %H:%M:%S UTC')

    return {
        'sunset_utc': sunset_utc_str,
        'lat': lat,
        'lon': lon,
        'elevasi': elevasi,
        'altitude_sun': round(altitude_sun, 4),
        'altitude_moon': round(altitude_moon, 4),
        'azimuth_sun': round(azimuth_sun, 4),
        'azimuth_moon': round(azimuth_moon, 4),
        'elongasi': round(elongasi_deg, 4),
        'arcv': round(arcv, 4),
        'lebar_sabit_W': round(W, 4) if kriteria == 'odeh' else None,
        'illuminasi': round(illuminasi, 2),
        'umur_bulan_jam': round(umur_bulan_jam, 2),
        'verdict': verdict,
        'keterangan': keterangan,
        'kriteria': kriteria,
    }


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/hilal', methods=['POST'])
def api_hilal():
    try:
        data = request.get_json()

        tanggal  = data.get('tanggal')
        lat      = float(data.get('lat'))
        lon      = float(data.get('lon'))
        elevasi  = float(data.get('elevasi', 0))
        kriteria = data.get('kriteria', 'mabims')

        if not tanggal:
            return jsonify({'error': 'Parameter tanggal wajib diisi'}), 400

        result = hitung_hilal(tanggal, lat, lon, elevasi, kriteria)
        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': f'Nilai tidak valid: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    print("Jalankan: python app.py")
    app.run(host='0.0.0.0', debug=True, port=5000)