#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_new_content.py

MML 챕터 2-7 + 미적분/생성모델/확률과 통계/_memo 컬렉션 Jekyll 마이그레이션 스크립트

실행:
    python migrate_new_content.py
"""

import os, re, shutil, yaml
from pathlib import Path

REPO  = Path(__file__).parent
ASSETS = REPO / 'assets'
BASE_URL = '{{ site.baseurl }}'
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}

# ─── 삭제 대상 ────────────────────────────────────────────────────────────────
DELETE_TARGETS = [
    REPO / '확률과 통계' / '이전 정리',           # 폴더째 삭제
    REPO / 'MML' / 'Part I Mathematical Foundations'
           / '4. Matrix Decompositions' / '정리.md',  # 파일 삭제
]

# ─── 한국어 이미지명 → 영어 이미지명 매핑 ───────────────────────────────────
KOREAN_IMG_MAP = {
    # MML Ch3
    '예제3.11 시각화.png'                              : '1_example_3_11.png',
    # 미적분 (3_)
    '(sin(x)y)square=x.png'                           : '3_sinxy_squared.png',
    '극한이 존재하지만 연속함수가 아닌 경우.png'        : '3_limit_exists_not_continuous.png',
    '무한대로 발산하는 경우.png'                        : '3_diverges_to_infinity.png',
    '좌극한과 우극한이 불일치하는 경우.png'             : '3_left_right_limit_mismatch.png',
    # 확률과 통계 (4_)
    'Q-Q plot.png'                                     : '4_qq_plot.png',
    '다변량 확률 변수의 정사영과 이차 형식의 관계.png'  : '4_multivariate_projection_quadratic.png',
    # 생성모델 (6_)
    '볼츠만 머신 1.png'                                : '6_boltzmann_machine_1.png',
    '볼츠만 머신 2.png'                                : '6_boltzmann_machine_2.png',
    '위너 과정.png'                                    : '6_wiener_process.png',
    # 무제 폴더 (Pasted image → 실제 이미지)
    'Pasted image 20251208100229.png'                  : '6_vae_algorithm2.png',
    # 소스파일에서 참조하는 이름 → assets 내 이름 (무제 복사본)
    'vae_algorithm2.png'                               : '6_vae_algorithm2.png',
}

# ─── MML 챕터 목록 ───────────────────────────────────────────────────────────
MML_CHAPTERS = [
    '2. Linear Algebra',
    '3. Analytic Geometry',
    '4. Matrix Decompositions',
    '5. Vector Calculus',
    '6. Probability and Distributions',
    '7. Continuous Optimization',
]
MML_SRC = REPO / 'MML' / 'Part I Mathematical Foundations'
MML_DST = REPO / '_mml' / 'Part I Mathematical Foundations'

# ─── 노트/메모 마이그레이션 설정 ─────────────────────────────────────────────
NOTES_CONFIGS = [
    {'src': REPO / '미적분',         'dst': REPO / '_notes' / 'calculus',
     'prefix': '3_', 'col': 'notes'},
    {'src': REPO / '확률과 통계',    'dst': REPO / '_notes' / 'probability-statistics',
     'prefix': '4_', 'col': 'notes'},
    {'src': REPO / '생성모델',       'dst': REPO / '_notes' / 'generative-models',
     'prefix': '6_', 'col': 'notes'},
    {'src': REPO / 'Memo',           'dst': REPO / '_memo',
     'prefix': '7_', 'col': 'memo'},
]

# ─── 이미지 이름 변환 ────────────────────────────────────────────────────────
def mml_img_rename(stem: str, ext: str) -> str:
    """MML figure/table 이미지명 변환: 'figure 3.1' → '1_figure_3_1'"""
    m = re.match(r'^(figure|table)\s*(\d+)\.(\d+(?:\.\d+)?)$', stem, re.IGNORECASE)
    if m:
        t   = m.group(1).lower()
        ch  = m.group(2)
        fig = m.group(3).replace('.', '_')
        return f'1_{t}_{ch}_{fig}{ext}'
    # fallback
    slug = re.sub(r'[\s.]+', '_', stem.lower())
    slug = re.sub(r'[^\w_]+', '', slug)
    slug = re.sub(r'_+', '_', slug).strip('_')
    return f'1_{slug}{ext}'

def notes_img_rename(filename: str, prefix: str) -> str:
    """노트/메모 이미지명 변환 (한국어 포함)"""
    if filename in KOREAN_IMG_MAP:
        return KOREAN_IMG_MAP[filename]
    stem = Path(filename).stem
    ext  = Path(filename).suffix.lower()
    slug = re.sub(r'[\s,;:.!@#$%^&*()\[\]{}|<>?/\\\'\"]+', '_', stem)
    slug = re.sub(r'_+', '_', slug).strip('_')
    return f'{prefix}{slug}{ext}'

def build_img_rename_map() -> dict:
    """전체 이미지명 변환 맵 생성"""
    rename_map = {}

    # MML 챕터 이미지
    for chapter in MML_CHAPTERS:
        assets_dir = MML_SRC / chapter / 'assets'
        if not assets_dir.exists():
            continue
        for f in assets_dir.iterdir():
            if f.suffix.lower() in IMG_EXTS:
                rename_map[f.name] = mml_img_rename(f.stem, f.suffix.lower())

    # 노트/메모 이미지
    for cfg in NOTES_CONFIGS:
        assets_dir = cfg['src'] / 'assets'
        if not assets_dir.exists():
            continue
        for f in assets_dir.iterdir():
            if f.suffix.lower() in IMG_EXTS:
                rename_map[f.name] = notes_img_rename(f.name, cfg['prefix'])

    # 무제 폴더 이미지 (Pasted images)
    munje = REPO / '무제'
    if munje.exists():
        for f in munje.iterdir():
            if f.suffix.lower() in IMG_EXTS:
                rename_map[f.name] = KOREAN_IMG_MAP.get(f.name, f'6_{f.name}')

    # 한국어 맵의 키도 등록 (전역 fallback)
    rename_map.update(KOREAN_IMG_MAP)
    return rename_map

# ─── 백링크 맵 (노트명 → URL) ────────────────────────────────────────────────
def build_notes_map() -> dict:
    """_notes, _mml, _memo 에서 노트명 → 상대 URL 맵 생성"""
    notes_map = {}
    for coll_dir, url_prefix in [('_notes', 'notes'), ('_mml', 'mml'), ('_memo', 'memo')]:
        d = REPO / coll_dir
        if not d.exists():
            continue
        for md in d.rglob('*.md'):
            rel     = md.relative_to(d)
            url     = str(rel).replace('.md', '').replace('\\', '/')
            notes_map[md.stem] = f'{url_prefix}/{url}'
    return notes_map

# ─── 파일명 날짜 prefix 제거 ─────────────────────────────────────────────────
def strip_date_prefix(filename: str) -> str:
    """6자리 날짜+공백 prefix 제거: '251219 확률이란(수정).md' → '확률이란(수정).md'"""
    return re.sub(r'^\d{6}\s+', '', filename)

# ─── 마크다운 콘텐츠 변환 ────────────────────────────────────────────────────
def transform(content: str, file_path: Path,
              notes_map: dict, img_map: dict, col_name: str) -> str:

    title = file_path.stem

    # 1) Front matter 추가 (없을 경우)
    if not content.startswith('---'):
        fm = yaml.dump(
            {'layout': 'sidebar', 'title': title, 'collection_name': col_name},
            allow_unicode=True, default_flow_style=False
        )
        content = f'---\n{fm}---\n\n' + content

    # 2) 이미지 위키링크 ![[name.png]] 또는 ![[name.png|width]]
    def rep_img(m):
        txt = m.group(1)
        if '|' in txt:
            raw, rest = txt.split('|', 1)
            w = rest.strip() if rest.strip().isdigit() else None
        else:
            raw, w = txt.strip(), None
        raw = raw.strip()
        new = img_map.get(raw, raw)
        url  = f'{BASE_URL}/assets/{new}'
        attr = f'{{: width="{w}" }}' if w else ''
        return f'![{new}]({url}){attr}'

    content = re.sub(r'!\[\[(.*?)\]\]', rep_img, content)

    # 3) 백링크 [[note]] 또는 [[note|alias]]
    def rep_link(m):
        txt = m.group(1)
        if '|' in txt:
            note_name, alias = [x.strip() for x in txt.split('|', 1)]
        else:
            note_name = alias = txt.strip()

        if note_name in notes_map:
            return f'[{alias}]({BASE_URL}/{notes_map[note_name]}/)'
        if Path(note_name).suffix.lower() in IMG_EXTS:
            new = img_map.get(note_name, note_name)
            return f'![{new}]({BASE_URL}/assets/{new})'
        print(f'  [WARN] 백링크 미발견: {note_name}')
        return f'[{alias}](#)'

    content = re.sub(r'(?<!!)\[\[(.*?)\]\]', rep_link, content)

    # 4) 표준 마크다운 링크 [text](file.md)
    def rep_mdlink(m):
        alias     = m.group(1)
        path_part = m.group(2).strip('<> ')
        note_name = Path(path_part).stem.strip()
        if note_name in notes_map:
            return f'[{alias}]({BASE_URL}/{notes_map[note_name]}/)'
        return m.group(0)

    content = re.sub(r'\[(.*?)\]\((.*?\.md.*?)\)', rep_mdlink, content)

    # 5) 수식 블록 $$...$$ 앞뒤 빈줄 보장
    def rep_math(m):
        inner = m.group(1).strip()
        return f'\n\n$$\n{inner}\n$$\n\n'

    content = re.sub(r'\s*\$\$(.*?)\$\$\s*', rep_math, content, flags=re.DOTALL)

    # 6) 이미지 중앙 정렬 래핑
    def rep_final_img(m):
        full = m.group(0).strip()
        alt, url = m.group(1), m.group(2)
        if '{:' in full:
            return f'\n\n<div style="text-align: center;" markdown="1">\n  {full}\n</div>\n\n'
        return (f'\n\n<div style="text-align: center;" markdown="1">\n'
                f'  ![{alt}]({url}){{: width="500" }}\n</div>\n\n')

    content = re.sub(r'\s*!\[(.*?)\]\((.*?)\)(\{:.*?\})?\s*', rep_final_img, content)

    # 7) 일반 텍스트 줄 끝 공백 2개 (kramdown hard_wrap)
    lines = content.split('\n')
    in_math = in_code = in_fm = False
    fm_count = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '---':
            fm_count += 1
            in_fm = (fm_count < 2)
            continue
        if in_fm:
            continue
        if s == '$$':
            in_math = not in_math
        if s.startswith('```'):
            in_code = not in_code
        if not in_math and not in_code and line and not line.endswith('  '):
            if not s.startswith(('<', '![', '#', '>', '- ', '* ')):
                lines[i] = line + '  '

    content = '\n'.join(lines)

    # 8) 연속 빈줄 정리
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip() + '\n'

# ─── 메인 ────────────────────────────────────────────────────────────────────
def main():
    print('=' * 60)
    print('  Extended Jekyll Migration')
    print('=' * 60)

    # ── Step 0: 삭제 처리 ────────────────────────────────────────────────────
    print('\n[Step 0] 불필요 파일/폴더 삭제...')
    for target in DELETE_TARGETS:
        if target.is_dir():
            shutil.rmtree(target)
            print(f'  Deleted dir : {target.relative_to(REPO)}')
        elif target.is_file():
            target.unlink()
            print(f'  Deleted file: {target.relative_to(REPO)}')
        else:
            print(f'  Not found   : {target.relative_to(REPO)} (skip)')

    # ── Step 1: 이미지 rename 맵 생성 ────────────────────────────────────────
    print('\n[Step 1] 이미지 rename 맵 생성...')
    img_map = build_img_rename_map()
    print(f'  {len(img_map)}개 이미지 등록 완료')

    # ── Step 2: 이미지 → assets/ 복사 ────────────────────────────────────────
    print('\n[Step 2] 이미지 → assets/ 복사...')
    ASSETS.mkdir(exist_ok=True)

    for chapter in MML_CHAPTERS:
        assets_dir = MML_SRC / chapter / 'assets'
        if not assets_dir.exists():
            continue
        for f in assets_dir.iterdir():
            if f.suffix.lower() in IMG_EXTS and f.name in img_map:
                dst = ASSETS / img_map[f.name]
                shutil.copy2(f, dst)
                print(f'  {f.name:50s} → {img_map[f.name]}')

    for cfg in NOTES_CONFIGS:
        assets_dir = cfg['src'] / 'assets'
        if not assets_dir.exists():
            continue
        for f in assets_dir.iterdir():
            if f.suffix.lower() in IMG_EXTS and f.name in img_map:
                dst = ASSETS / img_map[f.name]
                shutil.copy2(f, dst)
                print(f'  {f.name:50s} → {img_map[f.name]}')

    # 무제 폴더 (Pasted images)
    munje = REPO / '무제'
    if munje.exists():
        for f in munje.iterdir():
            if f.suffix.lower() in IMG_EXTS:
                new_name = KOREAN_IMG_MAP.get(f.name, f'6_{f.name}')
                dst = ASSETS / new_name
                shutil.copy2(f, dst)
                print(f'  {f.name:50s} → {new_name} (무제)')

    # ── Step 3: .md 파일 복사 (raw) ───────────────────────────────────────────
    print('\n[Step 3] 마크다운 파일 복사...')
    newly_copied: list[tuple[Path, str]] = []

    # MML 챕터 2-7
    for chapter in MML_CHAPTERS:
        src_dir = MML_SRC / chapter
        dst_dir = MML_DST / chapter
        dst_dir.mkdir(parents=True, exist_ok=True)

        for f in sorted(src_dir.iterdir()):
            if f.suffix != '.md':
                continue
            new_name = strip_date_prefix(f.name)
            dst      = dst_dir / new_name
            shutil.copy2(f, dst)
            newly_copied.append((dst, 'mml'))
            print(f'  [MML/{chapter[:1]}] {f.name} → {new_name}')

    # 노트 및 메모
    for cfg in NOTES_CONFIGS:
        src, dst_dir, col = cfg['src'], cfg['dst'], cfg['col']
        dst_dir.mkdir(parents=True, exist_ok=True)

        if not src.exists():
            print(f'  [SKIP] {src.name} 폴더 없음')
            continue

        for f in sorted(src.iterdir()):
            if f.suffix != '.md':
                continue
            new_name = strip_date_prefix(f.name)
            dst      = dst_dir / new_name
            shutil.copy2(f, dst)
            newly_copied.append((dst, col))
            print(f'  [{col}/{src.name}] {f.name} → {new_name}')

    # ── Step 4: 백링크 맵 빌드 ───────────────────────────────────────────────
    print('\n[Step 4] 백링크 맵 빌드...')
    notes_map = build_notes_map()
    print(f'  {len(notes_map)}개 노트 인식 완료')

    # ── Step 5: 마크다운 변환 ─────────────────────────────────────────────────
    print('\n[Step 5] 마크다운 변환 적용...')
    ok = fail = 0
    for file_path, col_name in newly_copied:
        try:
            content     = file_path.read_text(encoding='utf-8')
            transformed = transform(content, file_path, notes_map, img_map, col_name)
            file_path.write_text(transformed, encoding='utf-8')
            print(f'  ✓ {file_path.relative_to(REPO)}')
            ok += 1
        except Exception as e:
            print(f'  ✗ {file_path.name}: {e}')
            fail += 1

    print(f'\n  완료: {ok}개 성공 / {fail}개 실패')
    print('\n' + '=' * 60)
    print('  Migration Complete!')
    print('=' * 60)


if __name__ == '__main__':
    main()
