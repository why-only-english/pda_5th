import numpy as np
import time

# 테스트할 메모리 크기 (10억 개의 float64 값, 약 8GB)
size = 1_000_000_000  # 10억 개

# 1. 대용량 메모리 할당 (Numpy 배열 생성)
start_time2 = time.time()
start_time = time.time()

# Numpy 배열에 값 쓰기
array = np.ones(size, dtype=np.float64)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"메모리 할당 및 초기화에 걸린 시간: {elapsed_time:.5f} 초")

# 2. 메모리 접근 및 연산 테스트
start_time = time.time()

# 배열의 값을 모두 2로 변경
array *= 2

end_time = time.time()
elapsed_time = end_time - start_time
print(f"메모리 값을 변경하는 데 걸린 시간: {elapsed_time:.5f} 초")

# 3. 메모리 읽기 테스트
start_time = time.time()

# 배열 값의 합계 계산
total_sum = np.sum(array)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"배열 값을 읽고 합계를 계산하는 데 걸린 시간: {elapsed_time:.5f} 초")
end_time2 = time.time()
elapsed_time2= end_time2 - start_time2
print(f"총 걸린 시간: {elapsed_time2:.5f} 초")
