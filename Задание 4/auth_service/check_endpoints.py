import requests

BASE_URL = "http://localhost:8000"

def check_endpoints():
    print("Проверяем доступность эндпоинтов...")
    
    endpoints = [
        "/",
        "/docs",
        "/redoc",
        "/auth/register",
        "/auth/login", 
        "/auth/refresh",
        "/auth/logout",
        "/user/me",
        "/user/history",
        "/user/update"
    ]
    
    for endpoint in endpoints:
        try:
            if endpoint == "/":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            print(f"{endpoint}: {response.status_code}")
            
        except Exception as e:
            print(f"{endpoint}: ERROR - {e}")

def check_openapi_schema():
    print("\nПроверяем OpenAPI схему...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            paths = list(schema.get("paths", {}).keys())
            print("Доступные пути в OpenAPI:")
            for path in sorted(paths):
                print(f"  {path}")
        else:
            print(f"OpenAPI схема недоступна: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при получении OpenAPI схемы: {e}")

if __name__ == "__main__":
    check_endpoints()
    check_openapi_schema()