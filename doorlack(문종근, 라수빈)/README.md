# 인스턴스 성능별로 N-Queen 문제 해결하는 데 걸리는 시간을 알아보자

## 1. N-Queen 문제란?
- N-Queen 문제는 크기가 N × N인 체스판 위에 퀸 N개를 서로 공격할 수 없게 놓는 문제
<img src="https://github.com/user-attachments/assets/6d9fbadf-93fc-4514-badd-00834c41d318" width="400"/>

## 2. 사용 코드 
```python
import time
import os

def is_safe(graph, row, col, n):
    # 같은 열에 퀸이 있는지 확인
    for i in range(row):
        if graph[i] == col:
            return False

    # 대각선에 퀸이 있는지 확인
    for i in range(row):
        if abs(graph[i] - col) == abs(i - row):
            return False

    return True

def solve_nqueens(graph, row, n):
    # 마지막 행까지 도달하면 해결된 경우
    if row == n:
        return 1

    count = 0
    for col in range(n):
        if is_safe(graph, row, col, n):
            graph[row] = col
            count += solve_nqueens(graph, row + 1, n)

    return count

def nqueens(n):
    graph = [-1] * n
    return solve_nqueens(graph, 0, n)

# n값 13으로 지정
n = 13

# 시작 시간 측정
start_time_real = time.time()  # 실제 경과 시간 측정
start_time_cpu = os.times()    # CPU 시간 측정

# N-Queens 실행
result = nqueens(n)

# 종료 시간 측정
end_time_real = time.time()    # 실제 경과 시간 측정 종료
end_time_cpu = os.times()      # CPU 시간 측정 종료

# 경과 시간 계산
real_time = end_time_real - start_time_real
user_time = end_time_cpu.user - start_time_cpu.user
sys_time = end_time_cpu.system - start_time_cpu.system

# 결과 출력
print(f"N={n}인 경우 가능한 해답의 수: {result}")
print(f"실행 시간(real): {real_time:.6f} 초")
print(f"CPU 사용자 모드 시간(user): {user_time:.6f} 초")
print(f"CPU 시스템 모드 시간(sys): {sys_time:.6f} 초")

```


## 3. 사용한 인스턴스 종류
| 인스턴스 종류 | t3.micro | t3.medium | t3.xlarge | t3.2xlarge |
| --- | --- | --- | --- | --- |
| vCPU | 2 | 2 | 4 | 8 |
| 메모리(GiB) | 1 | 4 | 16 | 32 |
| 시간당 요금(USD) | 0.013 | 0.052 | 0.208 | 0.416 |

| 인스턴스 종류 | c4.large | c4.xlarge | c4.4xlarge | c4.8xlarge |
| --- | --- | --- | --- | --- |
| vCPU | 2 | 2 | 4 | 8 |
| 메모리(GiB) | 3.75 | 15 | 30 | 60 |
| 시간당 요금(USD) | 0.10 | 0.398 | 0.796 | 1.591 |

## 4. 사용자 모드 시간과 시스템 모드 시간
- 사용자 모드(user): 프로그램이 애플리케이션 레벨에서 실행된 CPU 시간. 계산, 논리 실행 등 주로 사용자 코드에서 처리

- 시스템 모드(sys): 프로그램이 운영 체제 커널에서 실행된 CPU 시간
 파일 I/O, 네트워크 통신, 메모리 관리와 같은 시스템 호출에서 처리된 시간

> 알고리즘 계산 시 주로 CPU에서 계산 작업 한다! → 계산 작업에 용이한 **C계열 인스턴스 사용이 유리하다는 것을 알 수 있음 !!**

<p align="center">
    <img src="https://github.com/user-attachments/assets/1c04b06b-360c-4789-a625-55f2da8307af" width="200"/>
</p>

>
## 5. 결과 
아는 것이 돈이다!

