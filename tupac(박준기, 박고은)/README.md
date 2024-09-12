# 1. 압축 해제로 성능 비교를 선택한 이유
파일 압축 해제엔 CPU 성능, CPU 갯수와 RAM 용량의 양의 상관관계가 있을 것이라는 생각이 들었습니다.
실제로 컴퓨터 성능을 측정할 때 압축 및 압축해제 성능을 기록.

[CPU 성능과 압축 해제 속도의 관계 - 인텔](https://www.intel.co.kr/content/www/kr/ko/gaming/resources/read-cpu-benchmarks.html)
[램과 컴퓨터 성능의 상관관계 - newegg ](https://www.newegg.com/insider/what-is-ram-speed-and-how-does-it-affect-my-pcs-performance/)

# 2. **Zstandard**(zstd) 압축 프로그램
facebook에서 만든 프로그램으로 멀티 스레딩을 지원합니다.
압축 프로그램 중 준수한 성능.

# 3. 가설 : 더 좋은 인스턴스 패밀리와 더 큰 인스턴스 사이즈일 수록 압축 해제 속도가 더 빠를 것이다.

# 4. 테스트 환경 목록

![[Pasted image 20240912113249.png]]

| Instance Type | vCPU | Memory (GiB) | Cost (USD) | ARM (t4g/m6g/c6g) | x86 (t3/m5/c5) |
| ------------- | ---- | ------------ | ---------- | ----------------- | -------------- |
| **t-large**   |      |              |            |                   |                |
| t4g.large     | 2    | 8            | 0.0832     | ARM               |                |
| t3.large      | 2    | 8            | 0.104      |                   | x86            |
| t4g.xlarge    | 4    | 16           | 0.1664     | ARM               |                |
| t3.xlarge     | 4    | 16           | 0.208      |                   | x86            |
| **m-large**   |      |              |            |                   |                |
| m6g.large     | 2    | 8            | 0.094      | ARM               |                |
| m5.large      | 2    | 8            | 0.118      |                   | x86            |
| m6g.xlarge    | 4    | 16           | 0.188      | ARM               |                |
| m5.xlarge     | 4    | 16           | 0.236      |                   | x86            |
| **c-large**   |      |              |            |                   |                |
| c6g.large     | 2    | 4            | 0.077      | ARM               |                |
| c5.large      | 2    | 4            | 0.096      |                   | x86            |
| c6g.xlarge    | 4    | 8            | 0.154      | ARM               |                |
| c5.xlarge     | 4    | 8            | 0.192      |                   | x86            |

![[스크린샷 2024-09-12 140757.png]]



# 5. 결과
arm 계열의 cpu가 압축 해제 성능이 좋은 경향을 보이고, 가설은 기각.
![[image 1.png]]

![[image (1) 1.png]]

![[image (3).png]]