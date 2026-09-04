userName = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print("Username: ", userName)
print("Age: ", age)
print("Category: ", category)

if age>40 and category == "Fun":
    print("You are old what is fun for you?")


