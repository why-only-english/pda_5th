# EC2 벤치마크 결과보고서

### EC2 인스턴스 종류별 벤치마크 분석

팀 장투 (장우진, 장성준)

### 목적

다양한 프로그램 환경에서, EC2의 Instance Family, 제조사 별로 어떠한 인스턴스 성능 차이가 나는지 분석하고 우리가 사용할 실제 프로젝트 환경에서 어떤 인스턴스를 사용하는것이 가장 가격, 성능적으로 유리한가를 알아본다.

이를 위해 각 인스턴스별 특성을 파악하고 각 프로그램들을 수행했을때의 예상 결과를 예측하고, CPU/Memory/API 처리 프로그램을 인스턴스 에서 실행한다. 이후 예측값과 결과값 과의 괴리 이유를 기술적으로 분석하며 다양한 인스턴스간 특성에 대해 파악한다.

또한 x86, ARM 아키텍쳐간의 차이점을 알아보기 위해,  Intel / Graviton2 계열을 선정하여 결과에 대해 분석한다.

---

### 테스트 대상 인스턴스 목록

> OS와 스토리지는 모든 인스턴스에서 동일하게 설정
> 
- **m6i.large**: 인텔 기반 최신 인스턴스로, 메모리와 네트워크 성능이 향상된 범용 인스턴스.
- **c6i.large**: 인텔 기반의 고성능 컴퓨팅 인스턴스, CPU 집중형 작업에 적합.
- **t2.large**: 버스트 가능한 성능의 범용 인스턴스, 비용 효율성 중시.
- **m6g.large**: ARM 기반의 범용 인스턴스, 에너지 효율성 및 가격 대비 성능 우수.

인스턴스 스펙 : 2 vCPU, 8GB Memory (c6i.large 의 경우 4GB Memory), Ubuntu 24.04, 16GIB

---

### 성능 테스트 목표 및 방법

> 각 테스트는 동일한 리전 및 가용 영역에서 수행되며, 동일한 컴퓨터 및 네트워크 환경(핫스팟)을 통해 일관된 조건을 유지
> 
1. **CPU 성능 테스트**
    - 목표: CPU 연산 속도를 비교
    - 방법: 1억 번의 연산을 수행하는 테스트를 5회 반복하여 평균 소요 시간(ms)을 산출
2. **Memory I/O 성능 테스트**
    - 목표: 메모리 쓰기/읽기 속도를 비교
    - 방법: 10만 개의 정수형 배열을 메모리에 기록 및 읽는 작업 테스트를 5회 반복하여 평균 소요 시간(ms)을 산출
3. **API 성능 테스트**
    - 목표: Flask 기반 API의 응답 성능 측정
    - 방법: ApachBench(ab) 도구를 사용해 3초 동안 동시 요청 10개를 보내는 테스트를 3회 반복하여 평균 총 요청 회수를 산출
    - 옵션: `c 10 -t 3` 옵션을 사용하여 3초간 10개의 병렬 요청 수행

---

### 결과 예측 및 가설

- **CPU 성능 테스트**: c계열이 CPU 특화형이므로 반복된 연산에서 C6i 인스턴스가 높은 성능 결과 예상
- **Memory I/O 테스트**: c계열이 CPU 중심이므로 메모리 성능에서는 다소 낮은 성능 결과 예상
- **API 성능 테스트**: m 및 t 계열이 범용 인스턴스이므로 API 테스트에서 더 좋은 성능 결과 예상
- Graviton 계열은 효율적인 전력 소비와 ARM 아키텍처 기반의 설계 특성으로 미루어보아 동일 스펙의 x86 계열보다 약 120% 더 나은 성능을 보일 것으로 예상됨.

## 테스트 코드

### CPU Test Code

```python
import time

start_time = time.time()  # 시작 시간 기록

# 1억번 반복
for i in range(100000000):
    if i ** 2 + i == i ** 3 - i:
        pass  # 단순 비교만 수행하고 아무 작업도 하지 않음

end_time = time.time()  # 종료 시간 기록
execution_time = (end_time - start_time) * 1000  # 밀리초 단위

print(f"Execution time: {execution_time} ms")
```

### Memory Test Code

```python
import time
import numpy as np  # 대용량 메모리 사용을 위해 numpy 사용

# 메모리 IO 작업을 위한 큰 배열 생성 (10만개의 정수를 담는 배열)
array_size = 100000
data = np.random.randint(0, 100, size=array_size)

start_time = time.time()  # 시작 시간 기록

# 메모리 쓰기 작업 (배열의 모든 값을 다른 값으로 변경)
for i in range(array_size):
    data[i] = i

# 메모리 읽기 작업 (배열의 모든 값을 읽음)
temp = 0
for i in range(array_size):
    temp = data[i]

end_time = time.time()  # 종료 시간 기록
execution_time = (end_time - start_time) * 1000  # 밀리초 단위

print(f"Execution time: {execution_time} ms")

```

### API Test Code

```python
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import requests

from flask import Flask

app = Flask(__name__)

# 각 웹사이트에서 유튜브, 인스타그램, 링크드인 주소를 정리하는 함수
@app.route('/')
def extract_social_media_links():
    response = requests.get('https://github.com/JangWooJin1')
    soup = BeautifulSoup(response.text, 'html.parser')
    social_media_links = {'YouTube': [], 'Instagram': [], 'LinkedIn': []}

    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'youtube.com' in href:
            social_media_links['YouTube'].append(href)
        elif 'instagram.com' in href:
            social_media_links['Instagram'].append(href)
        elif 'linkedin.com' in href:
            social_media_links['LinkedIn'].append(href)

    return social_media_links

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

```

## 결과

### 표

| Instance Type | CPU Test(ms) | Memory Test(ms) | API Test(count) | Cost($) |
| --- | --- | --- | --- | --- |
| c6i.large | 16314.35 | 19.83 | 45 | 0.096 |
| t2.large | 20968.43 | 21.86 | 48 | 0.1152 |
| m6i.large | 15987.88 | 19.21 | 48 | 0.118 |
| m6g.large | 39589.81 | 48.06 | 25 | 0.094 |

### 그래프 분석

### 각 인스턴스 별 처리 시간(ms) / API 처리 횟수(1회)

<img width="1164" alt="image" src="https://github.com/user-attachments/assets/0ab89480-284b-4fb3-bc02-55b99290a1be">

### 1. CPU 성능 분석

- **m6i.large**와 **c6i.large**는 각각 15,987.88ms, 16,314.35ms로 가장 빠른 CPU 성능 기록
    - x86 프로세서의 고성능 코어 구조가 반복 연산에 효율적으로 작동한 결과
    - 미세한 성능 차이는 캐시 구조나 클럭 속도의 차이로 인한 가능성
- **t2.large**는 20,968.43ms로 상대적으로 느린 성능
    - **t2** 인스턴스가 크레딧을 이용한 버스트 성능에 의존하기 때문에 지속적인 CPU 작업에서 성능 저하 발생 가능
    - 크레딧은 CPU가 유휴상태일때 누적되고 활성상태일때 사용
- **m6g.large**는 39,589.81ms로 가장 저조한 성능
    - **Graviton2**가 고성능 단일 코어 연산에 최적화되지 않았기 때문

### 2. Memory I/O 성능 분석

- **m6i.large**와 **c6i.large**는 각각 19.21ms, 19.83ms로 우수한 메모리 I/O 성능
    - 최신 **DDR4** 메모리 기술을 사용하여 높은 대역폭 제공
- **t2.large**는 21.86ms로 다소 느린 성능
    - t2 인스턴스가 낮은 대역폭과 메모리 성능을 보이는 결과
- **m6g.large**는 48.06ms로 메모리 성능이 가장 저조
    - ARM 아키텍처의 메모리 처리 성능이 x86 기반 인스턴스보다 낮기 때문

### 3. API 성능 분석

- **t2.large**와 **m6i.large**는 각각 48회의 요청을 처리, API 성능에서 우수한 결과
    - **컴퓨팅, 메모리, 네트워킹 리소스**의 균형 잡힌 성능 제공, 네트워크 처리와 API 응답 속도에서 높은 일관성
- **c6i.large**는 45회의 요청을 처리하여 약간 낮은 성능
    - 높은 CPU 성능에도 불구하고, 네트워크 작업에서 리소스 배분이 적어 API 처리 성능에서 차이 발생
- **m6g.large**는 25회의 요청만 처리, 네트워크 처리 성능이 x86 기반 인스턴스에 비해 낮음을 시사


### 단위 비용당 처리 시간  / 단위 비용당 응답 횟수

<img width="1158" alt="image" src="https://github.com/user-attachments/assets/db4c51aa-6d38-495f-ba9a-fd77d1171be9">

### 4. 가격 대비 성능 분석
- **m6g.large**는 가장 저렴하지만, 성능이 현저히 낮아 예산이 매우 제한된 경우를 제외하고는 추천하지 않음
- **c6i.large**는 비교적 저렴한 비용으로 전반적으로 균형 잡힌 성능을 제공하므로, 가성비가 가장 뛰어난 선택
- **t2.large**는 비용 대비 성능이 다소 낮고, 성능 변동이 있을 수 있어 특정 환경에 적합할 수 있지만 일관성은 떨어짐
- **m6g.large**는 가장 저렴하지만, 성능이 현저히 낮아 예산이 매우 제한된 경우를 제외하고는 추천하지 않음

### 결론

**ARM 기반 인스턴스 성능 평가**

- **m6g.large**는 저전력, 비용 효율성에 강점을 지닌 ARM 기반 인스턴스이지만, 연산 집약적이고 메모리 대역폭이 중요한 작업에서는 **x86** 아키텍처 기반의 인스턴스가 더 나은 성능을 발휘
- 테스트 코드에서 반복 연산과 메모리 작업이 ARM 아키텍처의 약점을 부각시켰기 때문에, **m6g.large**가 상대적으로 낮은 성능을 보임

**서비스 환경에 적합한 인스턴스 선택**

- **C6i.large**는 CPU와 메모리 성능이 균형 잡히고 비용 효율이 좋아, 전반적인 가성비가 뛰어난 인스턴스
- **M6i.large**는 CPU, 메모리, API 성능 모두에서 가장 뛰어나며, 고성능이 필요한 서비스나 안정성이 중요한 환경에서 적합한 선택. 비용은 높지만, 서비스 품질을 최우선으로 하는 경우 좋은 선택
- **T2.large**는 성능이 다소 변동할 수 있으나, 버스트 성능을 활용할 수 있어 일시적으로 트래픽이 급증하는 서비스에 적합. 다만, 안정적인 CPU 성능이 요구되는 환경에서는 신중한 선택이 필요
- **M6g.large**는 가장 저렴하지만, 전반적인 성능이 낮아 성능이 중요하지 않은 비핵심 업무나 비용을 절감해야 하는 환경에서만 고려할 수 있는 옵션