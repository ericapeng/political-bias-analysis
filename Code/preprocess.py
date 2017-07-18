from stemming.porter2 import stem
import string 

# Takes list of words as input and returns the preprocessed version
def preprocess(words):
    newwords = []
    for word in words:
        newword = ""
        # Normalize email adresses
        if "@" in word:
            newword = "@"
        # Normalize links
        elif "https://www" in word:
            newword = "www"
            print("found link")
        else:
            for c in word:
                # Only keep letters - discard all punctuation
                if (ord(c) >= 97 and ord(c) <= 122) or (ord(c) >= 65 and ord(c) <= 90):
                    newword += c
                # Normalize numbers
                if ord(c) >= 48 and ord(c) <= 57:
                    newword = "#"
                    break
            if newword != "#":
                # Lowercase and destem
                newword = stem(newword.lower())
        if newword != "":
            newwords.append(newword)
    return newwords

def preprocessAllData():
    trainingComp = open("training.txt","w")
    labeledLinks = {}
    for i in range(1,51):
        trainingSource = open("../Txt Files/Labeled Data/article"+str(i)+".txt")
        label = trainingSource.readline()
        currLink = trainingSource.readline()
        labeledLinks[currLink] = 1
        article = []
        currLine = trainingSource.readline()
        while currLine != "":
            article = article + currLine.split(' ')
            currLine = trainingSource.readline()
        article = preprocess(article)
        trainingComp.write(label+currLink+" ".join(article)+"\n")
        trainingSource.close()
    trainingComp.close()


    articleComp = open("compilation.txt", "w")
    sourceFolders = ["Bloomberg", "Fox News", "Huffington Post", "NBC News", "Washington Post"]
    navigation = "../Txt Files/"
    currArticleNumber = 1
    for folder in sourceFolders:
        print("\nIn folder, "+folder+" now:")
        uniqueLinks = {}
#        for i in range(1,2):       # For testing first article of each news source
        for i in range(1,101):
            f = open(navigation + folder + "/article" + str(i) + ".txt")

            article = []
            currLink = f.readline()     # Discard the first line with the link to the article
            if not currLink in uniqueLinks:
                if not currLink in labeledLinks:
                    uniqueLinks[currLink] = 1
                    currLine = f.readline()
                    while currLine != "":
                        article = article + currLine.split(' ')
                        currLine = f.readline()

                    article = preprocess(article)
                    #print(article)
                    articleComp.write(currLink+" ".join(article)+"\n")

            else:
                print(i)

            f.close()
        print("\t",len(uniqueLinks))
    articleComp.close()






def main():
    #test_file = open("test.txt", "r+")
    '''test_file = open("../Txt Files/Bloomberg/article1.txt", "r+")
    article = []
    currLine = test_file.readline()
    while currLine != "":
        article = article + currLine.split(' ')
        currLine = test_file.readline()

    article = preprocess(article)
    print(article)

    test_file.close()'''

    preprocessAllData()



if __name__ == "__main__":
    main()
