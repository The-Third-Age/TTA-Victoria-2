# Small Mechanics

## Wild Goblins
	Any pop from the culture group wild_goblins is considered a wild goblin by FOR
		Any province with wild_goblins cultures will get marked as a wild goblin province
	
	These provinces have a rather large debuff, scaling depending on the ratio of wild goblins to other pops
		Goblins can raid adjacent provinces (owned by the same player), killing some of the goblins and some of the targeted province's pops
	
	Realms can handle wild goblins one of two ways:
		Hunting and extermination. All wild goblin pops are removed when their settlement is found
		Enslaving (needs to be a slaving country). Some wild goblin pops are killed when their settlement is found, the rest are enslaved
	
	Events:
		5000 - Raid against a neighboring province
		5001 - Successful hunt against the settlement (extermination)
		5002 - Unsuccessful hunt
		5003 - Successful hunt against the settlement (enslavement)
	
	Country Flags:
		looking_for_goblin_settlement - used to ensure that only one search can happen at the same time
									  - also ensures that no settlement has multiple searches at once
	
	Modifiers:
		recent_raid - applied for a year after a province gets raided
		wild_goblin_outpost - applied by FOR for any province with wild goblins (but not a majority)
		wild_goblin_hold - applied by FOR for any province with a majority of wild goblins