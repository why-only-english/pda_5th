import requests
import time
from bs4 import BeautifulSoup
import numpy as np
import requests
import time
import psutil
import math 
import os

"""
종목 10개 현재 주가 크롤링하는 
걸리는 평균 시간 
"""
stock_urls = "https://m.stock.naver.com/worldstock/stock/AAPL.O/total"   # 애플
times = []

def crawl_stock_price(url):
    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    end_time = time.time()
    elapsed_time = end_time - start_time
    times.append(elapsed_time)

for _ in range(1000):
    crawl_stock_price(stock_urls)

average_time = sum(times) / len(times)
print(f"\n10개의 종목에 대한 평균 크롤링 시간: {average_time:.5f} 초")

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

# 파일 삭제
if os.path.exists(file_path):
    os.remove(file_path)

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

for i in range(100):
    for user in users:
        fetch_github_user_data(user)

# 평균 요청 시간 계산
average_time = sum(times) / 1000
print(f"10명의 사용자에 대한 평균 요청 시간: {average_time:.5f} 초")

