# Modding Notes

## Scripted Wars

If possible, using standard cbs is the preferred method. However, if the existing cbs don't work as needed here's some tips:
- Add `is_triggered_only = yes` to make sure that the engine doesn't do checks when at war to see if the cb can be added for infamy (boosts performance)
- Add `constructing_cb = no` to ensure that the cb can't be justified against the target (boosts performance)
- If the AI is just not able to enforce the wargoal, the peace cost is likely too high
	- if using a peace option (po) that doesn't transfer land like `po_remove_prestige`, you should be able to change the peace_cost_factor until the AI is able to enforce the cb
	- Peace options that transfer land are more complicated (ones like `po_demand_state` or `po_transfer_provinces`)
		- Remove all of the peace options, and add `po_remove_prestige = yes`
		- Then you'll need to script any affects you want to have happen in the `on_add` and `on_po_accepted` blocks of the cb
			- `on_add` handles any pre-work that needs to happen. Things like setting country flags to make sure that you're targetting the right country with the ending events and what not
				- the basic scope and THIS both point to the country applying the wargoal. FROM refers to the target of the wargoal
			- `on_po_accepted` will handle the effects when the war ends. If you're wanting to transfer land, this is where you do it. You can put the effects right in this block, or you can call an event to do the effects
				- the basic scope is the country that's the target of the wargoal. THIS is the country that applied the wargoal