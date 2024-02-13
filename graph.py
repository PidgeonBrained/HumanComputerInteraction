import csv
import matplotlib.pyplot as plt
import numpy as np
import math

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) #skip the first row
        for csvRow in reader:
            outputRow = [] #outputRow will be [Distance/Width, Time, Error]

            #Creating distance/width
            csvPerm = int(csvRow[0])

            if csvPerm == 0 or csvPerm == 4 or csvPerm == 9 or csvPerm == 13 or csvPerm == 26 or csvPerm == 30:
                outputRow.append(math.log2(2*100.0/32))
            elif csvPerm == 1 or csvPerm == 5 or csvPerm == 10 or csvPerm == 14 or csvPerm == 27 or csvPerm == 31:
                outputRow.append(math.log2(2*100.0/64))
            elif csvPerm == 2 or csvPerm == 6 or csvPerm == 11 or csvPerm == 15:
                outputRow.append(math.log2(2*100.0/128))
            elif csvPerm == 3 or csvPerm == 7:
                outputRow.append(math.log2(2*100.0/256))
            elif csvPerm == 8 or csvPerm == 12 or csvPerm == 25 or csvPerm == 29:
                outputRow.append(math.log2(2*200.0/32))
            elif csvPerm == 16 or csvPerm == 20:
                outputRow.append(math.log2(2*300.0/32))
            elif csvPerm == 17 or csvPerm == 21:
                outputRow.append(math.log2(2*300.0/64))
            elif csvPerm == 18 or csvPerm == 22:
                outputRow.append(math.log2(2*300.0/128))
            elif csvPerm == 19 or csvPerm == 23:
                outputRow.append(math.log2(2*300.0/256))
            elif csvPerm == 24 or csvPerm == 28:
                outputRow.append(math.log2(2*400.0/32))
            else:
                raise ValueError("Permutation not found?")
            
            outputRow.append(float(csvRow[1])) #time
            outputRow.append(float(csvRow[3])) #Error
            data.append(outputRow)

    return data

def create_graph(data):
    x = []
    y = []
    for subject in data:
        for row in subject:
            x.append(row[0])
            y.append(row[1])

    
    x = np.array(x)
    y = np.array(y)
    plt.scatter(x, y)
    plt.xlabel('Log2(2 * Distance/Width)')
    plt.ylabel('Time (ms)')
    plt.title('Fitts Law')

    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color='red', label='Linear Regression')
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    
    data = []
    #reading Sam's data
    for i in range(1,6):
        filename = 'sam-subject' + str(i) + '.csv'
        data.append(read_csv(filename))
    
    #reading Cole's data
    for i in range(1,4):
        filename = 'cole-subject' + str(i) + 'date1-21-2014.csv'
        data.append(read_csv(filename))

    #reading Pidge's data
    for i in range(1,3):
        filename = 'pidge-subject' + str(i) + '.csv'
        data.append(read_csv(filename))

    #reading Ahmed's data
    for i in range(1,2):
        filename = 'ahmed-subject' + str(i) + '.csv'
        data.append(read_csv(filename))

    create_graph(data)
