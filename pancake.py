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
    
    def _flip(self, stack: List[int], k: int, start_idx: int = 0) -> None:
        """
        Helper method to reverse a portion of the stack.
        - `k` is the position counted from the bottom of the current sub-stack.
        - `start_idx` allows us to ignore the topping (index 0) when sorting the rest.
        """
        # Calculate how many elements are in the sub-stack we are currently looking at
        sub_size = len(stack) - start_idx
        
        # Translate 'k from the bottom' to the number of elements we need to flip from the top
        num_to_flip = sub_size - k + 1
        
        # Slice and reverse
        end_idx = start_idx + num_to_flip
        stack[start_idx:end_idx] = reversed(stack[start_idx:end_idx])

    def sort(self, stack: List[int], topping: int) -> Tuple[List[int], List[int]]:
        flips = []
        working_stack = stack.copy()
        n = len(working_stack)
        
        # Move topping to the top
        topping_idx = working_stack.index(topping)
        
        if topping_idx != 0: # If it's not already at the top
            # Calculate k for the topping. Since we look at the whole stack, start_idx is 0.
            k = n - topping_idx
            flips.append(k)
            self._flip(working_stack, k, start_idx=0)


        # Sort the remaining sub-stack
        sub_size = n - 1 
        
        # We shrink the 'unsorted' portion by 1 each time we place the largest pancake at the bottom
        for curr_size in range(sub_size, 1, -1):
            
            # 1. Find the index of the largest pancake in the current unsorted portion
            max_val = -1
            max_idx = -1
            # We check from index 1 (just below topping) up to the current unsorted boundary
            for i in range(1, 1 + curr_size):
                if working_stack[i] > max_val:
                    max_val = working_stack[i]
                    max_idx = i
                    
            # 2. If the largest is already at the bottom of the unsorted pile, do nothing
            if max_idx == 1 + curr_size - 1:
                continue
                
            # 3. If the largest is NOT at the top of the sub-stack (index 1), flip it to the top
            if max_idx > 1:
                k = sub_size - max_idx + 1
                flips.append(k)
                self._flip(working_stack, k, start_idx=1)
                
            # 4. Now that the largest is at the top of the sub-stack, flip it to the bottom of the unsorted pile
            k = sub_size - curr_size + 1
            flips.append(k)
            self._flip(working_stack, k, start_idx=1)

        # End sequence with 0 as required by the constraints
        flips.append(0) 
        
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
                
            # We grab index 0 for the topping
            topping = int(lines[0].strip()) 
            
            # We grab index 1 for the pancake stack
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