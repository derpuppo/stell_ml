import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# Carga de datos
data = pd.read_csv('stell_metrics_2_window2000ms.csv')  # Asume que los datos están exportados como CSV

filtered_data = data.loc[(data['epc'] != "") & (data['zone'] != "")] # EEA10001, EEA12222, EEA14444

# Características y etiquetas
# freq_count,rssi_count,rssi_max,rssi_min,rssi_spread,rssi_stdev,zone
X_test = filtered_data[['freq_count','rssi_count','rssi_max','rssi_min','rssi_spread','rssi_stdev']]
#X = filtered_data[['freq_count','rssi_count','rssi_max']]
y_test = filtered_data['zone']  # Etiquetas: 'far', 'med', 'near'

scaler = StandardScaler()
#X_train = scaler.fit_transform(X_train)
#X_test = scaler.transform(X_test)

clf = joblib.load('rf_model.pkl')

y_pred = clf.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
