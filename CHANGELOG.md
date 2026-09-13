# Changelog

## 1.0.0 - 2026-09-13

Initial public release.

- Field-map YAML source of truth for six areas: Accounts & Households, Contacts,
  Opportunities/Payments/Gifts, Recurring Donations, Allocations & GAUs, Affiliations &
  Relationships.
- `scripts/generate_tables.py` - YAML to Markdown table generator.
- `scripts/validate_org.py` - live-org schema validator via the Salesforce REST Describe API.
- Every field-level entry tagged with `relationship` and `confidence`, with sources cited or
  explicitly marked absent.
- Known gap flagged up front: Affiliations & Relationships has no confirmed Salesforce-documented
  object-level replacement as of this release.
