import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
	if f[0] == '.' and f[-3] != '.py':
		print 'Deleting ', f
		os.remove(f)

print 'done'
