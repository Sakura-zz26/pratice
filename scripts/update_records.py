"""Update only the page selected for the actor, and append a README audit entry."""
import argparse
from datetime import datetime, timezone
import html
import os
from pathlib import Path
import re
import subprocess

ACTOR_PAGES = {'Sakura-zz26': 'index.html'}

def metadata():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    commit = subprocess.check_output(['git', 'rev-parse', '--short=12', 'HEAD'], text=True).strip()
    if not re.fullmatch(r'[0-9a-f]{7,40}', commit):
        raise ValueError('Unexpected source commit hash')
    return timestamp, commit

def update_html(root, actor, role, timestamp, commit, target):
    if target not in {'index.html', 'member1.html', 'member2.html'}:
        raise ValueError('Page is outside the configured exercise files')
    path = root / target
    original = path.read_text()
    if '</body>' not in original:
        raise ValueError('Target HTML is missing its closing body tag')
    safe_actor, safe_role = html.escape(actor), html.escape(role)
    entry = f'  <p>Updated by {safe_actor} ({safe_role}) on {timestamp} [Commit: {commit}]</p>\n'
    path.write_text(original.replace('</body>', entry + '</body>', 1))

def update_readme(root, actor, role, timestamp, commit):
    safe_actor = actor.replace('\n', ' ').replace('\r', ' ')
    with (root / 'README.md').open('a') as stream:
        stream.write(f'\n### Updated by {safe_actor} ({role}) on {timestamp} [Commit: {commit}]\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=['html', 'readme'])
    args = parser.parse_args()
    actor = os.environ.get('GITHUB_ACTOR', '')
    target = ACTOR_PAGES.get(actor)
    if target is None:
        print('Skipped: the actor is not configured for this solo exercise.')
        return
    role = 'Solo learner'
    timestamp, commit = metadata()
    if args.step == 'html':
        update_html(Path('.'), actor, role, timestamp, commit, target)
        print(f'Updated {target} for actor {actor}')
    else:
        update_readme(Path('.'), actor, role, timestamp, commit)
        print(f'Logged actor {actor} and source commit {commit}')

if __name__ == '__main__':
    main()
