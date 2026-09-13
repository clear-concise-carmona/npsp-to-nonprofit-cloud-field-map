# Allocations Gau: Field Map

_Generated from `field-map/allocations-gau.yaml` by `scripts/generate_tables.py`. Do not hand-edit this file - edit the YAML source and regenerate._

## Object-level mapping

**NPSP object(s):** `npsp__Allocation__c + npsp__General_Accounting_Unit__c`

NPSP splits a gift's designation across one or more General Accounting Units (GAUs, e.g. funds or programs) via child Allocation records against the Opportunity.

**Nonprofit Cloud object(s):** `GiftDesignation + GiftTransactionDesignation + GiftDefaultDesignation`

Nonprofit Cloud represents this with GiftDesignation ("a designation that can be assigned to a gift transaction") and a GiftTransactionDesignation junction, plus GiftDefaultDesignation for defaulting designations on gifts generated from an Opportunity, Campaign, or commitment.

**Relationship: Renamed**

Conceptually the closest thing to a direct rename in this whole migration - "GAU + Allocation" becomes "GiftDesignation + GiftTransactionDesignation." Object purposes are confirmed from Salesforce's own developer documentation; exact field-level names within GiftDesignation were not enumerated in the pages reviewed for this map and should be confirmed with scripts/validate_org.py before building migration scripts against them.

Sources: [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm); [source](https://plative.com/insights/blog/creating-gau-allocations-in-salesforce-nonprofit-cloud/); [source](https://www.dataimporter.io/blog/npsp-to-nonprofit-cloud-data-migration)

## Field-level mapping

| NPSP field | Nonprofit Cloud field | Relationship | Confidence | Notes | Source |
|---|---|---|---|---|---|
| `npsp__General_Accounting_Unit__c.Name` | `GiftDesignation (name/label field, exact API name unconfirmed)` | Renamed | Inferred | Object-level rename confirmed; field-level name not yet verified against a live org. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
| `npsp__Allocation__c.npsp__Amount__c / npsp__Percent__c` | `GiftTransactionDesignation (amount/percent split field, exact API name unconfirmed)` | Renamed | Inferred | GiftTransactionDesignation is confirmed as the junction between a gift transaction and a designation in Salesforce's Fundraising standard objects list, matching the role NPSP's Allocation record plays today. Field-level names unconfirmed. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
| `npsp__Allocation__c.npsp__Opportunity__c (default GAU behavior for un-allocated gifts)` | `GiftDefaultDesignation` | Direct | Confirmed | Confirmed as its own object: "represents the default designation for gifts that originate from an opportunity, campaign, or commitment" - a direct conceptual match for NPSP's default-GAU behavior. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
| `n/a - NPSP has no soft-credit-specific default allocation object` | `GiftDefaultSoftCredit` | New in Nonprofit Cloud | Confirmed | "Represents the default allocation for soft credits on gift commitment transactions that are created by a recurrence engine and credited to constituents who influenced the commitment" - new behavior with no direct NPSP precursor, added API v62.0+. | [source](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud.meta/nonprofit_cloud/npc_fundraising_standard_objects.htm) |
