import csv
import matplotlib.pyplot as plt
import numpy as np
import math
import statistics
from scipy.stats import linregress

def read_csv(filename):
    data = [[] for i in range(16)]
    '''Data will be a 3d list.
    data[perm#][row#][entryInRow]
    
    Perm # is going to be
        100  200  300  400
        ----------------
    32  | 0    4    8   12   
    64  | 1    5    9   13
    128 | 2    6   10   14
    256 | 3    7   11   15
    '''
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) #skip the first row
        for csvRow in reader:
            outputRow = [] #outputRow will be [Distance, Width, Time, Error]

            #Creating distance/width
            csvPerm = int(csvRow[0])

            #lord forgive me for this nasty ass code
            if csvPerm == 0 or csvPerm == 4:
                outputRow.append(100)
                outputRow.append(32)
                permNum = 0
            elif csvPerm == 1 or csvPerm == 5:
                outputRow.append(100)
                outputRow.append(64)
                permNum = 1
            elif csvPerm == 2 or csvPerm == 6:
                outputRow.append(100)
                outputRow.append(128)
                permNum = 2
            elif csvPerm == 3 or csvPerm == 7:
                outputRow.append(100)
                outputRow.append(256)
                permNum = 3
            elif csvPerm == 8 or csvPerm == 12:
                outputRow.append(200)
                outputRow.append(32)
                permNum = 4
            elif csvPerm == 9 or csvPerm == 13:
                outputRow.append(200)
                outputRow.append(64)
                permNum = 5
            elif csvPerm == 10 or csvPerm == 14:
                outputRow.append(200)
                outputRow.append(128)
                permNum = 6
            elif csvPerm == 11 or csvPerm == 15:
                outputRow.append(200)
                outputRow.append(256)
                permNum = 7
            elif csvPerm == 16 or csvPerm == 20:
                outputRow.append(300)
                outputRow.append(32)
                permNum = 8
            elif csvPerm == 17 or csvPerm == 21:
                outputRow.append(300)
                outputRow.append(64)
                permNum = 9
            elif csvPerm == 18 or csvPerm == 22:
                outputRow.append(300)
                outputRow.append(128)
                permNum = 10
            elif csvPerm == 19 or csvPerm == 23:
                outputRow.append(300)
                outputRow.append(256)
                permNum = 11
            elif csvPerm == 24 or csvPerm == 28:
                outputRow.append(400)
                outputRow.append(32)
                permNum = 12
            elif csvPerm == 25 or csvPerm == 29:
                outputRow.append(400)
                outputRow.append(64)
                permNum = 13
            elif csvPerm == 26 or csvPerm == 30:
                outputRow.append(400)
                outputRow.append(128)
                permNum = 14
            elif csvPerm == 27 or csvPerm == 31:
                outputRow.append(400)
                outputRow.append(256)
                permNum = 15
            else:
                raise ValueError("Permutation not found")
            
            
            outputRow.append(float(csvRow[1])) #time
            outputRow.append(float(csvRow[3])) #Error
            data[permNum].append(outputRow)

    return data

def create_graph(data):
    x = []
    y = []
    for perm in data:
        x.append(perm[3])
        y.append(perm[2])

    
    x = np.array(x)
    y = np.array(y)
    plt.scatter(x, y)
    plt.xlabel('Index of Difficulty')
    plt.ylabel('Mean time (ms)')
    plt.title('Fitt\'s Law')

    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    plt.plot(x, slope*x + intercept, color='red', label='Linear Regression')
    equation = f'y = {slope:.4f}x + {intercept:.4f}'
    r_squared = f'R^2 = {r_value**2:.10f}'
    plt.text(x[0], y[0]-300, equation, fontsize=10)
    plt.text(x[0], y[0]-325, r_squared, fontsize=10)

    plt.legend()
    plt.grid(True)

    plt.show()


def create_csv_from_data(data, csvName):
    with open(csvName, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Distance", "Width", "MT", "ID", "IP"])
        for row in data:
            writer.writerow([row[0], row[1], row[2], row[3], row[4]])


# def trim_data(data, trimNum):
#     '''data is your data, trimNum is the # of points you want to trim off the top and the bottom'''
#     for i in range(trimNum):
#         maxSecondsIndex = 0
#         minSecondsIndex = 0
#         for j in range(len(data)):
#             if data[j][1] < data[minSecondsIndex][1]:
#                 minSecondsIndex = j
#             if data[j][1] > data[maxSecondsIndex][1]:
#                 maxSecondsIndex = j
        
#         data.pop(minSecondsIndex)
#         data.pop(maxSecondsIndex)
#     return data


def consolidate_data(data):
    dataFromAllSubjects = [[] for i in range(16)]
    for subject in data:
        for permNum in range(16):
            for row in subject[permNum]:
                dataFromAllSubjects[permNum].append(row)

    outputData = [[] for i in range(16)] #Output Data will be [distance, width, mean, ID, IP] for each permNum
    for permNum in range(16):
        outputData[permNum].append(dataFromAllSubjects[permNum][0][0])
        outputData[permNum].append(dataFromAllSubjects[permNum][0][1])
        
        
        #Calculating mean
        tempTimings = []
        for row in dataFromAllSubjects[permNum]:
            tempTimings.append(row[2])
        stdDev = statistics.stdev(tempTimings)
        untrimmedMean = statistics.mean(tempTimings)

        lowerBound = untrimmedMean - 3 * stdDev
        upperBound = untrimmedMean + 3 * stdDev
        sum = 0
        count = 0
        for row in dataFromAllSubjects[permNum]:
            if lowerBound <= row[2] <= upperBound: #If within 3 stdDevs of our untrimmed mean
                sum += row[2] #adding times
                count += 1
        mean  = sum / count
        outputData[permNum].append(mean)

        #Calculating ID
        #ID = math.ceil(math.log2((outputData[permNum][0]/outputData[permNum][1]) + 1)) 
        ID = math.log2((outputData[permNum][0]/outputData[permNum][1]) + 1)
        outputData[permNum].append(ID)

        IP = round(ID/(mean/1000), 1)
        outputData[permNum].append(IP)
    
    return outputData


    

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
    for i in range(1,6):
        filename = 'ahmed-subject' + str(i) + '.csv'
        data.append(read_csv(filename))

    data = consolidate_data(data)

    create_csv_from_data(data, "results.csv")
    create_graph(data)
