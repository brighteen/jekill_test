---
layout: sidebar
title: 피타고라스 정리+Matrix Norm
collection_name: notes
nav_order: 1099
---

밑변이 $$a,$$ 높이가 $$b$$, 빗변이 $$c$$인 직각삼각형을 떠올려보자. 피타고라스는 임의의 직각삼각형이 $$a^2+b^2=c^2$$를 만족한다고 한다. 이는 한 변을 각각 $$a,b$$인 두 정사각형의 넓이의 합이 한 변의 길이가 $$c$$인 정사각형의 넓이와 같다는 말이다.  

$$a+b$$를 한 변으로 가지는 임의의 정사각형과 그 정사각형 내부에 한 변의 길이가 $$c$$인 정사각형의 꼭짓점을 네 변와 접하는 상황을 생각해보자. 큰 정사각형 내부는 직각삼각형 4개와 작은 정사각형 하나로 쪼개진다. 이를 다음과 같이 표현할 수 있다.  

<div class="math-container">
$$
(a+b)^2 = c^2 + 4 \cdot \frac{1}{2}ab
$$  
</div>


양 변을 정리하면 다음과 같다.  

<div class="math-container">
$$
a^2+2ab+b^2 = c^2+2ab
$$  
</div>


따라서 다음 결론이 도출된다.  

<div class="math-container">
$$
a^2+b^2=c^2
$$  
</div>


# Matrix Norm
행렬의 Norm은 다음과 같이 정의된다.  

<div class="math-container">
$$
\Vert A\Vert _2 = \sup_{\Vert x\Vert _2=1} \Vert Ax\Vert _2
$$  
</div>


sum(Supremum)은 '상한'이라는 뜻으로, 길이가 1인 벡터 $$x$$를 행렬 $$A$$로써 변환했을 때, 그 상($$Ax$$)의 길이가 최대 얼마나 길어지는가를 묻는 것이다. 이는 [정의 4.23]({{ site.baseurl }}/mml/Part I Mathematical Foundations/4. Matrix Decompositions/4.6 Matrix Approximation/)에서 $$x$$의 크기가 1인 특별한 경우를 다룬다.  

이를 내적 형태로 바꾸면 다음과 같다:  

<div class="math-container">
$$
= \sup_{\Vert x\Vert _2=1} (x^\top A^\top A x)^{\frac{1}{2}}
$$  
</div>


$$A^\top A$$는 대칭 행렬이므로 항상 직교 행렬로 고유값 분해가 가능하다:  

<div class="math-container">
$$
= \sup_{\Vert x\Vert _2=1} (x^\top Q^\top \Lambda Q x)^{\frac{1}{2}}
$$  
</div>


$$Q$$는 직교행렬($$Q^{\top}Q=I, q_i^{\top}q_i=1$$, 각 벡터들이 orthonormal하기 때문에 엄밀하게는 정규 직교 행렬이다)이기 때문에 $$\Vert Qx\Vert $$는 여전히 1이다. $$\Lambda$$는 대각 성분이 고유값인 대각 행렬이다. $$y = Qx$$로 치환하면:  

<div class="math-container">
$$
= \sup_{\Vert y\Vert _2=1} (y^\top \Lambda y)^{\frac{1}{2}} \quad \text{for } y = Qx
$$  
</div>


이 식은 $$\sqrt{y^\top \Lambda y}$$으로 쓸 수 있으며, $$\Lambda$$는 대각 행렬이므로 풀어서 쓰면 다음과 같다:  

<div class="math-container">
$$
\sqrt{\lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2}
$$  
</div>


여기서 $$y$$는 길이가 1인 벡터($$y_1^2 + \dots + y_n^2 = 1$$)이다. 이때 이 값을 최대로 만들려면 가장 큰 고유값($$\lambda_{\max}$$)에 해당하는 성분($$y_i$$)에 가중치를 1로 두고 나머지를 0으로 만들면 된다. 그럼 최대값은 $$\sqrt{\lambda_{\max}}$$가 된다. $$A^\top A$$의 고유값($$\lambda$$)의 제곱근은 $$A$$의 특이값($$\sigma$$)이므로 결국 최대값은 $$\sigma_{\max}(A)$$이며 이는 $$\sigma_{1}$$이다.  


왜 행렬의 노름(Norm)을 입력 대비 출력의 최대 비율로 정의했을까?  
가장 중요한 수학적 이유는 모든 벡터에 대해 성립하는 부등식을 만들기 위함이다. 우리가 행렬 $$A$$의 크기를 $$\Vert A\Vert $$라고 정의했을 때, "출력($$Ax$$)의 크기는 절대로 입력($$x$$) 크기의 $$\Vert A\Vert $$배를 넘지 않는다"를 다음과 같이 정의할 수 있다.  

<div class="math-container">
$$
\Vert Ax\Vert  \le \Vert A\Vert  \Vert x\Vert 
$$  
</div>


만약 $$\Vert A\Vert $$을 평균값으로 정의한다면, 어떤 벡터는 평균보다 많이 늘어날 수 있다. 그러면 위 부등식이 깨지게 되고, 이 시스템이 가지는 변환의 크기를 모르는 불확실성을 안게 된다.  
$$\Vert A\Vert $$를 최대값으로 정의함으로써 임의의 벡터 $$x$$에 대해 그것이 늘어나는 비율은 절대 최대값 $$\Vert A\Vert $$을 넘을 수 없다.  

기하학적 관점에서 보자. 표준 기저 $$x, y$$축을 가지는 2차원 좌표 평면에서 반지름이 1인 단위 원을 생각해보자. 이때 $$A = \begin{bmatrix} 3 & 0 \\ 0 & 0.5 \end{bmatrix}$$이면 단위 원 위의 점들을 $$A$$로 변환했을 때 $$y$$축으로 0.5비율만큼 찌그러지고 $$x$$축으로 3비율만큼 늘어난 타원을 생각할 수 있다. 이를 $$\Vert Ax\Vert  \le \Vert A\Vert  \Vert x\Vert $$에 대입해봤을 때, 크기가 1인 벡터 $$x$$를 변환했을 때($$Ax$$) 그 크기는 최대 $$3x$$를 넘지 않는다. $$A$$가 대칭행렬이므로 고유값분해를 통해 얻은 고유값 중 가장 큰 고유값은 $$\lambda_{1}=3$$이다.
