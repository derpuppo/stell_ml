import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Carga de datos
data = pd.read_csv('stell_metrics_2_window2000ms.csv')  # Asume que los datos están exportados como CSV

filtered_data = data.loc[(data['epc'] != "") & (data['zone'] != "")] # EEA10001, EEA12222, EEA14444

# Características y etiquetas
# freq_count,rssi_count,rssi_max,rssi_min,rssi_spread,rssi_stdev,zone
#X = filtered_data[['freq_count','rssi_count','rssi_max','rssi_min','rssi_spread','rssi_stdev']]
X = filtered_data[['freq_count','rssi_count','rssi_max']]
y = filtered_data['zone']  # Etiquetas: 'far', 'med', 'near'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# SVM
# svm_model = SVC(kernel='rbf', random_state=42)  # Cambia el kernel si deseas probar otros (e.g., 'linear')
# svm_model.fit(X_train, y_train)
# y_pred_svm = svm_model.predict(X_test)

# print("Resultados con SVM:")
# print(f'Exactitud: {accuracy_score(y_test, y_pred_svm):.2f}')
# print('Matriz de confusión:')
# print(confusion_matrix(y_test, y_pred_svm))
# print('Reporte de clasificación:')
# print(classification_report(y_test, y_pred_svm))

# Gradient Boosting
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

print("\nResultados con Gradient Boosting:")
print(f'Exactitud: {accuracy_score(y_test, y_pred_gb):.2f}')
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred_gb))
print('Reporte de clasificación:')
print(classification_report(y_test, y_pred_gb))
