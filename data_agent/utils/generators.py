import csv

def iter_row(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
            
def batched(iterable, size):
    """Yield successive batches of a given size from an iterable."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
        
if __name__ == "__main__":
    # Example usage of iter_row
    for row in iter_row("output.csv"):
        print(row)

    # Example usage of batched
    data = range(7)
    for batch in batched(data, 3):
        print(batch)