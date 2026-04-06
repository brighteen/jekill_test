#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, yaml, urllib.parse
from pathlib import Path

REPO  = Path(__file__).parent
ASSETS = REPO / 'assets'
BASE_URL = '{{ site.baseurl }}'
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
ASSETS_MAP = {} # 원본파일명 -> 변환된파일명 매핑

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
}

# ─── 상수 설정 ─────────────────────────────────────────────────────────────
MML_CHAPTERS = [
    '1. Introduction and Motivation',
    '2. Linear Algebra',
    '3. Analytic Geometry',
    '4. Matrix Decompositions',
    '5. Vector Calculus',
    '6. Probability and Distributions',
    '7. Continuous Optimization',
]
MML_SRC = REPO / 'MML' / 'Part I Mathematical Foundations'
MML_DST = REPO / '_mml' / 'Part I Mathematical Foundations'

NOTES_CONFIGS = [
    {'src': REPO / 'Note' / '1.linear-algebra',          'dst': REPO / '_notes' / '1.linear-algebra', 'col': 'notes'},
    {'src': REPO / 'Note' / '2.calculus',                'dst': REPO / '_notes' / '2.calculus', 'col': 'notes'},
    {'src': REPO / 'Note' / '3.probability-statistics', 'dst': REPO / '_notes' / '3.probability-statistics', 'col': 'notes'},
    {'src': REPO / 'Note' / '4.machine-learning',        'dst': REPO / '_notes' / '4.machine-learning', 'col': 'notes'},
    {'src': REPO / 'Note' / '5.generative-models',       'dst': REPO / '_notes' / '5.generative-models', 'col': 'notes'},
    {'src': REPO / 'Research',                           'dst': REPO / '_research', 'col': 'research'},
]

# ─── 헬퍼 함수 ─────────────────────────────────────────────────────────────
def strip_date_prefix(filename: str) -> str:
    return re.sub(r'^\d{6}\s+', '', filename)

def get_english_name(stem: str) -> str:
    clean = re.sub(r'^\d{6}\s+', '', stem)
    return KOREAN_TO_ENG.get(clean, clean)

def sanitize_asset_name(name: str, prefix: str = "") -> str:
    """파일명의 한글/특수문자/공백을 안전한 ASCII로 변환"""
    stem = Path(name).stem
    ext = Path(name).suffix.lower()
    
    # 1. 날짜 접두사 제거
    clean = re.sub(r'^\d{6}\s+', '', stem)
    
    # 2. 매핑 테이블 확인
    eng_name = KOREAN_TO_ENG.get(clean, clean)
    
    # 3. 특수문자 및 공백 처리 (안전한 ASCII화)
    # 한글이 포함된 경우 (매핑에 없는 경우) 최소한의 안전문자만 남김
    if any(ord(c) > 127 for c in eng_name):
        # 한글 보존: 공백과 특수문자만 '-'로 치환
        safe = re.sub(r'[\s\(\)\[\]\{\}\=,]', '-', eng_name)
    else:
        # 영어인 경우: ASCII 필터링
        safe = re.sub(r'[^a-zA-Z0-9]', '-', eng_name).lower()
        
    safe = re.sub(r'-+', '-', safe).strip('-')
    
    # 만약 safe가 비어버린다면 (한글 제거 등으로 인해) 폴백 생성
    if not safe:
        safe = "image-" + urllib.parse.quote(clean).replace('%', '')[:10].lower()
    
    final_name = f"{prefix}{safe}{ext}" if prefix else f"{safe}{ext}"
    return final_name

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
                    
            # MML 섹션 번호 (예: 7.1)
            m = re.match(r'^(\d+\.\d+)', md.stem)
            if m:
                if m.group(1) not in notes_map:
                    notes_map[m.group(1)] = f'{url_prefix}/{url}'
            
            # MML 챕터 (예: 7.)
            m_ch = re.match(r'^(\d+)\.', md.stem)
            if m_ch and m_ch.group(1) not in notes_map:
                notes_map[m_ch.group(1)] = f'{url_prefix}/{url}'
                
    return notes_map

# ─── 마크다운 변환 핵심 로직 ─────────────────────────────────────────────────
def transform(content: str, file_path: Path, notes_map: dict, col_name: str) -> str:
    title = file_path.stem
    # 영문 이름으로 바뀌었을 경우 실제 제목(title)은 한글 타이틀 유지
    for kor, eng in KOREAN_TO_ENG.items():
        if eng == title:
            title = kor
            break

    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        body = content[fm_match.end():]
    else:
        fm_content = ""
        body = content

    def resolve_target(note_name: str) -> str:
        clean_name = re.sub(r'^\d{6}\s+', '', note_name) # 날짜 접두사 제거
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
            raw_lines[i] = '> ' + line
    body = '\n'.join(raw_lines)

    # 위키 링크 옵시디언 (이미지) 처리
    def rep_img(m):
        txt = m.group(1)
        if '|' in txt:
            raw, width_attr = txt.split('|', 1)
        else:
            raw, width_attr = txt.strip(), None
        raw_name = raw.strip()
        
        # ASSETS_MAP에서 변환된 파일명 찾기, 없으면 실시간 산출
        new_name = ASSETS_MAP.get(raw_name, sanitize_asset_name(raw_name))
        url = f'{BASE_URL}/assets/{new_name}'
        
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
        if path_obj.suffix.lower() in IMG_EXTS:
            new_name = ASSETS_MAP.get(note_name, sanitize_asset_name(note_name))
            return f'![{note_name}]({BASE_URL}/assets/{new_name}){{: .img-normal }}'
            
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
    # 기존에 {: width="300" } 같은 명시적 크기가 있다면 유지하고, 없다면 .img-normal을 부여합니다.
    def rep_final_img(m):
        prefix_str = m.group(1)
        q_prefix = m.group(2)
        alt = m.group(3)
        url = m.group(4)
        attr = m.group(5)
        
        # 이미 URL이 ASCII화 되었거나 외부 링크인 경우 유지하되, 정렬 클래스 주입
        if '://' in url or not any(ord(c) > 127 for c in url):
            if attr:
                clean_attr = attr.strip('{: }').strip()
                return f"{prefix_str}{q_prefix}![{alt}]({url}){{: .img-normal {clean_attr} }}"
            return f"{prefix_str}{q_prefix}![{alt}]({url}){{: .img-normal }}"

        # 한글 경로 등이 포함된 경우 ASSETS_MAP 대조
        filename = Path(url).name
        raw_name = urllib.parse.unquote(filename)
        new_name = ASSETS_MAP.get(raw_name, sanitize_asset_name(raw_name))
        new_url = f'{BASE_URL}/assets/{new_name}'
        
        # 모든 이미지에 .img-normal 클래스를 강제 주입하여 중앙 정렬 보장
        if attr:
            # 기존 속성이 있는 경우 (예: {: width="500" }) .img-normal을 앞에 추가
            clean_attr = attr.strip('{: }').strip()
            new_attr = f'{{: .img-normal {clean_attr} }}'
            return f"{prefix_str}{q_prefix}![{alt}]({new_url}){new_attr}"
        return f"{prefix_str}{q_prefix}![{alt}]({new_url}){{: .img-normal }}"

    body = re.sub(
        r'(^|\n)(>?\s*)!\[(.*?)\]\((.*?)\)(\{:.*?\}|)?',
        rep_final_img,
        body
    )

    # [중요] 인용구(>) 블록화 로직
    # 연속된 > 줄들을 찾아서 하나의 <div class="obsidian-callout" markdown="1"> 로 감쌉니다.
    # 이렇게 하면 내부의 수식/이미지가 박스를 깨트리지 않습니다.
    def group_blockquotes(text):
        new_lines = []
        lines = text.split('\n')
        i = 0
        while i < len(lines):
            if lines[i].lstrip().startswith('>'):
                # 블록 시작
                block = []
                while i < len(lines) and (lines[i].lstrip().startswith('>') or lines[i].strip() == ''):
                    # 만약 중간에 빈 줄이 있고 그 다음 줄이 > 가 아니면 블록 끝
                    if lines[i].strip() == '' and (i+1 >= len(lines) or not lines[i+1].lstrip().startswith('>')):
                        break
                    
                    line = lines[i].lstrip()
                    if line.startswith('>'):
                        content = line[1:].lstrip() # '>' 제거
                        block.append(content)
                    else:
                        block.append('') # 빈 줄 유지
                    i += 1
                
                # 블록 완성
                inner_content = '\n'.join(block).strip('\n')
                new_lines.append(f'\n<div class="obsidian-callout" markdown="1">\n{inner_content}\n</div>\n')
            else:
                new_lines.append(lines[i])
                i += 1
        return '\n'.join(new_lines)

    body = group_blockquotes(body)

    # 블록 수식 ($$) 처리 - markdown="1" 부활 및 Callout 내 중복 방지
    def rep_math(m):
        inner = m.group(1).strip()
        
        # 이미 callout div 작업에서 > 를 떼어냈으므로 여기서 추가 prefix 처리는 불필요함
        return f'\n<div class="math-container" markdown="1">\n$$\n{inner}\n$$\n</div>\n'

    # 수식 정규식도 단순화 - 끝부분 $$ 뒤의 공백(\s*)까지 허용하도록 개선
    body = re.sub(r'(?:\n|^)\s*\$\$(.*?)\$\$\s*(?:\n|$)', rep_math, body, flags=re.DOTALL)

    # 인라인 수식($ ... $)을 ($$ ... $$)로 변환하여 Kramdown의 마크다운 엔진 간섭(기울임표 등) 차단
    # (?<!\$) : 앞에 $가 없을 것
    # (?!\$) : 뒤에 $가 없을 것
    # (.*?) : 수식 내용 (줄바꿈 미포함)
    body = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'$$\1$$', body)

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

    # Liquid 구문 이스케이프
    body = body.replace('{{ site.baseurl }}', '___SITE_BASEURL___')
    body = body.replace('{{', '{{ "{{" }}')
    body = body.replace('{%', '{{ "{%" }}')
    body = body.replace('___SITE_BASEURL___', '{{ site.baseurl }}')

    # Front matter
    fm = {'layout': 'sidebar', 'title': title, 'collection_name': col_name}
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

    print('\n[Step 1] 에셋 준비 및 마크다운 파일 복사 (파일명 영어 치환)')
    newly_copied: list[tuple[Path, str]] = []

    # _mml, _notes, _research 초기화 (깨끗한 상태에서 빌드)
    for col_dir in ['_mml', '_notes', '_research']:
        target = REPO / col_dir
        if target.exists(): shutil.rmtree(target)
    
    # ── 에셋 수집 및 복사 로직 통합 ──
    def process_assets(src_assets_dir: Path, prefix: str = ""):
        if not src_assets_dir.exists(): return
        for f in src_assets_dir.iterdir():
            if f.is_file() and f.suffix.lower() in IMG_EXTS:
                new_fn = sanitize_asset_name(f.name, prefix)
                ASSETS_MAP[f.name] = new_fn
                shutil.copy2(f, ASSETS / new_fn)

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

    # 2. MML 에셋 (MML은 챕터별 assets 폴더 사용)
    for chapter in MML_CHAPTERS:
        src_dir = MML_SRC / chapter
        dst_dir = MML_DST / chapter
        dst_dir.mkdir(parents=True, exist_ok=True)
        # 마크다운 복사
        for f in sorted(src_dir.iterdir()):
            if f.suffix == '.md':
                dst = dst_dir / f.name
                shutil.copy2(f, dst)
                newly_copied.append((dst, 'mml'))
        # 에셋 복사 (mml_ 접두사)
        process_assets(src_dir / 'assets', "mml_")

    # 3. Notes & Research 에셋
    for cfg in NOTES_CONFIGS:
        src, dst_dir, col = cfg['src'], cfg['dst'], cfg['col']
        dst_dir.mkdir(parents=True, exist_ok=True)
        if not src.exists(): continue

        # 마크다운 복사
        for f in sorted(src.iterdir()):
            if f.suffix == '.md':
                e_name = get_english_name(f.stem)
                dst = dst_dir / f'{e_name}.md'
                shutil.copy2(f, dst)
                newly_copied.append((dst, col))
        
        # 에셋 복사 (폴더 번호 추출하여 접두사로 사용)
        # 예: '1.linear-algebra' -> '1_'
        prefix = ""
        m = re.match(r'^(\d+)\.', src.name)
        if m: prefix = f"{m.group(1)}_"
        elif col == 'research': prefix = "res_"
        
        # 서브폴더 내의 모든 assets 폴더 탐색
        for asset_dir in src.rglob('assets'):
            process_assets(asset_dir, prefix)

    # 4. 인덱스 파일들
    mml_index = REPO / 'MML' / 'index.md'
    if mml_index.exists():
        dst = REPO / '_mml' / 'index.md'
        shutil.copy2(mml_index, dst)
        newly_copied.append((dst, 'mml'))

    root_index = REPO / 'index.md'
    if root_index.exists():
        for col in ['notes', 'research']:
            dst = REPO / f'_{col}' / 'index.md'
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root_index, dst)
            newly_copied.append((dst, col))

    print(f'  ✓ {len(newly_copied)}개의 마크다운 파일 복사 완료')

    print('\n[Step 2] 백링크 주소록 맵퍼 생성')
    notes_map = build_notes_map()
    print(f'  ✓ {len(notes_map)}개 노드 연결')

    print('\n[Step 3] 파일 변경 작업 (수식 패치, 인용구 보존, 인코딩된 이미지 매핑)')
    for file_path, col_name in newly_copied:
        try:
            content = file_path.read_text(encoding='utf-8')
            transformed = transform(content, file_path, notes_map, col_name)
            file_path.write_text(transformed, encoding='utf-8')
            # print(f'  ✓ {file_path.relative_to(REPO)}') # 너무 많아서 생략
        except Exception as e:
            print(f'  ✗ {file_path.name}: {e}')

    print('\n' + '=' * 60)
    print('  Migration Complete!')
    print('=' * 60)

if __name__ == '__main__':
    main()
