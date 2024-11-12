import requests
from tqdm import tqdm
import pathos as pa
import json5

# 0 = loot
# 1 = pickpocketing
# 2 = skinning
idx = 2

loot_type = ["drops", "pickpocketing", "skinning"]
table_type = ['creature_loot_template', 'pickpocketing_loot_template', 'skinning_loot_template']

with open(f"missing_{loot_type[idx]}_entries.txt", "r") as f:
  entries = f.readlines()

def get_npc_name(response: str) -> str:
  start = response.find("<title>") + len("<title>")
  end = response.find("</title>")
  title = response[start:end]
  name = title.replace(" - NPC - WotLK Classic", "")
  return name

def filter_bad_properties(substr: str) -> str:
  for variable in [f"WH.TERMS.{loot_type[idx]}", "tabsRelated", "Listview.funcBox.initLootTable", "Listview.funcBox.addModesAndSeasonsPhases", "Listview.extraCols.count", "Listview.extraCols.percent"]:
    substr = substr.replace(variable, "123")

  # remove "note: WH.sprintf(WH.TERMS.npcpickpocketed_format, 15),"
  start_remove = substr.find("note:")
  end_remove = substr.find("),", start_remove)+2
  substr = substr.replace(substr[start_remove:end_remove], "")

  return substr

def get_clean_wowhead_data(source_html: str) -> dict:
  start = source_html.find(f"template: 'item', id: '{loot_type[idx]}',")
  end = source_html.find("}]});", start)+3

  substr = '{' + source_html[start: end]

  substr = filter_bad_properties(substr)

  wowhead_info = json5.loads(substr)

  return wowhead_info["data"]

def generate_sql_query(wowhead_data: dict, npc_name: str, npc_entry: str) -> str:
  sql_query = f"""
-- {npc_name} ({npc_entry})
DELETE FROM `{table_type[idx]}` WHERE (`Entry` = {npc_entry});
INSERT INTO `{table_type[idx]}` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
"""

  for item in wowhead_data:
    chance = item["count"]/item["outof"]
    rounded_chance = round(chance*100, 2)

    escaped_npc_name = npc_name.replace("'", "\\'")
    escaped_item_name = item["name"].replace("'", "\\'")
    sql_query += f"""({npc_entry}, {item["id"]}, 0, {rounded_chance}, 0, 1, 0, {item["stack"][0]}, {item["stack"][1]}, '{escaped_npc_name} - {escaped_item_name}'),\n"""

  sql_query = sql_query[:-2] + ';' + "\n"

  # print(sql_query)

  return sql_query

def parallel(entry: int, _loot_type = loot_type[idx]) -> None:
  # print(entry)

  response = requests.get(f'https://www.wowhead.com/wotlk/npc={entry}')

  npc_name = get_npc_name(response.text)
  npc_entry = entry.strip()

  wowhead_data = get_clean_wowhead_data(response.text)
  # print(wowhead_data)

  sql_query = generate_sql_query(wowhead_data, npc_name, npc_entry)

  with open(f"fix_{_loot_type}_entries.sql", "a+") as f:
    f.write(sql_query)

ncpu = 16
with pa.multiprocessing.ProcessingPool(ncpu) as p:
  all_entries = list(tqdm(p.imap(parallel, entries), total=len(entries)))

# for entry in entries:
#   parallel(entry)
#   break
