import numpy as np

def add_arrays(a, b):
    """Add two numpy arrays and return the result."""
    return np.add(a, b)

if __name__ == "__main__":
    # Example usage
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    print("Sum:", add_arrays(arr1, arr2))
