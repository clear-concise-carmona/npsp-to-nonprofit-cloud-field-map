# Affiliations Relationships: Field Map

_Generated from `field-map/affiliations-relationships.yaml` by `scripts/generate_tables.py`. Do not hand-edit this file - edit the YAML source and regenerate._

## Object-level mapping

**NPSP object(s):** `npe5__Affiliation__c (Contact-to-Organization) + npsp__Relationship__c (Contact-to-Contact)`

NPSP tracks two distinct kinds of connection: Affiliations link a Contact to an organization Account (e.g. employer, board membership), and Relationships link two Contacts to each other (e.g. spouse, parent/child) with reciprocal-role automation.

**Nonprofit Cloud object(s):** `Native Salesforce Person Account relationship groups (per community/practitioner reporting)`

Independent practitioner writeups (not yet cross-checked against an official Salesforce object reference for this specific pairing) describe Nonprofit Cloud leaning on Person Accounts plus standard/native Salesforce relationship-group mechanisms rather than NPSP's two custom junction objects.

**Relationship: Redesign required**

This entry carries the lowest confidence in the whole map. Unlike the Fundraising objects (GiftCommitment, GiftTransaction, etc.), Salesforce's own Nonprofit Cloud developer documentation reviewed for this project did not surface a direct, object-level replacement for npe5__Affiliation__c or npsp__Relationship__c. The source below discusses Person Accounts, groups, and relationships in Nonprofit Cloud generally, but a field-level crosswalk has not been confirmed. Treat this file as the least mature part of the map and prioritize validating it against a live Nonprofit Cloud sandbox before relying on it for a migration.

Sources: [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud); [source](https://www.odnosworks.com/post/what-s-new-and-what-s-not-in-salesforce-nonprofit-cloud)

## Field-level mapping

| NPSP field | Nonprofit Cloud field | Relationship | Confidence | Notes | Source |
|---|---|---|---|---|---|
| `npe5__Affiliation__c.npe5__Contact__c / npe5__Organization__c` | `Not confirmed - likely a native Account-to-Account or Contact-to-Account relationship construct` | No equivalent | Unconfirmed | No object-level confirmation found in the Salesforce developer documentation reviewed for this map. Open item - please file an issue with a source (official docs preferred, a screenshot of a live org's schema acceptable) if you've confirmed the replacement. | _none cited_ |
| `npsp__Relationship__c.npsp__RelatedContact__c / npsp__Type__c / npsp__ReciprocalType__c` | `Not confirmed` | No equivalent | Unconfirmed | Same status as the row above - flagged as an open research item rather than guessed at. This map will not put a specific field name here without a citable source. | _none cited_ |
| `npsp__Relationship__c (auto-reciprocal-role automation, e.g. Parent <-> Child)` | `Not confirmed` | No equivalent | Unconfirmed | If Nonprofit Cloud has no equivalent automation, orgs relying heavily on NPSP's reciprocal relationship engine (e.g. for household mail-merge or grant reporting) should treat this as a required custom-build item in the migration plan, not an assumed carryover. | _none cited_ |
