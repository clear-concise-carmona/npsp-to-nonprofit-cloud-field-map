# Contacts: Field Map

_Generated from `field-map/contacts.yaml` by `scripts/generate_tables.py`. Do not hand-edit this file - edit the YAML source and regenerate._

## Object-level mapping

**NPSP object(s):** `Contact (standard), child of a Household Account`

NPSP keeps the standard Contact object as the individual constituent record, related to a Household Account for grouping and rollups.

**Nonprofit Cloud object(s):** `Account + Contact merged into a single Person Account record`

Person Accounts collapse Account and Contact into one record. Most standard Contact fields (name, email, phone, mailing address) survive as Person Account fields with the same or a near-identical API name, since Person Accounts expose the underlying Contact fields directly on the Account record.

**Relationship: Renamed**

This is the most "direct" of the major object changes - most demographic/contact-info fields keep the same meaning and often the same API name, just accessed through a Person Account record instead of a standalone Contact. The structural risk here is less about individual fields and more about anything that assumed "a Contact belongs to a Household Account with siblings" - that grouping assumption breaks (see accounts-households.yaml).

Sources: [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud); [source](https://magicfuse.co/blog/salesforce-nonprofit-cloud-vs-npsp)

## Field-level mapping

| NPSP field | Nonprofit Cloud field | Relationship | Confidence | Notes | Source |
|---|---|---|---|---|---|
| `Contact.FirstName / LastName` | `Account.FirstName / Account.LastName (Person Account)` | Direct | Confirmed | Standard Salesforce Person Account behavior - these fields are exposed directly on Account when Person Accounts are enabled. | [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud) |
| `Contact.Email / Contact.Phone / Contact.MailingAddress` | `Account.PersonEmail / Account.Phone / Account.BillingAddress (Person Account)` | Renamed | Confirmed | Standard Person Account field renames (Contact.MailingAddress becomes Account.BillingAddress on the Person Account record) - this is core Salesforce platform behavior, not Nonprofit Cloud-specific. | [source](https://www.level12.io/blog/person-accounts-groups-relationships-nonprofit-cloud) |
| `Contact.npo02__TotalOppAmount__c / npo02__NumberOfClosedOpps__c (individual rollups)` | `DonorGiftSummary` | Redesign required | Confirmed | Same DonorGiftSummary object referenced in accounts-households.yaml - it summarizes gifts for both accounts and contacts per Salesforce's own object description. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
| `Contact.npsp__Deceased__c` | `Not confirmed against Salesforce documentation reviewed for this map` | No equivalent | Unconfirmed | Open item pending a source-backed confirmation. File an issue if you've verified this in a live org. | _none cited_ |
