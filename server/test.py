import requests

def fetch_data_from_api(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")

def get_all_data(api_url="https://cyan.io.vn/xg79/get_data_1.php"):
    all_data = []
    params = {'page': 1, 'limit': 1000}  # page = 1, limit = 100 rows per page
    while True:
        data = fetch_data_from_api(api_url, params)
        if not data:  # Nếu không còn dữ liệu
            break
        all_data.extend(data)
        params['page'] += 1  # Tiến sang trang tiếp theo
    return all_data


all_data = get_all_data()

