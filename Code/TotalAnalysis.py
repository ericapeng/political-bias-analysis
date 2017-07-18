def loadData():
    sentimentStream = open("SentimentLabels.txt","r+")
    articLengths = [100,100,100,100,100,116,93,88,100,109]
    sourceNames = ["Bloomberg","Fox News","Huffington Post","NBC News","Washington Post","USA Today","LA Times","CBS","ABC","CNN"]
    data = {}   # Contains all article analysis summaries
    currSource = 0
    nextCP = articLengths[currSource]

    # Go through articles in articleStream
    currNum = 0
    currLink = sentimentStream.readline()
    currLine = sentimentStream.readline()
    while currLink != "":
        # Update the checkpoint if at a checkpoint
        if currNum == nextCP:
            currSource += 1
            nextCP += articLengths[currSource]

        # Save data
        currData = currLine.split(" ")
        sentiment = 0
        if currData[0] == "neutral":
            sentiment = 1
        elif currData[0] == "neg":
            sentiment = 2
        data[currLink] = {
                "link": currLink, 
                "sentiment": sentiment, 
                "probability": float(currData[1]),
                "source": currSource
                }

        # Load next article's info
        currLink = sentimentStream.readline()
        currLine = sentimentStream.readline()
        currNum += 1

    print(len(data),"articles total")
    sentimentStream.close()

    # Add svm classifications
    svmStream = open("SVMLabels.txt")
    currNum = 0
    svmLabel = svmStream.readline()
    currLink = svmStream.readline()
    while currLink != "":
        if currLink in data:
            if not "svm" in data[currLink]:
                data[currLink]["svm"] = int(svmLabel)-1
                currNum += 1
        svmLabel = svmStream.readline()
        currLink = svmStream.readline()
    svmStream.close()
    print(currNum,"svm's updated")

    for l in data:
        if not "svm" in data[l]:
            print(l.rstrip(),"missing svm")

    #Analyze results
    results = [[[0 for g in range(3)] for j in range(3)] for i in range(10)]
    for i in range(10):
        articLengths[i] = 0
    for l in data:
        source = data[l]["source"]
        articLengths[source] += 1
        svm = data[l]["svm"]
        sentiment = data[l]["sentiment"]
        results[source][svm][sentiment] += 1

    # Print Results
    svmAxis = ["dem","ntrl","rep"]
    for i in range(10):
        print("News Source: "+sourceNames[i])
        print("\tpos\tntrl\tneg")
        for j in range(3):
            strData = svmAxis[j]
            for k in range(3):
                ratio = (1.0*results[i][j][k])/articLengths[i]
                strData += "\t"+"{0: .2f}".format(round(ratio,2))
            print(strData)
        print()



def main():
    loadData()

if __name__ == "__main__":
    main()
