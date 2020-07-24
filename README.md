# Introduction:
This is a project that aims to make downloading from Nyaa.si easier for the user.
It is inspired from [anime dl](https://github.com/vn-ki/anime-downloader "anime dl").
### Usage:
```
Usage: nyaaScrapev2.py [OPTIONS]

Options:
  -s, --search QUERY              Search the specified string on nyaa.
                                  [required]

  -f, --filter ['size', 'seeders', 'date']
                                  Filter the search results using the given
                                  filter.  [default: seeders]

  --sort ['asc', 'desc']          Sort the search result in the given order.
                                  [default: desc]

  -mt, --media-type ['anime', 'manga']
                                  Choose what type of media to search for.
                                  [default: anime]

  -xd, --external-downloader TEXT
                                  When used the download will start with the
                                  given program. Use "system" as a program
                                  value to download with the default torrent
                                  program.

  -c, --choice INTEGER            When used the results will not be printed
                                  and the download for the selected result
                                  will start.

  --help                          Show this message and exit.
```
### Tips and tricks:
1. The usage section is always accessible with just typing the name of the script and --help next to it in the terminal.
example: ``python nyaaScrape.py --help``
