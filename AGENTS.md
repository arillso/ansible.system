# arillso.system

Ansible collection with roles and plugins that configure Linux hosts. Roles live
in `roles/`, plugins in `plugins/{filter,lookup,modules}`, molecule scenarios in
`extensions/molecule/`.

## Commands

Most `make` targets print `SKIP: …` and exit 0 when their tool is missing, so a
green local run can mean nothing ran; CI is the gate.

- Install the repository's Lefthook hooks with `lefthook install`; see
  [lefthook.yml](lefthook.yml) for the checks they run.
- `make test` runs `pytest tests/unit/` as a fast local smoke test. CI runs the
  same directory through `ansible-test units --docker` (job `unit-test` of the
  reusable `ci-ansible-collection.yml`). The two runners collect tests
  differently, so a green `make test` does not guarantee green CI. Treat the
  `ansible-test` run as authoritative.
- `ansible-test` (and `make test-integration`) only works when the collection
  sits at `.../ansible_collections/arillso/system/`. Copy the tree with
  `git archive HEAD | tar -x -C <dir>`; a symlink fails because `ansible-test`
  resolves the real path.
- `make test-molecule-<role>` runs one scenario from `extensions/molecule/`
  against the installed collection, not the working tree. Reinstall with
  `ansible-galaxy collection install . --force` after every change; setup steps
  are in `tests/README.md`, section "Running scenarios".

## Conventions

- Organization-wide conventions are defined in
  [arillso/.github/AGENTS.md](https://github.com/arillso/.github/blob/main/AGENTS.md).
- Changelog and breaking-change rules are documented in
  [CONTRIBUTING.md](CONTRIBUTING.md#submitting-changes).
- Before adding a role or a plugin, load the skill `adding-role-or-plugin`
  (`.claude/skills/adding-role-or-plugin/`). It lists the mandatory role files,
  including `meta/argument_specs.yml`, and where plugin documentation lives per
  plugin type.

## Traps

- The molecule matrix in `.github/workflows/pull-request.yml` is pinned, not
  discovered. A new scenario under `extensions/molecule/<role>/` runs in CI only
  after it is added to the `scenarios:` list of the `molecule` job.
  Kernel-bound scenarios (`zram`, `tuning`) run in their own jobs with
  `driver: qemu`; a docker-driver job does not provision QEMU/KVM.
- A job calling a reusable workflow must grant every permission the reusable
  declares. A narrower grant fails the whole workflow with `startup_failure`
  before any job runs, without logs.

## Further docs

- Before changing tests, adding an integration target or a molecule scenario,
  read `tests/README.md`.
- Before cutting a release, follow `CONTRIBUTING.md` section "Release Process".
  Tags carry no `v` prefix; `tag.yml` triggers only on `X.Y.Z`.
- `REVIEW.md` sets scope and severity for the `claude-review` job in
  `pull-request.yml`. Change review behaviour there.
