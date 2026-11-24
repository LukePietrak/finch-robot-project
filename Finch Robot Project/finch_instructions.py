from robot.finch import Finch
import json

def follow_instructions(finch_to_move, instructions, default_speed=50): # Defaulted speed will be 50
    # First test to see if inputs are valid
    if not instructions_are_valid(instructions):
        raise ValueError("Invalid instructions in 'follow_instructions'")

    # Set up instructions into mini lists
    for i in instructions:
        direction = i[0]
        distance_or_angle = i[1]
        speed = i[2] if len(i) > 2 else default_speed # If the input doesn't include speed, the default parameter will make it 50

        # Check if front or back, then move accordingly
        if direction in ["F", "B"]:
            finch_to_move.move(direction, distance_or_angle, speed)
        # Check if right or left, then turn accordingly
        elif direction in ["R", "L"]:
            finch_to_move.turn(direction, distance_or_angle, speed)


def reverse_instructions(instructions):
    # First test to see if inputs are valid
    if not instructions_are_valid(instructions):
        raise ValueError("Invalid instructions in 'reverse_instructions'")

    # Define opposites (We don't need to make oppsities for distance or speed)
    opposites = {"F": "B", "B": "F", "R": "L", "L": "R"}
    reversed_list = []

    # Set up instructions into mini lists again
    for i in reversed(instructions):
        direction = i[0]
        amount = i[1]
        speed = i[2]

        new_direction = opposites[direction]
        reversed_list.append([new_direction, amount, speed])

    return reversed_list


def instruction_is_valid(instruction): # Return true if an instruction is a list of length 3, has a valid direction, and numbers for distance and speed
    direction, amount, speed = instruction

    # Check for list and correct length
    if not isinstance(instruction, list) or len(instruction) != 3:
        return False

    # Check for correct direction
    if direction not in ["F", "B", "R", "L"]:
        return False

    # Check for int/float for distance and speed
    if not isinstance(amount, (int, float)) or not isinstance(speed, (int, float)):
        return False

    return True # The all clear


def instructions_are_valid(instructions): # Returns true if the input is a list and every instruction inside it is valid
    # Check to see if instructions are in list form
    if not isinstance(instructions, list):
        return False

    # Check to see if direction, distance, and speed are valid
    for item in instructions:
        if not instruction_is_valid(item):
            return False

    return True # The all clear


def generate_instructions(sides, default_speed=50):
    instructions = [] # List for instructions

    angle = 360 / sides # Calculate the angle for the turns

    for i in range(sides):
            instructions.append(["F", 25, default_speed])
            instructions.append(["R", angle, default_speed])

    return instructions


def expand_instructions(instructions):
    # First test to see if inputs are valid
    if not instructions_are_valid(instructions):
        raise ValueError("Invalid instructions in 'expand_instructions'")

    # Create new list for the doubled instructions
    expanded_instructions = []

    # Set up instructions into mini lists
    for i in instructions:
        direction = i[0]
        distance = i[1]
        speed = i[2]

        # Double the distance of the Forwards and Backwards
        if direction in ["F", "B"]:
            distance = distance * 2

        expanded_instructions.append([direction, distance, speed]) # Add the doubled distance instructions to the list

    return expanded_instructions


def save_instructions_to_file(instructions, filename): # Write instructions into file
    with open(filename, "w") as file:
        json.dump(instructions, file)


def load_instructions_from_file(filename): # Read instructions in file
    with open(filename, "r") as file:
        return json.load(file)


def load_saved_shapes(filename): # Get instructions from file
    try:
        data = load_instructions_from_file(filename)
    except FileNotFoundError:
        return[]

    if data is None:
        return []

    return data


def shape_choice_to_sides(user_input): # Whichever shape = a number
    shape_sides = {
        "triangle": 3,
        "square": 4,
        "pentagon": 5,
        "hexagon": 6,
        "heptagon": 7,
        "octagon": 8,
    }

    if user_input in shape_sides:
        return shape_sides[user_input]

    if user_input == "custom":
        return int(input("Enter the number of sides: "))

    return None


def create_new_shape(finch, saved_shapes, filename): # User input for the shapes
    print("\nChoose which shape you'd like to create:")
    print("Triangle, Square, Pentagon, Hexagon, Heptagon, Octagon.")
    print("Or type 'Custom' to enter your own number of sides.")
    user_input = input("Enter here: ").lower() # User input

    sides = shape_choice_to_sides(user_input)

    if sides is None:
        print("Invalid input.")
        return

    base_instructions = generate_instructions(sides)

    # Actually make the finch move
    if finch is not None:
        follow_instructions(finch, base_instructions)

    # Add this new shape onto the list of saved shapes and then save everything
    saved_shapes.append(base_instructions)
    save_instructions_to_file(saved_shapes, filename)
    print("Shape created and saved!")

def use_old_shape(finch, saved_shapes, filename):
    # First check if there's any saved shapes
    if len(saved_shapes) == 0:
        print("No saved shapes.")
        return

    print("\nSaved shapes:")
    for shape in saved_shapes:
        print(shape)

    choice = input("Enter the number of the shape you want to use: ")


def prompt_user_and_run(filename):
    # Define finch
    finch = Finch("A")

    # Define the file of the saved shapes as saved_shapes
    saved_shapes = load_saved_shapes(filename) # Load saved shapes

    # Prompt the user for what shape they want
    print("Would you like to:")
    print("1: Create a new shape")
    print("2: Use an old shape")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        create_new_shape(finch, saved_shapes, filename)
    elif choice == "2":
        use_old_shape(finch, saved_shapes, filename)
    else:
        print("Enter either 1 or 2.")


def main():
    # Define filename
    filename = "finch_saves.json"
    prompt_user_and_run(filename)


if __name__ == "__main__":
    main()