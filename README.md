
Se ha intentando la aproximación ML para la detección de la posición (zonal, 3 zonas) en base a las características extraídas de las lecturas RFID, de 1 y 2 antenas.
```
feature_names = [
    'freq_count_1', 'rssi_count_1', 'rssi_max_1', 'rssi_min_1', 'rssi_spread_1', 'rssi_stdev_1',
    'freq_count_2', 'rssi_count_2', 'rssi_max_2', 'rssi_min_2', 'rssi_spread_2', 'rssi_stdev_2'
]
```
Para 1 antena los resultados son muy pobres (<70% en el entrenamiento + test). Para 2 antenas mejoran (85-90%), pero luego no es muy usable a la hora de obtener resultados dinámicos.

Se ha publicado el modelo, en ml_remote.py, y se invoca periódicamente desde InfluxDB.