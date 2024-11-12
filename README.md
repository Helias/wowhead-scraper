# wowhead-scraper

### Installation

```bash
pip install requests json5 pathos tqdm
```

### Usage

Run the commands included in `get_all_loot_entries.sh` to get all the NPC entries without loot,skinloot or pickpocketloot.

Run `extract-missing-loot.py` changing the `idx` variable for loot, skinloot or pickpocketloot to extract all the npc entries that in WoWHead have the loots but not in your database.

Run `extract-sql.py` changing the `idx` variable for loot, skinloot or pickpocketloot to extract all the sql fixes extracting the data from wowhead.
