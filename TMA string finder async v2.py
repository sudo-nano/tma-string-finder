# Connor's quick and dirty Magnus Archives transcript searcher
# async 2 electric boogaloo, but hopefully I do it right this time
# Version 8 August 2022

import requests
import asyncio
import aiohttp
import ssl
import certifi
import sys
from codetiming import Timer
from bs4 import BeautifulSoup

# Startup information
print("Thanks for using Connor's quick and dirty TMA transcript searcher.")
print("This is the improved async version, and is much faster.")
print()
print("Some details you should be aware of:")
print("- The index numbers are inclusive. This means that if you specify 20 as the end of the search, it will search episode 20's transcript but stop before 21.")
print("- The string you input to search for will be looked for exactly. If you input more than one word, the program will only search for instances in which they appear together exactly as typed.")
print("- The input string is CaSe SeNsItIvE.")
print("- There is currently no input checking. If you give invalid inputs, the program will just crash.")
print()

# Check for debug argument
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        print("* Execution timer and debug output enabled. *")
        debug = True

    else:
        print("Invalid argument. 'debug' is the only valid argument for this program.")
        exit()

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
        print("Invalid input. Please use 'y' or 'n'.")

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

async def task(name, work_queue):
    # Stuff to make certificates work
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    # The rest of the task function
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession(connector=conn) as session:

        while not work_queue.empty():
            episode_number = await work_queue.get()
            url = url_prefix + pad0s(str(episode_number)) + ".html"

            if debug:
                print(f"Task {name} checking episode {episode_number}")
                timer.start()

            async with session.get(url) as response:
                page = await response.text()
                page_clean = None

                # Error info printout if the cleanPage function fails, because the BeautifulSoup
                # error stack trace is really not helpful
                try:
                    page_clean = cleanPage(page)

                except:
                    print("** Error detected **")
                    print("Episode: " + str(episode_number))
                    print("URL: " + url)

                page_sentences = page_clean.split(". ")

                for sentence in page_sentences:
                    if sentence.find(search_term) != -1:
                        print(pad0s(str(episode_number)) + ": " + sentence)
                        print()


            if debug:
                timer.stop()



async def main():
    work_queue = asyncio.Queue()

    # Put work in the queue
    for i in range(1, end_index + 1):
        await work_queue.put(i)

    # Run some tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
            asyncio.create_task(task("Three", work_queue)),
            asyncio.create_task(task("Four", work_queue))
        )

if __name__ == "__main__":
    asyncio.run(main())
