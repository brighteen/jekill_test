layout: page
title: 머신러닝 노트 목록
permalink: /notes/머신러닝/
---

# 🤖 머신러닝 지식 저장소

이 섹션에 저장된 모든 강의 및 학습 노트들의 리스트입니다.

{% assign notes = site.notes | where_exp: "note", "note.path contains '머신러닝/'" %}
<ul>
  {% for note in notes %}
    {% if note.title != "머신러닝 노트 목록" %}
      <li>
        <a href="{{ site.baseurl }}{{ note.url }}">{{ note.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>

---
[🏠 홈으로 돌아가기]({{ site.baseurl }}/)
