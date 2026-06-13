# Code Review Guidelines

## Scope

In scope:

- Role changes (`roles/`)
- Lookup/module plugin changes (`plugins/`)
- Test changes (`tests/`, `roles/*/molecule/`)
- CI/CD workflow changes
- Renovate configuration updates
- Collection metadata (`galaxy.yml`, `meta/`)

Out of scope:

- `.ansible/` directories — local galaxy/fact caches
- Renovate dependency-only PRs (patch/minor with automerge enabled)
- Generated changelog entries from release automation

## Required checks

- No secrets committed — no credentials, tokens, or keys in defaults/vars/templates
- `ansible-lint --profile=production` passes
- yamllint passes
- Unit tests (pytest) pass for plugins
- Molecule / integration tests pass for affected roles
- Security scans pass (gitleaks, secretlint, trivy)
- `argument_specs.yml` present and complete for any new or changed role

## Severity levels

| Level        | Meaning                                             | Merge impact       |
| ------------ | --------------------------------------------------- | ------------------ |
| Bug          | Incorrect behavior or broken contract               | Blocks merge       |
| Nit          | Minor issue — suboptimal but not incorrect          | Non-blocking       |
| Pre-existing | Issue present before this PR; flagged for awareness | No action required |

## Skip

- Renovate PRs with `automerge: true` (patch/minor) after CI passes
- Documentation-only changes with no functional impact
