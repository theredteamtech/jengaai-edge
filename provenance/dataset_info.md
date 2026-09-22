# Dataset provenance

JengaCoder v1.2 was trained using two datasets assembled and curated by the JengaAI Edge team for practical coding, debugging, embedded-systems and engineering-assistance tasks.

- `training/data/jengacoder_train_v1.json`
  - Purpose: supervised fine-tuning
  - Size: 160 records
  - SHA256: `b40facb331160fab145a0b0b88f1a953ec21ffd2d629059f6bfd15bec56f194f`
- `training/data/jengacoder_validation_v1.json`
  - Purpose: validation during training
  - Size: 20 records
  - SHA256: `a81ec8ae4c4fdc90ced02c6ad3ad0ed5aecd4c774cb5194707ad68345ad610df`

Both datasets are included directly in this repository and are distributed under the repository's GNU General Public License v3.0 (`LICENSE`).

The later `training/data/v2/` development dataset was not used to train the submitted JengaCoder v1.2 model.
