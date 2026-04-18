---
layout: sidebar
title: 두 행렬의 곱
collection_name: notes
nav_order: 1006
---

서로 다른 두 행렬 $$A, B$$이 다음과 같다.  

<div class="math-container">
$$
A=\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B=\begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$  
</div>


이때 두 행렬의 곱 $$AB$$를 정의하면 다음과 같다.  

<div class="math-container">
$$
AB=\begin{bmatrix} 1 \cdot a + 2 \cdot c \quad 1 \cdot b + 2 \cdot d \\ 3 \cdot a + 4 \cdot c \quad 3 \cdot b + 4 \cdot d\end{bmatrix}
$$  
</div>


AB의 첫 열만 볼때, 이를 $$A$$의 행벡터와 $$B$$의 열벡터의 내적으로 표현할 수 있다.  

<div class="math-container">
$$
A\mathbf{b}_1 = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \begin{bmatrix} a \\ c \end{bmatrix} = \begin{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix}\begin{bmatrix} a \\ c \end{bmatrix}  \\ \begin{bmatrix} 3 & 4 \end{bmatrix}\begin{bmatrix} a \\ c \end{bmatrix} \end{bmatrix}
$$  
</div>


다른 관점으로는, A의 열벡터의 선형결합으로 표현할 수 있다.  

<div class="math-container">
$$
A\mathbf{b}_1 = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}\begin{bmatrix} a \\ c \end{bmatrix} = a\begin{bmatrix} 1 \\ 3 \end{bmatrix} + c\begin{bmatrix} 2 \\ 4 \end{bmatrix}
$$  
</div>


이를 기하학적으로 생각한다면 표준 기저를 $$\begin{bmatrix} 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1\end{bmatrix}$$으로 가지는 2차원 좌표계를 변환 B와 A를 적용시켜 변형된 좌표계를 생각할 수 있다.  

---  

두 행렬 $$A$$와 $$B$$의 곱 연산 $$AB$$을 어떻게 보느냐에 따라 다르게 해석될 수 있다.  

먼저 다음과 같은 두 $$2 \times 2$$ 행렬 $$A, B$$를 가정한다.  

<div class="math-container">
$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$  
</div>


## 1. 행과 열의 내적 (Inner Product) 관점: 데이터의 투영

행렬 $$AB$$의 각 원소는 $$A$$의 행벡터와 $$B$$의 열벡터 간의 내적으로 정의된다. 행렬 $$AB$$의 1열을 $$A$$의 행벡터를 기준으로 전개하면 다음과 같다.  

<div class="math-container">
$$
A\mathbf{b}_1 = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \begin{bmatrix} a \\ c \end{bmatrix} = \begin{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix} \begin{bmatrix} a \\ c \end{bmatrix} \\ \begin{bmatrix} 3 & 4 \end{bmatrix} \begin{bmatrix} a \\ c \end{bmatrix} \end{bmatrix} = \begin{bmatrix} 1 \cdot a + 2 \cdot c \\ 3 \cdot a + 4 \cdot c \end{bmatrix}
$$  
</div>


기하학적으로 내적은 한 벡터를 다른 벡터의 축으로 정사영(Orthogonal Projection)하여 성분의 크기를 추출하는 연산이다. 따라서 이 관점에서 행렬 곱은 **'$$B$$의 열벡터들이 $$A$$의 행공간에서 어떠한 좌표값을 가지는가'**를 측정하는 투영 연산으로 해석된다.  

## 2. 열벡터의 선형 결합 (Linear Combination) 관점: 공간의 생성

동일한 행렬 곱 $$A\mathbf{b}_1$$을 $$A$$의 열벡터(Column Vector)를 기준으로 묶어 분해하면 다음과 같은 수식이 도출된다.  

<div class="math-container">
$$
A\mathbf{b}_1 = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \begin{bmatrix} a \\ c \end{bmatrix} = a \begin{bmatrix} 1 \\ 3 \end{bmatrix} + c \begin{bmatrix} 2 \\ 4 \end{bmatrix}
$$  
</div>


이 수식은 행렬 곱의 결과 벡터가 행렬 $$A$$를 구성하는 열벡터들의 선형 결합(Linear Combination)임을 증명한다. 이때 행렬 $$B$$의 원소 $$a, c$$는 각 열벡터의 스케일을 결정하는 가중치(Weight)로 작동한다.  

결과적으로 행렬 $$AB$$의 모든 열벡터는 행렬 $$A$$의 열공간(Column Space, $$C(A)$$)에 종속된다. 이 관점은 데이터 차원 축소나 해의 존재 여부를 판별하는 랭크(Rank)의 개념을 정의하는 대수적 기반이다.  

## 3. 기하학적 관점: 선형 변환의 합성 (Composition of Transformations)

행렬은 어떤 벡터 공간을 다른 벡터 공간으로 매핑하는 선형 변환(Linear Transformation) 함수 $$T(\mathbf{x}) = W\mathbf{x}$$와 동치이다. 임의의 벡터 $$\mathbf{x}$$에 대한 두 행렬의 곱 $$(AB)\mathbf{x}$$는 결합법칙에 의해 $$A(B\mathbf{x})$$로 연산할 수 있다.  

이는 표준 기저 벡터 $$\begin{bmatrix} 1 \ 0 \end{bmatrix}, \begin{bmatrix} 0 \ 1 \end{bmatrix}$$로 이루어진 초기 좌표계에 대해, 다음의 순차적 변환이 발생함을 의미한다.  

1. 행렬 $$B$$가 적용되어 공간을 1차적으로 변형시킨다. ($$B\mathbf{x}$$)  
    
2. 변형된 해당 좌표계 위에 다시 행렬 $$A$$가 적용되어 2차 변형을 가한다. ($$A(B\mathbf{x})$$)  
    

즉, 행렬의 곱 $$AB$$는 서로 다른 두 공간 변환 과정 $$B$$와 $$A$$를 하나의 단일 변환 행렬로 병합하는 함수의 합성(Composition)이다. 행렬 곱의 교환법칙이 성립하지 않는 이유($$AB \neq BA$$) 역시, 축을 변환하는 순서가 달라지면 최종 도달하는 기하학적 좌표 공간이 일치하지 않기 때문이다.  

이러한 함수의 합성 관점은 딥러닝 신경망에서 레이어를 깊게 쌓는 행위($$Layer_2(Layer_1(\mathbf{x}))$$)가 수학적으로 다수의 가중치 행렬을 연속적으로 곱하는 선형 변환의 합성임을 뜻한다.
