# Metlabs Regulatory Index

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23873539.svg)](https://doi.org/10.5281/zenodo.23873539)

Regulatory assessment of **122 jurisdictions** (97 countries and territories, 23 US states and 2 UAE emirates) for businesses that provide crypto-asset services or tokenize assets. Each row links to the full guide on [metlabs.io](https://metlabs.io/en/blockchain-regulation/), which cites the regulator, the law in force and the latest regulatory change.

- **Ranking:** [Most crypto-friendly countries](https://metlabs.io/en/blockchain-regulation/crypto-friendly-countries/)
- **Methodology:** [How the index is calculated](https://metlabs.io/en/blockchain-regulation/#metodologia)
- **Change log:** [Crypto regulation changes by country](https://metlabs.io/en/blockchain-regulation/changes/) ([RSS](https://metlabs.io/feeds/blockchain-regulation-en.xml))
- **Spanish:** [Índice Regulatorio de Metlabs](https://metlabs.io/regulacion-blockchain/)
- **Also on:** [Zenodo](https://doi.org/10.5281/zenodo.23873539) · [Hugging Face](https://huggingface.co/datasets/Pablogomezgzl/metlabs-regulatory-index) · [Kaggle](https://www.kaggle.com/datasets/pablogomezgzl/metlabs-regulatory-index)

## Files

| File | Format |
|---|---|
| [`data/blockchain-regulation-index.csv`](data/blockchain-regulation-index.csv) | CSV (RFC 4180), one row per jurisdiction |
| [`data/blockchain-regulation-index.json`](data/blockchain-regulation-index.json) | JSON with dataset metadata and the same records |

The always-current files live at `https://metlabs.io/data/blockchain-regulation-index.csv` and `.json`, regenerated from the guides on every deploy. Each month, if the data has changed, a new [release](https://github.com/MetlabsBlockchain/blockchain-regulation-index/releases) with both files is published here, a new version on Zenodo (with its own DOI) and the same files on Hugging Face and Kaggle. The `data/` folder holds the snapshot of the first release.

## Columns

| Column | Description |
|---|---|
| `jurisdiction`, `jurisdiction_es` | Name in English and Spanish |
| `code` | ISO 3166-1 alpha-2 code; `US-<STATE>` and `AE-<EMIRATE>` for sub-regions |
| `region_type` | `country`, `us-state` or `uae-emirate` |
| `parent_code` | Parent country of a sub-region (`US`, `AE`) |
| `status` | Assessment: `favorable`, `neutral`, `restrictive` (unfavourable) or `prohibited` |
| `score` | Weighted score from 0 to 100; empty when comparable evidence is missing |
| `rank` | Position among scored countries (ties share a position); empty for sub-regions |
| `clarity`, `access`, `tokenization`, `services`, `international` | Level 0-4 in each dimension (weights 25/25/20/20/10) |
| `gate` | Barrier that caps the score: `none`, `restricted`, `prohibited` or `unverified` |
| `confidence` | `high`, `medium` or `limited` |
| `scope` | Applicable framework scope (for example, European Union) |
| `authorities` | Competent authorities, separated by `;` |
| `last_regulatory_change` | Date of the latest regulatory change recorded in the guide |
| `assessed_at` | Date of the index assessment |
| `last_reviewed` | Date of the latest editorial review of the guide |
| `methodology_version` | Version of the scoring methodology |
| `guide_url`, `guide_url_es` | Guide in English and Spanish |

The score describes the environment for private businesses. It is not investment advice and does not replace the legal analysis of each project.

## License and citation

[CC BY 4.0](LICENSE): you may share and adapt the data, including commercially, as long as you credit Metlabs and link to the source. Suggested citation:

> Metlabs (2026). *Metlabs Regulatory Index* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23873539

See also [`CITATION.cff`](CITATION.cff). Corrections: [metlabs.io/en/contact](https://metlabs.io/en/contact/).
