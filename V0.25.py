import csv, os

    #PASS TO WRITER TO WRITE MASTERS.

numDict = {"Bills": 0, "Food": 0, "Income": 0, "Gifts": 0, "Travel": 0, "Other": 0, "Savings": 0} #this helps us to keep track of how many of each transaction we have and therefore where in the csv they need to go

def list_grabber():
    '''
    This function opens a standardised file to read the types of transactions into a dictionary, storing the worksheet, column and row for each kind of transaction.

    (csv) --> dict
    '''
    foodnum=0
    billsnum=0
    giftsnum=0
    travelnum=0
    incomenum=0
    othernum=0
    savingsnum=0
    global numDict

    file1 = 'keys.csv' #filepath

    keys1 = {} #stores the keys

    with open(file1, 'r') as keys:
        reader = csv.reader(keys) # set up the reading function

        for row in reader: #start reading
            title = row[0] #Find the name of the transaction

            keys1[title] = [row[1], int(row[2])] #Create a key for the transaction with a list
                                                 #holding the type of transaction and the column number.
            if row[1] == "Bills":
                billsnum = billsnum+1
            elif row[1] == "Food":
                foodnum = foodnum+1
            elif row[1] == "Income":
                incomenum = incomenum+1
            elif row[1] == "Gifts":
                giftsnum = giftsnum+1
            elif row[1] == "Travel":
                travelnum = travelnum+1
            elif row[1] == "Other":
                othernum = othernum+1
            elif row[1] == "Savings":
                savingsnum = savingsnum+1

    numDict = {"Bills": billsnum, "Food": foodnum, "Income": incomenum, "Gifts": giftsnum, "Travel": travelnum, "Other": othernum, "Savings": savingsnum}

    return keys1 #return key dictionary



def key_maker(lister):
    '''
    need to make a function which creates a key list from the new transactions found on this cycle

    (dict) ---> csv
    '''
    with open ("keys.csv", "w") as keysfile:
        keyWriter = csv.writer(keysfile)
        for key in lister.keys():
            keyWriter.writerow([key, lister[key][0], lister[key][1]])



def NDays(month, year):
    '''
    (int, int) ---> int
    calculates the number od#f days in the year based on a given month number and year number.

    >>>NDays(12, 2012)
    31
    >>>NDays(9, 2007)
    30
    >>>NDays(2, 2011)
    28
    >>>NDays(2, 2016)
    29
    '''
    if month in [1,3,5,7,8,10,12]: #31 day months
        return 31
    elif month in [4,6,9,11]: #30 day months
        return 30
    else: #feb
        if year%4 == 0: #leapyear
            return 29
        else:
            return 28

def date_sorter(date):
    q = 0 
    qq = 0
    x = ''
    day = ''
    month = ''
    year = ''
    
    for i in date: #lets find the min date

        if q>1: # Have we passed the year and month?
           
            if qq==1: # Are we on the second digit of the day?
                x = x+i
                day = x
                x = ''
            else:
                x = x+i
                qq = qq+1 # First half of the day done

        elif i == "-": # This can only happen immediately after the full year or month.
           
            if q == 1: # Is it the month?
                month = x
            elif q==0: # Then it's the year
                year = x
                #NO Q ADDING
            x= ""
            q = q+1 # Move on to the next part of the date

        else: # we're either in the month or year
            x = x+i
    
    return day, month, year



def date_cleaner(datesList):
    '''
    A function which cleans out the datelist to hold every day between the two days regardless of whether it exists within the file

    (lst) ---> lst

    >>>date_cleaner(["2014-03-24", "2014-03-20"])
    ["2014-03-20", "2014-03-21", "2014-03-22", "2014-03-23", "2014-03-24"]
    '''
    #declare variables to hold the individual parts of the min and max dates
    #use these to find all the inbetween dates and enter the new ones into newDates
    years = []
    months = []
    days = []
    newDates = []

    #Just a placeholder for the date parts
    dayss = ''
    monthss = ''
    yearss = ''
   
    day, month, year = date_sorter(datesList[0]) #grab max date

    days.append(int(day))
    months.append(int(month))
    years.append(int(year))
    
    day, month, year = date_sorter(datesList[len(datesList)-1]) #grab min date

    days.append(int(day))
    months.append(int(month))
    years.append(int(year))

            
    if years[0]-years[1]==1: #then we've shifted a year

        for month in range(months[1], 13): #for those months in the first year which are relevant

            if month == months[1]: #we are at the beginning
                for day in range(days[1], NDays(month, years[1])+1): #for this month find the first day, and then the max number of days in this month
                    newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))

            else: # we are past the beginning
                for day in range(1, NDays(month, years[1])+1): #for each following month go from 1 to the limit
                    newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))

        for month in range(1, months[0]+1): #for the next year

            if month == months[0]: #if we've reached the last month
                for day in range(1, days[0]+1): #then go to the limit of that month
                    newDates.append((str(years[0])+"-"+str(month)+"-"+str(day)))

            else: #otherwise
                for day in range(1, NDays(month, years[0])+1): #do the whole of each preceding month.
                    newDates.append((str(years[0])+"-"+str(month)+"-"+str(day)))

    elif (years[0]-years[1])>1: #if greater than a years difference
		
        for year in range(years[1], years[0]+1):

            if year == years[1]: #if the first year

                for month in range(months[1], 13): #for those months in the first year which are relevant

                    if month == months[1]: #we are at the beginning
                        for day in range(days[1], NDays(month, years[1])+1): #for this month find the first day, and then the max number of days in this month
                            newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))

                    else: # we are past the beginning
                        for day in range(1, NDays(month, years[1])+1): #for each following month go from 1 to the limit
                            newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))
                    
            elif year == years[0]: #for all preceding years but the latest

                for month in range(1, months[0]+1): #for the next year

                    if month == months[0]: #if we've reached the last month
                        for day in range(1, days[0]+1): #then go to the limit of that month
                            newDates.append((str(years[0])+"-"+str(month)+"-"+str(day)))

                    else: #otherwise
                        for day in range(1, NDays(month, years[0])+1): #do the whole of each preceding month.
                            newDates.append((str(years[0])+"-"+str(month)+"-"+str(day)))

            else: #for the final year
                      
                for month in range(1, 13): #for the next year

                    if month == months[0]: #if we've reached the last month
                        for day in range(1, days[0]+1): #then go to the limit of that month
                            newDates.append((str(year)+"-"+str(month)+"-"+str(day)))

                    else: #otherwise
                        for day in range(1, NDays(month, year)+1): #do the whole of each preceding month.
                            newDates.append((str(year)+"-"+str(month)+"-"+str(day)))

    else: #all in the same year

        if months[1] == months[0]: #all in the same month
            for day in range(days[1], days[0]+1):
                newDates.append(str(years[1])+"-"+str(month[1])+"-"+str(day))

        else: #multiple months

            for month in range(months[1], months[0]+1): #from first to last month

                        
                if month == months[1]: #if first month
                    for day in range(days[1], NDays(month, years[1])+1):
                        newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))
				
                elif month == months[0]: #if last month
                    for day in range(1, days[0]+1):
                        newDates.append((str(years[0])+"-"+str(month)+"-"+str(day)))
                
                else: #all the months inbetween
                    for day in range(1, NDays(month, years[1])+1):
                        newDates.append((str(years[1])+"-"+str(month)+"-"+str(day)))
    
    
    origin=0

    for every in newDates:
        if len(every) == 8:
            isEight = True
        else:
            isEight = False
        middle = False
        if (len(every)==9) or (isEight == True):
            news = ''
            countser = 0
            for each in every:
                if countser == 5:
                    if (isEight == True) or (every[6] == "-"):
                        news = news+"0"+each
                        middle = True
                    else:
                        news = news+each
                    countser = countser+1
                elif countser == 7:
                    if isEight == True:
                        news = news+"0"+each
                    else:
                        news = news+each
                    countser = countser+1
                elif countser == 8:
                    if middle == False:
                        news = news+"0"+each
                    else:
                        news = news+each
                    countser = countser+1
                else:
                    news = news+each
                    countser = countser+1
            newDates[origin] = news
        origin = origin+1
    for every in newDates:
        if len(every)==9:
            news = ''
            countser = 0
            for each in every:
                if countser == 8:
                    news = news+"0"+each
                    countser = countser+1
                else:
                    news = news+each
                    countser = countser+1
            newDates[origin] = news
        origin = origin+1

    return newDates

def HSBC(file, dates, organiser):
    '''
    A function to read out HSBC CSVs into the standardised format.
    (file, lst, dict) ---> dict, lst
    '''

    global keylist
    global numDict
    types = ["Food", "Travel", "Bills", "Income", "Gifts", "Other", "Savings"]
    with open(file, 'r') as statement:
        reader = csv.reader(statement)

        for row in reader:

            isAmazon = False

            if not row[0] in dates: #add to date list
                dates.append(row[0])
            if not row[0] in organiser: #add date to dict
                organiser[row[0]] = {}
            if ("Amazon" in row[1]) or ("AMAZON" in row[1]): #Check if amazon purchase as no specific transaction id
                isAmazon = True

            #start the process of adding an unknown to the keylist
            if (not row[1] in keylist) and (isAmazon==False): #If we can't find the key
                #Then what kind of transaction is it?
                ktypeo = input("What type of transaction is " + row[1] +" for "+row[2]+"on the "+row[0]+"? Bills, Food, Income, Gifts, Travel, Savings or Other: ") #ask for the type
                
                if not ktypeo in types: #make sure it is a valid type
                    vals = False
                    while vals == False:
                        ktypeo = input("That is not a valid type of transaction, please enter either Bills, Food, Income, Gifts, Travel, Savings or Other. Capitalisation is important: ") #keep asking until it is a valid type
                        if ktypeo in types: #Then it is a valid type
                            vals = True

                for key in numDict.keys(): #We now know what type of transaction it is.
                    if ktypeo == key: #so loop through the transaction types until we find the right one.
                        numDict[key] += 1 #increment the number of transactions we have of this type.
                        keylist[row[1]] = [ktypeo, numDict[key]-1] #and add it to the keylist.

                '''    I need to test this bit but the above 4 lines should represent the below 28.
                if ktypeo == "Bills": #change the number of the specific type for what was chosen
                    global billsNumber
                    keylist[row[1]] = [ktypeo, billsNumber]
                    billsNumber = billsNumber+1
                if ktypeo == "Food":
                    global foodNumber
                    keylist[row[1]] = [ktypeo, foodNumber]
                    foodNumber = foodNumber+1
                if ktypeo == "Income":
                    global incomeNumber
                    keylist[row[1]] = [ktypeo, incomeNumber]
                    incomeNumber = incomeNumber+1
                if ktypeo == "Gifts":
                    global giftNumber
                    keylist[row[1]] = [ktypeo, giftNumber]
                    giftNumber = giftNumber+1
                if ktypeo == "Travel":
                    global travelNumber
                    keylist[row[1]] = [ktypeo, travelNumber]
                    travelNumber = travelNumber+1
                if ktypeo == "Other":
                    global otherNumber
                    keylist[row[1]] = [ktypeo, otherNumber]
                    otherNumber = otherNumber+1
                if ktypeo == "Savings":
                    global savingsNumber
                    keylist[row[1]] = [ktypeo, savingsNumber]
                    savingsNumber = savingsNumber+1
                
                global keyNumber
                keyNumber = keyNumber+1 #add to total number of key values '''
                #end process of adding an unknown to the keylist
            if isAmazon == True: #Amazon values are special
                if not "Amazon" in organiser[row[0]]:
                    organiser[row[0]]["Amazon"] = []
                organiser[row[0]]["Amazon"].append(float(row[2]))
            else: #Now we must have the key for the transaction so we can add it into the organiser.
                if not row[1] in organiser[row[0]]: #can't add to nothing so if the key is new, make the value 0 to give something to add to.
                    organiser[row[0]][row[1]] = []
                organiser[row[0]][row[1]].append(float(row[2]))  #for key date, open the value which is a dictionary.
                                                                                     #Therefore find key termed the transaction.
                                                                                     #Add value of transaction to that value.
    key_maker(keylist) #update keylist

    return organiser, dates

def Halifax(file, dates, organiser):
    '''
    A function to read out Halifax CSVs into the standardised format.
    (file, lst, dict) ---> dict, lst
    '''

    global keylist
    global numDict

    with open(file, 'r') as statement:
        reader = csv.reader(statement)
        reader.__next__()

        for row in reader:
            row5 = 0
            row6 = 0
            try:
                row5 = float(row[5])
            except ValueError:
                row5 = 0
            try:
                row6 = float(row[6])
            except ValueError:
                row6 = 0
            
            isAmazon = False
            datecomp  = ''
            dateCount = 0
            day = ""
            month = ""
            year = ""
            for part in row[0]:
                if part == "/":
                    part = part
                elif dateCount < 2:
                    day = day+part
                elif dateCount < 5:
                    month = month+part
                else:
                    year = year+part
                dateCount = dateCount+1
            datecomp = year+"-"+month+"-"+day
            if not datecomp in dates: #add to date list
                dates.append(datecomp)
            if not datecomp in organiser: #add date to dict
                organiser[datecomp] = {}
                
            if "CD 5333" in row[4]:
                typer1 = row[4].replace(" CD 5333", "")
                typer = typer1.rstrip()
            else:
                typer = row[4].rstrip()
                
            if ("Amazon" in typer) or ("AMAZON" in typer): #Check if amazon purchase as no specific transaction id
                isAmazon = True
            #start the process of adding an unknown to the keylist

            if (not typer in keylist) and (isAmazon==False): #check if it is in the keylist
                ktypeo = input("What type of transaction is " + typer +" for "+str(row6-row5)+" on the "+datecomp+"? Bills, Food, Income, Gifts, Travel, Savings or Other: ") #ask for the type
                if not ktypeo in ["Bills", "Food", "Income", "Gifts", "Travel", "Other", "Savings"]: #make sure it is a valid type
                    vals = False
                    while vals == False:
                        ktypeo = input("That is not a valid type of transaction, please enter either Bills, Food, Income, Gifts, Travel, Savings or Other. Capitalisation is important: ") #keep asking until it is a valid type
                        if ktypeo in ["Bills", "Food", "Income", "Gifts", "Travel", "Other", "Savings"]:
                            vals = True

                for key in numDict.keys(): #We now know what type of transaction it is.
                    if ktypeo == key: #so loop through the transaction types until we find the right one.
                        numDict[key] += 1 #increment the number of transactions we have of this type.
                        keylist[typer] = [ktypeo, numDict[key]-1] #and add it to the keylist.
                '''
                if ktypeo == "Bills": #change the number of the specific type for what was chosen
                    global billsNumber
                    keylist[typer] = [ktypeo, billsNumber]
                    billsNumber = billsNumber+1
                if ktypeo == "Food":
                    global foodNumber
                    keylist[typer] = [ktypeo, foodNumber]
                    foodNumber = foodNumber+1
                if ktypeo == "Income":
                    global incomeNumber
                    keylist[typer] = [ktypeo, incomeNumber]
                    incomeNumber = incomeNumber+1
                if ktypeo == "Gifts":
                    global giftNumber
                    keylist[typer] = [ktypeo, giftNumber]
                    giftNumber = giftNumber+1
                if ktypeo == "Travel":
                    global travelNumber
                    keylist[typer] = [ktypeo, travelNumber]
                    travelNumber = travelNumber+1
                if ktypeo == "Other":
                    global otherNumber
                    keylist[typer] = [ktypeo, otherNumber]
                    otherNumber = otherNumber+1
                if ktypeo == "Savings":
                    global savingsNumber
                    keylist[typer] = [ktypeo, savingsNumber]
                    savingsNumber = savingsNumber+1
                global keyNumber
                keyNumber = keyNumber+1 #add to total number of key values
                '''
                #end process of adding an unknown to the keylist
            if isAmazon == True: #Amazon values are special
                if not "Amazon" in organiser[datecomp]:
                    organiser[datecomp]["Amazon"] = []
                organiser[datecomp]["Amazon"].append(float(row6-row5))
            else:
                if not typer in organiser[datecomp]: #can't add to nothing so if the key is new, make the value 0 to give something to add to.
                    organiser[datecomp][typer] = []
                organiser[datecomp][typer].append(float(row6-row5))  #for key date, open the value which is a dictionary. Therefore find key termed the transaction. Add value of transaction to that value.
                
    key_maker(keylist) #update keylist
	
    return organiser, dates


def date_splitter():
    '''
    This function needs to take the main statement file and split it out into manageable and separable chunks.
    '''
    dates = [] #set this to store the dates in order
    organiser = {} #set this to organise all of the information but in manageable slices
    
    numms = True
    while numms == True:
        try:
            numm = int(input("How many statements do you want to compile on this cycle? "))
            break
        except ValueError:
            print("That wasn't a number, please try again")

    for something in range(0, numm):
        #with open(input("Type in the filepath for statement " + str(something+1) + " here: "), 'r') as statement:
        #    reader = csv.reader(statement)

        banker = True
        typeo = input("Which bank did this statement come fromm? (currently supporting HSBC and Halifax) ")
        
        if not typeo in ["HSBC", "Halifax"]: #Don't know this bank
            banker = False

        while banker == False: #We need a known bank
            typeo = input("This programme doesn't support that bank right now. If you would like it to, please send a sample of a CSV file from that bank to nick.a.sarbicki@live.com. Otherwise please enter either HSBC or Halifax, remember capitalisation is important. ")
            if typeo in ["HSBC", "Halifax"]:
                banker = True

        if typeo.lower() == "hsbc": #It's HSBC
            organiser, dates = HSBC(input("Type in the filepath for statement " + str(something+1) + " here: "), dates, organiser)
            #So convert HSBC to standard format
            
        elif typeo.lower() == "halifax": #It's Halifax
            organiser, dates = Halifax(input("Type in the filepath for statement " + str(something+1) + " here: "), dates, organiser)
            #So convert Halifax to standard format.

    dates.sort(reverse = True) #get the dates in order

    for key in organiser.keys():
        for innerKey in organiser[key].keys():
            organiser[key][innerKey] = list(set(organiser[key][innerKey]))
    
    dates = date_cleaner(dates)
    dates = list(set(dates))
    dates.sort()
    return organiser, dates


def dupli_clean(organiser, dates):
    '''
    This function needs to take the now compiled list of transactions, which has been wiped of duplicates.
    It then needs to write each individual transaction out for future reference (so as to not to steadily accumulate duplicates).
    Do I need a key system? probably not

    (dict, lst) ---> file
    '''
    oldFile = False
    
    for date in dates:
        if not date in organiser:
            organiser[date] = {}
        retainer = {}
        paths = "ref/"+date[:4]+"/"+date[5:7]+"/"

        if not os.path.exists(paths):
            os.makedirs(paths)
        try:
            with open(paths+date[8:]+".rl", "r") as oldFile:
                for line in oldFile:
                    newLine = line.split("~") #files are written as tilda delimited so split into an array.
                    
                    if not date in organiser: #we need all the active dates to be added here
                        organiser[date][newLine[0]] = []
                    elif not newLine[0] in organiser[date]: #and definitely need the active types
                        organiser[date][newLine[0]] = []

                    counts = 0
                    for item in newLine: 
                        if counts > 0: #as long as we're past the type
                            organiser[date][newLine[0]].append(float(item)) #add all the items to the array.
                        counts = counts+1
        	
        except FileNotFoundError:
            oldFile = False
		
        with open(paths+date[8:]+".rl", "w") as newFile: #time to create our new file
            for key in organiser[date].keys(): #for each type
                instr = "" #create a blank string
                    
                organiser[date][key] = list(set(organiser[date][key])) # get rid of any duplicates
                            
                instr = key #make the first value the type
                            
                for i in organiser[date][key]: #find each transaction value
                    instr = instr+"~"+str(i) #add a tilda to delimit the items and then add the next transaction as a string
                            
                instr = instr+"\n" #add a newline
                newFile.write(instr)
    organiser = sum_items(organiser)
    return organiser
	
def sum_items(organiser):
	for key in organiser:
		for innerKey in organiser[key]:
			organiser[key][innerKey] = float("{0:.2f}".format(sum(organiser[key][innerKey]))) #summing all items and formatting to avoid float point form issue
	return organiser


def type_splitter(datee, org, dictnum):
    
    #create required lists and pull in global variables
    foods = {}
    billss = {}
    incomes = {}
    gifts = {}
    travels = {}
    others = {}
    savingss = {}
    x = 0
    for date in datee: #create a dictionary for each date
        foods[date] = [date]
        billss[date] = [date]
        incomes[date] = [date]
        gifts[date] = [date]
        travels[date] = [date]
        others[date] = [date]
        savingss[date] = [date]
       
        for q in range(0, dictnum["Bills"]): # append total number of possible types of transactions for bills and following corresponding lists, inputting 0 values as placeholders
            billss[date].append(0)

        for q in range(0, dictnum["Food"]):
            foods[date].append(0)

        for q in range(0, dictnum["Income"]):
            incomes[date].append(0)

        for q in range(0, dictnum["Gifts"]):
            gifts[date].append(0)

        for q in range(0, dictnum["Travel"]):
            travels[date].append(0)

        for q in range(0, dictnum["Other"]):
            others[date].append(0)

        for q in range(0, dictnum["Savings"]):
            savingss[date].append(0)
        x = x+1
        
    count = 0 #set counter
    for date1 in datee: #for each date
        if date1 in org:
            for key in org[date1].keys(): #find the key values within that date and loop through them
                if not key in keylist: #make sure it exists (no reason it wouldn't)
                    print(str(key)+" not found in keylist. Error occured")
                elif keylist[key][0] == "Bills": #otherwise check what kind of transaction it was
                    billss[date1][keylist[key][1]+1] = org[date1][key] #grab the latest list and for the current date (decided using count) find the column value from the keylist (the second value in the keys dictionary). From this grab the relevant value from the org list using the date and key for transaction.
                elif keylist[key][0] == "Food":
                    foods[date1][keylist[key][1]+1] = org[date1][key] 
                elif keylist[key][0] == "Income":
                    incomes[date1][keylist[key][1]+1] = org[date1][key] 
                elif keylist[key][0] == "Gifts":
                    gifts[date1][keylist[key][1]+1] = org[date1][key] 
                elif keylist[key][0] == "Travel":
                    travels[date1][keylist[key][1]+1] = org[date1][key] 
                elif keylist[key][0] == "Other":
                    others[date1][keylist[key][1]+1] = org[date1][key] 
                elif keylist[key][0] == "Savings":
                    savingss[date1][keylist[key][1]+1] = org[date1][key]

        count = count+1
    masterList = {"Bills": billss, "Food": foods, "Income": incomes, "Gifts": gifts, "Travel": travels, "Other": others, "Savings": savingss}
    return masterList


def writer(masterList, datee, dictNum):

    datee.sort()


    column = 0

    localfiles = []
    dater = []
    billsList = []
    foodList = []
    incomeList = []
    giftList = []
    travelList = []
    otherList = []
    savingsList = []
	
	
    for q in range(0, dictNum["Bills"]): #create placeholders for the transactions of each type in a list
        billsList.append(0)
    for q in range(0, dictNum["Food"]):
        foodList.append(0)
    for q in range(0, dictNum["Income"]):
        incomeList.append(0)
    for q in range(0, dictNum["Gifts"]):
        giftList.append(0)
    for q in range(0, dictNum["Travel"]):
        travelList.append(0)
    for q in range(0, dictNum["Other"]):
        otherList.append(0)
    for q in range(0, dictNum["Savings"]):
        savingsList.append(0)
    

    for ii in keylist: #run through the transactions

        if keylist[ii][0] == "Bills": #if this transaction is x type than add it in at y place in the list
            billsList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Food":
            foodList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Income":
            incomeList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Gifts":
            giftList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Travel":
            travelList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Other":
            otherList[keylist[ii][1]] = ii
        elif keylist[ii][0] == "Savings":
            savingsList[keylist[ii][1]] = ii #current problem as out of range index
        else:
            print("Not found key type, error thrown")
   
 
    for file in os.listdir():
        if file.endswith(".csv"):
            localfiles.append(file)
    if "bills.csv" in localfiles:
        with open("bills.csv", "r") as bills, open("food.csv", "r") as food, open("income.csv", "r") as income, open("gifts.csv", "r") as gift, open("travel.csv", "r") as travel, open("other.csv", "r") as other, open("savings.csv", "r") as savings:
            billsReader = csv.reader(bills)
            foodReader = csv.reader(food)
            incomeReader = csv.reader(income)
            giftReader = csv.reader(gift)
            travelReader = csv.reader(travel)
            otherReader = csv.reader(other)
            savingsReader = csv.reader(savings)

            billsReader.__next__()
            foodReader.__next__()
            incomeReader.__next__()
            giftReader.__next__()
            travelReader.__next__()
            otherReader.__next__()
            savingsReader.__next__()

            for row in billsReader:
                if row[0] not in datee:
                    datee.append(row[0])
                    dater.append(row[0])
                    if len(row)<dictNum["Bills"]:
                        for it in range(len(row), dictNum["Bills"]+1):
                            row.append(0)
                    masterList["Bills"][row[0]] = row
                    
                
            for row in foodReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Food"]:
                        for it in range(len(row), dictNum["Food"]+1):
                            row.append(0)
                    masterList["Food"][row[0]] = row

            for row in incomeReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Income"]:
                        for it in range(len(row), dictNum["Income"]+1):
                            row.append(0)
                    masterList["Income"][row[0]] = row

            for row in giftReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Gifts"]:
                        for it in range(len(row), dictNum["Gifts"]+1):
                            row.append(0)
                    masterList["Gifts"][row[0]] = row

            for row in travelReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Travel"]:
                        for it in range(len(row), dictNum["Travel"]+1):
                            row.append(0)
                    masterList["Travel"][row[0]] = row

            for row in otherReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Other"]:
                        for it in range(len(row), dictNum["Other"]+1):
                            row.append(0)
                    masterList["Other"][row[0]] = row

            for row in savingsReader:
                if row[0] in dater or row[0] not in datee:
                    if len(row)<dictNum["Savings"]:
                        for it in range(len(row), dictNum["Savings"]+1):
                            row.append(0)
                    masterList["Savings"][row[0]] = row

    datee = list(set(datee))
    datee.sort()

    for key in masterList:
        for innerKey in masterList[key]:
            for it in range(0, len(masterList[key][innerKey])):
                if len(str(masterList[key][innerKey][it])) < 1:
                    masterList[key][innerKey][it] = 0
    
    with open("bills.csv", "w") as bills, open("food.csv", "w") as food, open("income.csv", "w") as income, open("gifts.csv", "w") as gift, open("travel.csv", "w") as travel, open("other.csv", "w") as other, open("savings.csv", "w") as savings:
        billswriter = csv.writer(bills)
        foodwriter = csv.writer(food)
        incomewriter = csv.writer(income)
        giftwriter = csv.writer(gift)
        travelwriter = csv.writer(travel)
        otherwriter = csv.writer(other)
        savingswriter = csv.writer(savings)

        billswriter.writerow([""]+billsList)
        foodwriter.writerow([""]+foodList)
        incomewriter.writerow([""]+incomeList)
        giftwriter.writerow([""]+giftList)
        travelwriter.writerow([""]+travelList)
        otherwriter.writerow([""]+otherList)
        savingswriter.writerow([""]+savingsList)

        
                
        for dated in datee:
            billswriter.writerow(masterList["Bills"][dated])
            foodwriter.writerow(masterList["Food"][dated])
            incomewriter.writerow(masterList["Income"][dated])
            giftwriter.writerow(masterList["Gifts"][dated])
            travelwriter.writerow(masterList["Travel"][dated])
            otherwriter.writerow(masterList["Other"][dated])
            savingswriter.writerow(masterList["Savings"][dated])


keylist = list_grabber() #Grab the keylist

transactions, dateList = date_splitter() #compile the csvs, generate the transaction dictionary and a list of dates.

transactions = dupli_clean(transactions, dateList) #Check against previous records or that date. Clean out duplicates, update the transaction dictionary and update the records of that date.

master = type_splitter(dateList, transactions, numDict)

writer(master, dateList, numDict)
