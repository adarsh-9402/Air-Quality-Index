from flask import Flask, request, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# Load and preprocess the dataset
df = pd.read_csv(r'city_data.csv')  # File should be in the same directory or update the path
df = df.dropna(subset=['PM2.5', 'PM10', 'NO2', 'AQI_Bucket'])

label_encoder = LabelEncoder()
df['AQI_Label'] = label_encoder.fit_transform(df['AQI_Bucket'])

X = df[['PM2.5', 'PM10', 'NO2']]
y = df['AQI_Label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Flask App Setup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            pm25 = float(request.form['pm25'])
            pm10 = float(request.form['pm10'])
            no2 = float(request.form['no2'])

            input_data = scaler.transform([[pm25, pm10, no2]])
            pred = knn.predict(input_data)
            prediction = label_encoder.inverse_transform(pred)[0]

        except ValueError:
            prediction = "Invalid input. Please enter numeric values."

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
