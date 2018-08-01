from os import listdir, walk
from os.path import isfile, join
import re
import os

# Keywords for each required column
# Date of Sighting = Date - Sighting
# Date of Report = Receipt
# Shape = Decription
# Location = Position
# Duration = Duration
# Description = How Observed + Direction

def readNextFile(path, fileName):
    index = fileName.index(".txt")
    name = fileName[:index]
    nextNum = int(name) + 1
    nextFileName = str(nextNum)+".txt"

    file_object = open(path + nextFileName, "r", encoding="utf-8")
    lines = file_object.readlines()

    for i in range(0,len(lines)):
        line = lines[i]
        while not re.search(receipt_regex, line):
            i = i + 1
            if i >= len(lines):
                break
            line = lines[i]
            line = line.replace("\n", "")
        if re.search(receipt_regex, line):
            index = re.search(receipt_regex, line).end()
            rep_regex = re.compile("[rR][eE]?[pP][0oOa]?[rR][tT1lL]")

            report_date = ""
            # if the format is DATE OF RECEIPT OF REPORT
            if re.search(rep_regex, line):
                index2 = re.search(rep_regex, line).end()
                report_date = line[index2:]
                # if the date is not in the same line
                if not report_date:
                    i = i + 1
                    if i >= len(lines):
                        break
                    line = lines[i]
                    line = line.replace("\n", "")
                    while not line:
                        i = i + 1
                        if i >= len(lines):
                            break
                        line = lines[i]
                        line = line.replace("\n", "")
                    report_date = line

            # if the format is DATE OF RECEIPT
            else:
                report_date = line[index:]
                if not report_date:
                    i = i + 1
                    if i >= len(lines):
                        break
                    line = lines[i]
                    line = line.replace("\n", "")
                    while not line:
                        i = i + 1
                        if i >= len(lines):
                            break
                        line = lines[i]
                        line = line.replace("\n", "")
                    report_date = line
            return report_date




flying_regex = re.compile("[fF][lL1\s]?[yY][iI1tT\s][Nn\s]?[gGoO8bB]?")

date_regex = re.compile("[Dd]+[aeiAEI\?]+[t1T\?]+[aeiAEI]+")
min_regex = re.compile("m[iI1]?[nN][aAuUe]?[1tT][eEaiIA][sS]?")
sec_regex = re.compile("[sS][eEaoO]?[cCaoO]{1,2}[nN]?[dD][sS?]")
sight_regex = re.compile("[sS8][iI1tT\s][gGoO8bB][hH\s]?[iI1tT\s]{1,2}[Nn\s]?[gGoO8bB]?")
receipt_regex = re.compile("[[rR][eE]?[cC][Ee][iIl1]?[pPrR][tTiIl]")
desc_regex = re.compile("[Dd]+[aeiAEI]?[sS]?[cC]?[rR]?[iI1\?]?[pPgG]?[tT]?[iI]?[oO0][nN]")
pos_regex = re.compile("[pP]+[oO0a]?[sS\s]?[iI1\s]+[tT]?[iI\s]?[oO0]?[nN]")
howObs_regex = re.compile("[hH][oO08][wW\s]{1,2}[Oo][bB68][sS]?[eEaA][rR][vV\swW]?[eEaoO0][dD]")
dir_regex = re.compile("[Dd]+[aeiAEI]?[sSrR]?[aeEA][aAcCoO][iI1\?]?[tT]?[iI]?[oO0]?[nN]")
angle_regex = re.compile("[aA][nNmM][gG][uU]?[lL1iI][aAeE][rR]?")

# Remove the keywords belonging to questionnaire
loc_rub_regex = re.compile('(.*)geo(.*)loc(.*)door(.*)stat(.*)mov[a-z]*', re.IGNORECASE | re.DOTALL)
shape_rub_regex = re.compile('number of|object|size|shape|colour', re.IGNORECASE | re.DOTALL)
dir_rub_regex = re.compile('(.*)landmark(.*)bearing(.*)', re.IGNORECASE | re.DOTALL)



# Iterating through the generated directories for each PDF
directories = [ name for name in listdir(".") if os.path.isdir(os.path.join(".", name)) ]


with open("OCR_TSV_final.tsv", "w", encoding="utf-8") as tsv_file:
    tsv_file.write("DateOfSighting\tDateOfReport\tLocation\tShape\tDuration\tDescription\n")

    for each_dir in directories:
        path = each_dir+"/outtxt/"

        txtfiles = [f for f in sorted(listdir(path)) if isfile(join(path, f))]

        for file in txtfiles:
            if "txt" not in file:
                continue

            finalDict = {}
            finalDict["Date"] = []
            finalDict["Report"] = ""
            finalDict["Location"] = []
            finalDict["Shape"] = []
            finalDict["Duration"] = ""
            finalDict["Description"] = []


            file_object = open(path + file, "r", encoding="utf-8")
            lines = file_object.readlines()

            for i in range(0, len(lines)):
                line = lines[i]
                line = line.replace("\n", "")

                # if there is FLYING keyword in file
                if re.search(flying_regex, line):
                    i = i + 1
                    line = lines[i]
                    line = line.replace("\n", "")

                    # find the keyword "Date"
                    while not re.search(date_regex, line):
                        i = i + 1
                        if i >= len(lines):
                            break
                        line = lines[i]
                        line = line.replace("\n", "")

                        # when the keyword "Date" is found
                        if re.search(date_regex, line):
                            if re.search(sight_regex, line):
                                i = i
                            else:
                                # Look for keyword "Sighting"
                                while not re.search(sight_regex, line):
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            i = i + 1
                            if i >= len(lines):
                                break
                            line = lines[i]
                            line = line.replace("\n", "")

                            # parse the data till the keyword "Description" is found
                            while not re.search(desc_regex, line):
                                if re.search(min_regex, line) or re.search(sec_regex, line):
                                    finalDict["Duration"] = line
                                else:
                                    if line.strip() != "":
                                        finalDict["Date"].append(str(line))

                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")

                            # When the keyword "Description" is found
                            if re.search(desc_regex, line):
                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")
                                # remove extra matter from "Description" field
                                if re.search(shape_rub_regex, line):
                                    line = ""
                                # parse the data till the keyword "Position" is found
                                while not re.search(pos_regex, line):
                                    finalDict["Shape"].append(line)
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            # When the keyword "Position" is found
                            if re.search(pos_regex, line):
                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")
                                # remove extra matter from "Position" field
                                if re.search(loc_rub_regex, line):
                                    line = ""
                                # parse the data till the keyword "How Observed" is found
                                while not re.search(howObs_regex, line):
                                    finalDict["Location"].append(line)
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            # When the keyword "How Observed" is found
                            if re.search(howObs_regex, line):
                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")

                                # parse the data till the keyword "Direction" is found
                                while not re.search(dir_regex, line):
                                    finalDict["Description"] = [line]
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            # When the keyword "Direction" is found
                            if re.search(dir_regex, line):
                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")
                                if re.search(dir_rub_regex, line):
                                    line = ""
                                # parse the data till the keyword "Angle" is found
                                while not re.search(angle_regex, line):
                                    finalDict["Description"].append(line)
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            #Look for Date of "Receipt" keyword
                            if re.search(angle_regex, line):
                                i = i + 1
                                if i >= len(lines):
                                    break
                                line = lines[i]
                                line = line.replace("\n", "")
                                while not re.search(receipt_regex, line):
                                    i = i + 1
                                    if i >= len(lines):
                                        break
                                    line = lines[i]
                                    line = line.replace("\n", "")

                            # if "Receipt is in same file
                            if re.search(receipt_regex, line):
                                index = re.search(receipt_regex, line).end()
                                rep_regex = re.compile("[rR][eE]?[pP][0oOa]?[rR][tT1lL]")
                                report_date = ""
                                if re.search(rep_regex, line):
                                    index2 = re.search(rep_regex, line).end()
                                    report_date = line[index2:]
                                else:
                                    report_date = line[index:]
                                finalDict["Report"] = report_date
                            else:
                                # Read Next File to Extract the Date of Receipt
                                report_date = readNextFile(path, file)
                                finalDict["Report"] = report_date



            # Writing the final TSV

            # if not finalDict["Date"]:
            #     continue

            print(file)

            for data in finalDict["Date"]:
                tsv_file.write(data + " ")
            tsv_file.write("\t")
            tsv_file.write(finalDict["Report"])
            tsv_file.write("\t")
            for data in finalDict["Location"]:
                tsv_file.write(data + " ")
            tsv_file.write("\t")
            for data in finalDict["Shape"]:
                tsv_file.write(data + " ")
            tsv_file.write("\t")
            tsv_file.write(finalDict["Duration"])
            tsv_file.write("\t")
            tsv_file.write("Seen")
            for data in finalDict["Description"]:
                tsv_file.write(data + " ")
            tsv_file.write("\n")





