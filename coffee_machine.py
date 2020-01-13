# Write your code here
class CoffeeMachine:
    def __init__(self, water, milk, beans, cups, money):
        self.resources = [water, milk, beans, cups, money]
        self.coffees = [[250, 0, 16, 1, -4], [350, 75, 20, 1, -7], [200, 100, 12, 1, -6]]
        self.state = None
        self.sub_state = None
    
    def handle_input(self, input_string):
        if self.state is None:
            print("Write action (buy, fill, take, remaining, exit): ")
            self.state = "menu"
        elif self.state == "menu":
            return self.menu(input_string)
        elif self.state == "buy":
            self.buy(input_string)
        elif self.state == "fill":
            self.fill(input_string)
        elif self.state == "take":
            self.take()

    def menu(self, input_string):
        self.state = input_string
        if input_string == "buy":
            self.buy(input_string)
        elif input_string == "fill":
            self.fill(input_string)
        elif input_string == "take":
            self.take()
        elif self.state == "remaining":
            self.remaining()
        elif input_string == "exit":
            return False
        else:
            self.reset_state()

    def reset_state(self):
        self.sub_state = None
        self.state = "menu"
        print("Write action (buy, fill, take, remaining, exit): ", end="")

    def buy(self, input_string):
        if self.sub_state is None:
            self.sub_state = "choosing"
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
        elif self.sub_state == "choosing":
            if input_string != "back":
                try:
                    coffee = int(input_string) - 1
                    assert coffee in range(3)
                except (ValueError, AssertionError):
                    print("Invalid choice!")
                    self.reset_state()
                    return
                lowest_amount = self.check_amounts(coffee)
                if lowest_amount[0] < 0:
                    print(f"Sorry, not enough {lowest_amount[1]}!")
                else:
                    print("I have enough resources, making you a coffee!")
                    for i in range(5):
                        self.resources[i] -= self.coffees[coffee][i]
            self.reset_state()

    def check_amounts(self, coffee_type):
        keys = ["water", "milk", "beans", "cups"]
        return min(([self.resources[i] - self.coffees[coffee_type][i], keys[i]] for i in range(4)), key=lambda o: o[0])

    def fill(self, input_string):
        prompts = ["Write how many ml of water do you want to add: ", "Write how many ml of milk do you want to add: ",
                   "Write how many grams of coffee beans do you want to add: ", "Write how many disposable cups of coffee do you want to add: "]
        if self.sub_state is None:
            self.sub_state = 0
        else:
            try:
                self.resources[self.sub_state] += int(input_string)
                self.sub_state += 1
            except ValueError:
                print("Invalid value!")
        if self.sub_state == len(prompts):
            self.reset_state()
        else:
            print(prompts[self.sub_state])

    def take(self):
        print(f"I gave you ${self.resources[4]}")
        self.resources[4] = 0
        self.reset_state()

    def remaining(self):
        print(self)
        self.reset_state()

    def __str__(self):
        return f"""The coffee machine has:\n{self.resources[0]} of water\n{self.resources[1]} of milk
{self.resources[2]} of coffee beans\n{self.resources[3]} of disposable cups\n{self.resources[4]} of money"""


def main():
    machine = CoffeeMachine(400, 540, 120, 8, 550)
    machine.handle_input("")
    loop = True
    while loop is not False:
        loop = machine.handle_input(input())

main()
