import requests
from django.http import JsonResponse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello_visitor(request):
    visitor_name = request.GET.get('visitor_name', 'Mark')
    client_ip = get_client_ip(request)

    ipinfo_token = "fc501babab5244"  # Replace with your actual IPInfo API key
    ipinfo_url = f"http://ipinfo.io/{client_ip}/json?token={ipinfo_token}"

    location_data = requests.get(ipinfo_url).json()
    city = location_data.get('city', 'Unknown')

    weather_api_key = '6db68c32ead55d4834cefefba5f19120'  # Replace with your actual OpenWeatherMap API key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"

    weather_data = requests.get(weather_url).json()
    weather_description = weather_data.get('weather', [{}])[0].get('description', 'No weather information available')
    temperature = weather_data.get('main', {}).get('temp', 'N/A')
    temperature_celsius = temperature - 273.15 if temperature != 'N/A' else 'N/A'

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the teperature is {temperature} degrees celcious in {city}"

    }

    return JsonResponse(response)
