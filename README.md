# tma-string-finder
A spoiler free search utility for transcripts of The Magnus Archives. 

This program lets you specify a range of Magnus Archives episodes to search for a specific string, so that you can exclude episodes you haven't listened to yet. I made it because I wanted to check whether characters had appeared before, but the search of the semi-official transcript had no way to filter spoilers. 

Includes the ability to either return the episodes containing the search string, or return the sentences in each episode containing the string. 

## How to use:
The program will provide you with instructions when run. It will prompt you to give the episodes to begin and end searching, the string you're searching for, and whether you want it to print sentences. 

The main reason I made this program is that the search function on the snarp.github.io TMA transcripts doesn't have episode filtering options, so you can't prevent yourself from getting spoilers. 

This program is dumb. By that I mean that I've put little effort into making it catch bad user input. If you want to improve it, contributions are welcome.

## Async Version
The file "TMA transcript searcher async v2.py" is the experimental version that does asynchronous web requests. This cuts execution time by about 75%, assuming your network speed isn't the bottleneck. It's very unpolished, the invalid input handling is bad and it doesn't actually listen if you tell it not to print sentences. It's fast, though. 
