def main():
    names1 = []

    # Ask for number of roommates
    while True:
        try:
            num_roommates1 = int(input("Please enter the number of roommates:\n> "))
            if num_roommates1 < 0:
                print("Number of roommates cannot be negative. Try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Collect roommate names
    print("\nEnter roommate names:")
    for i in range(num_roommates1):
        name1 = input(f"> Roommate {i + 1}: ").strip()
        if name1:
            names1.append(name1)
        else:
            print("Name cannot be empty. Try again.")
            name1 = input(f"> Roommate {i + 1}: ").strip()
            names1.append(name1)

    # Ask which roommate's financials to view
    while True:
        try:
            index1 = int(input("\nWhose financials would you like to see? (Enter index 0 to {}):\n> ".format(num_roommates1 - 1)))
            if 0 <= index1 < len(names1):
                print(f"\n{names1[index1]}'s Financials:")
                break
            else:
                print("Invalid index. Please enter a number between 0 and {}.".format(num_roommates1 - 1))
        except ValueError:
            print("Invalid input. Please enter a whole number.")



    #add financial values
    #initialize adjustable array to store string called items
    items1 = []
    #initialize adjustable array to store float called values
    values1 = []
    #loop to get items and values
    while True:
        item1 = input("Enter item (or 'done' to finish):\n> ").strip()
        if item1.lower() == 'done':
            break
        try:
            value1 = float(input(f"Enter value for {item1}:\n> "))
            items1.append(item1)
            values1.append(value1)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    print("\nFinancial Summary:")
    for item, value in zip(items1, values1):
        print(f"{item}: ${value:.2f}")
    


        



if __name__ == "__main__":
    main()
# This is a simple command-line program to manage roommate financials.
