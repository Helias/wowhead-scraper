import requests
from tqdm import tqdm
import pathos as pa

# 0 = loot
# 1 = pickpocketing
# 2 = skinning
idx = 0

loot_type = ["drops", "pickpocketing", "skinning"]

with open(f"entries_{loot_type[idx]}.txt", "r") as f:
  entries = f.readlines()

def parallel(entry: int, _loot_type = loot_type[idx]) -> None:
  # print(entry)

  response = requests.get(f'https://www.wowhead.com/wotlk/npc={entry}')

  is_loot_in_wowhead = response.text.find(f"id: '{_loot_type}'") > -1
  if is_loot_in_wowhead:
    with open(f"missing_{_loot_type}_entries.txt", "a+") as f:
      f.write(entry)
      print("## FOUND!")

ncpu = 16
with pa.multiprocessing.ProcessingPool(ncpu) as p:
  all_entries = list(tqdm(p.imap(parallel, entries), total=len(entries)))

# for entry in entries:
#   parallel(entry)
