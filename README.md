# npsp-to-nonprofit-cloud-field-map

A source-cited **NPSP field mapping** for anyone planning an **NPSP to Nonprofit Cloud migration**:
every Nonprofit Success Pack (NPSP) object and field lined up against its equivalent in the new
**Agentforce nonprofit data model**, with the gaps flagged instead of papered over.

## Why this exists

NPSP has been frozen since 2023 - no new features shipped since March of that year, no announced
retirement date - and new nonprofit orgs are now routed to Nonprofit Cloud by default
([Salesforce Ben](https://www.salesforceben.com/the-state-of-salesforce-nonprofit-offerings-in-2026/); [ynexgen](https://ynexgen.com/blog/is-npsp-going-away)). Every org still running NPSP is on a clock, whether or not anyone's told
them so. That leaves a large number of orgs planning a migration with no
Salesforce-published field-level crosswalk between the two data models. Blog posts describe the
high-level shape of the change - Person Accounts replace Household Accounts, and the **Nonprofit
Cloud Gift Commitment** object (GiftCommitment) plus GiftTransaction replace Opportunity + Payment
([charityplatform](https://www.charityplatform.com/blog/salesforce-nonprofit-cloud-migration-from-npsp)) - but nobody has published the field-by-field detail, and NPSP and Nonprofit Cloud can't run in
the same org side by side while you figure it out ([MagicFuse](https://magicfuse.co/blog/salesforce-nonprofit-cloud-vs-npsp)).

This repo is that detail: a field-by-field NPSP field mapping built from Salesforce's own developer
documentation wherever possible, with every entry tagged by how confident we actually are in it.
Where the docs didn't say, we say so instead of guessing.

**This is not a Salesforce product and is not officially endorsed by Salesforce.** It's an
independent reference maintained by [Clear Concise Consulting](https://www.clearconciseconsulting.com),
built because we needed it for client migration work and didn't want to rebuild it privately every
time.

## Quick start

**Browse the map as tables:** everything in [`docs/`](docs/) is human-readable Markdown, generated
from the YAML source of truth:

- [Accounts & Households](docs/field-map-accounts-households.md)
- [Contacts](docs/field-map-contacts.md)
- [Opportunities, Payments & Gifts](docs/field-map-opportunities-payments-gifts.md)
- [Recurring Donations](docs/field-map-recurring-donations.md)
- [Allocations & General Accounting Units](docs/field-map-allocations-gau.md)
- [Affiliations & Relationships](docs/field-map-affiliations-relationships.md)

**Validate against your own org:**

```bash
pip install -r scripts/requirements.txt
export SF_INSTANCE_URL="https://your-domain.my.salesforce.com"
export SF_ACCESS_TOKEN="..."   # e.g. from `sf org display --json`
python scripts/validate_org.py --side both
```

This runs read-only schema describe calls against your org and reports every map entry that
doesn't match what your org's schema actually has - useful both for orgs still on NPSP (confirming
the source side) and for sandboxes already provisioned with Nonprofit Cloud (confirming the target
side).

**Regenerate the docs after editing the YAML:**

```bash
python scripts/generate_tables.py
```

## How the map is organized

Each file in [`field-map/`](field-map/) is a YAML source of truth for one area of the data model.
Every field-level entry carries:

| Attribute | Meaning |
|---|---|
| `relationship` | `direct`, `renamed`, `redesign_required`, `no_equivalent`, or `new_in_npc` |
| `confidence` | `confirmed` (verified against Salesforce docs), `inferred` (derived but not explicit), or `unconfirmed` (practitioner-reported, not yet verified) |
| `sources` | The actual URL(s) the entry is based on - never left as a bare claim |

**Read the confidence column before you trust a row.** Some of the Fundraising object fields
(GiftCommitment, GiftTransaction) are confirmed straight from Salesforce's developer guide. Some of
the Affiliation/Relationship mappings are marked `unconfirmed` because Salesforce's own docs don't
yet spell out a replacement - that file says so plainly rather than inventing a plausible-sounding
field name.

## Known gaps

- **Affiliations & Relationships** (`npe5__Affiliation__c`, `npsp__Relationship__c`) has no
  confirmed object-level replacement in the Salesforce documentation reviewed for this project.
  This is the least mature file in the repo - see
  [field-map-affiliations-relationships.md](docs/field-map-affiliations-relationships.md).
- Several Recurring Donation (RD2) status and type fields are marked `inferred` or `unconfirmed`
  pending validation against a live Nonprofit Cloud org.
- Exact field-level API names within `GiftDesignation` and `GiftTransactionDesignation` were not
  enumerated in the Salesforce pages reviewed so far.

If you've confirmed any of these against a live org or a newer Salesforce doc, please open a pull
request - see [CONTRIBUTING.md](CONTRIBUTING.md).

## A note on NPSP-to-Nonprofit-Cloud migration planning

If you're at the "should we migrate, and how bad will it be" stage rather than the "here's our
field map" stage, see Salesforce's own migration implementation guide
([help.salesforce.com](https://help.salesforce.com/s/articleView?id=sfdo.NPC_Implementation_Migration_Guides.htm&language=en_US))
and consider running the [npsp-migration-readiness-scanner](https://github.com/clear-concise-carmona/npsp-migration-readiness-scanner) -
a companion tool that scores your NPSP to Nonprofit Cloud assessment 0-100 and flags nonprofit cloud
migration risk - against your org first. It shows how much of this map's "redesign required"
territory your specific org actually touches, rather than treating the whole migration as one
undifferentiated project.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: every new or edited row needs a source. "I
think this is right" is not a source.

## About

Maintained by [Jeremy Carmona](https://www.clearconciseconsulting.com/about), a 13x certified
Salesforce Architect and founder of [Clear Concise Consulting](https://www.clearconciseconsulting.com),
a Salesforce consultancy for nonprofit, healthcare, and enterprise organizations. If you're planning
an NPSP-to-Nonprofit-Cloud migration and want a second set of eyes on scope before you start,
[get in touch](https://www.clearconciseconsulting.com/contact).

## License

[MIT](LICENSE) for all code in this repo (`scripts/`). The field-map data itself
(`field-map/*.yaml`, `docs/*.md`) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) -
reuse it anywhere, just keep the attribution and the source citations intact.
