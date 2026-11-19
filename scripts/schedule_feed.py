"""Capture schedule excerpts for review; never infer dates or change reviewed rows.

--seed reads only dated repository snapshots. The scheduled job uses live URLs.
"""
import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from check_source_facts import assert_official, fetch, to_text_variants

DATA = Path(__file__).resolve().parents[1] / 'data'
OUT = DATA / 'schedule_feed.json'
TIME = re.compile(r'\b(?:\d{1,2}(?::\d\d)?\s*[ap]\.?m\.?|noon|midnight)\b', re.I)
FORMAT = re.compile(r'hold.?em|\bNLH\b|poker|tournament|omaha|satellite|bounty|guarantee', re.I)


def excerpts(text):
    lines = [' '.join(x.split()) for x in text.splitlines() if x.strip()]
    result = []
    for i, line in enumerate(lines):
        if not TIME.search(line):
            continue
        # Adjacent cells of an HTML schedule often become separate text lines.
        context = ' · '.join(lines[max(0, i-1):i+4])
        if FORMAT.search(context) and context not in result:
            result.append(context)
    return result


def _digest(rows):
    return hashlib.sha256('\n'.join(rows).encode()).hexdigest() if rows else None


def capture_state(previous, plain_text, layout_text, is_pdf, layout_error=None, plain_error=None):
    """Compare complete schedule renders separately; archive their union for review."""
    previous = previous or {}
    plain_rows = excerpts(plain_text)
    layout_rows = excerpts(layout_text) if layout_text else []
    union_rows = list(plain_rows)
    union_rows.extend(x for x in layout_rows if x not in union_rows)
    plain_digest = _digest(plain_rows)
    layout_digest = _digest(layout_rows)
    old_plain_digest = previous.get('plain_digest') or previous.get('digest')
    old_layout_digest = previous.get('layout_digest')
    plain_changed = bool(not plain_error and not previous.get('plain_error') and
                         old_plain_digest and plain_digest and old_plain_digest != plain_digest)
    layout_changed = bool(not layout_error and not previous.get('layout_error') and
                          old_layout_digest and layout_digest and old_layout_digest != layout_digest)
    layout_pending = bool(is_pdf and layout_rows and not layout_error and
                          (not old_layout_digest or previous.get('layout_error')))
    plain_pending = bool(plain_rows and not plain_error and
                         (not old_plain_digest or previous.get('plain_error')))
    if not is_pdf:
        layout_status = 'not-applicable'
    elif plain_error or layout_error:
        layout_status = 'partial'
    elif not layout_text:
        layout_status = 'unavailable'
    elif not layout_rows:
        layout_status = 'no-readable-schedule-excerpts'
    elif layout_pending:
        layout_status = 'baseline-pending'
    else:
        layout_status = 'comparable'
    return {
        'excerpts': union_rows,
        'plain_excerpts_count': len(plain_rows),
        'layout_excerpts_count': len(layout_rows),
        'digest': _digest(union_rows),
        'plain_digest': plain_digest,
        'layout_digest': layout_digest,
        'changed': plain_changed or layout_changed,
        'plain_baseline_pending': plain_pending,
        'layout_baseline_pending': layout_pending,
        'layout_status': layout_status,
        'plain_error': plain_error,
        'layout_error': layout_error,
        'status': 'Fetched' if union_rows else 'No readable schedule excerpts; review source',
    }


def main(seed):
    sources = [s for s in json.loads((DATA/'sources.json').read_text())['sources']
               if s['kind'] == 'schedule' or s['id'] in {'h_aria_poker','sp_sched_page','orl_daily_pdf'}]
    assert_official(sources)
    old = {r['source']: r for r in json.loads(OUT.read_text())['rooms']} if OUT.exists() and not seed else {}
    def collect(s):
        url = s['url']; prev = old.get(url, {})
        row = dict(venue=s['venue'], label=s['label'], source=url,
                   attempted_at=None if seed else datetime.now(timezone.utc).isoformat(timespec='seconds'),
                   read_at=prev.get('read_at'), excerpts=prev.get('excerpts', []), digest=prev.get('digest'),
                   plain_digest=prev.get('plain_digest', prev.get('digest')),
                   layout_digest=prev.get('layout_digest'), changed=False,
                   plain_baseline_pending=False, layout_baseline_pending=False,
                   layout_status=prev.get('layout_status', 'not-applicable'),
                   plain_error=None, layout_error=None, plain_excerpts_count=prev.get('plain_excerpts_count'),
                   layout_excerpts_count=prev.get('layout_excerpts_count'))
        try:
            if seed:
                plain_text = (DATA/'snapshots'/(s['id']+'.txt')).read_text()
                layout_path = DATA/'snapshots'/(s['id']+'.layout.txt')
                layout_text = layout_path.read_text() if layout_path.exists() else ''
                is_pdf = url.lower().split('?')[0].endswith('.pdf')
                layout_error = 'seed: no position-aware snapshot on file' if is_pdf and not layout_text else None
                plain_error = None if plain_text.strip() else 'seed: no plain snapshot text'
            else:
                _, content = fetch(url, timeout=25)
                variants = to_text_variants(url, content)
                plain_text, layout_text = variants['plain'], variants['layout']
                is_pdf = variants['is_pdf']
                plain_error, layout_error = variants.get('plain_error'), variants.get('layout_error')
            state = capture_state(prev, plain_text, layout_text, is_pdf, layout_error, plain_error)
            row.update(state)
            if seed and row['excerpts']:
                row['status'] = 'Archived'
                row['read_at'] = '2026-11-17'
            elif not seed and row['excerpts']:
                row['read_at'] = row['attempted_at']
        except (OSError, ValueError, TimeoutError) as e:
            row['status'] = 'Not captured' if seed else 'Fetch failed; review source'
            row['plain_error'] = '%s: %s' % (type(e).__name__, e)
            row['layout_error'] = '%s: %s' % (type(e).__name__, e)
            row['layout_status'] = 'unavailable'
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(collect, sources))
    OUT.write_text(json.dumps({'rooms':rows}, indent=1, ensure_ascii=False)+'\n')
    print(f'{len(rows)} official schedule sources; {sum(r["status"] == "Fetched" for r in rows)} live captures')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', action='store_true')
    main(parser.parse_args().seed)
