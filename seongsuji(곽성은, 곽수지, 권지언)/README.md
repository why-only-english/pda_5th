# Team Seongsuji
<br>

# 실험 개요

### 목적
AWS EC2 인스턴스의 성능을 인스턴스 크기, 아키텍처(x86 vs ARM), 옵션, 인스턴스 패밀리에 따라 비교하여, 
머신러닝 작업에 최적화된 인스턴스 유형을 찾아 성능과 비용 효율성을 최적화합니다.
### 측정 지표
1. 학습 소요 시간 (초)
2. CPU 사용량 (%)
### 비교 항목
1. 인스턴스 크기 비교
2. x86 vs ARM 아키텍처
3. 옵션 비교
4. 인스턴스 패밀리 비교
### 모델
- 512개의 노드
- 레이어 3개
### 데이터
MNIST 데이터 셋 60000만장의 이미지를 28*28크기로 나눠 총 784번을 입력합니다.
### 코드
```js
import tensorflow as tf
import time  # 시간 측정을 위한 모듈

# MNIST 데이터셋 로드
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# 데이터 형태 확인
train_images = train_images.reshape((60000, 784))
train_images = train_images.astype('float32') / 255.0
test_images = test_images.reshape((10000, 784))
test_images = test_images.astype('float32') / 255.0
train_labels = tf.keras.utils.to_categorical(train_labels)
test_labels = tf.keras.utils.to_categorical(test_labels)

# 모델 정의
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(512, activation='relu', input_shape=(784,)))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='sigmoid'))

# 모델 컴파일
model.compile(optimizer='Adam',
              loss='mse',
              metrics=['accuracy'])

# 학습 시간 측정
start_time = time.time()  # 학습 시작 시간 기록

# 모델 학습
history = model.fit(train_images, train_labels, epochs=5, batch_size=128)
end_time = time.time()  # 학습 종료 시간 기록

# 학습에 걸린 시간 계산 및 출력
elapsed_time = end_time - start_time
print(f"학습 소요 시간: {elapsed_time:.2f} 초")

# 모델 평가
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('테스트 정확도:', test_acc)

```
<br> 

# 실험
## 1. 인스턴스 크기 비교
### t4g
![image](https://github.com/user-attachments/assets/e7538808-4e69-436b-a00c-59af9cb84e2b)
| 인스턴스 유형 | 학습 소요 시간(초) | CPU 사용량(%) | 
| --- | --- | --- | 
| t4g.small | 47.15 | 14 |
| t4g.medium | 43.04 | 13.8 |
| t4g.large | 43.55 | 11.6 |
| t4g.xlarge | 28.38 | 7.37 |
| t4g.2xlarge | 22.76 | 7.03 |

<br>

### t2
![image](https://github.com/user-attachments/assets/5e7abdd5-ded0-4af9-9daf-a4c0266532e9)
| 인스턴스 유형 | 학습 소요 시간(초) | CPU 사용량(%) | 
| --- | --- | --- | 
| t2.small | 50.73 | 18.05 |
| t2.medium | 31.69 | 9.65 |
| t2.large | 26.45 | 12.5 |
| t2.xlarge | 19.43 | 6 |

<br>


## 2. x86 vs ARM 아키텍처
### 학습 소요 시간 비교
![image](https://github.com/user-attachments/assets/09adf936-3a83-4993-97cb-09bbf42ec64d)
### CPU 사용량 비교
![image](https://github.com/user-attachments/assets/1bba891f-0061-4193-8932-8b6accc7bb6f)

<br> 


## 3. 옵션 비교
<img src='https://github.com/user-attachments/assets/a145c923-852f-467f-9ebe-46f9571c4286'>
<img src='https://github.com/user-attachments/assets/fc5cefbf-a037-4f1b-8055-46aacc974f14' width='500'>

### 소요 시간
c6gn.medium이 가장 빠른 학습 시간(95.95초)을 기록했고, c6g.medium과 c6gd.medium의 소요 시간은 거의 비슷했습니다.
네트워크 성능이 강화된 c6gn 인스턴스가 소요 시간에 기여했음을 추측할 수 있습니다.
### CPU 사용량 
c6gd.medium이 다른 두 인스턴스에 비해 낮은 CPU 사용률(18.4%)을 보였고, c6g.medium과 c6gn.medium의 CPU 사용률은 유사했습니다.
고성능 스토리지를 가진 c6gd 인스턴스가 작업 중 CPU 부하를 적게 받았음을 추측할 수 있습니다.

<br>
<br>

## 4. 인스턴스 패밀리 비교(t family, c family)
<img src='https://github.com/user-attachments/assets/0ed2c4f2-53c7-49a1-8b8f-cfaeaed7c9db'>
<img src='https://github.com/user-attachments/assets/b290b97e-1a4e-422e-90cb-11d3dd0e1dc1' width='500'>

### 소요 시간
t2.small이 43.04초로 c6g.medium의 104.15초보다 더 빠른 결과를 보였습니다.
컴퓨팅 최적화 인스턴스인 c6g.medium이 우세할 것이라고 예상했으나, 머신 러닝 학습 작업은 CPU 성능뿐만 아니라 메모리 대역폭, 병렬 처리 능력, 리소스 관리 등의 역할도 중요하기 때문에 범용 인스턴스인 t2.small이 다양한 리소스를 효율적으로 사용하여 더 빠르게 학습 작업을 완료했다고 예상했습니다.
### CPU 사용량 
c6g.medium이 23.2%, t2.small이 13.8%로 더 높았습니다.
c6g.medium은 컴퓨팅 최적화 인스턴스로 더 많은 CPU 리소스를 사용해 작업을 처리하려 했지만 그만큼의 CPU 자원이 필요하지 않았을 수도 있습니다. 범용 인스턴스인 t2.small는 더 적은 CPU 자원을 사용하면서도 효율적으로 작업을 처리했음을 예측할 수 있습니다.
<br>

<br>
<br>

# 정리
### X86(Intel) 과 Arm 의 차이
- X86 : Instance의 크기가 커질수록 학습 속도가 빨랐습니다. <br>
- Arm : small, medium, large / xlarge, 2xlarge 두 그룹 간에 유의미한 학습 속도 차이를 보였습니다. <br>
두 종류의 아키텍처 중 X86의 학습 속도가 약간 더 빠른 경향을 보였습니다.

### 인스턴스 크기의 차이
인스턴스 크기가 커질 수록 CPU 활용률과 소요 시간이 개선되는 경향을 보였습니다. 메모리보다 CPU에서 유의미한 차이가 있었습니다.

### 옵션 별 차이
n의 경우 네트워크의 최적화로 소요 시간에서 유리하고, d의 경우 스토리지 최적화로 CPU 활용률에서 유리했습니다.

### 인스턴스 패밀리 차이 (범용 인스턴스와 컴퓨팅 최적화 인스턴스)
컴퓨팅 최적화 인스턴스가 더 높은 성능을 보일 것이라 예상했지만, 시간과 CPU 활용률 모두에서 t시리즈가 유리했습니다.
이는 머신러닝에서는 CPU 성능 뿐만 아니라 메모리 대역폭, 병력 처리 능력, 리소스 관리 등 범용적인 역할도 중요하기 때문에 범용 인스턴스가 유리한 것으로 추측했습니다.

### 인스턴스 별 비용
|요금(USD/hour)|t4g.small|t4g.medium|t4g.large|t4g.xlarge|t4g.2xlarge|t2.small|t2.medium|t2.large|t2.xlarge|
|---|---|---|---|---|---|---|---|---|---|
|온디맨드 Linux 기본|0.0208|0.0979|0.0832|0.2227|0.3382|0.0288|0.0756|0.144|0.2714|
<br>

## 결론
- 모델 학습을 위해 적합한 아키텍트는 Intel이며, 원하는 비용과 속도에 맞추어 용량을 선택하는 것을 권장합니다.
- ARM에서 속도가 중요하다면 xlarge를 그렇지 않다면 small을 선택하는 것이 경제적입니다.
- 소요 시간을 줄이고 싶다면 c6gn, CPU사용률을 줄이고 싶다면 c6gd를 사용하는 것이 유리합니다.
- 경우에 따라, 범용 인스턴스의 리소스 관리 방식이 컴퓨팅 최적화 인스턴스보다 머신 러닝 학습 작업에 더 적합할 수 있습니다.

