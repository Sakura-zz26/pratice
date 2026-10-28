"""Run all five Lecture 1 activities in isolated, explicitly simulated workspaces."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile

def page(title, text):
    return f'<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8"><title>{title}</title></head>\n<body>\n<h1>{title}</h1>\n<p>{text}</p>\n</body>\n</html>\n'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--remote')
    parser.add_argument('--run-id', default=os.environ.get('PRACTICE_RUN_ID', 'local'))
    parser.add_argument('--output', default='evidence/lecture1')
    args = parser.parse_args()
    remote = args.remote or 'https://github.com/' + os.environ['PRACTICE_REPOSITORY'] + '.git'
    if '://' not in remote:
        remote = str(Path(remote).resolve())
    prefix = 'practice/run-' + re.sub(r'[^A-Za-z0-9_-]', '-', args.run_id)[:70]
    main_ref = prefix + '/main'
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    records = {'started_utc': datetime.now(timezone.utc).isoformat(), 'remote': remote,
               'branch_prefix': prefix, 'mode': 'solo workspaces executed with Codex assistance',
               'activities': [], 'conflicts': []}
    transcript = output / 'commands.log'
    transcript.write_text('Real command transcript; leader/member names are simulated workspaces.\n')
    environment = os.environ.copy()
    environment.update({'GIT_TERMINAL_PROMPT': '0', 'GIT_EDITOR': 'true', 'GIT_MERGE_AUTOEDIT': 'no'})

    with tempfile.TemporaryDirectory(prefix='git-course-practice-') as temporary:
        base = Path(temporary)
        askpass = base / 'askpass.sh'
        askpass.write_text('#!/bin/sh\ncase "$1" in *Username*) printf "%s\\n" "x-access-token";; *) printf "%s\\n" "$PRACTICE_TOKEN";; esac\n')
        askpass.chmod(0o700)
        environment['GIT_ASKPASS'] = str(askpass)

        def run(where, *command, expected=0):
            result = subprocess.run(command, cwd=where, env=environment, text=True, capture_output=True, timeout=120)
            label = Path(where).name
            with transcript.open('a') as stream:
                stream.write(f'\n[{label}] $ {shlex.join(command)}\n{result.stdout}{result.stderr}[exit {result.returncode}]\n')
            if result.returncode != expected:
                raise RuntimeError(f'{label}: {shlex.join(command)} returned {result.returncode}\n{result.stderr}')
            return result.stdout.strip()

        def git(where, *command, expected=0):
            return run(where, 'git', *command, expected=expected)

        def config(where):
            git(where, 'config', 'user.name', 'Codex assisted solo exercise')
            git(where, 'config', 'user.email', '306978125+Sakura-zz26@users.noreply.github.com')

        def commit(where, message):
            git(where, 'add', '.')
            git(where, 'commit', '-m', message)
            return git(where, 'rev-parse', 'HEAD')

        def push(where, branch='main', remote_branch=None):
            git(where, 'push', 'origin', branch + ':refs/heads/' + (remote_branch or main_ref))

        def sync(where):
            git(where, 'fetch', 'origin')
            git(where, 'switch', 'main')
            git(where, 'reset', '--hard', 'origin/' + main_ref)

        def passed(number, name, **details):
            records['activities'].append({'activity': number, 'name': name, 'status': 'passed', **details})
            print(f'Activity {number} passed: {name}', flush=True)

        leader = base / 'leader'
        leader.mkdir()
        git(leader, 'init', '--initial-branch=main')
        config(leader)
        git(leader, 'remote', 'add', 'origin', remote)
        git(leader, 'remote', '-v')
        (leader / 'index.html').write_text(page('Base title', 'Base description'))
        (leader / 'README.md').write_text('# Solo Git practice\n\nLeader and member labels are simulated workspaces run with Codex assistance.\n')
        initial = commit(leader, 'Activity 1: initialize solo practice repository')
        git(leader, 'push', '--set-upstream', 'origin', 'main:refs/heads/' + main_ref)
        passed(1, 'Create, initialize and associate the remote', initial_commit=initial, remote_branch=main_ref)

        members = []
        for number in [1, 2]:
            member = base / f'member{number}'
            run(base, 'git', 'clone', '--branch', main_ref, '--single-branch', remote, str(member))
            git(member, 'branch', '-m', 'main')
            # Fetch the exercise branches needed by later activities.
            git(member, 'config', 'remote.origin.fetch', '+refs/heads/' + prefix + '/*:refs/remotes/origin/' + prefix + '/*')
            config(member)
            git(member, 'pull', '--ff-only')
            with (member / 'README.md').open('a') as stream:
                stream.write(f'\nSimulated member {number} workspace synchronized.\n')
            commit(member, f'Activity 2: commit from simulated member {number} workspace')
            push(member)
            members.append(member)
            git(leader, 'pull', '--ff-only')
        for member in members:
            git(member, 'pull', '--ff-only')
        passed(2, 'Clone two workspaces, commit and synchronize', workspace_count=3, collaborators_invited=0)

        git(leader, 'switch', '-c', 'leader-feature')
        (leader / 'leader.html').write_text(page('Leader feature', 'Solo leader workspace'))
        commit(leader, 'Activity 3: add leader HTML feature')
        push(leader, 'leader-feature', prefix + '/leader-feature')
        git(leader, 'switch', 'main')
        git(leader, 'merge', '--no-ff', 'leader-feature', '-m', 'Activity 3: merge leader feature')
        push(leader)
        for number, member in enumerate(members, start=1):
            git(member, 'pull', '--ff-only')
            feature = f'member{number}-feature'
            git(member, 'switch', '-c', feature)
            (member / f'member{number}.html').write_text(page(f'Member {number}', f'Member {number} base'))
            commit(member, f'Activity 3: add simulated member {number} feature')
            push(member, feature, prefix + '/' + feature)
            git(leader, 'fetch', 'origin', prefix + '/' + feature)
            git(leader, 'merge', '--no-ff', 'FETCH_HEAD', '-m', f'Activity 3: merge member {number} feature')
            push(leader)
            git(member, 'switch', 'main')
        for member in members:
            git(member, 'pull', '--ff-only')
            assert all((member / f).is_file() for f in ['index.html', 'leader.html', 'member1.html', 'member2.html'])
        passed(3, 'Create feature branches, merge and synchronize HTML files', merged_features=3)

        # Rewrite only this run's isolated branch and retain the old commit in a snapshot branch.
        text = (leader / 'index.html').read_text().replace('Base title', 'Updated tite')
        (leader / 'index.html').write_text(text)
        old_amend = commit(leader, 'Activity 4: title update before amendment')
        push(leader)
        push(leader, 'HEAD', prefix + '/before-amend')
        text = text.replace('Updated tite', 'Updated title').replace('</body>', '<p>Description added during amend.</p>\n</body>')
        (leader / 'index.html').write_text(text)
        git(leader, 'add', 'index.html')
        git(leader, 'commit', '--amend', '-m', 'Activity 4: correct title and add missing description')
        new_amend = git(leader, 'rev-parse', 'HEAD')
        git(leader, 'push', '--force-with-lease=refs/heads/' + main_ref + ':' + old_amend, 'origin', 'HEAD:refs/heads/' + main_ref)
        assert old_amend != new_amend

        member1, member2 = members
        sync(member1)
        original_member1 = (member1 / 'member1.html').read_text()
        (member1 / 'member1.html').write_text(original_member1.replace('</body>', '<p>Accidental addition</p>\n</body>'))
        accidental = commit(member1, 'Activity 4: accidental addition for revert demonstration')
        push(member1)
        git(member1, 'log', '--oneline', '-4')
        git(member1, 'revert', '--no-edit', accidental)
        reverted = git(member1, 'rev-parse', 'HEAD')
        push(member1)
        assert (member1 / 'member1.html').read_text() == original_member1

        sync(member2)
        reset_target = git(member2, 'rev-parse', 'HEAD')
        (member2 / 'temporary.txt').write_text('Disposable reset exercise file.\n')
        reset_old = commit(member2, 'Activity 4: unnecessary commit for reset demonstration')
        push(member2)
        push(member2, 'HEAD', prefix + '/before-reset')
        git(member2, 'log', '--oneline', '-3')
        git(member2, 'reset', '--hard', reset_target)
        git(member2, 'push', '--force-with-lease=refs/heads/' + main_ref + ':' + reset_old, 'origin', 'HEAD:refs/heads/' + main_ref)
        assert not (member2 / 'temporary.txt').exists()
        sync(leader)
        git(leader, 'log', '--oneline', '-5')
        git(leader, 'checkout', initial)
        assert (leader / 'index.html').read_text() == page('Base title', 'Base description')
        git(leader, 'switch', 'main')
        passed(4, 'Amend, revert, reset and inspect a commit by hash',
               amend_before=old_amend, amend_after=new_amend, reverted_commit=accidental,
               revert_commit=reverted, reset_before=reset_old, reset_after=reset_target, inspected_commit=initial)

        # Conflicts require overlapping edits to the same lines, not merely different files.
        for member in members:
            sync(member)
        git(member1, 'switch', '-c', 'member1-rebase')
        (member1 / 'member1.html').write_text((member1 / 'member1.html').read_text().replace('Member 1 base', 'Member 1 feature edit'))
        feature1 = commit(member1, 'Activity 5: edit the shared member1 paragraph on a feature branch')
        push(member1, 'HEAD', prefix + '/member1-rebase')
        git(member2, 'switch', '-c', 'member2-rebase')
        (member2 / 'index.html').write_text((member2 / 'index.html').read_text().replace('<h1>Updated title</h1>', '<h1>Member 2 feature heading</h1>'))
        feature2 = commit(member2, 'Activity 5: edit the shared index heading on a feature branch')
        push(member2, 'HEAD', prefix + '/member2-rebase')
        (leader / 'member1.html').write_text((leader / 'member1.html').read_text().replace('Member 1 base', 'Main branch member1 edit'))
        (leader / 'index.html').write_text((leader / 'index.html').read_text().replace('<h1>Updated title</h1>', '<h1>Main branch heading</h1>'))
        commit(leader, 'Activity 5: overlapping main-branch changes to demonstrate conflicts')
        push(leader)

        for number, member, filename, old_feature in [(1, member1, 'member1.html', feature1), (2, member2, 'index.html', feature2)]:
            git(member, 'fetch', 'origin')
            git(member, 'rebase', 'origin/' + main_ref, expected=1)
            unmerged = git(member, 'diff', '--name-only', '--diff-filter=U').splitlines()
            assert unmerged == [filename], unmerged
            conflict = (member / filename).read_text()
            assert '<<<<<<<' in conflict and '>>>>>>>' in conflict
            (output / f'member{number}_conflict.txt').write_text(conflict)
            if number == 1:
                resolved = page('Member 1', 'Main branch member1 edit; Member 1 feature edit')
            else:
                resolved = (leader / 'index.html').read_text().replace('<h1>Main branch heading</h1>', '<h1>Main branch heading and Member 2 feature heading</h1>')
            (member / filename).write_text(resolved)
            git(member, 'add', filename)
            git(member, 'rebase', '--continue')
            new_feature = git(member, 'rev-parse', 'HEAD')
            remote_feature = prefix + f'/member{number}-rebase'
            git(member, 'push', '--force-with-lease=refs/heads/' + remote_feature + ':' + old_feature, 'origin', 'HEAD:refs/heads/' + remote_feature)
            git(leader, 'fetch', 'origin', remote_feature)
            git(leader, 'merge', '--no-ff', 'FETCH_HEAD', '-m', f'Activity 5: integrate resolved member {number} feature')
            push(leader)
            records['conflicts'].append({'workspace': f'member{number}', 'file': filename, 'before_rebase': old_feature, 'after_rebase': new_feature, 'status': 'resolved'})

        for number, member in enumerate(members, start=1):
            sync(member)
            git(member, 'branch', '-d', f'member{number}-feature')
            git(member, 'branch', '-d', f'member{number}-rebase')
        git(leader, 'branch', '-d', 'leader-feature')
        final = git(leader, 'rev-parse', 'HEAD')
        for workspace in [leader, *members]:
            assert git(workspace, 'rev-parse', 'HEAD') == final
            for name in ['index.html', 'leader.html', 'member1.html', 'member2.html']:
                content = (workspace / name).read_text()
                assert '<<<<<<<' not in content and '>>>>>>>' not in content
        git(leader, 'fetch', 'origin')
        graph = git(leader, 'log', '--graph', '--oneline', '--all', '-40')
        git(leader, 'fsck', '--full')
        git(leader, 'bundle', 'create', str(output / 'lecture1-history.bundle'), '--all')
        git(leader, 'bundle', 'verify', str(output / 'lecture1-history.bundle'))
        passed(5, 'Rebase, resolve two real conflicts, integrate and clean local branches', final_commit=final)
        records['completed_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
        summary = '# Lecture 1 practical execution\n\n'
        summary += f"Mode: {records['mode']}.\n\nRemote branch: `{main_ref}`.\n\n"
        summary += '\n'.join(f"- Activity {a['activity']}: {a['name']} - {a['status']}" for a in records['activities'])
        summary += '\n\nTwo real overlapping rebase conflicts were resolved. The commands log includes before/after states and exit codes. No additional collaborators were invited.\n\n```text\n' + graph + '\n```\n'
        (output / 'summary.md').write_text(summary)

if __name__ == '__main__':
    main()
