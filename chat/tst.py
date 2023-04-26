
import random

def diffculty_level(diffculty_no):
    if diffculty_no==1:
        random_number1 = random.randint(0,9)
        random_number2 = random.randint(0,9)
        result = int(input("You chose difficulty level: \n 1 Please write the answer of "+str(random_number1)+"*"+str(random_number2)))
        if random_number1*random_number2==result:
            print("you enter correct value")
        else:
            print("You enter wrong value")
    elif diffculty_no==1:
        random_number1 = random.randint(0,9)
        random_number2 = random.randint(10,99)
        result = int(input("You chose difficulty level: 2 \n Please write the answer of "+str(random_number1)+"*"+str(random_number2)))
        if random_number1*random_number2==result:
            print("you enter correct value")
        else:
            print("You enter wrong value")
    elif diffculty_no==1:
        random_number1 = random.randint(100,999)
        random_number2 = random.randint(10,99)
        result = int(input("You chose difficulty level: 3 \n Please write the answer of "+str(random_number1)+"*"+str(random_number2)))
        if random_number1*random_number2==result:
            print("you enter correct value")
        else:
            print("You enter wrong value")




if __name__ == '__main__':
    while True:
        level_of_diffculty=int(input("Hasasn (A00232390) - Multiplication Test \n Difficulty level (1, 2, 3, or 99 to quit):"))
        if level_of_diffculty>=1 and level_of_diffculty<=3:
            diffculty_level(level_of_diffculty)
        elif level_of_diffculty==99:
            break

