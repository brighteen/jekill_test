---
layout: sidebar
title: 정밀도 행렬의 기하학적 의미
collection_name: notes
nav_order: 1999
---

정밀도 행렬(precision matrix)에서 정밀도는 혼동 행렬에서 말하는 정밀도와 다른 개념이다.  

일변수 확률 변수 $$x$$에 대해 $$x$$가 평균이 $$m$$이고 분산이 $$s$$인 정규분포를 따른다고 가정했을 때, 분산의 역수($$\frac{1}{s}$$)는 무엇일까?  
분산이란, 어떤 확률 변수의 불확실성을 내포한다. 그 역수는 이 불확실성의 역수인데, 만약 분산이 크다면 그의 역수는 작아질 것이고, 분산이 작아진다면 그 역수는 커질것이다.  
불확실의 역은 확신과 결이 통한다.  

다변수를 다룰 경우, 정밀도 행렬은 다변수 가우시안의 지수항에 볼 수 있으며(1), 선형회귀에서 해석적 해를 찾는 정규방정식에서도 볼 수 있다(2).  

![두 변수간의 양의 상관관계.png]({{ site.baseurl }}/assets/notes/linear-algebra/두-변수간의-양의-상관관계.png){: .img-normal width="500" }

위 그림처럼 데이터가 $$y=x$$방향으로 길게 늘어져 있는(양의 상관관계) 타원형 분포를 생각해보자.  
- 중심에서 $$y=x$$ 방향(긴 축)으로 5만큼 떨어진 점 A.
- 중심에서 $$y=-x$$ 방향(짧은 축)으로 3만큼 떨어진 점 B.
유클리드 거리로 재면 점 B가 중심에 더 가깝다.  
하지만 데이터의 맥락에서 보면, 점 A는 데이터의 흐름을 잘 따르는 '정상적인' 점이지만, 점 B는 데이터의 경향성을 벗어난 이상치이다. 통계적 맥락에서는 점 A가 중심에 훨씬 더 가까운 점이어야 한다.  
이때 '데이터의 맥락'이라는 것이 주관적인 표현인데 이를 수학적으로 정의할 수 있을까?  

기하학적으로 공분산 행렬 $$\boldsymbol{\Sigma}$$가 원을 타원으로 길게 쭈욱 늘리는 변환이라면, 그 역행렬인 정밀도 행렬은 그 늘어난 타원을 다시 꾹 눌러서 완벽한 원형으로 압축하는(되돌리는, 역산) 변환이다.  
이 '공간 변환'은 정밀도 행렬의 제곱근인 $$\boldsymbol{\Sigma}^{-1/2}$$를 데이터에 곱해주는 것이며, 이를 백색화(whitening)변환이라고 부른다.  
- $$y=x$$ 축처럼 데이터가 넓게 퍼져 분산이 큰 방향은 압축.
- $$y=-x$$ 축처럼 데이터가 좁게 뭉친 방향으로 늘림.
- 상관관계(기울기)를 회전시켜 제거.

<video controls class="img-normal" width="100%"><source src="{{ site.baseurl }}/assets/notes/linear-algebra/mahalanobiswhitening.mp4" type="video/mp4">Your browser does not support the video tag.</video>

변환 후 데이터 분포는 구형이 되며, 이 공간에서 재는 유클리드 거리는 합당한 거리 측정이다.  

<div class="math-container">
$$
D^2 = (\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})
$$  
</div>


백색화(whitening)란 다변량 확률 변수의 상관관계를 제거하고 모든 분산을 1로 표준화하는 선형변환이다.  
'백색'이라는 용어는 신호 처리 분야의 백색 잡음(White Noise)에서 유래했다. 가시광선의 모든 주파수가 균일하게 혼합될 때 백색광이 되는 물리적 현상에 빗대어, 모든 주파수 대역의 에너지가 균일하고 서로 독립적인 무작위 신호를 백색 잡음이라고 부른다. 데이터에 존재하는 특성 간의 편중이나 상관관계를 완전히 소거하여 이 백색 잡음과 같은 무상관 상태로 변환하기 때문에 백색화라고 불린다.  
공분산 행렬 $$\Sigma$$와 평균 $$\mu$$를 갖는 다차원 확률 변수 벡터 $$X$$가 존재한다. 목표는 공분산이 항등 행렬인 새로운 확률 변수 Y를 도출하는 것이다. 공분산 행렬이 항등 행렬이라는 것은 비대각 성분이 0(상관관계 없음)이고, 대각 성분이 1(분산이 1)이라는 뜻이다.  
mean-centering된 데이터에 행렬 $$W$$를 곱하여 새 확률변수 $$Y$$를 정의한다.  

<div class="math-container">
$$
Y = W(X - \mu
$$  
</div>


이때 백색화 행렬 $$W$$는 반드시 **$$W^T W = \Sigma^{-1}$$** 조건을 만족해야 한다.  
실제로 정밀도 행렬($$\Sigma^{-1}$$) 자체의 변환이 데이터의 상관관계와 표준화를 수행하는 것이 아니다. 만약 데이터에 $$\Sigma^{-1}$$를 직접 곱하면 결과 확률 변수의 분산은 1이 되는 것이 아니라 오히려 원래 분산의 역수($$\Sigma^{-1}$$)가 된다.  
어떤 일변수 데이터 $$X$$의 분산이 $$\sigma^2$$ 이라고 해보자($$Var(X) = \sigma^2$$). 이때 목표는 새로운 데이터 $$Y$$의 분산을 1로 만드는 것이다.  
만약 정밀도(분산의 역수)를 직접 데이터의 곱한다면($$Y = \frac{1}{\sigma^2} X$$) 새로운 확률 변수 $$Y$$의 분산은 다음과 같다.  

<div class="math-container">
$$
Var(Y) = Var\left(\frac{1}{\sigma^2} X\right) = \left(\frac{1}{\sigma^2}\right)^2 Var(X) = \frac{1}{\sigma^4} \times \sigma^2 = \mathbf{\frac{1}{\sigma^2}}
$$  
</div>


분산이 1이 되지 않고, 오히려 정밀도 값 자체가 되었다.  
이번엔 정밀도의 제곱근(표준편차의 역수)를 곱해보자($$Y = \frac{1}{\sigma} X$$):  

<div class="math-container">
$$
Var(Y) = Var\left(\frac{1}{\sigma} X\right) = \left(\frac{1}{\sigma}\right)^2 Var(X) = \frac{1}{\sigma^2} \times \sigma^2 = \mathbf{1}
$$  
</div>


이는 다변수에서도 동일하게 적용된다. 행렬 곱의 공분산을 구하는 공식은 $$Cov(AX) = A \cdot Cov(X) \cdot A^T$$이다.  
초기 데이터 $$X$$의 공분산 행렬은 $$\Sigma$$이다. 이때 새 확률 변수 $$Y$$의 공분산 행렬이 $$I$$가 되게 만드는게 목표이다.  
만약 데이터에 $$\Sigma^{-1}$$를 직접 곱하는 경우($$Y = \Sigma^{-1} X$$)  

<div class="math-container">
$$
Cov(Y) = Cov(\Sigma^{-1} X) = \Sigma^{-1} \cdot Cov(X) \cdot (\Sigma^{-1})^T
$$  
</div>


$$\Sigma$$는 대칭 행렬이므로 역행렬의 전치 행렬은 자기 자신과 같다$$( (\Sigma^{-1})^T = \Sigma^{-1} )$$  

<div class="math-container">
$$
Cov(Y) = \Sigma^{-1} \cdot \Sigma \cdot \Sigma^{-1} = I \cdot \Sigma^{-1} = \mathbf{\Sigma^{-1}}
$$  
</div>


확률 변수 $$Y$$의 공분산은 $$I$$가 아니라 $$\Sigma^{-1}$$이 된다.  
$$W^TW = \Sigma^{-1}$$를 만족하는 $$W$$를 곱해보자($$Y = W X$$). 이때 $$W = \Sigma^{-1/2}$$는 대칭행렬이다.  

<div class="math-container">
$$
Cov(Y) = Cov(WX) = W \cdot Cov(X) \cdot W^T = \Sigma^{-1/2} \cdot \Sigma \cdot \Sigma^{-1/2}
$$  
</div>



<div class="math-container">
$$
Cov(Y) = \Sigma^{-1/2} \cdot \Sigma^{1/2} \cdot \Sigma^{1/2} \cdot \Sigma^{-1/2} = I \cdot I = \mathbf{I}
$$  
</div>


또한 이 형태는 다변량 가우시안 분포의 지수항에서 볼 수 있다.  

<div class="math-container">
$$
\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma}) \propto \exp\left( -\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu}) \right)
$$  
</div>


가우시안 확률 분포가 계산하는 확률 값이라는 것은, "데이터의 맥락(공분산)을 고려하여 공간을 왜곡한 뒤, 중심으로부터 측정한 유클리드 거리(마할라노비스 거리)가 얼마나 먼가?"를 재는 것이다.  



<div class="obsidian-callout" markdown="1">
$$\to$$ 정밀도 행렬을 곱함으로써 일변수 가우시안에서 단위를 제거한 것의 연산이 이루어지는가?  

일변수(1D) 정규분포에서 우리가 거리를 잴 때, 단위를 없애기 위해 값에서 평균을 빼고 '표준편차($$\sigma$$)'로 나눈다.  

<div class="math-container">
$$
z = \frac{x - \mu}{\sigma}
$$  
</div>


이 거리를 제곱하면 다음과 같다.  

<div class="math-container">
$$
z^2 = (x - \mu)^2 \frac{1}{\sigma^2}
$$  
</div>


여기서 $$\frac{1}{\sigma^2}$$이 바로 1차원에서의 정밀도이다. 즉, 거리를 잴 때 정밀도를 곱해준다는 것은 분산(단위의 크기)을 1로 만드는, 즉 단위를 제거(무차원 물리 상수: 무차원량인 물리 상수, 즉 단위가 없어 단위에 무관하게 같이 같은 수이다)하여 통계적 거리만 남기는 연산이다.  

다변수 공간의 마할라노비스 거리를 구할 때($$D^2 = (\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})$$) 정밀도 행렬 $$\boldsymbol{\Sigma}^{-1}$$이 이와 같다.  
</div>





<div class="obsidian-callout" markdown="1">
$$\to$$ 상관관계를 제거한다는 것은 공분산행렬의 고유벡터축으로 회전한다는 것인가?  

정밀도 행렬로 공간을 변환하려 상관관계를 제거하고 단위를 제거하는 과정(백색화)은 고유값 분해로 해석할 수 있다.  

공분산 행렬 $$\boldsymbol{\Sigma}$$는 대칭 행렬이므로, 직교 행렬(고유벡터, $$\mathbf{Q}$$)과 대각 행렬(고윳값, $$\boldsymbol{\Lambda}$$)로 분해할 수 있다. $$\boldsymbol{\Sigma} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^\top$$ 따라서 이 공간을 '원상 복구'시키는 정밀도 행렬의 제곱근 변환($$\boldsymbol{\Sigma}^{-1/2}$$)은 다음과 같다.  

<div class="math-container">
$$
\boldsymbol{\Sigma}^{-1/2} = \mathbf{Q} \boldsymbol{\Lambda}^{-1/2} \mathbf{Q}^\top
$$  
</div>


위 예시($$y=x$$ 축으로 퍼져있는 데이터 분포)에서 $$y=x$$ 방향으로 비스듬하게 퍼져있는 데이터 전체를 돌려서($$\mathbf{Q}^\top$$), 각 축에 대해 독립적인 1차원 분산(고윳값 $$\lambda$$)의 제곱근($$1/\sqrt{\lambda}$$)을 곱한다($$\boldsymbol{\Lambda}^{-1/2}$$, 단위 제거 및 스케일링). 이후 다시 원래 축 방향으로 회전시킨다($$\mathbf{Q}$$).  
</div>





<div class="obsidian-callout" markdown="1">
$$\to$$ 공분산 행렬 $$\boldsymbol{\Sigma}$$의 고윳값들이 내림차순으로 정렬되어 있다고 하자.  

<div class="math-container">
$$
\lambda_1 > \lambda_2 > \lambda_3 > \dots > \lambda_n
$$  
</div>


정밀도 행렬 $$\boldsymbol{\Sigma}^{-1}$$의 고윳값은 원래 고윳값의 역수인 $$1/\lambda$$이므로, 위 부등호의 방향은 반대가 된다.  

<div class="math-container">
$$
\frac{1}{\lambda_1} < \frac{1}{\lambda_2} < \frac{1}{\lambda_3} < \dots < \frac{1}{\lambda_n}
$$  
</div>


공분산의 관점에서 $$\lambda_1$$은 데이터가 이 고유벡터 방향으로 가장 넓게 퍼져 있다는 뜻이다. 즉, 이 방향의 정보가 가장 불확실하다는 것을 의미한다. PCA에서 이를 첫 번째 주성분이라 부른다.  

정밀도의 관점에서 $$1/\lambda_1$$은 어떤 '확신의 강도'라고 볼 수 있다. 데이터가 사방으로 흩어져 있어 가장 불확실한 방향이므로, 이 방향에 대해서 우리가 가질수 있는 확신이 가장 작을 수밖에 없다.  

반대로 $$\lambda_n$$에 대응되는 고유벡터 방향으로 데이터의 분산이 거의 0에 가깝다.  

이또한 정밀도의 관점에서 보았을 때 $$1/\lambda_n$$는 가장 큰 고윳값이며, 데이터가 아주 좁은 범위에 밀집해 있으므로, 이 방향에 대해 가장 강력하게 확신할 수 있다.  
</div>





<div class="obsidian-callout" markdown="1">
$$\to$$ 공분산행렬을 분해했을 때 얻어지는 고유벡터 행렬($$\mathbf{Q}$$)과 정밀도 행렬을 분해했을 때 얻는 고유벡터 행렬($$\mathbf{Q}$$)은, '고유벡터의 집합'자체는 동일하지만, 고유값의 순서가 역전되었으므로 고유벡터의 순서또한 그에 맞게 배치되어야 한다.  
</div>





<div class="obsidian-callout" markdown="1">
정밀도를 곱하는 것이 어떻게 분산을 1로 만드는 것인가?  
</div>





<div class="obsidian-callout" markdown="1">
변수 간 조건부 독립이 성립하는 무차원 표준 공간이란 무엇인가?  
</div>





<div class="obsidian-callout" markdown="1">
가우시안 분포는 그럼 애초에 각 변수간의 상관관계를 제거한 확률분포인가?  
</div>



아래 영상은 공분산행렬과 정밀도 행렬이 2차원 직교좌표계를 어떻게 변환하는지 나타낸 것이다. 공분산행렬이 곱해진   
<video controls class="img-normal" width="500"><source src="{{ site.baseurl }}/assets/notes/linear-algebra/stablecovarianceinverse.mp4" type="video/mp4">Your browser does not support the video tag.</video>




<div class="obsidian-callout" markdown="1">
데이터와 평균과의 차이를 어떤 벡터 $$\boldsymbol{d} := \boldsymbol{x} - \boldsymbol{\mu}$$라고 했을 때, 아래 이차형식은 어떤 의미를 가지는가?  

<div class="math-container">
$$
D^2 = \boldsymbol{d}^\top \boldsymbol{\Sigma}^{-1} \boldsymbol{d}
$$  
</div>


또, 이 이차형식에서 $$\boldsymbol{d}$$에 대한 1차 도함수와 2차 도함수(헤시안)가 가지는 의미는 무엇인가?  

가우시안 분포의 로그 우도 $$\log p(\boldsymbol{x})$$를 미분한 스코어 함수는 $$-\boldsymbol{\Sigma}^{-1}\boldsymbol{d}$$이다? -> 현재 위치에서 확률 밀도가 가장 높아지는 방향(데이터 매니폴드로 돌아가는 힘)을 나타내는 그래디언트이다.  
</div>




Reference  
[마할라노비스거리](https://angeloyeo.github.io/2022/09/28/Mahalanobis_distance.html). 공돌이의 수학정리노트  
[wikipedia](https://en.wikipedia.org/wiki/Whitening_transformation)
