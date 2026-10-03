
# writing report text file
with open('report.txt', 'w') as f:
    f.write('dataset quality report\n')
    f.write('='*30 + '\n')
    f.write('null rate: 0.24%\n')
    f.write('clean column: 12 / 15\n')  

# Read as one string    
with open('report.txt', 'r') as f:
    content = f.read()
print('reading as one string:')
print(content)

# read line by line
with open('report.txt', 'r') as f:
    for line in f:
        print('reading as line by line:')
        print(f'line: {line.strip()}')

# read in to a list
with open('report.txt', 'r') as f:
    content = f.readlines()
print('reading as list:')    
print (content)

if __name__ == "__main__":
    print('Running ex.py as a script')
        
with open('score', 'w') as f:
    f.write('score: 0.85\n')
    f.write('grade: B\n')
    f.write('remarks: Needs improvement in data cleaning\n')

with open('score', 'r') as f:
    score_content = f.read()
print('Score file content:')
print(score_content)

with open('score', 'r') as f:
    for line in f:
        #print('Reading score file line by line:')
        print(f'line: {line.strip()}')