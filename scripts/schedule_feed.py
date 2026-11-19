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

from check_source_facts import assert_official, fetch, to_text

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


def main(seed):
    sources = [s for s in json.loads((DATA/'sources.json').read_text())['sources']
               if s['kind'] == 'schedule' or s['id'] in {'h_aria_poker','sp_sched_page','orl_daily_pdf'}]
    assert_official(sources)
    old = {r['source']: r for r in json.loads(OUT.read_text())['rooms']} if OUT.exists() and not seed else {}
    def collect(s):
        url = s['url']; prev = old.get(url, {})
        row = dict(venue=s['venue'], label=s['label'], source=url,
                   attempted_at=None if seed else datetime.now(timezone.utc).isoformat(timespec='seconds'),
                   read_at=prev.get('read_at'), excerpts=prev.get('excerpts', []), digest=prev.get('digest'), changed=False)
        try:
            if seed:
                text = (DATA/'snapshots'/(s['id']+'.txt')).read_text()
            else:
                _, content = fetch(url, timeout=25)
                text = to_text(url, content)
            found = excerpts(text)
            if not found:
                row['status'] = 'No readable schedule excerpts; review source'
            else:
                digest = hashlib.sha256('\n'.join(found).encode()).hexdigest()
                row.update(status='Archived' if seed else 'Fetched', read_at='2026-11-17' if seed else row['attempted_at'],
                           excerpts=found, digest=digest, changed=bool(prev.get('digest') and digest != prev['digest']))
        except (OSError, ValueError, TimeoutError) as e:
            row['status'] = 'Not captured' if seed else 'Fetch failed; review source'
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(collect, sources))
    OUT.write_text(json.dumps({'rooms':rows}, indent=1, ensure_ascii=False)+'\n')
    print(f'{len(rows)} official schedule sources; {sum(r["status"] == "Fetched" for r in rows)} live captures')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', action='store_true')
    main(parser.parse_args().seed)
