"""Test file with intentional bugs for Atlas Coder demo."""

def divide_numbers(a, b):
    """Divide two numbers and return the result."""
    result = a / b  # Bug: No check for division by zero
    return result

def process_list(items):
    """Process a list of items."""
    total = 0
    for i in range(len(items) + 1):  # Bug: Off-by-one error
        total += items[i]
    return total

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if len(numbers) == 0:  # Bug: Should check if numbers is None first
        return 0
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    # Test the functions
    print(divide_numbers(10, 2))
    print(divide_numbers(10, 0))  # This will cause ZeroDivisionError
    
    print(process_list([1, 2, 3]))  # This will cause IndexError
    
    print(calculate_average([1, 2, 3]))
    print(calculate_average(None))  # This will cause TypeError