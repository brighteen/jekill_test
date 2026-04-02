# Score-Based Generative Modeling through Stochastic Differential Equations
>Yang Song

## 핵심 내용 정리
NCSN와 DDPM을 SDE이라는 하나의 수학적 프레임워크로 통합한 논문.

### 1. 점을 선으로 잇다
- 기존 방식(NCSN, DDPM): 데이터를 훼손시키는 노이즈 단계가 유한했음.
- 이 논문은 노이즈 단계를 무한히 잘게 쪼개어, 데이터가 노이즈로 변해가는 과정을 연속적인 시간 $t \in [0, T]$상의 움직임으로 봄.
	- 이 연속적인 움직임을 기술하는 수학적 언어가 SDE임.

### 2. Forward SDE: 데이터 -> 노이즈(확산 과정)
데이터 x(0)에서 시작해서 시간 t가 흐를수록 점차 망가져서 x(T)(완전한 노이즈)가 되는 과정을 다음과 같은 이토 SDE로 정의.
$$dx = f(x, t)dt + g(t)dw$$
- $f(x, t)$: Drift Coefficient(흐름). 데이터가 변해가는 결정론적 경향성임.
- $g(t)$: Diffusion Coefficient(확산). 얼마나 강한 노이즈($dw$)가 주입되는지 결정함.
- $dw$: 배운 위너 과정(브라운 운동).
이 과정은 학습 파라미터가 없는 고정된 과정이며, T시점에서는 데이터가 단순한 사전 분포(Prior Distribution, 보통 $\mathcal{N}(0, I)$)가 되도록 설계.

### 3. Reverse SDE: 노이즈 -> 데이터(생성 과정)
이 논문의 가장 강력한 정리는 "어떤 확산 과정(Forward SDE)이든, 시간을 거꾸로 돌리는 역과정(Reverse SDE) 또한 확산 과정이며, 그 수식은 존재한다"는 것임.
시간을 거꾸로 흐르게 할 때($dt \rightarrow -dt$)의 SDE는 다음과 같음:
$$dx = [f(x, t) - g(t)^2 \nabla_x \log p_t(x)]dt + g(t)d\bar{w}$$
- $d\bar w$: 역시간에서의 위너 과정.
- 핵심 발견: 이 식을 풀려면 $\nabla_x \log p_t(x)$를 알아야 함. 이것이 Score Function임.
- 결론: 신경망 $s_\theta(x, t)$를 학습시켜서 이 스코어($\nabla_x \log p_t(x)$)만 근사할 수 있다면, 위 식을 수치적으로 풀어서 노이즈로부터 데이터를 생성할 수 있음.

### 4. 기존 모델의 통합(VE-SDE & VP-SDE)
1. VE-SDE(Variance Exploding):
- NCSN(Noise Conditional Score Network) (SMLD, Score matching with Langevin dynamics)방식.
- 시간이 지날수록 분산이 폭발적으로 커지는 SDE임.($dx = \sqrt{\frac{d[\sigma^2(t)]}{dt}} dw$).
2. VP-SDE(Variance Preserving):
- DDPM 방식.
- 노이즈를 더함과 동시에 데이터의 스케일을 줄여서, 분산이 일정하게 유지되도록 만든 SDE임.

### 5. 새로운 샘플링 기법: Predictor-Corrector(PC) Sampler
NCSN의 Langevin Dynamics와 SDE의 수치해석적 풀이법을 결합한 강력한 샘플링 방법을 제안.
- Predictor(예측기): 역방향 SDE를 수치적으로 한 스텝 품. 노이즈에서 데이터 쪽으로 큼직하게 이동함.
- Corrector(보정기): 이동한 지점의 분포가 올바른지 확인하기 위해 Langevin dynamics를 수행하여 분포를 교정함. 스코어가 제일 높아지는 방향으로 이동(방향을 수정).

### 6. Probability Flow ODE
SDE는 매번 실행할 때마다 노이즈($dw$)때문에 생성 경로가 달라짐(Stochastic). 하지만 저자들은 이와 동일한 주변 확률 분포$p_t(x)$를 가지면서도 결정론적인 ODE(Ordinary Differential Equation)를 유도함.
$$dx = [f(x, t) - \frac{1}{2}g(t)^2 \nabla_x \log p_t(x)]dt$$
- 의의:
	- 이 ODE를 풀면 데이터 x(0)를 잠재 공간의 x(T)로 오차 없이 1:1 매핑(Encoding)할 수 있음.
	- 반대로 x(T)에서 x(0)로 돌아올 수도 있음.