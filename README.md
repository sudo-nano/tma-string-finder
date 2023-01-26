# tma-string-finder
A spoiler free search utility for transcripts of The Magnus Archives. 

This program lets you specify a range of Magnus Archives episodes to search for a specific string, so that you can exclude episodes you haven't listened to yet. I made it because I wanted to check whether characters had appeared before, but the search of the semi-official transcript had no way to filter spoilers. 

Includes the ability to either return the episodes containing the search string, or return the sentences in each episode containing the string. 

## How to use:
Run the program with `python3 "TMA string finder.py"`. It will provide you with instructions when run. It will prompt you to give the episodes to begin and end searching, the string you're searching for, and whether you want it to print sentences. 

This code is pretty quick and dirty, so the invalid input handling isn't perfect. Contributions are welcome. 

## Async Version
Run `python3 "TMA transcript searcher async v2.py"` for the experimental version that does asynchronous web requests. This cuts execution time by about 75%, assuming your network speed isn't the bottleneck. It's very unpolished, the invalid input handling is bad and it doesn't actually listen if you tell it not to print sentences. 
