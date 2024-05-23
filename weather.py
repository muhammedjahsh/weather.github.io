import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

API_key = '2be5ba57c13d6ec3e83d3fbd47d90d46'






def convert_temperature(temperature, unit):
    if unit == 'Celsius':
        return round(temperature - 273.15, 2)
    elif unit == 'Fahrenheit':
        return round((temperature - 273.15) * 9/5 + 32, 2)
    else:
        return temperature


def find_current_weather(city):
    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
    weather_data = requests.get(base_url).json()

    try:
        general = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        icon_id = weather_data['weather'][0]['icon']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        icon = f'https://openweathermap.org/img/wn/{icon_id}@2x.png'
        coordinates = (weather_data['coord']['lat'], weather_data['coord']['lon'])
    except KeyError:
        st.error('City not found')
        st.stop()

    return general, description, temperature, humidity, wind_speed, icon, coordinates

def display_satellite_image(coordinates):
    st.subheader('Satellite Image')

    # Create a Folium Map centered around the specified coordinates
    my_map = folium.Map(location=coordinates, zoom_start=10)

    # Add a marker at the specified coordinates
    folium.Marker(location=coordinates, popup='City').add_to(my_map)

    # Display the Folium Map using streamlit
    folium_static(my_map)

def main():
    
    

    st.header('CIty v/s Weather condition')
    city = st.text_input('Enter the city name').lower()
    temperature_unit = st.radio('Select Temperature Unit:', ('Celsius', 'Fahrenheit'))


    if st.button('Find'):
        general, description, temperature, humidity, wind_speed, icon, coordinates = find_current_weather(city)

        col_1, col_2 = st.columns(2)
        with col_1:
            st.metric(label='Temperature', value=f'{convert_temperature(temperature, temperature_unit)}°{temperature_unit[0]}')
            st.metric(label='Humidity', value=f'{humidity}%')
            
        with col_2:
            st.write(f'{general}, {description}')
            st.metric(label='Wind Speed', value=f'{wind_speed} m/s')
            st.image(icon, caption='Weather Icon', use_column_width=True)
            
        display_satellite_image(coordinates)
            

if __name__ == '__main__':
    main()
