import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# Carga de datos
data = pd.read_csv('stell_metrics.csv')  # Asume que los datos están exportados como CSV

filtered_data = data.loc[data['epc'] == "EEA14444"] # EEA10001, EEA12222, EEA14444

# Características y etiquetas
# freq_count,rssi_count,rssi_max,rssi_min,rssi_spread,rssi_stdev,zone
X = filtered_data[['freq_count','rssi_count','rssi_max','rssi_min','rssi_spread','rssi_stdev']]
y = filtered_data['zone']  # Etiquetas: 'cerca', 'media', 'lejos'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
