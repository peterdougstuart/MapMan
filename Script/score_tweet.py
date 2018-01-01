import twitter

class ScoreTweet(object):
	
	def __init__(self, score, completion, pb):
		
		#http://omz-software.com/pythonista/docs/ios/twitter.html
		
		all_accounts = twitter.get_all_accounts()
		
		if len(all_accounts) >= 1:
			
			account = all_accounts[0]
			
			if not completion and pb:
				text = 'I just got a new PB of {0} in #MapMan, coming soon on iOS app store'.format(score)
			elif completion and not pb:
				text = 'I just got completed #MapMan with a score of {0}, coming soon on iOS app store'.format(score)
			elif completion and ob:
				text = 'I just got completed #MapMan with a pb of {0}, coming soon on iOS app store'.format(score)
			else:
				text = ''
			
			if len(text) > 0:
				twitter.post_tweet(account, text)
			
