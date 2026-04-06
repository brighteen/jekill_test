---
layout: sidebar
title: 최대 우도 추정(수정)
collection_name: notes
---

maximum likelihood estimation(MLE)  

데이터가 i.i.d.라고 가정하면 다음과 같이 각 데이터들끼리 상호 독립이며 같은 분포에서 발생했다고 말할 수 있다.  
<div class="math-container" markdown="1">
$$
p(\boldsymbol{x}_1, \dots, \boldsymbol{x}_N) = \prod_{i=1}^N p(\boldsymbol{x}_i)
$$  
</div>
언더플로우를 방지하기 위해 위 식에 로그를 씌우면:  
<div class="math-container" markdown="1">
$$
\log p(\boldsymbol{x}_1, \dots, \boldsymbol{x}_N) = \log \left( \prod_{i=1}^N p(\boldsymbol{x}_i) \right) = \sum_{i=1}^N \log p(\boldsymbol{x}_i)
$$  
</div>
i.i.d.를 가정함으로써 도출된 하나의 $$p(x)$$에 로그를 씌워 로그 우도함수를 만들고, 이를 최대화한다는건, $$p(x|\theta)$$에서 임의의 파라미터$$\theta$$가 주어졌을 때(=확률 분포를 알고 있을 때) 관측된 데이터 $$x$$가 그 분포에서 나왔을 가능도(확률 밀도)를 가장 높게 만들어주는 파라미터 $$\theta$$를 찾아내는 과정이다.  
<div class="math-container" markdown="1">
$$
\hat{\boldsymbol{\theta}}_{\text{MLE}} = \underset{\boldsymbol{\theta}}{\arg\max} \sum_{i=1}^{N} \log p(\boldsymbol{x}_i \mid \boldsymbol{\theta})
$$  
</div>
위 식은 확률 밀도 함수의 면적을 구하는게 아닌 각각의 확률 밀도에 로그를 씌운 총합을 최대화하는 $$\theta$$를 찾는 과정이다.
