import csv
from datetime import datetime, timedelta

def get_prayer_times():
    prayer_times = {}
    current_date = datetime.now().strftime('%Y-%m-%d')
    iqama_file = '/config/iqama.csv'
    csv_file = f"/config/{datetime.now().strftime('%m')}.csv"

    # Charger les horaires de prière pour aujourd'hui
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['date'] = datetime.now().strftime('%Y-') + row['date']
                if row['date'] == current_date:
                    prayer_times = {
                        'Fajr': row['Fajr'],
                        'Dhuhr': row['Dhuhr'],
                        'Asr': row['Asr'],
                        'Maghrib': row['Maghrib'],
                        'Isha': row['Isha'],
                    }
                    if 'Shurouq' in row:
                        prayer_times['Shurouq'] = row['Shurouq']
                    break
    except FileNotFoundError:
        print(f"File not found: {csv_file}")

    # Charger les délais d'Iqama pour chaque prière
    iqama_offsets = {}
    try:
        with open(iqama_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Ignorer l'en-tête
            for row in reader:
                iqama_offsets = {
                    'Fajr': int(row[0]),
                    'Dhuhr': int(row[1]),
                    'Asr': int(row[2]),
                    'Maghrib': int(row[3]),
                    'Isha': int(row[4])
                }
                break
    except FileNotFoundError:
        print(f"File not found: {iqama_file}")
    
    # Calculer les heures de Iqama en ajoutant les offsets
    for prayer, time_str in prayer_times.items():
        prayer_time = datetime.strptime(time_str, '%H:%M')
        if prayer in iqama_offsets:
            iqama_time = prayer_time + timedelta(minutes=iqama_offsets[prayer])
            prayer_times[f"{prayer}_Iqama"] = iqama_time.strftime('%H:%M')
    
    # Ajouter l'heure de vendredi si disponible
    try:
        with open('/config/vendredi.csv', mode='r') as file:
            friday_time = file.readline().strip()
            if friday_time:
                prayer_times['Vendredi'] = friday_time
    except FileNotFoundError:
        print("File not found: /config/vendredi.csv")

    return prayer_times
