#!/usr/bin/env python3
"""Validate this marketplace catalog.

Usage: validate-catalog.py [ROOT] [--online] [--self-test]

Offline checks: .claude-plugin/marketplace.json parses; it has a name, owner and plugins; every entry has a unique
kebab-case name, a description, and an https git URL source (https://github.com/owner/repo.git); the version equals VERSION; no absolute
paths or personal email addresses anywhere. --online also fetches each plugin's own .claude-plugin/plugin.json from its
repository and checks that the manifest name equals the catalog entry name (a mismatch breaks `/plugin install`).
--self-test proves the checks fire on a broken catalog. Standard library only.
"""
import json, os, re, sys, tempfile, shutil, urllib.request

FORBIDDEN = [(re.compile('/' + 'Users/|/' + r'home/[a-z]|private' + '/tmp'), 'absolute path'),
             (re.compile(r'[\w.+-]+@(?:gmail|hotmail|outlook|yahoo)\.com'), 'personal email address')]


def validate(root, online=False):
    errs = []
    def e(m): errs.append(m)
    p = os.path.join(root, '.claude-plugin', 'marketplace.json')
    try:
        j = json.load(open(p, encoding='utf-8'))
    except Exception as x:
        return [f'marketplace.json: {x}']
    for k in ('name', 'owner', 'plugins'):
        if k not in j: e(f'marketplace.json: missing {k}')
    ver = open(os.path.join(root, 'VERSION')).read().strip() if os.path.exists(os.path.join(root, 'VERSION')) else None
    if ver and j.get('version') != ver: e(f'version {j.get("version")} != VERSION {ver}')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', str(j.get('name', ''))): e('marketplace name must be kebab-case')
    seen = set()
    for i, pl in enumerate(j.get('plugins', [])):
        n = pl.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', n): e(f'plugins[{i}]: name {n!r} must be kebab-case')
        if n in seen: e(f'plugins[{i}]: duplicate name {n}')
        seen.add(n)
        if not pl.get('description'): e(f'{n}: description missing')
        s = pl.get('source')
        repo = None
        if isinstance(s, dict) and s.get('source') == 'url':
            m = re.fullmatch(r'https://github\.com/([\w.-]+/[\w.-]+?)(?:\.git)?', s.get('url', ''))
            repo = m.group(1) if m else None
            if not repo: e(f'{n}: url source must be an https://github.com/owner/repo.git address (https avoids the SSH keys a stranger may not have)')
        elif isinstance(s, dict) and s.get('source') == 'github':
            e(f'{n}: use {{"source": "url", "url": "https://github.com/owner/repo.git"}}: the github source type clones over SSH and fails for anyone without SSH keys')
        else:
            e(f'{n}: source must be {{"source": "url", "url": "https://github.com/owner/repo.git"}}')
        if repo and online:
            url = f'https://raw.githubusercontent.com/{repo}/HEAD/.claude-plugin/plugin.json'
            try:
                m = json.load(urllib.request.urlopen(url, timeout=20))
                if m.get('name') != n: e(f'{n}: the plugin\'s own manifest is named {m.get("name")!r}')
            except Exception as x:
                e(f'{n}: cannot read {url}: {x}')
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x not in ('.git', '__pycache__')]
        for f in fs:
            if f.endswith(('.md', '.json', '.yml', '.py', '.sh')) and os.path.abspath(os.path.join(d, f)) != os.path.abspath(__file__):
                t = open(os.path.join(d, f), encoding='utf-8').read()
                for rx, why in FORBIDDEN:
                    if rx.search(t): e(f'{os.path.relpath(os.path.join(d, f), root)}: {why}')
    return errs


def self_test():
    T = tempfile.mkdtemp()
    try:
        os.makedirs(T + '/.claude-plugin')
        open(T + '/VERSION', 'w').write('2.0.0\n')
        json.dump({'name': 'Bad Name', 'version': '1.0.0', 'owner': {'name': 'x'}, 'plugins': [
            {'name': 'a', 'description': 'd', 'source': './local'}, {'name': 'a', 'source': {'source': 'github', 'repo': 'x/y'}}]},
            open(T + '/.claude-plugin/marketplace.json', 'w'))
        open(T + '/README.md', 'w').write('see ' + '/' + 'Users/someone/x\n')
        errs = '\n'.join(validate(T))
        for needle in ('!= VERSION', 'kebab-case', 'duplicate name', 'description missing', 'source must be', 'clones over SSH', 'absolute path'):
            if needle not in errs: print('SELF-TEST FAIL: did not catch', needle); return 1
        print('self-test OK: every check fires on a broken catalog'); return 0
    finally:
        shutil.rmtree(T, ignore_errors=True)


if __name__ == '__main__':
    if '--self-test' in sys.argv: sys.exit(self_test())
    root = next((a for a in sys.argv[1:] if not a.startswith('-')), '.')
    errs = validate(os.path.abspath(root), online='--online' in sys.argv)
    for x in errs: print('FAIL', x)
    print('RESULT: OK' if not errs else f'RESULT: {len(errs)} problem(s)')
    sys.exit(1 if errs else 0)
