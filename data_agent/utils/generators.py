import csv

def iter_rows(path):
    """Yield rows from a CSV file as dictionaries."""
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
            
def batched(iterable, size):
    """Yield successive batches of a given size from an iterable."""
    if size <1:
        raise ValueError(f"size must be >= 1, got {size}")
    
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
        
if __name__ == "__main__":
    # Example usage of iter_rows
    for row in iter_rows("output.csv"):
        print(row)
    
    # Example usage of batched
    data = range(3)
    for batch in batched(data, 0):
        print(batch)
        