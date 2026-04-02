---
layout: sidebar
title: Hadamard product
---

아다마르 곱  
같은 크기의 두 행렬의 각 성분을 곱하는 연산이다.  

아다마르 곱은 기호 $\odot$를 사용하여 표기하며, 두 행렬의 크기가 완전히 동일할 때 같은 위치의 원소끼리만 곱하는 연산이다. 두 행렬 $A, B$가 다음과 같이 정의할 때:  

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}
$$  

일반적인 행렬 곱셈 $AB$와 아다마르 곱 $A \odot B$는 대수적으로 완전히 다른 결과를 낸다.  

$$
A \odot B = \begin{bmatrix} 1 \times 2 & 2 \times 0 \\ 3 \times 1 & 4 \times 3 \end{bmatrix} = \begin{bmatrix} 2 & 0 \\ 3 & 12 \end{bmatrix}
$$  

파이썬의 NumPy 모듈에서 `A * B`를 수행하면 이 아다마르 곱이 실행되며, 수학적으로 엄밀한 행렬 곱셈을 수행하려면 `np.dot(A, B)` 또는 `A @ B`를 사용해야 한다.  

일반적인 선형 계층 연산 $\boldsymbol{y} = W\boldsymbol{x}$는 가중치 행렬 $W$의 각 행과 입력 벡터 $\boldsymbol{x}$의 내적으로 모든 변수가 서로 얽히는 선형 결합이다.  
반면 아다마르 곱 $\boldsymbol{u} \odot \boldsymbol{v}$는 $i$번째 원소는 오직 $i$번째 원소와만 연산된다. 이는 특성(Feature) 간의 상호작용을 대수적으로 완벽하게 차단한 채, 오직 개별 차원의 크기만을 독립적으로 증폭시키거나 축소시키는 연산이다.  

가장 강력한 활용처는 순환 신경망(RNN) 계열인 LSTM이나 GRU의 게이트(Gate) 연산이다.  
예를 들어 망각 게이트(Forget Gate) $\boldsymbol{f}_t$는 시그모이드(Sigmoid) 함수를 통과하여 모든 원소가 $[0, 1]$ 사이의 실수값을 가지는 벡터로 도출되는데, 이를 이전 시점의 셀 상태(Cell State) $\boldsymbol{c}_{t-1}$에 적용할 때 반드시 아다마르 곱을 사용한다.  

$$
\boldsymbol{c}_t' = \boldsymbol{f}_t \odot \boldsymbol{c}_{t-1}
$$  

만약 $\boldsymbol{f}_t$의 특정 원소가 $0.01$이라면 해당 차원의 정보는 $1\%$ 크기로 붕괴하며 사실상 소거되고, $0.99$라면 정보가 그대로 보존된다. 즉, 비선형 활성화 함수의 출력 벡터를 이용해 데이터의 흐름을 $0$에서 $1$ 사이의 비율로 연속적으로 제어하는 필터로 볼 수 있다.  

자연어 처리(NLP) 트랜스포머(Transformer) 모델의 어텐션 마스크(Attention Mask)나 드롭아웃 기법에서는 원소가 ${0, 1}$로만 이루어진 이진 벡터(또는 행렬) $M$을 무작위적, 혹은 규칙적으로 생성한다. 신경망의 은닉 상태 $X$에 아다마르 곱 $M \odot X$를 수행하면, $M$의 원소가 $0$에 대응되는 은닉 상태의 값들은 모두 0이 된다. 이는 연산 중에 특정 데이터를 모델이 아예 보지 못하게 하거나, 과적합을 막기 위해 신경망의 일부 차원을 의도적으로 절단해 버리는 차원 제어 방식이다.  

참고  
wikipedia
