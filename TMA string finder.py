# Connor's quick and dirty Magnus Archives transcript searcher

import requests
from bs4 import BeautifulSoup

# Startup information
print("Thanks for using Connor's quick and dirty TMA transcript searcher.")
print()
print("Some details you should be aware of:")
print("- The index numbers are inclusive. This means that if you specify 20 as the end of the search, it will search episode 20's transcript but stop before 21.")
print("- The string you input to search for will be looked for exactly. If you input more than one word, the program will only search for instances in which they appear together exactly as typed.")
print("- The input string is CaSe SeNsItIvE.")
print()

# User input
start_index = input("Episode on which to begin search: ")
end_index = int(input("Episode on which to end search: "))
search_term = str(input("Word(s) to search for: "))

pr_sen_valid = False
pr_sen_valid_inputs = ["yes", "y", "no", "n"]

# If invalid input given, re-prompt user for input
while not pr_sen_valid:
    print_sentences = input("Print sentences? (y/n) ")
    print_sentences = print_sentences.lower()

    if print_sentences in pr_sen_valid_inputs:
        pr_sen_valid = True

    else:
        print("Invalid input. Please use '11y' or 'n'.")

# Change print_sentences to true if user answers y or yes
if print_sentences == "y" or print_sentences == "yes":
    print_sentences = True

elif print_sentences == "n" or print_sentences == "no":
    print_sentences = False

else:
    print("Error: Print sentences query expects only 'y' or 'n'")

# Invalid episode input handling
if int(start_index) > 200:
    print("Error: Starting episode too high.")
    exit()

if int(start_index) < 0:
    print("Error: Negative starting episode.")
    exit()

if int(end_index) > 200:
    print("Error: Ending episode too high.")
    exit()

if int(end_index) < 0:
    print("Error: Negative ending episode.")

def pad0s(inputString):
    while len(inputString) < 3:
        inputString = "0" + inputString

    return(inputString)

# Page cleaner function using BeautifulSoup HTML parser
# HTML parsing my detested
def cleanPage(content):
    page_parsed = BeautifulSoup(content, "html.parser")
    page_div = page_parsed.find("div", class_="entry-content")
    page_p = page_div.find_all("p")

    page_text = ""
    for line in page_p:
        page_text += line.text + " "

    return page_text

# Vars for main loop
url_prefix = "https://snarp.github.io/magnus_archives_transcripts/episode/"
currentIndex = int(start_index)
episodesWithTerm = []
termAppearanceSentences = {}

# Main program loop
while currentIndex <= end_index:
    episodeNumber = pad0s(str(currentIndex))
    url = url_prefix + episodeNumber + ".html"

    page = requests.get(url)
    page_parsed = cleanPage(page.content) # uses cleanPage to remove HTML tags from page content
    page_sentences = page_parsed.split(". ")

    if str(page) != "<Response [200]>":
        print("Error: Unable to fetch transcript for episode " + episodeNumber)

    if page_parsed.find(search_term) != -1:
        episodesWithTerm.append(episodeNumber)

    if print_sentences:
        for sentence in page_sentences:

            if sentence.find(search_term) != -1:
                if str(episodeNumber) in termAppearanceSentences:
                    termAppearanceSentences[str(episodeNumber)].append(sentence)
                    # Debug
                    #print('Debug: Appending "' + sentence + '" to termAppearanceSentences')

                else:
                    termAppearanceSentences[str(episodeNumber)] = [sentence]


    currentIndex += 1

# After main loop, print results
if episodesWithTerm == []:
    print("Text not found in selected episodes.")
    exit()

elif print_sentences:
    print()
    # Print episode numbers and sentences containing the search string
    for episode in termAppearanceSentences:

        episode_sentences = termAppearanceSentences[episode]

        for sentence in episode_sentences:
            print(str(episode) + ": " + sentence + ".")

        print()

else:
    print()
    print("Text found in the following episodes:")
    for i in episodesWithTerm:
        print(i)
