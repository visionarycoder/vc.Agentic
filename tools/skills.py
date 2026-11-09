#!/usr/bin/env python3
"""Maintain the agent-neutral library using only the Python standard library."""
from __future__ import annotations

import argparse
import csv
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit

VERSION = '1.0.0'
FIELDS = ['name', 'description', 'collection', 'path', 'updated', 'files', 'sha256']
META = ['metadata-version', 'title', 'document-type', 'repository', 'language', 'updated', 'collection']
COLLECTIONS = {
    'core': 'Recommended development core',
    'dotnet': '.NET, C#, MSBuild, MSTest, and Roslyn',
    'azure': 'Azure platform and service workflows',
    'vbd': 'Volatility-based decomposition architecture',
    'security': 'Security engineering and weakness remediation',
    'data': 'Data analysis and Microsoft Fabric',
    'biology': 'Biology and life-sciences research',
    'accounting': 'Accounting systems and controls',
    'trading': 'Financial trading and investment research',
    'optional': 'Additional workflows, integrations, and specialist utilities',
}
CORE = {
    'adr', 'api-documentation', 'assertion-quality', 'code-refactoring', 'code-review',
    'dry-principles', 'executing-plans', 'prepare-task-handoff', 'repo-reconciliation',
    'skill-authoring', 'skill-selection', 'solid-principles', 'systematic-debugging',
    'test-anti-patterns', 'test-driven-development', 'token-efficient-implementation',
    'verification-before-completion', 'writing-plans',
}
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
LINK = re.compile(r'(!?)\[([^\]\n]*)\]\(([^)]+)\)')
TEXT_SUFFIXES = {'.md', '.markdown', '.json', '.yaml', '.yml', '.txt', '.py', '.ps1', '.sh'}


def parse(text: str) -> tuple[dict, str]:
    """Parse the documented JSON-string YAML subset, rejecting ambiguous input."""
    text = text.replace('\r\n', '\n')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError('Missing opening or closing frontmatter delimiter')
    header, body = text[4:].split('\n---\n', 1)
    result: dict = {}
    nested = None
    for line in header.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'(  )?([a-z][a-z0-9_-]*):(?: (.*))?', line)
        if not match:
            raise ValueError('Invalid header line: ' + line)
        indent, key, raw = match.groups()
        if indent:
            if nested != 'metadata':
                raise ValueError('Indented fields must belong to metadata')
            target = result['metadata']
        else:
            nested = None
            target = result
        if key in target:
            raise ValueError('Duplicate field: ' + key)
        if raw is None:
            if indent or key != 'metadata':
                raise ValueError('Only metadata may contain nested fields')
            result[key] = {}
            nested = key
        else:
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as error:
                raise ValueError('Use a JSON double-quoted string for ' + key) from error
            if not isinstance(value, str):
                raise ValueError('Header values must be strings: ' + key)
            target[key] = value
    return result, body.lstrip('\n')


def render(data: dict, body: str) -> str:
    body = re.sub(r'\n(?:[ \t]*\n){2,}', '\n\n', body)
    lines = ['---']
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(key + ':')
            lines.extend('  ' + k + ': ' + json.dumps(v, ensure_ascii=False) for k, v in value.items())
        else:
            lines.append(key + ': ' + json.dumps(value, ensure_ascii=False))
    return '\n'.join(lines) + '\n---\n\n' + body.strip() + '\n'


def title(name: str) -> str:
    acronyms = {'api': 'API', 'adr': 'ADR', 'vbd': 'VBD', 'mstest': 'MSTest',
                'msbuild': 'MSBuild', 'dotnet': '.NET', 'csharp': 'C#', 'ui': 'UI'}
    return ' '.join(acronyms.get(word, word.capitalize()) for word in name.split('-'))


def classify(name: str) -> str:
    if name in CORE:
        return 'core'
    for prefix, group in [('accounting-', 'accounting'), ('bio-', 'biology'),
                          ('trading-', 'trading'), ('azure-', 'azure'), ('vbd-', 'vbd'),
                          ('cwe-', 'security'), ('fabric-', 'data')]:
        if name.startswith(prefix):
            return group
    if name.startswith(('dotnet-', 'msbuild-', 'mstest-', 'roslyn-', 'wpf-', 'maui-',
                        'aspnet', 'efcore-', 'blazor-', 'winui', 'windows-ai-')):
        return 'dotnet'
    if name in {'build-report', 'build-dashboard', 'data-analytics-routing',
                'analyze-data-quality', 'metric-diagnostics', 'visualize-data'}:
        return 'data'
    return 'optional'


def outside_fences(text: str, transform) -> str:
    output, block = [], None
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            token = fence.group(1)
            if block is None:
                block = token
            elif token[0] == block[0] and len(token) >= len(block):
                block = None
            output.append(line)
        else:
            output.append(line if block else transform(line))
    return ''.join(output)


class Library:
    def __init__(self, root: Path, updated: str | None = None):
        self.root = root.resolve()
        self.skills = self.root / '.agents/skills'
        self.updated = updated or date.today().isoformat()
        date.fromisoformat(self.updated)

    def entrypoints(self):
        return sorted(self.skills.glob('*/SKILL.md'))

    def package(self, name: str) -> Path:
        if not NAME.fullmatch(name) or len(name) > 64:
            raise ValueError('Use a kebab-case skill name of at most 64 characters')
        path = self.skills / name
        if path.is_symlink() or path.resolve().parent != self.skills.resolve():
            raise ValueError('Package path leaves the library: ' + name)
        for child in path.rglob('*'):
            if not child.resolve().is_relative_to(path.resolve()):
                raise ValueError('Package contains an external link: ' + str(child))
        return path

    def text_files(self):
        return sorted(p for p in self.root.rglob('*')
                      if p.is_file() and '.git' not in p.relative_to(self.root).parts
                      and p.suffix.lower() in TEXT_SUFFIXES)

    def normalize(self, apply=False):
        planned = []
        for path in self.entrypoints():
            data, body = parse(path.read_text(encoding='utf-8'))
            name = data.get('name', path.parent.name)
            heading = re.search(r'^# (.+)$', body, re.M)
            heading_text = heading.group(1) if heading else title(name)
            if not heading:
                body = '# ' + heading_text + '\n\n' + body
            previous = data.get('metadata', {})
            if previous.get('metadata-version', VERSION) != VERSION:
                raise ValueError('Unsupported metadata profile; explicit migration required: ' + name)
            metadata = {
                'metadata-version': VERSION, 'title': heading_text,
                'document-type': 'skill', 'repository': 'vc.Agentic',
                'language': 'Standard Technical English', 'updated': self.updated,
                'collection': previous.get('collection', classify(name)),
            }
            for key, value in previous.items():
                if key not in metadata and key != 'last_updated':
                    metadata[key] = value
            data['metadata'] = metadata
            new = render(data, re.sub(r'\n(?:[ \t]*\n){2,}', '\n\n', body))
            if new.encode() != path.read_bytes():
                planned.append((path, new))
        if apply:
            for path, new in planned:
                path.write_text(new, encoding='utf-8', newline='\n')
        return [str(path.relative_to(self.root)) for path, _ in planned]

    def rows(self):
        rows = []
        for path in self.entrypoints():
            data, _ = parse(path.read_text(encoding='utf-8'))
            metadata = data.get('metadata', {})
            rows.append({'name': data['name'], 'description': data['description'],
                         'collection': metadata.get('collection', classify(data['name'])),
                         'path': path.relative_to(self.root).as_posix(),
                         'updated': metadata.get('updated', metadata.get('last_updated', '')),
                         'files': sum(p.is_file() for p in path.parent.rglob('*')),
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        return sorted(rows, key=lambda row: row['name'])

    def document(self, path, heading, description, body):
        data = {'metadata-version': VERSION, 'title': heading, 'description': description,
                'document-type': 'index', 'repository': 'vc.Agentic',
                'language': 'Standard Technical English', 'updated': self.updated}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(data, '# ' + heading + '\n\n' + body), encoding='utf-8', newline='\n')

    def refresh(self):
        rows = self.rows()
        inventory = self.root / '.agents/inventory.csv'
        inventory.parent.mkdir(parents=True, exist_ok=True)
        with inventory.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        counts = {key: sum(row['collection'] == key for row in rows) for key in COLLECTIONS}
        body = (f'The library contains **{len(rows)} skills**. All entrypoints are under '
                '`skills/<name>/SKILL.md`. [Inventory](inventory.csv) records current metadata and hashes. '
                '[Collections](collections.md) distinguish the recommended core from optional capabilities. '
                '[Maintenance](../tools/README.md) describes validation and safe changes.\n\n'
                '| Collection | Skills |\n| --- | --- |\n')
        body += '\n'.join(f'| {COLLECTIONS[key]} | {count} |' for key, count in counts.items())
        body += '\n\n| Skill | Collection | Purpose |\n| --- | --- | --- |\n'
        for row in rows:
            description = row['description'].replace('|', '\\|').replace('\n', ' ')
            if len(description) > 200:
                description = description[:197] + '...'
            body += (f"| [{row['name']}](skills/{row['name']}/SKILL.md) | "
                     f"{row['collection']} | {description} |\n")
        self.document(self.root / '.agents/README.md', 'Skill catalog',
                      'Locate agent-neutral skills by capability and collection.', body)
        body = ('Start with the recommended core and select optional capabilities for the actual task. '
                'Collection labels are catalog metadata; they do not activate or disable installed skills. '
                'Every skill remains in the single canonical skills directory.\n\n')
        for key, heading in COLLECTIONS.items():
            selected = [row for row in rows if row['collection'] == key]
            body += f'## {heading} ({len(selected)})\n\n'
            body += '\n'.join(f"- [{row['name']}](skills/{row['name']}/SKILL.md)" for row in selected)
            body += '\n\n'
        body += ('A stack or domain label is not a claim of universal portability. Read prerequisites '
                 'and use actual host capabilities. Skills never grant operation or approval authority.\n')
        self.document(self.root / '.agents/collections.md', 'Skill collections',
                      'Select a small development core and optional stacks or domains.', body)
        return rows

    def local_target(self, source, raw):
        raw = raw.strip('`<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', raw) or raw.startswith('//'):
            return None
        if '<' in raw or '{' in raw:
            return None
        path = unquote(urlsplit(raw).path)
        return (source.parent / path).resolve() if path else None

    def fix_links(self, apply=False):
        changes = []
        for path in self.text_files():
            if path.suffix.lower() not in {'.md', '.markdown'}:
                continue
            text = path.read_text(encoding='utf-8')
            def replace(match):
                target = self.local_target(path, match.group(3))
                if target is None or target.exists():
                    return match.group(0)
                changes.append({'file': path.relative_to(self.root).as_posix(),
                                'removed_target': match.group(3)})
                return match.group(2).rstrip('`')
            new = outside_fences(text, lambda line: LINK.sub(replace, line))
            if apply and new != text:
                path.write_text(new, encoding='utf-8', newline='\n')
        return changes

    def validate_frontmatter(self):
        errors, names = [], set()
        for path in self.entrypoints():
            relative = path.relative_to(self.root).as_posix()
            try:
                self.package(path.parent.name)
                data, body = parse(path.read_text(encoding='utf-8'))
                name, description = data.get('name', ''), data.get('description', '')
                if name != path.parent.name or not NAME.fullmatch(name) or len(name) > 64:
                    raise ValueError('Name must match its kebab-case folder and be at most 64 characters')
                if name in names:
                    raise ValueError('Duplicate skill name')
                names.add(name)
                if not description or len(description) > 1024:
                    raise ValueError('Description must contain 1-1024 characters')
                unsupported = set(data) - {'name', 'description', 'metadata', 'license', 'compatibility', 'allowed-tools'}
                if unsupported:
                    raise ValueError('Unsupported top-level fields: ' + ', '.join(sorted(unsupported)))
                metadata = data.get('metadata', {})
                missing = set(META) - metadata.keys()
                if missing:
                    raise ValueError('Missing metadata: ' + ', '.join(sorted(missing)))
                if metadata['metadata-version'] != VERSION or metadata['document-type'] != 'skill':
                    raise ValueError('Unsupported metadata profile or document type')
                if metadata['repository'] != 'vc.Agentic' or metadata['language'] != 'Standard Technical English':
                    raise ValueError('Incorrect repository or language metadata')
                if metadata['collection'] not in COLLECTIONS:
                    raise ValueError('Unknown collection: ' + metadata['collection'])
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', metadata['updated']):
                    raise ValueError('Use YYYY-MM-DD for the maintenance date')
                date.fromisoformat(metadata['updated'])
                heading = re.search(r'^# (.+)$', body, re.M)
                if not heading or heading.group(1) != metadata['title']:
                    raise ValueError('Metadata title must match the first H1 heading')
            except (ValueError, KeyError, OSError) as error:
                errors.append(relative + ': ' + str(error))
        return errors

    def validate(self, inventory=True):
        errors = self.validate_frontmatter()
        actual = set(self.entrypoints())
        for path in self.skills.rglob('SKILL.md'):
            if path not in actual:
                errors.append('Nested entrypoint: ' + path.relative_to(self.root).as_posix())
        for path in self.skills.iterdir() if self.skills.exists() else []:
            if path.is_dir() and not (path / 'SKILL.md').is_file():
                errors.append('Package without SKILL.md: ' + path.name)
        for path in self.skills.rglob('*'):
            if path.name.lower() in {'openai.yaml', 'openai.yml', '__pycache__', '.agentic-unification', '.agentic-consolidation'}:
                errors.append('Unexpected package artifact: ' + path.relative_to(self.root).as_posix())
        for path in self.text_files():
            if path.suffix.lower() not in {'.md', '.markdown'}:
                continue
            blob = path.read_bytes()
            if b'\r' in blob or re.search(rb'\n[ \t]*\n[ \t]*\n', blob):
                errors.append('Markdown spacing/LF: ' + path.relative_to(self.root).as_posix())
            for change in self._missing_links(path):
                errors.append(path.relative_to(self.root).as_posix() + ': missing link ' + change)
        if inventory and not errors:
            path = self.root / '.agents/inventory.csv'
            try:
                with path.open(encoding='utf-8-sig', newline='') as stream:
                    stored = list(csv.DictReader(stream))
                current = [{key: str(value) for key, value in row.items()} for row in self.rows()]
                if stored != current:
                    errors.append('Inventory is stale; run refresh')
            except OSError:
                errors.append('Inventory is missing; run refresh')
        return errors

    def _missing_links(self, path):
        found = []
        def inspect(line):
            for match in LINK.finditer(line):
                target = self.local_target(path, match.group(3))
                if target is not None and not target.exists():
                    found.append(match.group(3))
            return line
        outside_fences(path.read_text(encoding='utf-8'), inspect)
        return found

    def new(self, name, description, collection='optional', apply=False):
        path = self.package(name)
        if path.exists():
            raise ValueError('Package already exists: ' + name)
        if collection not in COLLECTIONS or not description or len(description) > 1024:
            raise ValueError('Supply a valid collection and a 1-1024 character description')
        heading = title(name)
        metadata = dict(zip(META, [VERSION, heading, 'skill', 'vc.Agentic',
                                 'Standard Technical English', self.updated, collection]))
        text = render({'name': name, 'description': description, 'metadata': metadata},
                      '# ' + heading + '\n\nDescribe the assigned task, required inputs, workflow, outputs, and checks.\n')
        if apply:
            path.mkdir(parents=True)
            (path / 'SKILL.md').write_text(text, encoding='utf-8', newline='\n')
            self.refresh()
        return text

    def rename(self, old, new, apply=False):
        source, target = self.package(old), self.package(new)
        if not (source / 'SKILL.md').is_file() or target.exists():
            raise ValueError('Source must exist and target must be absent')
        if not apply:
            return {'from': str(source.relative_to(self.root)), 'to': str(target.relative_to(self.root))}
        data, _ = parse((source / 'SKILL.md').read_text(encoding='utf-8'))
        if not set(META).issubset(data.get('metadata', {})):
            raise ValueError('Normalize the source header before renaming')
        source.rename(target)
        for path in self.text_files():
            if re.match(r'^(license|licence|notice|copying)([.-]|$)', path.name, re.I):
                continue
            try:
                text = path.read_text(encoding='utf-8')
            except UnicodeError:
                continue
            updated = text.replace('skills/' + old + '/', 'skills/' + new + '/')
            updated = updated.replace('../' + old + '/', '../' + new + '/')
            updated = re.sub(r'(?<![\w/-])' + re.escape(old) + r'(?![\w/-])', new, updated)
            if updated != text:
                path.write_text(updated, encoding='utf-8', newline='\n')
        entry = target / 'SKILL.md'
        data, body = parse(entry.read_text(encoding='utf-8'))
        data['name'] = new
        data['metadata']['updated'] = self.updated
        entry.write_text(render(data, body), encoding='utf-8', newline='\n')
        self.refresh()
        return {'renamed': new}

    def remove(self, names, apply=False):
        if len(set(names)) != len(names):
            raise ValueError('Each skill may appear only once in a removal request')
        packages = [self.package(name) for name in names]
        if any(not (path / 'SKILL.md').is_file() for path in packages):
            raise ValueError('Every requested skill must exist')
        if apply:
            for path in packages:
                shutil.rmtree(path)
            self.fix_links(apply=True)
            self.refresh()
        return {'skills': names, 'applied': apply}

    def audit(self):
        bodies, overlaps = {}, []
        entries = []
        stop = {'the', 'and', 'for', 'with', 'when', 'use', 'skill', 'this', 'from', 'into', 'that'}
        for path in self.entrypoints():
            data, body = parse(path.read_text(encoding='utf-8'))
            digest = hashlib.sha256(re.sub(r'\s+', ' ', body).strip().encode()).hexdigest()
            bodies.setdefault(digest, []).append(data['name'])
            words = set(re.findall(r'[a-z][a-z0-9]+', data['description'].lower())) - stop
            entries.append((data['name'], words))
        for index, (name, words) in enumerate(entries):
            for other, other_words in entries[index + 1:]:
                score = len(words & other_words) / max(1, len(words | other_words))
                if score >= 0.6:
                    overlaps.append({'skills': [name, other], 'description_similarity': round(score, 3)})
        return {'exact_body_duplicates': [names for names in bodies.values() if len(names) > 1],
                'review_candidates': sorted(overlaps, key=lambda row: -row['description_similarity']),
                'note': 'Similarity identifies review candidates, not permission to merge distinct capabilities.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--date', help='ISO maintenance date; defaults to the local date')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['check', 'refresh', 'audit']:
        sub.add_parser(name)
    for name in ['normalize', 'fix-links']:
        sub.add_parser(name).add_argument('--apply', action='store_true')
    new = sub.add_parser('new')
    new.add_argument('name')
    new.add_argument('--description', required=True)
    new.add_argument('--collection', choices=COLLECTIONS, default='optional')
    new.add_argument('--apply', action='store_true')
    rename = sub.add_parser('rename')
    rename.add_argument('old')
    rename.add_argument('new')
    rename.add_argument('--apply', action='store_true')
    remove = sub.add_parser('remove')
    remove.add_argument('names', nargs='+')
    remove.add_argument('--apply', action='store_true')
    args = parser.parse_args(argv)
    library = Library(args.root, args.date)
    try:
        if args.command == 'check':
            errors = library.validate()
            print(json.dumps({'skills': len(library.entrypoints()), 'errors': errors}, indent=2))
            return int(bool(errors))
        if args.command == 'refresh':
            result = {'skills': len(library.refresh())}
        elif args.command == 'normalize':
            result = {'changed': library.normalize(args.apply), 'applied': args.apply}
        elif args.command == 'fix-links':
            result = {'links': library.fix_links(args.apply), 'applied': args.apply}
        elif args.command == 'new':
            result = library.new(args.name, args.description, args.collection, args.apply)
        elif args.command == 'rename':
            result = library.rename(args.old, args.new, args.apply)
        elif args.command == 'remove':
            result = library.remove(args.names, args.apply)
        else:
            result = library.audit()
        print(result if isinstance(result, str) else json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
