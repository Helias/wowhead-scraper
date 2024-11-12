# generate entries lists
mysql -h 127.0.0.1 -u root -p acore_world -e "SELECT `entry` FROM `creature_template` WHERE lootid = 0;" > entries_drops.txt
mysql -h 127.0.0.1 -u root -p acore_world -e "SELECT `entry` FROM `creature_template` WHERE skinloot = 0;" > entries_skinning.txt
mysql -h 127.0.0.1 -u root -p acore_world -e "SELECT `entry` FROM `creature_template` WHERE pickpocketloot = 0;" > entries_pickpocketing.txt
