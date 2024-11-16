from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

class WeatherData:
    def __init__(self, city, temperature, humidity, description):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.description = description

    def display_info(self):
        return (f"City: {self.city}<br>"
                f"Temperature: {self.temperature}°C<br>"
                f"Humidity: {self.humidity}%<br>"
                f"Weather: {self.description}")

def fetch_weather_data(city):
    api_key = "register with Open Weather Map Services and insert you API here"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    weather = WeatherData(
        city=data['name'],
        temperature=data['main']['temp'],
        humidity=data['main']['humidity'],
        description=data['weather'][0]['description']
    )
    return weather

@app.route('/', methods=['GET', 'POST'])
def index():
    city_name = request.form.get('city', 'Cape Town') if request.method == 'POST' else 'Cape Town'
    weather_info = fetch_weather_data(city_name)
    return render_template_string(f"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
        </head>
        <body>
            <h1>Weather Information</h1>
            <form method="post">
                <input type="text" name="city" placeholder="Enter city name">
                <button type="submit">Get Weather</button>
            </form>
            <div class="weather-info">
                <p>{weather_info.display_info()}</p>
            </div>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
