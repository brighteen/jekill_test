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

# ─── 영어 파일명 매핑 ────────────────────────────────────────────────────────
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
    '로그': 'log',
    '제곱근': 'square-root',
    '열역학 제2법칙': 'second-law-of-thermodynamics',
    'Diffusion 1': 'diffusion-1',
    'Diffusion 2': 'diffusion-2',
    '관련 논문': 'related-papers',
    '디퓨전을 이해하기 위한 개념들': 'concepts-for-diffusion',
    '랑주뱅 동역학': 'langevin-dynamics',
    '브라운 운동': 'brownian-motion',
    '비평형 열역학': 'non-equilibrium-thermodynamics',
    '젠슨 부등식': 'jensens-inequality',
    '엔트로피': 'entropy',
    '정보량': 'information-amount',
    '할루시네이션': 'hallucination',
    '생성모델 메모': 'generative-model-memo',
}

# ─── 상수 설정 ─────────────────────────────────────────────────────────────
MML_ROOT_SRC = REPO / 'MML'
MML_ROOT_DST = REPO / '_mml'

NOTES_CONFIGS = [
    {'src': REPO / 'Note' / '기초',              'dst': REPO / '_notes' / 'basics', 'col': 'notes', 'order': 0},
    {'src': REPO / 'Note' / '선형대수',          'dst': REPO / '_notes' / 'linear-algebra', 'col': 'notes', 'order': 1},
    {'src': REPO / 'Note' / '미적분',            'dst': REPO / '_notes' / 'calculus', 'col': 'notes', 'order': 2},
    {'src': REPO / 'Note' / '확률과통계',        'dst': REPO / '_notes' / 'probability-statistics', 'col': 'notes', 'order': 3},
    {'src': REPO / 'Note' / '머신러닝',          'dst': REPO / '_notes' / 'machine-learning', 'col': 'notes', 'order': 4},
    {'src': REPO / 'Note' / '정보이론',          'dst': REPO / '_notes' / 'information-theory', 'col': 'notes', 'order': 5},
    {'src': REPO / 'GenAI' / 'Foundations',       'dst': REPO / '_genai' / 'foundations', 'col': 'genai', 'order': 6},
    {'src': REPO / 'GenAI' / 'VAE',               'dst': REPO / '_genai' / 'vae', 'col': 'genai', 'order': 7},
    {'src': REPO / 'GenAI' / 'Score Based Model', 'dst': REPO / '_genai' / 'score-based-model', 'col': 'genai', 'order': 8},
    {'src': REPO / 'GenAI' / 'Diffusion',         'dst': REPO / '_genai' / 'diffusion', 'col': 'genai', 'order': 9},
    {'src': REPO / 'Research',                   'dst': REPO / '_research', 'col': 'research', 'order': 10},
]

# ─── 헬퍼 함수 ─────────────────────────────────────────────────────────────
def strip_leading_numbers(text: str) -> str:
    """날짜(yymmdd) 또는 순번(01. ) 접두사를 제거하되, MML 섹션 번호(3.6 등)는 보존"""
    text = unicodedata.normalize('NFC', text)
    # yymmdd 날짜 형식 제거
    text = re.sub(r'^\d{6}\s+', '', text)
    # 단순 리스트형 순번(1. 2. 등) 제거 (단, 1.2 처럼 뒤에 숫자가 오면 유지)
    text = re.sub(r'^\d{1,2}\.(?!\d)\s*', '', text)
    return text.strip()

def get_english_name(stem: str) -> str:
    clean = strip_leading_numbers(stem)
    return KOREAN_TO_ENG.get(clean, clean)

def sanitize_asset_name(name: str) -> str:
    name = unicodedata.normalize('NFC', name)
    ext = Path(name).suffix.lower()
    # 파일명에서 확장자를 제외한 부분만 가져와서 처리
    base_name = Path(name).stem
    eng_name = KOREAN_TO_ENG.get(base_name, base_name)
    # 한글 및 특수문자 제거하고 소문자로 변환
    safe = re.sub(r'[^a-zA-Z0-9]', '-', eng_name).lower()
    safe = re.sub(r'-+', '-', safe).strip('-')
    final_name = safe if safe else 'asset'
    return f"{final_name}{ext}"

def get_assets_map_value(raw_name: str) -> str:
    if not raw_name: return None
    target = unicodedata.normalize('NFC', raw_name).strip().lower()
    if raw_name in ASSETS_MAP: return ASSETS_MAP[raw_name]
    for k, v in ASSETS_MAP.items():
        if unicodedata.normalize('NFC', k).strip().lower() == target: return v
    target_stem = Path(target).stem
    for k, v in ASSETS_MAP.items():
        if Path(unicodedata.normalize('NFC', k)).stem.strip().lower() == target_stem: return v
    return None

def build_notes_map() -> dict:
    notes_map = {}
    for coll_dir, url_prefix in [('_notes', 'notes'), ('_mml', 'mml'), ('_research', 'research'), ('_genai', 'genai')]:
        d = REPO / coll_dir
        if not d.exists(): continue
        for md in d.rglob('*.md'):
            if md.name == 'index.md': continue
            rel = md.relative_to(d)
            url = str(rel).replace('.md', '').replace('\\', '/')
            notes_map[md.stem] = f'{url_prefix}/{url}'
            for kor, eng in KOREAN_TO_ENG.items():
                if eng == md.stem:
                    notes_map[kor] = f'{url_prefix}/{url}'
                    break
            m_sec = re.match(r'^(\d+\.\d+)', md.stem)
            if m_sec and m_sec.group(1) not in notes_map:
                notes_map[m_sec.group(1)] = f'{url_prefix}/{url}'
            m_ch = re.match(r'^(\d+)\.', md.stem)
            if m_ch and m_ch.group(1) not in notes_map:
                notes_map[m_ch.group(1)] = f'{url_prefix}/{url}'
    return notes_map

# ─── 마크다운 변환 핵심 로직 (V11: Final Fix) ──────────────────────────────────
def transform(content: str, file_path: Path, notes_map: dict, col_name: str, nav_order: int) -> str:
    # 탭 문자를 공백으로 변환 (Kramdown의 의도치 않은 코드 블록 생성 방지)
    content = content.replace('\t', '    ')
    
    raw_stem = file_path.stem
    title = raw_stem
    for kor, eng in KOREAN_TO_ENG.items():
        if eng == raw_stem:
            title = kor
            break
    title = strip_leading_numbers(title)

    fm_match = re.match(r'^---+\s*\n(.*?)\n---+\s*\n', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        body = content[fm_match.end():]
    else:
        fm_content = ""
        body = content

    def resolve_target(note_name: str) -> str:
        clean_name = strip_leading_numbers(note_name)
        clean_name = re.sub(r'(절|장)$', '', clean_name).strip()
        if clean_name in notes_map: return f'{BASE_URL}/{notes_map[clean_name]}/'
        if note_name in notes_map: return f'{BASE_URL}/{notes_map[note_name]}/'
        return None

    # 옵시디언 느슨한 인용구 보정
    raw_lines = body.split('\n')
    in_bq = False
    for i, line in enumerate(raw_lines):
        sl = line.lstrip()
        if sl.startswith('>'): in_bq = True
        elif not sl: in_bq = False
        elif in_bq: raw_lines[i] = '> \n> ' + line
    body = '\n'.join(raw_lines)

    # Liquid 이스케이프
    body = body.replace('{{ site.baseurl }}', '___SITE_BASEURL___')
    body = re.sub(r'\{\{(?!\s*site\.baseurl|raw|endraw)', r'{{ "{{" }}', body)
    body = re.sub(r'\{%(?!\s*raw|endraw)', r'{{ "{%" }}', body)
    body = body.replace('___SITE_BASEURL___', '{{ site.baseurl }}')

    # 위키 링크 (이미지)
    def rep_img(m):
        txt = m.group(1)
        raw, w = txt.split('|', 1) if '|' in txt else (txt.strip(), None)
        raw_name = unicodedata.normalize('NFC', raw.strip())
        new_path = get_assets_map_value(raw_name) or sanitize_asset_name(raw_name)
        url = f'{BASE_URL}/assets/{new_path}'
        if Path(new_path).suffix.lower() in MEDIA_EXTS:
            return f'<video controls preload="auto" class="img-normal" width="{w if w else "100%"}"><source src="{url}" type="video/mp4"></video>'
        attr = f'{{: .img-normal width="{w}" }}' if w else '{: .img-normal }'
        return f'![{raw_name}]({url}){attr}'
    body = re.sub(r'!\[\[(.*?)\]\]', rep_img, body)

    # 위키 링크 (문서)
    def rep_link(m):
        txt = m.group(1)
        nm, al = txt.split('|', 1) if '|' in txt else (txt.strip(), txt.strip())
        po = Path(nm)
        if po.suffix.lower() in IMG_EXTS or po.suffix.lower() in MEDIA_EXTS:
            np = get_assets_map_value(nm) or sanitize_asset_name(nm)
            url = f'{BASE_URL}/assets/{np}'
            if po.suffix.lower() in MEDIA_EXTS:
                return f'<video controls class="img-normal" width="100%"><source src="{url}" type="video/mp4"></video>'
            return f'![{nm}]({url}){{: .img-normal }}'
        url = resolve_target(nm)
        return f'[{al}]({url if url else "#"})'
    body = re.sub(r'(?<!!)\[\[(.*?)\]\]', rep_link, body)

    # 표준 마크다운 링크 보정
    def rep_mdlink(m):
        al, pp = m.group(1), m.group(2).strip('<> ')
        if pp.startswith('{{') or pp.startswith('http'): return m.group(0)
        url = resolve_target(Path(pp).stem.strip())
        return f'[{al}]({url})' if url else m.group(0)
    body = re.sub(r'\[(.*?)\]\((.*?)\)', rep_mdlink, body)

    # 이미지 처리 (.img-normal 클래스 주입)
    def rep_final_img(m):
        ps, qp, alt, url, attr = m.groups()
        if '{{ site.baseurl }}' in url or '://' in url:
            at = attr.strip('{: }').strip() if attr else ""
            if '.img-normal' in at: return m.group(0)
            return f"{ps}{qp}![{alt}]({url}){{: .img-normal {at} }}".strip(' }') + ' }'
        fn = urllib.parse.unquote(Path(url).name)
        np = get_assets_map_value(fn) or sanitize_asset_name(fn)
        new_url = f'{BASE_URL}/assets/{np}'
        if any(new_url.lower().endswith(ext) for ext in ['.mp4', '.webm', '.ogg', '.mov']):
            return f'<video controls preload="auto" class="img-normal" {attr}><source src="{new_url}" type="video/mp4"></video>'
        at = attr.strip('{: }').strip() if attr else ""
        return f"{ps}{qp}![{alt}]({new_url}){{: .img-normal {at} }}".strip(' }') + ' }'
    body = re.sub(r'(^|\n)(>?\s*)!\[(.*?)\]\((.*?)\)(\{:.*?\}|)?', rep_final_img, body)

    # 인용구 블록 필터링
    def rep_blockquote(m):
        block = m.group(0)
        lines = block.split('\n')
        proc = []
        for i, line in enumerate(lines):
            line = line.rstrip()
            if line.startswith('>'):
                proc.append(line)
                if line != '>' and i + 1 < len(lines) and lines[i+1].rstrip().startswith('>') and lines[i+1].rstrip() != '>':
                    proc.append('>')
            else: proc.append(line)
        final_lines = [re.sub(r'^>\s?', '', ln) for ln in proc]
        inner_content = "\n".join(final_lines)
        return f'\n\n<div class="obsidian-callout" markdown="1">\n{inner_content}\n</div>\n\n'
    body = re.sub(r'(^>.*(?:\n>.*)*)', rep_blockquote, body, flags=re.MULTILINE)

    # 수식 처리 (Block)
    def rep_math(m):
        inner = m.group(1).strip().replace('\\|', r'\Vert ').replace('|', r'\vert ')
        return f'\n\n<div class="math-container">\n$$\n{inner}\n$$\n</div>\n\n'
    body = re.sub(r'(?:\n|^)\s*\$\$(.*?)\$\$\s*(?=\n|$)', rep_math, body, flags=re.DOTALL)

    # 수식 처리 (Inline) - V13: 공백 제거 + 강조 기호(*, _) 이스케이프 + 파이프 대체
    def rep_inline_math(m):
        content = m.group(1).strip().replace('\\|', r'\Vert ').replace('|', r'\vert ')
        # 강조 기호(*, _)가 마크다운 강조 쌍을 형성하지 않도록 이스케이프
        content = re.sub(r'([*_])', r'\\\1', content)
        # 수식 내부의 연속된 공백 및 줄바꿈 제거
        content = re.sub(r'\s+', ' ', content).strip()
        return f' ${content}$ '
    body = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]{1,300})(?<!\$)\$(?!\$)', rep_inline_math, body)

    # Hard Wrap 보정 (Kramdown) - 리스트나 수식 블록 제외하고 줄바꿈 유지
    lns = body.split('\n')
    m_in = c_in = False
    for i, ln in enumerate(lns):
        s = ln.strip()
        if s == '$$' or s.startswith(('<div', '</div')): m_in = not m_in
        if s.startswith('```'): c_in = not c_in
        # 줄 끝에 '  '를 추가하되, 이미 있거나 특수 시작 문자열인 경우 제외
        if not m_in and not c_in and ln and not ln.endswith('  ') and not s.startswith(('<', '![', '#', '>', '- ', '* ', '+ ', '1. ')):
            lns[i] = ln + '  '
    body = '\n'.join(lns)

    # Front matter
    fm = {'layout': 'sidebar', 'title': title}
    if col_name:
        fm['collection_name'] = col_name
        fm['nav_order'] = nav_order
    if fm_content:
        try:
            ex = yaml.safe_load(fm_content)
            if isinstance(ex, dict): fm.update(ex)
        except: pass
    if file_path.name == 'index.md':
        if col_name:
            fm['permalink'] = f'/{col_name}/'
            fm['title'] = 'Mathematics for Machine Learning' if col_name == 'mml' else ('GenAI' if col_name == 'genai' else col_name.capitalize())
        else:
            # 루트 index.md인 경우 permalink는 그대로(/) 두거나 title만 유지
            pass
        fm['layout'] = 'sidebar'
    
    fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{fm_str}\n---\n\n{body.strip()}\n"

def main():
    print('=' * 60); print('  V11 Jekyll Migration (Final Corrected)'); print('=' * 60)
    newly_copied = []
    for col_dir in ['_mml', '_notes', '_research', '_genai']:
        target = REPO / col_dir
        if target.exists(): shutil.rmtree(target)
    
    def process_assets(src_adir: Path, rel_dp: Path):
        if not src_adir.exists(): return
        dst = ASSETS / rel_dp; dst.mkdir(parents=True, exist_ok=True)
        for f in src_adir.iterdir():
            if f.is_file() and (f.suffix.lower() in IMG_EXTS or f.suffix.lower() in MEDIA_EXTS):
                nfn = sanitize_asset_name(f.name)
                ASSETS_MAP[unicodedata.normalize('NFC', f.name)] = (rel_dp / nfn).as_posix()
                shutil.copy2(f, dst / nfn)

    if ASSETS.exists():
        for it in ASSETS.iterdir():
            if it.name == 'main.scss': continue
            if it.is_dir(): shutil.rmtree(it)
            else: os.remove(it)
    ASSETS.mkdir(exist_ok=True)
    
    profile_src = REPO / 'profile_assets'
    for fn, sp in [('0_me.png', profile_src/'me.png'), ('mml_cover.png', REPO/'MML'/'MML.png'), ('passport_img.jpg', profile_src/'passport_img.jpg'), ('present1.jpg', profile_src/'present1.jpg')]:
        if sp.exists(): shutil.copy2(sp, ASSETS/fn); ASSETS_MAP[sp.name] = fn

    if MML_ROOT_SRC.exists():
        parts = [d for d in sorted(MML_ROOT_SRC.iterdir()) if d.is_dir() and d.name.startswith('Part')]
        for p_idx, p_dir in enumerate(parts, 1):
            chaps = [d for d in sorted(p_dir.iterdir(), key=lambda x: [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', x.name)]) if d.is_dir()]
            for c_idx, c_dir in enumerate(chaps, 1):
                m_ch = re.match(r'^(\d+)\.', c_dir.name)
                ch_n = m_ch.group(1) if m_ch else str(c_idx)
                dst_c = MML_ROOT_DST / p_dir.name.strip() / c_dir.name.strip()
                dst_c.mkdir(parents=True, exist_ok=True)
                for f_idx, f in enumerate(sorted(c_dir.iterdir()), 1):
                    if f.is_file() and f.suffix == '.md':
                        dst = dst_c / f.name.strip()
                        shutil.copy2(f, dst); order = 100000 + (p_idx*1000) + (c_idx*100) + f_idx
                        newly_copied.append((dst, 'mml', order))
                process_assets(c_dir / 'assets', Path('mml') / f"part{p_idx}" / ch_n)

    for cfg in NOTES_CONFIGS:
        src, dst_dir, col, fo = cfg['src'], cfg['dst'], cfg['col'], cfg['order']
        dst_dir.mkdir(parents=True, exist_ok=True)
        if not src.exists(): continue
        for f in sorted(src.rglob('*.md')):
            if f.is_file():
                rel_f = f.relative_to(src)
                m_n = re.match(r'^(\d+)\.', f.name)
                # Note 컬렉션의 경우 NOTES_CONFIGS에서 지정한 dst_dir 하위에 파일 배치
                # GenAI 등도 마찬가지로 dst_dir 하위에 rel_f.parent를 유지하여 사이드바에서 계층 구조 표현
                dst = dst_dir / rel_f.parent / f'{get_english_name(f.stem)}.md'
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst); newly_copied.append((dst, col, (fo*1000) + (int(m_n.group(1)) if m_n else 999)))
        for adir in src.rglob('assets'): process_assets(adir, Path(col) / dst_dir.name)

    midx, ridx = REPO/'MML'/'index.md', REPO/'index.md'
    if midx.exists(): dst = REPO/'_mml'/'index.md'; shutil.copy2(midx, dst); newly_copied.append((dst, 'mml', 100000))
    if ridx.exists():
        newly_copied.append((ridx, None, 0)) # 루트 index.md도 변환 대상에 포함
        for col in ['notes', 'research', 'genai']: dst = REPO/f'_{col}'/'index.md'; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ridx, dst); newly_copied.append((dst, col, 0))

    notes_map = build_notes_map(); processed = set()
    for fp, cn, no in newly_copied:
        if fp in processed: continue
        try:
            content = fp.read_text(encoding='utf-8')
            fp.write_text(transform(content, fp, notes_map, cn, no), encoding='utf-8')
            processed.add(fp)
        except Exception as e: print(f"  [X] {fp.name}: {e}")
    print('  Migration Complete!')

if __name__ == '__main__':
    main()
