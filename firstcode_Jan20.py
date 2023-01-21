#hi
print("Hi, welcome to coffee shop!\nWhat should I call you ?")
name = input()
print("Hi "+ name+ ",what would you like to have in below menu?\nWe are serving latte, filter coffee, nescafe, all are in same prize of 20 rs/-\nWhat would you like to have?")
order = input()
print("how many of these you want ?")
quant = input()
total = int(quant)*20
print("Noted, here is your total amount that you need to pay-" + str(total))
# print(int(quant)*20)
# print(total)
