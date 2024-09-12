# Team Seongsuji
<br>

## 실험 개요
### 목적
AWS EC2 인스턴스의 성능을 아키텍처(x86 vs ARM), 옵션, 인스턴스 크기에 따라 비교하여, 
머신러닝 작업에 최적화된 인스턴스 유형을 찾는 것이 목표입니다. 
이를 통해 성능과 비용 효율성을 분석하고 최적화합니다.

### 측정 지표
1. 학습 소요 시간 (초)
2. CPU 사용량 (%)

### 비교 항목
1.	x86 vs ARM 아키텍처
2.	인스턴스 크기 비교
3.	옵션 비교

<br>

## Code Block   
### Model
MNIST 데이터 셋을 이용하여 학습한 모델

### Data
60000만장의 이미지를 28*28크기로 나눠 총 784의 입력
극단적인 환경을 위해 512개 짜리 3개의 레이어를 두고 학습

### Code block
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

## t4g

| 인스턴스 유형 | 학습 소요 시간(초) | CPU 사용량(%) | 
| --- | --- | --- | 
| t4g.small | 47.15 | 14 |
| t4g.medium | 43.04 | 13.8 |
| t4g.large | 43.55 | 11.6 |
| t4g.xlarge | 28.38 | 7.37 |
| t4g.2xlarge | 22.76 | 7.03 |

![image](https://github.com/user-attachments/assets/e7538808-4e69-436b-a00c-59af9cb84e2b)

<br>

## x86 vs ARM   

<br> 

## 인스턴스 크기 비교

## 옵션 비교
![image](https://github.com/user-attachments/assets/a145c923-852f-467f-9ebe-46f9571c4286)

<br>

![image](https://github.com/user-attachments/assets/fc5cefbf-a037-4f1b-8055-46aacc974f14)
### 소요 시간
c6gn.medium이 가장 빠른 학습 시간(95.95초)을 기록했고, c6g.medium과 c6gd.medium의 소요 시간은 거의 비슷했습니다.
네트워크 성능이 강화된 c6gn 인스턴스가 소요 시간에 기여했음을 추측할 수 있습니다.
### CPU 사용량 
c6gd,medium이 다른 두 인스턴스에 비해 낮은 CPU 사용률(18.4%)을 보였고, c6g.medium과 c6gn.medium의 CPU 사용률은 유사했습니다.
고성능 스토리지를 가진 c6gd 인스턴스가 작업 중 CPU 부하를 적게 받았음을 추측할 수 있습니다.

<br>

## 결론
권지언 :
곽수지 :
곽성은 :

