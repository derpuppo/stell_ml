import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# Carga de datos
data = pd.read_csv('stell_metrics_2ant_0_window2000ms.csv')  # Asume que los datos están exportados como CSV

filtered_data = data.loc[(data['epc'] == "EEA15555") & (data['zone_1'] != "")] # EEA10001, EEA12222, EEA14444

# Características y etiquetas
feature_names = [
    'freq_count_1', 'rssi_count_1', 'rssi_max_1', 'rssi_min_1', 'rssi_spread_1', 'rssi_stdev_1',
    'freq_count_2', 'rssi_count_2', 'rssi_max_2', 'rssi_min_2', 'rssi_spread_2', 'rssi_stdev_2'
]
X = filtered_data[feature_names]
y = filtered_data['zone_1']  # Etiquetas: 'far', 'med', 'near'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
#X_train = scaler.fit_transform(X_train)
#X_test = scaler.transform(X_test)

clf = RandomForestClassifier(n_estimators=100, random_state=42)

#scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
#print("Puntajes en cada fold:", scores)
#print("Rendimiento promedio:", scores.mean())
#print("Desviación estándar:", scores.std())

clf.fit(X_train, y_train)

# Predicción de probabilidades
probas = clf.predict_proba(X_test)

# Mostrar probabilidades para las primeras 5 predicciones
#print("Probabilidades para cada clase (primeras 5 muestras):")
#print([(real, prob) for real, prob in zip(y_test.iloc[:5], probas[:5])])

# Predicción y su confianza máxima
y_pred = clf.predict(X_test)
confidences = probas.max(axis=1)
print("Predicción y confianza (primeras 5 muestras):")
for real, pred, conf in zip(y_test.iloc, y_pred, confidences):
    print(f"Predicción: {pred}, Confianza: {conf:.2f}, Real: {real}")

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 5. Obtener la importancia de las características
feature_importances = clf.feature_importances_
feature_names = X.columns

# 6. Mostrar las importancias
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

print(importance_df)

joblib.dump(clf, 'rf_model.pkl')