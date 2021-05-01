class safe:
    coins = {}
    def __init__(self):
      self.coins[1] = 0
      self.coins[2] = 0
      self.coins[5] = 0

    def add_coin(self,coin, value):
        self.coins[coin] += value
    def remove_coin(self, coin, value):
        self.coins[coin] -= value

    def give_change(self ,coin):
        if coin == 2:
            if self.coins[1] > 1:
                self.remove_coin(1, 1)
                self.add_coin(2, 1)
                print('Here is your soda')
            else:
                print('I have no change')
        elif coin == 5:
            if self.coins[2] > 2:
                self.remove_coin(2, 2)
                self.add_coin(5, 1)
                print('Here is your soda')
            elif self.coins[1] > 4:
                self.remove_coin(1, 4)
                self.add_coin(5, 1)
                print('Here is your soda')
            elif self.coins[2] >= 1 and self.coins[1] >= 2:
                self.remove_coin(2, 1)
                self.remove_coin(1, 2)
                self.add_coin(5, 1)
                print('Here is your soda')
            else:
                print('I have no change')

        def __str__(self):
            return 'Safe status is ' + self.coins
def main():
    test = safe()
    print(test)

if __name__ == '__main__':
    main()