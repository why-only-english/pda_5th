import numpy as np
import time

# 큰 행렬의 크기 설정 (예: 50,000 x 50,000 행렬, 매우 큰 메모리 사용)
matrix_size = 50_000

# 1. 대규모 행렬 생성 및 초기화 (메모리 할당)
print("대규모 행렬 생성 시작")
start_time = time.time()

# 두 개의 대규모 행렬을 생성
A = np.random.rand(matrix_size, matrix_size)
B = np.random.rand(matrix_size, matrix_size)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"대규모 행렬 생성 및 초기화에 걸린 시간: {elapsed_time:.5f} 초")

# 2. 대규모 행렬 곱셈 테스트 (메모리와 CPU를 많이 사용)
print("행렬 곱셈 시작")
start_time = time.time()

# 행렬 곱셈 수행
C = np.dot(A, B)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"행렬 곱셈에 걸린 시간: {elapsed_time:.5f} 초")

# 3. 행렬 결과의 합계 계산 (읽기 작업)
print("행렬 합계 계산 시작")
start_time = time.time()

# 행렬 C의 모든 값 합계 계산
total_sum = np.sum(C)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"행렬 합계를 계산하는 데 걸린 시간: {elapsed_time:.5f} 초")
print(f"행렬 합계: {total_sum}")
