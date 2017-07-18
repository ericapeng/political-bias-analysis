import requests
import json

# I think it would work well to make a document with an article on each line
def condenseData():
    articleComp = open("articles.txt", "w")
    sourceFolders = ["Bloomberg", "Fox News", "Huffington Post", "NBC News", "Washington Post"]
    navigation = "../Txt Files/"
    currArticleNumber = 1
    for folder in sourceFolders:
        print("\nIn folder, "+folder+" now:")
        uniqueLinks = {}
#        for i in range(1,2):       # For testing first article of each news source
        for i in range(1,101):
            f = open(navigation + folder + "/article" + str(i) + ".txt")

            article = ""
            num_words = 0
            currLink = f.readline()     # Discard the first line with the link to the article
            if not currLink in uniqueLinks:
                uniqueLinks[currLink] = 1
                currLine = f.readline()
                while currLine != "":
                    article += currLine.rstrip()
                    num_words += len(currLine.split())
                    currLine = f.readline()
                
                if num_words > 50000:
                    print("You have been warned...")
                articleComp.write(currLink+article+"\n")

            else:
                print(i)

            f.close()
        print("\t",len(uniqueLinks))
    articleComp.close()



def classifySentiment():
    # Get articles by line
    # make a post for each article
    # write to new file the label and the probability of that label
    sentimentComp = open("sentiments.txt", "w")
    articleStream = open("articles.txt", "r+")
    sentiments = []
    neutralMean = 0.0

    currLink = articleStream.readline()
    currArticle = articleStream.readline()
    while currArticle != "":
        apiResponse = requests.post("http://text-processing.com/api/sentiment/", data={'text':currArticle})
        sentiments.append(json.loads(apiResponse.text))
        sentiments[len(sentiments)-1]["link"] = currLink
        neutralMean += sentiments[len(sentiments)-1]["probability"]["neutral"]
        currLink = articleStream.readline()
        currArticle = articleStream.readline()
    
    neutralMean = neutralMean / len(sentiments)
    print("neutralMean:",neutralMean)
    label = ""
    value = 0.0
    for s in sentiments:
        if s["probability"]["neutral"] < neutralMean:
            label = "pos"
            value = s["probability"]["pos"]
            if value < 0.5:
                label = "neg"
                value = 1-value
        else:
            label = "neutral"
            value = s["probability"]["neutral"]
        sentimentComp.write(s["link"]+label+" "+str(value)+"\n")

    sentimentComp.close()
    articleStream.close()



def processResults():
    sentimentStream = open("sentiments.txt", "r+")
    sourceLengths = [100 for i in range(5)]
    sourcenum = 0
    currSent = sentimentStream.readline()
    articlenum = 1
    nextSource = 1
    numpos = 0
    numneg = 0

    while currSent != "":
        currData = currSent.split(" ")
        if articlenum == nextSource:
            if articlenum != 1:
                print("\tpos:",1.0*numpos/sourceLengths[sourcenum])
                print("\tneg:",1.0*numneg/sourceLengths[sourcenum])
                print("\tneutral:")
            print("Analyzing source",sourcenum,":",articlenum)
            nextSource += sourceLengths[sourcenum]
            sourcenum += 1
            numpos = 0
            numneg = 0

        if currData[0] == "pos":
            numpos += 1
        elif currData[0] == "neg":
            numneg += 1

        currSent = sentimentStream.readline()
        articlenum += 1

    sentimentStream.close()



def main():
    #condenseData()
    classifySentiment()
    #processResults()

if __name__ == "__main__":
    main()
