# [EC2 인스턴스 성능 리포트] - 아이셔

## 1. 서론

### 1.1. 개요

본 연구에서는 AWS 인스턴스 크기, 아키텍처, 인스턴스 유형에 따른 성능을 분석하였다. 성능 분석에는 두 개의 코드를 사용하였고, 이를 통해 최적의 인스턴스 선택을 지원하고자 한다.

### 1.2. 테스트 환경 설정

```python
sudo apt update
sudo apt upgrade
sudo reboot

wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-aarch64.sh
# wget https://repo.anaconda.com/archive/Anaconda3-2023.07-0-Linux-x86_64.sh
bash Anaconda3-2024.06-1-Linux-aarch64.sh
# bash Anaconda3-2023.07-0-Linux-x86_64.sh
source .bashrc
conda create -n test python=3.11
conda activate test
```

파이썬 코드를 실행시키기 위한 아나콘다 환경 설정을 진행하였다.

### 1.3. 테스트 코드

**코드1: Prime Number**

```python
import time

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_test(limit):
    start_time = time.time()
    primes = [i for i in range(limit) if is_prime(i)]
    end_time = time.time()
    print(f"Found {len(primes)} primes in {end_time - start_time:.6f} seconds.")

prime_test(2000000)
```

해당 코드는 2,000,000 이하의 소수의 개수를 찾는 코드이다.
<br/>

**코드2: CNN**

```python
import tensorflow as tf
from tensorflow.keras import layers, models
import time

# MNIST 데이터셋 로드
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# 데이터 전처리
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# 간단한 CNN 모델 정의
def create_cnn_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

# 모델 컴파일 및 학습
def dl_test(train_images, train_labels):
    model = create_cnn_model()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    start_time = time.time()
    model.fit(train_images, train_labels, epochs=5, batch_size=64, verbose=2)
    end_time = time.time()
    
    print(f"Trained CNN model in {end_time - start_time:.6f} seconds.")

dl_test(train_images, train_labels)
```

해당 코드는 TensorFlow를 사용하여 MNIST 데이터셋을 로드하고, 간단한 CNN 모델을 정의하여 훈련시키는 코드이다. 

<br/>

<br/>


## 2. 코드1(Prime Number)을 통한 성능 분석

### 2.1. 인스턴스 크기에 따른 성능 분석
<br/>

**2.1.1. 측정 대상**

| **인스턴스 크기** | **vCPU** | **메모리(GiB)** | **온디맨드 시간당 요금** |
| --- | --- | --- | --- |
| t4g.micro | 2 | 1 | USD 0.0084 |
| t4g.small | 2 | 2 | USD 0.0168 |
| t4g.medium | 2 | 4 | USD 0.0336 |
| t4g.large | 2 | 8 | USD 0.0672 |
| t4g.xlarge | 4 | 16 | USD 0.1344 |
| t4g.2xlarge | 8 | 32 | USD 0.2688 |
<br/>

**2.1.2 가설**

H1: 인스턴스 크기가 커질수록 코드 실행 시간이 줄어들 것이다.

<br/>

**2.1.3. 실행 시간 측정 결과**

| **인스턴스 크기** | **1회차(sec)** | **2회차(sec)** | **평균(sec)** |
| --- | --- | --- | --- |
| t4g.micro | 12.172703 | 12.167339 | 12.17002 |
| t4g.small | 12.325244 | 12.342499 | 12.33387 |
| t4g.medium | 12.401935 | 12.508585 | 12.45526 |
| t4g.large | 12.252724 | 12.620501 | 12.43661 |
| t4g.xlarge | 12.197164 | 12.175627 | 12.1864 |
| t4g.2xlarge | 12.580108 | 12.147315 | 12.36371 |


인스턴스 크기가 커질수록 코드 실행 시간이 줄어들 것이라 생각했으나 눈에 띄는 차이는 보이지 않았다.
<br/>

**2.1.4. CPU 사용률 측정 결과**

| **인스턴스 크기** | **평균 최대 사용률(%)** |
| --- | --- |
| t4g.micro | 2.5851 |
| t4g.small | 15.388 |
| t4g.medium | 9.9018 |
| t4g.large | 5.6123 |
| t4g.xlarge | 1.4509 |
| t4g.2xlarge | 0.67699 |

![image](https://github.com/user-attachments/assets/7d242339-a7c6-46f3-95a7-4be068a2c30b)

<br/>

**2.1.5. 결론**

T계열에서 CPU의 개수가 늘어나도 늘어난만큼 자원을 활용하지 못한다. 따라서 2xLarge같이 CPU의 개수가 많아도 IDLE하게 놀고 있는 CPU가 많다는 것을 알 수 있다.

⇒ T계열의 인스턴스 특징이 AWS 크레딧 시스템이 지원해서 급하게 사용량이 늘어났을 때를 대비해서 평소에는 cpu 리소스를 낮게 제공한다.

[Burstable performance instances - Amazon Elastic Compute Cloud](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

그렇다면 T계열이 아닌 다른 계열에서 작업을 수행하면 늘어난 만큼의 자원을 할 수 있을것인지 의문이 생겼다.

<br/>


### 2.2. 인스턴스 유형에 따른 성능 분석

**2.2.1. 측정 대상**

| **인스턴스 크기** | **vCPU** | **메모리(GiB)** | **온디맨드 시간당 요금** |
| --- | --- | --- | --- |
| c5.large | 2 | 4GiB | USD 0.096 |
| c5.xlarge | 4 | 8GiB | USD 0.192 |
| c5.2xlarge | 8 | 16GiB | USD 0.384 |

<br/>

**2.2.2. 측정 결과**

| **인스턴스 크기** | **1회차** | **2회차** | **평균** | **평균 최대사용률(%)** |
| --- | --- | --- | --- | --- |
| c5.large | 7.705007  | 7.699535  | 7.702271 | 25.598 |
| c5.xlarge | 7.690931 | 7.661475 | 7.676203 | 9.49 |
| c5.2xlarge | 7.699180  | 7.679794 | 7.689487 | 6.59 |

![image (1)](https://github.com/user-attachments/assets/ba04968a-e52a-4ce3-8175-7d849ca4640f)

<br/>


**2.2.3. 결론**

C계열도 T계열과 동일하게 스펙이 좋아져도 코드 실행 속도는 동일함을 확인했다. 

테스트에 사용했던 코드가 추가적인 CPU 자원을 활용하지 않아도 해결 가능한 간단한 코드였기에 위와 같은 결과가 나왔다고 추정하여 더 복잡한 코드를 테스트에 활용해보고자 3을 진행했다.

<br/>

## 3. 코드2(CNN)를 통한 성능 분석

### 3.1. 인스턴스 크기에 따른 성능 분석

**3.1.1. 측정 대상**

| **인스턴스 크기** | **vCPU** | **메모리(GiB)** | **온디맨드 시간당 요금** |
| --- | --- | --- | --- |
| t4g.large | 2 | 8GiB | USD 0.0672 |
| t4g.xlarge | 4 | 16GiB | USD 0.1344 |
| t4g.2xlarge | 8 | 32GiB | USD 0.2688 |

<br/>

**3.1.2. 가설**

H1 : 인스턴스 크기가 커질수록 코드 실행 시간이 줄어들 것이다.

<br/>


**3.1.3. 실행 시간 측정 결과**

| **인스턴스 크기** | **1회차(sec)** | **2회차(sec)** | **3회차(sec)** | **평균(sec)** |
| --- | --- | --- | --- | --- |
| t4g.large | 263.171795 | 263.188510 | 263.597437 | 263.319247 |
| t4g.xlarge | 113.392787 | 113.353860 | 113.661963 | 113.469537 |
| t4g.2xlarge | 72.927183 | 73.386210 | 73.139006 | 73.150800 |

![image (2)](https://github.com/user-attachments/assets/38852538-327d-4ea3-b53d-36d30e8240b5)



<br/>


**3.1.4 결론**

예상을 했던 것과 동일하게 인스턴스의 스펙이 좋아질수록 실행 시간이 줄어듦을 확인했다. 

<br/>


**3.2.1 측정 대상**

| **인스턴스 크기** | **vCPU** | **메모리(GiB)** | **온디맨드 시간당 요금** |
| --- | --- | --- | --- |
| c6g.large | 2 | 4GiB | USD 0.077 |
| t4g.large | 2 | 8GiB | USD 0.0832 |

<br/>


**3.2.2. 가설**

C계열은 컴퓨팅 목적으로 사용이 되고, T계열은 성능 순간 확장이 가능한 유형이기에 C계열이 빠를것이라고 예측했다.

<br/>


**3.2.2. 측정 결과**

| **인스턴스 이름** | **측정속도1** | **측정속도2** | **측정속도3** | **평균** |
| --- | --- | --- | --- | --- |
| c6g.large | 199.70362 | 199.976434 | 203.093583 | 200.9245 |
| t4g.large | 263.1718 | 263.18851 | 263.597437 | 263.3192 |

![image (3)](https://github.com/user-attachments/assets/f1e759f2-e00b-46b8-8cc8-73ec3344bd84)

<br/>



**3.3.1. 측정 대상**

| **인스턴스 크기** | **아키텍쳐** | **vCPU** | **메모리(GiB)** | **온디맨드 시간당 요금** |
| --- | --- | --- | --- | --- |
| t4g.large | ARM | 2 | 8GiB | USD 0.0832 |
| t3.large | x86 | 2 | 8GiB | USD 0.104 |

<br/>


**3.3.2. 가설**

ARM이 더 좋다고 공식 문서

<br/>


**3.3.3. 측정 결과**

| **인스턴스 이름** | **아키텍처** | **측정속도1** | **측정속도2** | **측정속도3** | **평균** |
| --- | --- | --- | --- | --- | --- |
| t4g.large | ARM  | 263.171795 | 263.188510 | 263.597437 | 263.3192 |
| t3.large | x86 | 183.550041 | 203.166146 | 203.552930 | 196.7564 |

![image (4)](https://github.com/user-attachments/assets/611a1cee-1cb1-41c7-9971-d7c21f8669e0)

<br/>


## 4. 결론

1. 소수 알고리즘처럼 가벼운 코드에 대해서는 인스턴스의 크기나 유형에 크게 영향을 받지 않으므로 가격이 저렴한 인스턴스를 사용하는 것을 권장한다.
2. 딥러닝 학습과 같이 무거운 코드는 성능이 좋은 인스턴스를 활용하면 그에 상응하는 효과를 볼 수 있다.


<br/>

