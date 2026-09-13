# Contributing

This repo's only real value is that its claims are checkable. That rule applies to contributions
too.

## Rules for any new or edited field-map row

1. **Every row needs a `sources` entry, or an explicit empty list with a note explaining why.**
   Official Salesforce documentation (developer docs, help articles) beats community blog posts.
   Community blog posts beat nothing. Nothing beats a guess - if you can't cite it, mark it
   `confidence: unconfirmed` and leave `sources: []` rather than inventing a plausible field name.
2. **Set `confidence` honestly:**
   - `confirmed` - you read it directly in Salesforce's own documentation, or verified it against
     a live org's schema with `scripts/validate_org.py`.
   - `inferred` - the object/behavior is documented, but the specific field-level detail in this
     row is your best reasonable read of that documentation, not a verbatim statement.
   - `unconfirmed` - reported by a practitioner (blog, community thread) but not yet checked
     against docs or a live org.
3. **Set `relationship` from the fixed set:** `direct`, `renamed`, `redesign_required`,
   `no_equivalent`, `new_in_npc`. Don't add new values without discussing in an issue first - the
   generator script and any downstream tooling (including `npsp-migration-readiness-scanner`)
   depend on this exact set.
4. **Edit the YAML in `field-map/`, never the generated files in `docs/`.** Run
   `python scripts/generate_tables.py` after editing and commit the regenerated docs alongside
   your YAML change in the same PR.

## Especially wanted

- Anything that resolves an `unconfirmed` row in
  [`field-map/affiliations-relationships.yaml`](field-map/affiliations-relationships.yaml) - this
  is the least mature file in the repo.
- Field-level API names for `GiftDesignation` / `GiftTransactionDesignation` (currently only
  object-level detail is confirmed).
- Corrections from anyone who has run an actual NPSP-to-Nonprofit-Cloud migration and found a row
  here wrong. Migration experience beats documentation reading every time - just still cite it
  (a description of what you saw in your own org's schema is a valid source).

## How to submit

1. Fork, branch, edit the relevant YAML file(s).
2. Run `python scripts/generate_tables.py` and commit the regenerated `docs/*.md` files too.
3. Open a PR describing what changed and why, with your source(s) linked in the PR description as
   well as in the YAML.

## Code changes (`scripts/`)

Keep `generate_tables.py` and `validate_org.py` dependency-light (PyYAML and requests only,
currently) - this repo's audience includes people who will run these scripts once, not people
maintaining a long-running service.
