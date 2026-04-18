#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, yaml, urllib.parse, unicodedata
from pathlib import Path

REPO  = Path(__file__).parent
ASSETS = REPO / 'assets'
BASE_URL = '{{ site.baseurl }}'
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
MEDIA_EXTS = {'.mp4', '.webm', '.mov', '.m4v'}
ASSETS_MAP = {} # 원본파일명 -> 변환된 상대경로

# ─── 영어 파일명 매핑 (작성자가 제안하는 번역 테이블) ─────────────────────────
KOREAN_TO_ENG = {
    '4대 부분공간': 'four-fundamental-subspaces',
    'A의 역행렬을 기본 행렬들의 곱으로 나타내기': 'representing-inverse-as-product-of-elementary-matrices',
    '기본 행 연산의 기하학적 의미': 'geometric-meaning-of-elementary-row-operations',
    '다항식도 벡터이다': 'polynomials-are-also-vectors',
    '두 벡터의 내적은 1x2 행렬의 변환이다.': 'dot-product-as-1x2-matrix-transformation',
    '두 행렬의 곱': 'product-of-two-matrices',
    '딥러닝 모델의 선형 변환이 아핀 변환인 이유': 'why-linear-transformations-in-dl-are-affine',
    '벡터는 왜 원점에 고정되어 있을까': 'why-vectors-are-fixed-to-origin',
    '사상(morphism)': 'morphism',
    '사영': 'projection',
    '삼각함수와 회전행렬': 'trigonometric-functions-and-rotation-matrices',
    '선형대수학을 왜 공부할까': 'why-study-linear-algebra',
    '선형성': 'linearity',
    '양의 정부호': 'positive-definite',
    '왜 제곱근인가': 'why-square-root',
    "왜 제곱'근'인가": 'why-square-root',
    '외적': 'cross-product',
    '이차 형식': 'quadratic-form',
    '전단': 'shear',
    '전진 모드와 후진 모드의 동일함': 'equivalence-of-forward-and-reverse-mode',
    "정답 벡터와 예측 벡터의 차이가 어떻게 '손실'이 되는가": 'how-difference-between-target-and-prediction-becomes-loss',
    '피타고라스 정리': 'pythagorean-theorem',
    '항등행렬 I에 대한 선형 시스템': 'linear-system-for-identity-matrix-i',
    '행공간과 영공간은 항상 수직이다.': 'row-space-and-null-space-are-always-orthogonal',
    "헤시안 행렬이 어떻게 곡률을 '측정'하는가": 'how-hessian-measures-curvature',
    '5. 지수함수의 미분과 오일러 상수 e': '5-derivative-of-exponential-and-euler-e',
    '6. 음함수의 미분': '6-implicit-differentiation',
    '7. 극한': '7-limit',
    '8. 적분(수정)': '8-integral-revised',
    '8. 적분': '8-integral',
    '그래디언트가 항상 가장 가파른 방향을 가리키는 이유': 'why-gradient-points-steepest-direction',
    '미분 상수를 상쇄하는 이유': 'why-cancel-derivative-constant',
    '완전미분방정식의 기하학적 의미': 'geometric-meaning-of-exact-differential-equation',
    '확률이란(수정)': 'what-is-probability-revised',
    '가설 설정과 가설 검정': 'hypothesis-setting-and-testing',
    '누적 분포 함수': 'cumulative-distribution-function',
    '독립 항등 분포': 'independent-identically-distributed',
    '불편추정량(수정중)': 'unbiased-estimator-revising',
    '샘플간의 관계(수정)': 'relationship-between-samples-revised',
    '순열과 조합': 'permutations-and-combinations',
    '중심극한정리(수정)': 'central-limit-theorem-revised',
    '최대 우도 추정(수정)': 'maximum-likelihood-estimation-revised',
    '필요충분조건(수정)': 'necessary-and-sufficient-condition-revised',
    '1차원 비선형 최적화 예제(보완)': '1d-nonlinear-optimization-example-supplement',
    '다중공선성의 기하학적 의미': 'geometric-meaning-of-multicollinearity',
    '다차원 확률 변수의 분산': 'variance-of-multidimensional-random-variable',
    '라그랑주 승수법': 'lagrange-multiplier-method',
    'SDE를 통한 SBM': 'sbm-via-sde',
    '미적분 기초': 'basics-of-calculus',
    '볼츠만 머신': 'boltzmann-machine',
    '생성모델 메모': 'generative-model-memo',
    '위너 과정': 'wiener-process',
    '이토 적분': 'ito-integral',
    '인간의 뇌와 인공지능의 블랙박스는 같은 맥락일까': 'are-human-brain-and-ai-blackbox-similar',
    '기본행렬의 기하학적 의미': 'geometric-meaning-of-elementary-matrix',
    '정밀도 행렬의 기하학적 의미': 'geometric-meaning-of-precision-matrix',
    '피타고라스 정리+Matrix Norm': 'pythagorean-theorem-and-matrix-norm',
    '항등행렬': 'identity-matrix',
    '노이즈와 오차': 'noise-and-error',
    '다중공선성(수정중)': 'multicollinearity-revising',
    '다항 회귀에서의 사전 예측(수정)': 'prior-prediction-in-polynomial-regression-revised',
    '오차 벡터와 손실 함수의 기하학적 의미': 'geometric-meaning-of-error-vector-and-loss-function',
    '확률론에서 합성곱이란': 'what-is-convolution-in-probability',
    'KL Divergence(수정 필요)': 'kl-divergence-needs-revision',
    # 이미지 전용 매핑 추가
    'L1 규제 1': 'l1-regularization-1',
    'L1 규제 2': 'l1-regularization-2',
    '행공간과 영공간의 직교 시각화': 'orthogonal-viz-row-null-space',
    '헤시안 행렬의 기하학적 의미': 'geometric-meaning-of-hessian',
    '예제3.11 시각화': 'viz-example-3-11',
    '좌극한과 우극한이 불일치하는 경우': 'left-right-limit-mismatch',
    '무한대로 발산하는 경우': 'diverging-to-infinity',
    '극한이 존재하지만 연속함수가 아닌 경우': 'limit-exists-not-continuous',
    '다변량 확률 변수의 정사영과 이차 형식의 관계': 'relationship-projection-quadratic-form',
    '대입과 정사영': 'substitution-and-projection',
    '라그랑지안 함수': 'lagrangian-function',
    '쌍대 문제 최대화': 'dual-problem-maximization',
    '원 문제와 제약조건': 'primal-problem-and-constraints',
    '볼츠만 머신 1': 'boltzmann-machine-1',
    '볼츠만 머신 2': 'boltzmann-machine-2',
    'desmos시각화': 'desmos-viz',
    '생성모델': 'generative-models',
}

# ─── 상수 설정 ─────────────────────────────────────────────────────────────
MML_ROOT_SRC = REPO / 'MML'
MML_ROOT_DST = REPO / '_mml'

NOTES_CONFIGS = [
    {'src': REPO / 'Note' / '선형대수',          'dst': REPO / '_notes' / 'linear-algebra', 'col': 'notes', 'order': 1},
    {'src': REPO / 'Note' / '미적분',            'dst': REPO / '_notes' / 'calculus', 'col': 'notes', 'order': 2},
    {'src': REPO / 'Note' / '확률과통계',        'dst': REPO / '_notes' / 'probability-statistics', 'col': 'notes', 'order': 3},
    {'src': REPO / 'Note' / '머신러닝',          'dst': REPO / '_notes' / 'machine-learning', 'col': 'notes', 'order': 4},
    {'src': REPO / 'Note' / '정보이론',          'dst': REPO / '_notes' / 'information-theory', 'col': 'notes', 'order': 5},
    {'src': REPO / 'Note' / '생성모델',          'dst': REPO / '_notes' / 'generative-models', 'col': 'notes', 'order': 6},
    {'src': REPO / 'Research',                   'dst': REPO / '_research', 'col': 'research', 'order': 7},
]

# ─── 헬퍼 함수 ─────────────────────────────────────────────────────────────
def strip_leading_numbers(text: str) -> str:
    """날짜(yymmdd) 또는 순번(01.) 접두사를 제거"""
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'^\d{6}\s+', '', text)
    text = re.sub(r'^\d+\.\s*', '', text)
    return text

def get_english_name(stem: str) -> str:
    clean = strip_leading_numbers(stem)
    return KOREAN_TO_ENG.get(clean, clean)

def sanitize_asset_name(name: str) -> str:
    """파일명의 한글/특수문자/공백을 안전한 ASCII로 변환"""
    name = unicodedata.normalize('NFC', name)
    stem = Path(name).stem
    ext = Path(name).suffix.lower()
    
    clean = strip_leading_numbers(stem)
    eng_name = KOREAN_TO_ENG.get(clean, clean)
    
    # 특수문자 및 공백 처리
    if any(ord(c) > 127 for c in eng_name):
        safe = re.sub(r'[\s\(\)\[\]\{\}\=,]', '-', eng_name)
    else:
        safe = re.sub(r'[^a-zA-Z0-9]', '-', eng_name).lower()
        
    safe = re.sub(r'-+', '-', safe).strip('-')
    if not safe:
        safe = "asset-" + urllib.parse.quote(clean).replace('%', '')[:10].lower()
    
    return f"{safe}{ext}"

def get_assets_map_value(raw_name: str) -> str:
    """ASSETS_MAP에서 유니코드 정규화 및 대소문자 무시하고 매칭되는 경로 반환"""
    if not raw_name: return None
    target = unicodedata.normalize('NFC', raw_name).strip().lower()
    
    # 1. 완전 일치 확인
    if raw_name in ASSETS_MAP: return ASSETS_MAP[raw_name]
    
    # 2. 정규화 및 대소문자 무시 확인
    for k, v in ASSETS_MAP.items():
        if unicodedata.normalize('NFC', k).strip().lower() == target:
            return v
            
    # 3. 확장자 제외 매칭 (사용자 실수 대비)
    target_stem = Path(target).stem
    for k, v in ASSETS_MAP.items():
        if Path(unicodedata.normalize('NFC', k)).stem.strip().lower() == target_stem:
            return v
            
    return None

def build_notes_map() -> dict:
    notes_map = {}
    for coll_dir, url_prefix in [('_notes', 'notes'), ('_mml', 'mml'), ('_research', 'research')]:
        d = REPO / coll_dir
        if not d.exists(): continue
        for md in d.rglob('*.md'):
            rel = md.relative_to(d)
            # 인덱스 파일은 맵퍼에 추가하지 않음 (링크 충돌 방지)
            if md.name == 'index.md': continue

            url = str(rel).replace('.md', '').replace('\\', '/')
            # 영문 치환이 끝난 실제 파일 이름 기반 URL 매핑
            notes_map[md.stem] = f'{url_prefix}/{url}'
            
            # 원래 옵시디언 한글 이름에 대해서도 매핑 생성 (백링크 해석용)
            for kor, eng in KOREAN_TO_ENG.items():
                if eng == md.stem:
                    notes_map[kor] = f'{url_prefix}/{url}'
                    # 혹시 날짜 프리픽스가 붙은 케이스 대응
                    notes_map[f"251219 {kor}"] = f'{url_prefix}/{url}' 
                    break
                    
            
            # MML 섹션 번호 (예: 7.1) 또는 챕터 번호 (예: 7.)
            # MML은 Part 구조로 인해 폴더가 깊으므로 파일명에서 번호를 추출하여 매핑 보강
            m_sec = re.match(r'^(\d+\.\d+)', md.stem)
            if m_sec:
                if m_sec.group(1) not in notes_map:
                    notes_map[m_sec.group(1)] = f'{url_prefix}/{url}'
            
            m_ch = re.match(r'^(\d+)\.', md.stem)
            if m_ch and m_ch.group(1) not in notes_map:
                notes_map[m_ch.group(1)] = f'{url_prefix}/{url}'
                
    return notes_map

# ─── 마크다운 변환 핵심 로직 ─────────────────────────────────────────────────
def transform(content: str, file_path: Path, notes_map: dict, col_name: str, nav_order: int) -> str:
    # 1. 원본 파일명 기반 제목 추출 및 숫자 제거
    raw_stem = file_path.stem
    # _notes/_mml 로 이동하면서 영문 slug가 되었을 수 있으므로 역매핑 확인
    title = raw_stem
    for kor, eng in KOREAN_TO_ENG.items():
        if eng == raw_stem:
            title = kor
            break
    
    # 사이드바 제목에서 숫자 접두사 제거 (사용자 요청)
    title = strip_leading_numbers(title)

    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        body = content[fm_match.end():]
    else:
        fm_content = ""
        body = content

    def resolve_target(note_name: str) -> str:
        clean_name = strip_leading_numbers(note_name) # 접두사 제거
        clean_name = re.sub(r'(절|장)$', '', clean_name).strip()
        if clean_name in notes_map: return f'{BASE_URL}/{notes_map[clean_name]}/'
        if note_name in notes_map: return f'{BASE_URL}/{notes_map[note_name]}/'
        return None

    # 옵시디언의 느슨한 인용구(Lax Blockquote)를 엄격한 인용구로 변환
    # 빈 줄이 나타나기 전까지는 계속 인용구로 간주하여 누락된 > 를 채워 넣습니다.
    raw_lines = body.split('\n')
    in_blockquote = False
    for i, line in enumerate(raw_lines):
        s_line = line.lstrip()
        if s_line.startswith('>'):
            in_blockquote = True
        elif not s_line:
            in_blockquote = False
        elif in_blockquote:
            # 새로운 문단으로 인식되도록 빈 인용 라인 한 줄 추가 후 내용 추가
            raw_lines[i] = '> \n> ' + line
    body = '\n'.join(raw_lines)

    # Liquid 구문 이스케이프 (수식 보호 태그 추가 전에 처리하여 충돌 방지)
    # {% raw %}와 {% endraw %}는 이스케이프 대상에서 제외
    body = body.replace('{{ site.baseurl }}', '___SITE_BASEURL___')
    body = re.sub(r'\{\{(?!\s*site\.baseurl|raw|endraw)', r'{{ "{{" }}', body)
    body = re.sub(r'\{%(?!\s*raw|endraw)', r'{{ "{%" }}', body)
    body = body.replace('___SITE_BASEURL___', '{{ site.baseurl }}')

    # 위키 링크 옵시디언 (이미지) 처리
    def rep_img(m):
        txt = m.group(1)
        if '|' in txt:
            raw, width_attr = txt.split('|', 1)
        else:
            raw, width_attr = txt.strip(), None
        raw_name = unicodedata.normalize('NFC', raw.strip())
        
        # ASSETS_MAP에서 변환된 파일명 찾기 (로버스트 매칭)
        new_path = get_assets_map_value(raw_name)
        if not new_path:
            new_path = sanitize_asset_name(raw_name)
            
        url = f'{BASE_URL}/assets/{new_path}'
        
        # 영상 파일인 경우 <video> 태그 반환
        if Path(new_path).suffix.lower() in MEDIA_EXTS:
            width_val = width_attr if width_attr else "100%"
            return f'<video controls class="img-normal" width="{width_val}"><source src="{url}" type="video/mp4">Your browser does not support the video tag.</video>'

        # 모든 이미지에 .img-normal 클래스를 강제 주입하여 중앙 정렬 보장
        attr = f'{{: .img-normal width="{width_attr}" }}' if width_attr else '{: .img-normal }'
        return f'![{raw_name}]({url}){attr}'
    
    body = re.sub(r'!\[\[(.*?)\]\]', rep_img, body)

    # 마크다운 백링크 처리
    def rep_link(m):
        txt = m.group(1)
        if '|' in txt:
            note_name, alias = txt.split('|', 1)
        else:
            note_name = alias = txt.strip()
            
        note_name = note_name.strip()
        alias = alias.strip()
        
        path_obj = Path(note_name)
        if path_obj.suffix.lower() in IMG_EXTS or path_obj.suffix.lower() in MEDIA_EXTS:
            new_path = get_assets_map_value(note_name)
            if not new_path:
                new_path = sanitize_asset_name(note_name)
                
            url = f'{BASE_URL}/assets/{new_path}'
            if path_obj.suffix.lower() in MEDIA_EXTS:
                return f'<video controls class="img-normal" width="100%"><source src="{url}" type="video/mp4">Your browser does not support the video tag.</video>'
            return f'![{note_name}]({url}){{: .img-normal }}'
            
        url = resolve_target(note_name)
        if url: return f'[{alias}]({url})'
        return f'[{alias}](#)'
    body = re.sub(r'(?<!!)\[\[(.*?)\]\]', rep_link, body)

    # 표준 마크다운 링크 복구
    def rep_mdlink(m):
        alias = m.group(1)
        path_part = m.group(2).strip('<> ')
        if path_part.startswith('{{') or path_part.startswith('http'):
            return m.group(0)
        note_name = Path(path_part).stem.strip()
        url = resolve_target(note_name)
        if url: return f'[{alias}]({url})'
        return m.group(0)
    body = re.sub(r'\[(.*?)\]\((.*?)\)', rep_mdlink, body)

    # 이미지 처리 (순수 마크다운 + 클래스 주입)
    def rep_final_img(m):
        prefix_str = m.group(1)
        q_prefix = m.group(2)
        alt = m.group(3)
        url = m.group(4)
        attr = m.group(5)
        
        # 이미 처리된 URL이거나 외부 링크인 경우 정렬 클래스만 주입
        if '{{ site.baseurl }}' in url or '://' in url:
            if attr:
                clean_attr = attr.strip('{: }').strip()
                if '.img-normal' in clean_attr: return m.group(0)
                return f"{prefix_str}{q_prefix}![{alt}]({url}){{: .img-normal {clean_attr} }}"
            return f"{prefix_str}{q_prefix}![{alt}]({url}){{: .img-normal }}"

        # 한글 경로 등이 포함된 경우 ASSETS_MAP 대조 (로버스트 매칭)
        filename = Path(url).name
        raw_name = urllib.parse.unquote(filename)
        new_path = get_assets_map_value(raw_name)
        if not new_path:
            new_path = sanitize_asset_name(raw_name)
            
        new_url = f'{BASE_URL}/assets/{new_path}'
        
        # 비디오 파일 확장자 체크
        video_exts = ['.mp4', '.webm', '.ogg', '.mov']
        is_video = any(new_url.lower().endswith(ext) for ext in video_exts)

        if is_video:
            return f'<video controls class="img-normal" {attr}><source src="{new_url}" type="video/mp4">Your browser does not support the video tag.</video>'

        # 모든 이미지에 .img-normal 클래스 주입
        if attr:
            clean_attr = attr.strip('{: }').strip()
            return f"{prefix_str}{q_prefix}![{alt}]({new_url}){{: .img-normal {clean_attr} }}"
        return f"{prefix_str}{q_prefix}![{alt}]({new_url}){{: .img-normal }}"

    body = re.sub(
        r'(^|\n)(>?\s*)!\[(.*?)\]\((.*?)\)(\{:.*?\}|)?',
        rep_final_img,
        body
    )

    # [중요] 인용구(>) 블록화 로직
    # 5. 인용구(>)를 Callout 박스로 변환
    def rep_blockquote(m):
        block = m.group(0)
        raw_lines = block.split('\n')
        processed_lines = []
        
        for i, line in enumerate(raw_lines):
            line = line.rstrip()
            if line.startswith('>'):
                processed_lines.append(line)
                # 만약 현재 줄에 내용이 있고, 다음 줄도 내용이 있는 인용구라면 빈 인용 라인 삽입하여 문단 분리
                if line != '>':
                    if i + 1 < len(raw_lines):
                        next_line = raw_lines[i+1].rstrip()
                        if next_line.startswith('>') and next_line != '>':
                            processed_lines.append('>')
            else:
                processed_lines.append(line)
        
        # 2. 각 라인에서 가장 앞의 '>' 한 개를 제거 (중복 인용구 방지)
        final_lines = [re.sub(r'^>\s?', '', line) for line in processed_lines]
        
        inner_content = '\n'.join(final_lines)
        return f'\n\n<div class="obsidian-callout" markdown="1">\n{inner_content}\n</div>\n\n'

    body = re.sub(r'(^>.*(?:\n>.*)*)', rep_blockquote, body, flags=re.MULTILINE)

    # 블록 수식 ($$) 처리
    def rep_math(m):
        inner = m.group(1).strip()
        # 노름 기호 \| 를 \Vert 로 변환 (가장 먼저 처리하여 | 와의 충돌 방지)
        inner = inner.replace('\\|', r'\Vert ')
        # 수식 내의 |를 \vert로 변환 (공백 추가하여 연이은 문자와의 결합 방지)
        inner = inner.replace('|', r'\vert ')
        # markdown="1"을 제거하여 kramdown이 수식 내부의 |를 표 구분자로 오해하지 않게 함
        # kramdown은 $$로 감싸진 내용을 마크다운 엔티티로 처리하지 않으므로 수식 보호가 가능함
        return f'\n\n<div class="math-container">\n$$\n{inner}\n$$\n</div>\n\n'

    body = re.sub(r'(?:\n|^)\s*\$\$(.*?)\$\$\s*(?=\n|$)', rep_math, body, flags=re.DOTALL)

    # 인라인 수식 ($) 처리 -> $ 유지 및 내부 | 보호
    def rep_inline_math(m):
        content = m.group(1)
        # 노름 기호 \| 를 \Vert 로 먼저 변환
        content = content.replace('\\|', r'\Vert ')
        # 인라인 수식 내의 |도 \vert로 변환 (공백 추가)
        content = content.replace('|', r'\vert ')
        # kramdown은 $$로 감싸진 내용을 마크다운 엔티티로 처리하지 않으므로 수식 보호가 가능함
        return f'$${content}$$'
    
    # 1. 인라인 수식 ($) 보호 (매칭 범위를 한 줄(300자)로 제한하여 본문 삼킴 방지)
    body = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]{1,300})(?<!\$)\$(?!\$)', rep_inline_math, body)

    # Hard Wrap - 리스트 내부나 특수태그 앞은 제외
    lines = body.split('\n')
    in_math = in_code = False
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '$$': in_math = not in_math
        if s.startswith('```'): in_code = not in_code
        if not in_math and not in_code and line and not line.endswith('  '):
            if not s.startswith(('<', '![', '#', '>', '- ', '* ')):
                lines[i] = line + '  '
    body = '\n'.join(lines)

    # 6. Front matter
    fm = {'layout': 'sidebar', 'title': title, 'collection_name': col_name, 'nav_order': nav_order}
    if fm_content:
        try:
            existing_fm = yaml.safe_load(fm_content)
            if isinstance(existing_fm, dict): fm.update(existing_fm)
        except: pass

    if file_path.name == 'index.md':
        fm['permalink'] = f'/{col_name}/'
        fm['layout'] = 'sidebar'
        if col_name == 'mml': fm['title'] = 'Mathematics for Machine Learning'
        elif col_name == 'notes':
            fm['title'] = 'Notes'
        elif col_name == 'research':
            fm['title'] = 'Research'

    fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{fm_str}\n---\n\n{body.strip()}\n"

def main():
    print('=' * 60)
    print('  V2 Jekyll Migration')
    print('=' * 60)

    print('\n[Step 1] 에셋 준비 및 마크다운 파일 복사')
    newly_copied: list[tuple[Path, str, int]] = []

    # _mml, _notes, _research 초기화 (깨끗한 상태에서 빌드)
    for col_dir in ['_mml', '_notes', '_research']:
        target = REPO / col_dir
        if target.exists(): shutil.rmtree(target)
    
    # ── 에셋 수집 및 복사 로직 통합 ──
    def process_assets(src_assets_dir: Path, rel_dst_path: Path):
        if not src_assets_dir.exists(): return
        dst_dir = ASSETS / rel_dst_path
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in src_assets_dir.iterdir():
            if f.is_file() and (f.suffix.lower() in IMG_EXTS or f.suffix.lower() in MEDIA_EXTS):
                new_fn = sanitize_asset_name(f.name)
                # ASSETS_MAP에는 assets 폴더로부터의 상대 경로 저장
                rel_path = (rel_dst_path / new_fn).as_posix()
                ASSETS_MAP[unicodedata.normalize('NFC', f.name)] = rel_path
                shutil.copy2(f, dst_dir / new_fn)

    # assets 폴더 초기화 (main.scss 제외)
    if ASSETS.exists():
        for item in ASSETS.iterdir():
            if item.name == 'main.scss': continue
            if item.is_dir(): shutil.rmtree(item)
            else: os.remove(item)
    ASSETS.mkdir(exist_ok=True)

    # 1. 특수 에셋
    for f_name, src_p in [('0_me.png', REPO / 'me.png'), ('mml_cover.png', REPO / 'MML' / 'MML.png')]:
        if src_p.exists():
            shutil.copy2(src_p, ASSETS / f_name)
            ASSETS_MAP[src_p.name] = f_name

    # 2. MML 에셋 및 문서 (Part I, II 등 모든 Part 자동 탐색)
    if MML_ROOT_SRC.exists():
        mml_parts = [d for d in sorted(MML_ROOT_SRC.iterdir()) if d.is_dir() and d.name.startswith('Part')]
        for p_idx, part_dir in enumerate(mml_parts, 1):
            print(f'  -> Processing {part_dir.name}...')
            # 파트 번호 추출 (Part I -> part1)
            part_tag = f"part{p_idx}"
            
            src_chapters = [d for d in sorted(part_dir.iterdir(), key=lambda x: [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', x.name)]) if d.is_dir()]
            for c_idx, src_chapter_dir in enumerate(src_chapters, 1):
                print(f'    [Chapter] {src_chapter_dir.name}')
                # 장 번호 추출 (예: '1. Intro' -> '1')
                m_ch = re.match(r'^(\d+)\.', src_chapter_dir.name)
                ch_num = m_ch.group(1) if m_ch else str(c_idx)
                        
                rel_asset_path = Path('mml') / part_tag / ch_num
                
                clean_part_name = part_dir.name.strip()
                clean_chapter_name = src_chapter_dir.name.strip()
                dst_chapter_dir = MML_ROOT_DST / clean_part_name / clean_chapter_name
                dst_chapter_dir.mkdir(parents=True, exist_ok=True)
                
                # 마크다운 파일 복사
                for f_idx, f in enumerate(sorted(src_chapter_dir.iterdir()), 1):
                    if f.is_file() and f.suffix == '.md':
                        clean_name = f.name.strip()
                        dst = dst_chapter_dir / clean_name
                        shutil.copy2(f, dst)
                        # MML nav_order: 100000 + (Part*1000) + (Chapter*100) + FileIndex
                        order = 100000 + (p_idx * 1000) + (c_idx * 100) + f_idx
                        newly_copied.append((dst, 'mml', order))
                
                # 에셋 복사 (각 장의 assets 폴더)
                process_assets(src_chapter_dir / 'assets', rel_asset_path)

    # 3. Notes & Research 에셋
    for cfg in NOTES_CONFIGS:
        src, dst_dir, col, folder_order = cfg['src'], cfg['dst'], cfg['col'], cfg['order']
        dst_dir.mkdir(parents=True, exist_ok=True)
        if not src.exists(): continue

        # 마크다운 복사
        for f in sorted(src.iterdir()):
            if f.suffix == '.md':
                # 파일명에서 숫자 접두사 추출 (nav_order 활용)
                m_num = re.match(r'^(\d+)\.', f.name)
                f_idx = int(m_num.group(1)) if m_num else 999
                
                e_name = get_english_name(f.stem)
                dst = dst_dir / f'{e_name}.md'
                shutil.copy2(f, dst)
                # Notes nav_order: (FolderOrder * 1000) + FileIndex
                order = (folder_order * 1000) + f_idx
                newly_copied.append((dst, col, order))
        
        # 에셋 복사 (구조화된 경로 사용 - 영문 폴더명 사용으로 주소 안정성 확보)
        rel_asset_path = Path(col) / dst_dir.name
        for asset_dir in src.rglob('assets'):
            process_assets(asset_dir, rel_asset_path)

    # 4. 인덱스 파일들
    mml_index = REPO / 'MML' / 'index.md'
    if mml_index.exists():
        dst = REPO / '_mml' / 'index.md'
        shutil.copy2(mml_index, dst)
        newly_copied.append((dst, 'mml', 100000))

    root_index = REPO / 'index.md'
    if root_index.exists():
        for col in ['notes', 'research']:
            dst = REPO / f'_{col}' / 'index.md'
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root_index, dst)
            newly_copied.append((dst, col, 0))

    print(f'  [OK] {len(newly_copied)} 마크다운 파일 복사 완료')

    print('\n[Step 2] 백링크 주소록 맵퍼 생성')
    notes_map = build_notes_map()
    print(f'  [OK] {len(notes_map)}개 노드 연결')

    print('\n[Step 3] 파일 변경 작업')
    processed_files = set()
    for file_path, col_name, nav_order in newly_copied:
        if file_path in processed_files: continue
        try:
            content = file_path.read_text(encoding='utf-8')
            transformed = transform(content, file_path, notes_map, col_name, nav_order)
            file_path.write_text(transformed, encoding='utf-8')
            processed_files.add(file_path)
            # print(f'  ✓ {file_path.relative_to(REPO)}') # 너무 많아서 생략
        except Exception as e:
            print(f'  ✗ {file_path.name}: {e}')

    print('\n' + '=' * 60)
    print('  Migration Complete!')
    print('=' * 60)

if __name__ == '__main__':
    main()
