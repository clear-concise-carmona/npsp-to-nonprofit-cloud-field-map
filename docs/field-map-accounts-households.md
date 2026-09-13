# Accounts Households: Field Map

_Generated from `field-map/accounts-households.yaml` by `scripts/generate_tables.py`. Do not hand-edit this file - edit the YAML source and regenerate._

## Object-level mapping

**NPSP object(s):** `Account (Household Account model) / npsp__Household__c (legacy Household object, pre-2016)`

NPSP's default data model since 2016 uses a "Household Account" - a standard Account record (record type: Household Account) that groups one or more Contacts. The legacy npsp__Household__c custom object still exists for orgs that never migrated off the pre-2016 Household object model.

**Nonprofit Cloud object(s):** `Account (Person Account record type) or standard Account for organizations`

Nonprofit Cloud's Fundraising data model is built around standard Salesforce Person Accounts for individual constituents rather than a Household-grouping Account. There is no direct "Household Account" concept carried over.

**Relationship: Redesign required**

This is the single largest structural change in the entire migration. NPSP's Household Account groups multiple Contacts under one Account record for combined giving history and mail-merge/soft-credit rollups. Nonprofit Cloud instead gives each individual constituent their own Person Account. There is no automated, lossless field-level mapping for this object - it requires a data model redesign, not a migration script. Multi-member household grouping, if still needed, must be rebuilt using a different mechanism (e.g., a custom household/grouping object, or Salesforce's relationship groups) rather than inherited directly from NPSP.

Sources: [source](https://www.charityplatform.com/blog/salesforce-nonprofit-cloud-migration-from-npsp); [source](https://magicfuse.co/blog/salesforce-nonprofit-cloud-vs-npsp); [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud)

## Field-level mapping

| NPSP field | Nonprofit Cloud field | Relationship | Confidence | Notes | Source |
|---|---|---|---|---|---|
| `Account.npe01__SYSTEM_AccountType__c` | `Account.RecordTypeId (Person Account record type)` | Redesign required | Inferred | NPSP flags an Account as a household/individual via this system field plus record type. Nonprofit Cloud uses Salesforce's native Person Account record type mechanism instead - there's no field-for-field copy, the record type itself has to change. | [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud) |
| `Account.Name (Household Account naming, e.g. 'Smith Household')` | `Account.Name (Person Account, auto-derived from FirstName/LastName)` | Redesign required | Inferred | Household naming conventions (e.g. NPSP's auto-generated "<LastName> Household") have no meaning once each person is their own Person Account. Any custom household-naming logic does not carry over and needs a replacement if multi-member grouping is still required. | [source](https://www.charityplatform.com/blog/salesforce-nonprofit-cloud-migration-from-npsp) |
| `Account.npo02__Formal_Greeting__c / npo02__Informal_Greeting__c` | `No direct equivalent found on Person Account` | No equivalent | Unconfirmed | These greeting fields are commonly used for mail-merge on the Household Account. No Nonprofit Cloud Fundraising object was found in Salesforce's developer documentation that replicates this concept as of the objects reviewed for this map. Flagging as open - please file an issue with a source if you've confirmed a replacement field or object. | _none cited_ |
| `Account.npo02__TotalOppAmount__c / npo02__NumberOfClosedOpps__c (household rollups)` | `DonorGiftSummary` | Redesign required | Confirmed | Nonprofit Cloud has a dedicated DonorGiftSummary object (API v59.0+) that represents gift summaries for accounts and contacts, replacing NPSP's household-level rollup fields on Account. The rollup no longer lives directly on Account - it's a related summary record. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
| `Contact.npe01__Household__c (legacy Household lookup, pre-2016 model only)` | `n/a - superseded by Person Account model entirely` | No equivalent | Confirmed | Orgs still on the legacy pre-2016 npsp__Household__c object model have an extra migration step: move to the modern Household Account model first, then plan the Nonprofit Cloud migration. Do not attempt to map the legacy object directly to Nonprofit Cloud. | [source](https://magicfuse.co/blog/salesforce-nonprofit-cloud-vs-npsp) |
