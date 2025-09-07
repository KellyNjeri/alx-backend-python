#!/usr/bin/python3
"""
Main script to demonstrate all generator functionalities with dash-named modules.
"""
import importlib.util
from itertools import islice


def dynamic_import(module_path, module_name):
    """Dynamically import a module even if its filename contains a dash (-)."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("=== Python Generators Project Demo ===\n")

    # 1. Streaming users one by one
    print("1. Streaming users one by one:")
    stream_module = dynamic_import("0-stream_users.py", "stream_users")
    if stream_module and hasattr(stream_module, "stream_users"):
        for i, user in enumerate(islice(stream_module.stream_users(), 3)):
            print(f"  User {i+1}: {user['name']} ({user['age']} years)")
    else:
        print("  Stream users module not available")
    print()

    # 2. Batch processing
    print("2. Batch processing (showing first batch):")
    batch_module = dynamic_import("1-batch_processing.py", "batch_processing")
    if batch_module and hasattr(batch_module, "batch_processing"):
        try:
            batch_module.batch_processing(batch_size=5)  # or your default size
            print("  Batch processing executed successfully")
        except Exception as e:
            print(f"  Error running batch processing: {e}")
    else:
        print("  Batch processing module not available")
    print()

    # 3. Memory-efficient age calculation
    print("3. Memory-efficient age calculation:")
    age_module = dynamic_import("4-stream_ages.py", "stream_ages")
    if age_module and hasattr(age_module, "calculate_average_age"):
        try:
            avg_age = age_module.calculate_average_age()
            print(f"  Average age: {avg_age}")
        except Exception as e:
            print(f"  Error calculating average age: {e}")
    else:
        print("  Age calculation module not available")
    print()


if __name__ == "__main__":
    main()
