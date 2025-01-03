import requests
from tqdm import tqdm
import pathos as pa


# entries_creature_text.txt is generated by using the following SQL query
# SELECT entry FROM creature_template WHERE entry NOT IN (SELECT CreatureID FROM creature_text);

with open("entries_creature_text.txt", "r") as f:
  entries = f.readlines()

def parallel(entry: int) -> None:
  # print(entry)

  response = requests.get(f'https://www.wowhead.com/wotlk/npc={entry}')

  has_quote_wowhead = response.text.find("""WH.ge('wougfh349t'), this)">Quotes""") > -1
  if has_quote_wowhead:
    with open(f"missing_creature_text_entries.txt", "a+") as f:
      f.write(entry)
      print("## FOUND!")

ncpu = 16
with pa.multiprocessing.ProcessingPool(ncpu) as p:
  all_entries = list(tqdm(p.imap(parallel, entries), total=len(entries)))

# for entry in entries:
#   parallel(entry)
