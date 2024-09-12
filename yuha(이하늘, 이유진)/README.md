### 개요
신한투자증권에서는 IPO 상장 시 트래픽이 몰려 대비를 해야 하는 것이 주요 쟁점이다.<br>
이 점에 주목하여 EC2 종류에 따른 부하 테스트를 진행하여 해당 서버의 시간당 처리량과 처리 시간을 알고자 한다.

### 실습 과정
1. 성능 테스트 도구 중 K6를 선택
2. 부하 테스트 종류 중 spike test 선택 <br>
   -> spike test란, 특정 시간 동안 트래픽을 급격히 증가시키고, 그 후 급격히 감소시키는 테스트 방식
3. 실험할 EC2 선택
4. spike test 진행
5. 결과 분석

### EC2 종류
| Instance Type | vCPU | Memory (GB) |
| ------------- | ---- | ----------- |
| t2.micro      | 1    | 1           |
| t2.small      | 1    | 2           |
| t3.micro      | 2    | 1           |
| t3.small      | 2    | 2           |
| t2.medium     | 2    | 4           |

### Spike Test

```javascript
import http from "k6/http";
import { sleep, check } from 'k6';

export let options = {
    insecureSkipTLSVerify: true,
    noConnectionReuse: false,
    stages: [
        { duration: '20s', target: 100 },
        { duration: '30s', target: 2000 },
        { duration: '20s', target: 100 },      
    ],
};

export default function () {
    const res = http.get('http://3.37.30.99:8080');
    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(1);
};
```
- 원초기 사용자 수 (100명): 100명의 가상 사용자로 시작해 서버가 적은 트래픽에서 어떻게 반응하는지 확인합니다.
- 급격한 트래픽 증가 (2000명): 20초 후 2000명으로 급증해 서버가 많은 요청을 어떻게 처리하는지 평가합니다.
- 트래픽 감소 (100명): 30초 동안 2000명을 유지한 후 다시 100명으로 감소하며, 서버의 복구 능력을 테스트합니다.

### 결과 분석

