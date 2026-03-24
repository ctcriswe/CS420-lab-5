# Colton Criswell
# CS 420
# Lab 5

from abc import ABC, abstractmethod
from typing import List, Tuple
import sys


# INTERFACES (Dependency Inversion Principle)
class IPancakeSorter(ABC):
    """
    Abstract interface for any pancake sorting algorithm. 
    High-level modules will depend on this abstraction, not a concrete class.
    """
    @abstractmethod
    def sort(self, stack: List[int], topping: int) -> Tuple[List[int], List[int]]:
        """
        Takes the initial stack and topping, returns the sorted stack and the sequence of flips.
        """
        pass


# CORE LOGIC (Open/Closed Principle)
class ToppingPancakeSorter(IPancakeSorter):
    """
    A concrete implementation of the sorter that specifically handles the 
    'topping first, then sort the rest' rule.
    """
    
    def _flip(self, stack: List[int], k: int) -> None:
        """
        Helper method to reverse the top elements of the stack down to position k.
        
        TODO: Implement the logic to reverse a sub-list of `stack`.
        Remember: In the problem description, 'k' is counted from the BOTTOM 
        of the current stack/sub-stack being considered!
        """
        pass

    def sort(self, stack: List[int], topping: int) -> Tuple[List[int], List[int]]:
        """
        Executes the sorting algorithm.
        
        TODO: 
        1. Find the topping and use self._flip() to move it to the top.
        2. Iterate through the remaining sub-stack below the topping.
        3. Use self._flip() to sort the remaining pancakes (smallest at top, largest at bottom).
        4. Track every 'k' used in a flip and append it to the `flips` list.
        5. Append 0 to the `flips` list when finished.
        """
        flips = []
        working_stack = stack.copy() # Good practice to not mutate the original input directly
        
        # --- YOUR ALGORITHM GOES HERE ---
        
        
        # --------------------------------
        
        return working_stack, flips


# APPLICATION MANAGER (Single Responsibility Principle)
class PancakeApp:
    """
    Responsible ONLY for managing the flow of data: reading input, 
    calling the sorter, and formatting the output.
    """
    def __init__(self, sorter: IPancakeSorter):
        # We inject the dependency here. The app doesn't care HOW it sorts, just that it HAS a sorter.
        self.sorter = sorter

    def run(self, input_text: str) -> None:
        """Parses the input, triggers the sort, and prints the exact required output."""
        lines = input_text.strip().split('\n')
        if len(lines) < 2:
            return
            
        topping = int(lines.strip())
        original_stack = [int(x) for x in lines[1].strip().split()]
        
        # Trigger the injected sorting algorithm
        sorted_stack, flips = self.sorter.sort(original_stack, topping)
        
        self._print_results(original_stack, topping, flips, sorted_stack)

    def _print_results(self, original: List[int], topping: int, flips: List[int], sorted_stack: List[int]) -> None:
        """Formats the output exactly as specified by the requirements."""
        print(f"Original stack: {' '.join(map(str, original))}")
        print(f"Topping: {topping}")
        print(f"Flips: {' '.join(map(str, flips))}")
        print(f"Sorted stack: {' '.join(map(str, sorted_stack))}")


# MAIN EXECUTION
if __name__ == "__main__":
    # Example input from the prompt
    sample_input = """5
3 1 5 2 4"""

    # 1. Instantiate our specific sorter
    my_sorter = ToppingPancakeSorter()
    
    # 2. Instantiate our app, passing in the sorter
    app = PancakeApp(sorter=my_sorter)
    
    # 3. Run the application
    app.run(sample_input)