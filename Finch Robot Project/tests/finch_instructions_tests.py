import pytest
import os

from finch_instructions import *

def test_reverse_instructions():
    o = [["F", 30, 20], ["R", 90, 20]] # o = original
    r = reverse_instructions(o) # r = reversed

    # Check to see if order and directions swapped correctly (direction & order flips)
    assert r[0] == ["L", 90, 20] # R becomes L
    assert r[1] == ["B", 30, 20] # F becomes B


def test_instruction_is_valid(): # Test is_valid
    assert instruction_is_valid(["F", 50, 20]) == True # Valid instructions
    assert instruction_is_valid(["D", 50, 20]) == False  # Invalid instructions
    assert instruction_is_valid(["F", "fifty", 20]) == False  # Invalid instructions
    assert instruction_is_valid(["F", 50, "twenty"]) == False  # Invalid instructions


def test_instructions_are_valid(): # Test are_valid
    assert instructions_are_valid([["F", 50, 20], ["R", 90, 20]]) == True # Valid instructions
    assert instructions_are_valid("this is a string, not a list!") == False # Invalid instructions


def test_reverse_instructions_raises_error(): # This test should only pass if a ValueError is raised when invalid instructions are passed
    with pytest.raises(ValueError):
        reverse_instructions([["Luke is cool", 50, 20]])


def test_generate_instructions():
    result = generate_instructions(4, default_speed = 50) # generate_instructions will divide it by 360, making it a square

    # Test if it makes 4 90 degree turns (360/4 = 90)
    expected = [
        ["F", 25, 50], ["R", 90, 50],
        ["F", 25, 50], ["R", 90, 50],
        ["F", 25, 50], ["R", 90, 50],
        ["F", 25, 50], ["R", 90, 50]
    ]

    assert result == expected # Test full square then starts and ends


def test_expand_instructions():
    dummy_list = [["F", 100, 20], ["R", 90, 20]] # Create a fake list to test the doubled distance

    result = expand_instructions(dummy_list) # Test the expand_instructions() function on the fake list

    assert result[0] == ["F", 200, 20] # Test if distance doubles
    assert result[1] == ["R", 90, 20] # Test if angle stays the same


def test_save_and_load_instructions_to_file():
    instructions = [["F", 50, 20], ["R", 90, 20]]
    save_instructions_to_file(instructions, "test_save.json")
    assert os.path.exists("test_save.json")


def test_load_instructions_from_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_instructions_from_file("does_not_exist.json")