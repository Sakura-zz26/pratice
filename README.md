# pratice

## 43030 GitHub practical activities

This repository contains a Codex-assisted implementation of the Lecture 1 and Lecture 2 practical activities. The exercises use one account and separate workspaces to simulate the leader and two members; they do not represent collaboration with additional people.

### Run and inspect

The **GitHub Practical Activities** workflow runs on a push to `main` or through **Actions → GitHub Practical Activities → Run workflow**.

1. Lecture 1 performs real Git commands against isolated branches named `practice/run-<run-id>/...`. It tests initialization, cloning, synchronization, branching, merging, amend, revert, reset, checkout by hash and two deliberately overlapping rebase conflicts.
2. Lecture 2 updates `index.html` for the actual workflow actor, appends a timestamp and source commit to this README, and commits the generated records back to `main`.
3. Inspect `evidence/lecture1/results.json`, `evidence/lecture1/commands.log` and `evidence/lecture1/summary.md` after a successful run. Download the **git-practical-evidence** Actions artifact for conflict records and a Git bundle.

Reset and history rewriting are limited to disposable workspaces and the workflow's own practice branches. The repository's main branch is not force-pushed.

### Activity mapping

| Lecture | Activity | Implementation and evidence |
| --- | --- | --- |
| 1 | 1 Create and initialize | Initialize a workspace, associate the GitHub remote and push a new isolated practice branch |
| 1 | 2 Clone and associate | Clone two workspaces from the practice branch, commit changes and synchronize |
| 1 | 3 Branching and merging | Create leader/member feature branches, merge and verify all HTML files |
| 1 | 4 Amend, revert, reset and hash checkout | Record before/after hashes and check expected file states |
| 1 | 5 Rebase and resolve conflicts | Produce real overlapping conflicts, retain markers, resolve, continue and integrate |
| 2 | 1 Setup workflow | `.github/workflows/main.yml` |
| 2 | 2 Update HTML | `scripts/update_records.py html` selects a page by actor |
| 2 | 3 Update README | `scripts/update_records.py readme` logs actor, UTC time and source commit |
| 2 | 4 Commit changes | Explicit staging and commit/push step using the workflow token |
| 2 | 5 Test workflow | Local integration checks plus the actual Actions job and generated commit |

### GitHub Pages

The workflow also includes an optional Pages deployment job. To publish, the repository owner must enable **Settings → Pages → Source → GitHub Actions** and create the repository Actions variable `ENABLE_PAGES` with value `true`, then run the workflow. Pages is not considered enabled or deployed until the deployment job succeeds. A private repository also requires a plan that supports Pages for private repositories. Keep the repository private unless you choose to publish it.

### Repeat locally

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git init --bare /tmp/git-practical-remote.git
python3 scripts/run_git_practicals.py --remote /tmp/git-practical-remote.git --run-id local-demo --output /tmp/git-practical-evidence
```

The local repeat uses a bare local remote. An actual GitHub Actions run uses the authenticated GitHub remote and records its run ID. Review the commands and repeat the exercises to assess independent proficiency.

### References

- UTS. Lecture 1 Practical Activities and Lecture 2 Practical Activities, supplied course materials.
- GitHub. [Use GITHUB_TOKEN for authentication](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
- GitHub. [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
- GitHub. [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Workflow update log

### Updated by Sakura-zz26 (Solo learner) on 2026-10-28 02:03:22 UTC [Commit: be9d663da6af]
