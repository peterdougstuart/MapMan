import game_levels as levels

first = None

for level in levels.levels:
	
	if not level in levels.loadings:
		
		if first is None:
			first = level
			
		print level

if not first is None:
	print '\n','first=', first
	print levels.levels[first]
		
print('Done')
