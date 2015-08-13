'''
	Beverages machine main class
	
'''

from collections import Counter


class BeveragesMachine(object):
    	
	def __init__(self):
		""" initialize machine and load it with some coins and drinks """
		self.prices = {
	   		'cola': 98,
			'orange': 122,
			'water': 21,
			'crystal': 120000,
			'butterbeer': 161, 
		}
		self.stock = {
			'cola': 100,
			'orange': 50,
			'water': 300,
			'crystal': 1,
			'butterbeer': 0,
		}
		# cents: amount 
		self.coins = {
			1: 136,
			10: 46,
			50: 32,
			100: 4,
		}
		# state_info: code and humanize description
		self.states_info = {
			'wating': 'We are ready to take new order',
			'not_enough_money': "You dont't have enought money. Add some coins!",
			'drink_not_available': 'We out of specific drink',
		}
		self.state = 'wating'
		self._balance = 0
	
	@property
	def balance(self):
		return round(self._balance/100, 2)
		
	def perform_sale(self, drink):
		""" Register a sale """
		prices = self.prices
		if self.stock[drink] > 0:
			if self._balance >= prices[drink]:
				self.stock[drink] -= 1
				self._balance -= prices[drink]
				self.give_change()
				self.state = 'wating'
			else: 
				self.state = 'not_enough_money'
		else:
			self.state = 'drink_not_available'
		return
		
	def make_deposit(self, deposite_coins={}):
		""" Make a deposite in coints """
		for coin in deposite_coins.keys():
			self._balance += coin*deposite_coins[coin]
		# update coins stock
		self.coins = dict(Counter(self.coins) + Counter(deposite_coins))
		return
		
	def give_change(self):
		change = {}
		balance = self._balance
		coins = list(self.coins.keys())
		if balance > 0:
			for coin in sorted(coins, reverse=True):
				coin_qty = balance//coin 
				# we can't give more coins then we have
				if coin_qty > self.coins[coin]:
					coin_qty = self.coins[coin]
				# update chance and balance 
				change.update({coin: coin_qty})
				balance -= coin*coin_qty
			# give a change and update coins stock
			self.coins = dict(Counter(self.coins) - Counter(change))
		return change
	