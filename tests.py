import unittest
from collections import Counter

from beverages_machine import BeveragesMachine


class TestBeveragesMachine(unittest.TestCase):
    
    def setUp(self):
        self.machine = BeveragesMachine()
    
    @staticmethod    
    def coins_sum(coins={}):
        return sum([k*v for k,v in coins.items()])

    def test_deposite_balance(self):
        # 2. User can add money
        machine = self.machine
        coins = {1: 33, 10: 12, 50: 2, 100: 1}
        machine.make_deposit(coins)
        self.assertEqual(machine._balance, self.coins_sum(coins))
        
    def test_deposite_coins(self):
        machine = self.machine
        coins = {1: 33, 10: 12, 50: 2, 100: 1}
        coins_before_deposit = machine.coins
        machine.make_deposit(coins)
        self.assertEqual(machine.coins, dict(Counter(coins_before_deposit) + Counter(coins)))
        
    def test_not_enought_money(self):
        machine = self.machine
        machine.perform_sale('crystal')
        self.assertEqual(machine.state, 'not_enough_money')
        
    def test_sucscess_buy(self):
        machine = self.machine
        machine.make_deposit({1: 33, 10: 12, 50: 2, 100: 1})
        drinks_before_buy = machine.stock['cola']
        machine.perform_sale('cola')
        self.assertEqual(machine.stock['cola'], drinks_before_buy - 1)
        
    def test_give_change(self):
        machine = self.machine
        machine._balance = 196
        change = machine.give_change()
        self.assertEqual(change, {100: 1, 50: 1, 10: 4, 1: 6})
        
    def test_give_change_and_out_of_dollar(self):
        machine = self.machine
        machine._balance = 196
        machine.coins.update({100:0})
        change = machine.give_change()
        self.assertEqual(change, {100: 0, 50: 3, 10: 4, 1: 6})
        
    def test_out_of_drinks(self):
        machine = self.machine
        machine.perform_sale('butterbeer')
        self.assertEqual(machine.state, 'drink_not_available')


if __name__ == '__main__':
    unittest.main()