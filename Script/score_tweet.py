import twitter

class ScoreTweet(object):
	
	def __init__(self, score):
		
		#http://omz-software.com/pythonista/docs/ios/twitter.html
		
		all_accounts = twitter.get_all_accounts()
		
		if len(all_accounts) >= 1:
			
			account = all_accounts[0]
			
			twitter.post_tweet(account, 'I just got a new PB of {0} in #MapMan, coming soon on iOS app store'.format(score))
			
