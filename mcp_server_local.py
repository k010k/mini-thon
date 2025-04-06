from mcp.server.fastmcp import FastMCP
<<<<<<< HEAD
=======
import requests
import os
from dotenv import load_dotenv
>>>>>>> mini

# Initialize FastMCP server with configuration
mcp = FastMCP(
    "Weather",  # Name of the MCP server
<<<<<<< HEAD
    instructions="You are a weather assistant that can answer questions about the weather in a given location.",  # Instructions for the LLM on how to use this tool
=======
    instructions="You are a weather assistant that can provide the current weather based on the user's automatically detected location.",
>>>>>>> mini
    host="0.0.0.0",  # Host address (0.0.0.0 allows connections from any IP)
    port=8005,  # Port number for the server
)

<<<<<<< HEAD

@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get current weather information for the specified location.

    This function simulates a weather service by returning a fixed response.
    In a production environment, this would connect to a real weather API.

    Args:
        location (str): The name of the location (city, region, etc.) to get weather for

    Returns:
        str: A string containing the weather information for the specified location
    """
    # Return a mock weather response
    # In a real implementation, this would call a weather API
    return f"It's always Sunny in {location}"
=======
# --- test_weather.py에서 가져온 함수들 --- START
def get_location():
    """
    IP 기반으로 위치 정보를 가져옵니다.
    https://ipinfo.io/json 을 호출하여 위도와 경도를 추출합니다.
    """
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        data = response.json()
        loc = data.get("loc")
        if loc:
            lat_str, lon_str = loc.split(',')
            return float(lat_str), float(lon_str)
    except Exception as e:
        print("(MCP Server) 위치 정보를 가져오는 중 오류 발생:", e)
    return None, None

def get_weather_data(lat, lon, api_key):
    """
    OpenWeatherMap API를 사용하여 주어진 위도와 경도의 날씨 정보를 가져옵니다.
    'units' 파라미터는 섭씨 온도를 반환하도록 설정합니다.
    """
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"  # 섭씨 온도
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("(MCP Server) 날씨 정보를 가져오는 중 오류 발생:", e)
    return None
# --- test_weather.py에서 가져온 함수들 --- END


@mcp.tool()
def get_weather() -> str:
    """
    Get current weather information based on the user's IP address location.
    Automatically detects location via IP and fetches weather using OpenWeatherMap.

    Returns:
        str: A string containing the current weather information or an error message.
    """
    # .env 파일 로드 (도구 호출 시마다 로드하는 것이 안전할 수 있음)
    load_dotenv()

    lat, lon = get_location()
    if lat is None or lon is None:
        return "위치 정보를 자동으로 가져올 수 없습니다."

    # OpenWeatherMap API 키를 환경 변수에서 불러오기
    api_key = os.getenv("WEATHERMAP_API_KEY") # test_weather.py 와 동일한 변수명 사용
    if not api_key:
        print("(MCP Server) 오류: WEATHERMAP_API_KEY 환경 변수가 설정되지 않았습니다.")
        return "날씨 정보를 가져오기 위한 설정(API 키)이 누락되었습니다."
    
    weather_data = get_weather_data(lat, lon, api_key)
    if weather_data:
        try:
            city = weather_data.get("name", "알 수 없는 도시")
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            return f"{city} 현재 날씨: {description}, 온도: {temperature}°C"
        except (KeyError, IndexError) as e:
            print(f"(MCP Server) 날씨 데이터 파싱 오류: {e}")
            return "날씨 데이터 형식이 예상과 다릅니다."
    else:
        return "날씨 정보를 가져오는 데 실패했습니다."
>>>>>>> mini


if __name__ == "__main__":
    # Start the MCP server with stdio transport
<<<<<<< HEAD
    # stdio transport allows the server to communicate with clients
    # through standard input/output streams, making it suitable for
    # local development and testing
=======
>>>>>>> mini
    mcp.run(transport="stdio")
