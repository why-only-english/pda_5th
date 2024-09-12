import requests
import time
from bs4 import BeautifulSoup
import numpy as np
import requests
import time
import psutil
import math 

"""
종목 10개 현재 주가 크롤링하는 
걸리는 평균 시간 
"""
stock_urls = [
    "https://m.stock.naver.com/worldstock/stock/AAPL.O/total",   # 애플
    "https://m.stock.naver.com/worldstock/stock/GOOGL.O/total",  # 구글
    "https://m.stock.naver.com/worldstock/stock/AMZN.O/total",   # 아마존
    "https://m.stock.naver.com/worldstock/stock/MSFT.O/total",   # 마이크로소프트
    "https://m.stock.naver.com/worldstock/stock/TSLA.O/total",   # 테슬라
    "https://m.stock.naver.com/worldstock/stock/FB.O/total",     # 페이스북 (메타)
    "https://m.stock.naver.com/worldstock/stock/NFLX.O/total",   # 넷플릭스
    "https://m.stock.naver.com/worldstock/stock/NVDA.O/total",   # 엔비디아
    "https://m.stock.naver.com/worldstock/stock/BRK.B/total",    # 버크셔 해서웨이
    "https://m.stock.naver.com/worldstock/stock/V.O/total"       # 비자
]
times = []

def crawl_stock_price(url):
    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    end_time = time.time()
    elapsed_time = end_time - start_time
    times.append(elapsed_time)

for url in stock_urls:
    crawl_stock_price(url)

average_time = sum(times) / len(times)
print(f"\n10개의 종목에 대한 평균 크롤링 시간: {average_time:.5f} 초")

"""
10만까지의 소수를 찾는 함수 
cpu 점유율과 소요시간 
"""
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# 주어진 범위에서 소수 찾는 함수
def find_primes(limit):
    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes

# CPU 사용량 측정 함수
def monitor_cpu_usage(interval=0.1):
    cpu_usage = psutil.cpu_percent(interval=interval)
    return cpu_usage

# 소수 판별을 하면서 최대 CPU 점유율 추적
def start(limit):
    max_cpu_usage = 0
    start_time = time.time()
    
    # 소수 판별 수행
    for i in range(0, limit, 1000):  # 범위를 나눠서 CPU 사용량을 모니터링
        find_primes(i + 1000)  # 1000 단위로 소수 판별 수행
        cpu_usage = monitor_cpu_usage()  # CPU 사용량 측정
        max_cpu_usage = max(max_cpu_usage, cpu_usage)
    
    end_time = time.time()
    print(f"소수찾기 최대 CPU 사용량: {max_cpu_usage:.2f}%")
    print(f"소요 시간: {end_time - start_time:.2f} 초")

primes = start(100000)

"""
대량의 문자열을 파일로 저장하는데 걸리는 시간 
디스크 쓰기 속도 비교 
"""
file_path = "large_file.txt"
large_text = "This is a test string.\n" * 10000000  # 대량의 문자열 생성

start_time = time.time()

# 파일에 대량의 문자열을 저장
with open(file_path, "w") as file:
    file.write(large_text)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"대량의 문자열을 파일에 저장하는데 걸린 시간: {elapsed_time:.5f} 초")

size = 100_000_000  # 1억 개의 float 값을 할당

start_time = time.time()

# Numpy 배열에 값을 쓰는 작업 (메모리 할당)
array = np.ones(size, dtype=np.float64)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Numpy로 배열에 값을 쓰는 작업에 걸린 시간: {elapsed_time:.5f} 초")

"""
github api로 request를 보내서 결과 받는데 평균 걸리는시간 
네트워크 성능 비교 
"""
# 요청할 GitHub 사용자 목록
users = [
    "qpwisu", "torvalds", "mojombo", "defunkt", "pjhyett",
    "wycats", "ezmobius", "ivey", "evanphx", "vanpelt"
]

# 요청 시간 기록을 위한 리스트
times = []

# GitHub API 요청 함수
def fetch_github_user_data(username):
    url = f"https://api.github.com/users/{username}"
    start_time = time.time()
    
    # API 요청
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    times.append(elapsed_time)

# 여러 사용자에 대한 요청 수행
for user in users:
    fetch_github_user_data(user)

# 평균 요청 시간 계산
average_time = sum(times) / len(times)
print(f"\n10명의 사용자에 대한 평균 요청 시간: {average_time:.5f} 초")
