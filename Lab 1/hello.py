# Activity 2: Update your Profile and add it to the repository

print("============================================")
print("Welcome here")
print("My first post!")
print("============================================")

username = "cool_creator"
bio = "Fun Blogger"
followers = 100

# Activity 3: Follower Growth tracker

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)

followers += 50
print("Day 1:", followers)

followers += 20
print("Day 2:", followers)

followers += 10
print("Day 3:", followers)

# Activity 4: Interactive profile creator

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print("Username:", username)
print("Age:", age)
print("Category:", category)

# Activity 5: Something fun to think about. More on this next week:

if age > 40 and category == "fun":
    print("You are old what is fun for you??")