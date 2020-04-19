# Introduction:
This is a project that aims to make downloading from Nyaa.si easier for the user.
It is inspired from [anime dl](https://github.com/vn-ki/anime-downloader "anime dl").
### Usage:
```
Usage: nyaascrape.py [OPTIONS]

Options:
  -t, --type Anime/Manga         Choose Anime or Manga.
                                 Default: Anime.

  -u, --uploader Uploader        Choose Anime/Manga provider.
                                 [HorribleSubs, PuyaSubs, Ynk, GJM,
                                 BlurayDesuYo] [0, 1, 2, 3, 4].

  -s, --search Anime/Manga       Search  [required]
  -e, --episode Episode/Chapter    Select an episode/chapter.
  -f, --filter INTEGER             Filter by: size(0), seeders(1), id(2). Default: Size.

  --sort INTEGER                 Sort by: ascending(1), descending(0). Default: Descending.

  -xd, --external [0/1]        Download with Aria2(0) or using an external downloader(1) Default: Aria2c.

  --help                         Show this message and exit.
```
### Tips and tricks:
1. If the episode option is not used then by default the script will search for all anime/manga from trusted sources and all the uploaders. Also it will sort out the print results by size so that its easier to find batch download torrents.
2. The usage section is always accessible with just typying the name of the script and --help next to it in the terminal.
