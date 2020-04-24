from bs4 import BeautifulSoup as bs
import sys, click, subprocess, os, re, urllib, requests
# from tabulate import tabulate
@click.command()
@click.option('--type', '-t', help='Choose Anime or Manga.                            Default: Anime.', default='Anime', metavar='[Anime/Manga]')
@click.option('--uploader', '-u', help='Choose Anime/Manga provider.	[HorribleSubs, PuyaSubs, Ynk, GJM, BlurayDesuYo].', default=9999, metavar='[0|1|2|3|4]')
@click.option('--search', '-s', help='Search', required=True, metavar='[Anime/Manga]', multiple=True)
@click.option('--episode', '-e', help='Select an episode/chapter.', metavar='Episode/Chapter')
@click.option('--filter', '-f', help='Filter by: size(0), seeders(1), id(2).          Default: Size.', default=0, metavar='[0|1|2]')
@click.option('--sort', help='Sort by: ascending(1), descending(0).          Default: Descending.', default=0, metavar='[0|1]')
@click.option('--external', '-xd', help='Download with Aria2c(0) or using an external downloader(1).          Default: Aria2c.', default=0, metavar='[0|1]')
def main(type, search, filter, sort, external, episode, uploader):
	if episode == None:
		if uploader == 9999:
			def userSelection():
				cataChecker = type
				searc = str(search).replace(' ', '+')
				if cataChecker == 'Anime' or cataChecker == 'anime' or cataChecker == 'a':
					link = f'https://nyaa.si/?f=2&c=1_2&q={searc}&s=size&o=asc'.lower()
					return link
				elif cataChecker == 'Manga' or cataChecker == 'manga' or cataChecker == 'm':
					link = f'https://nyaa.si/?f=2&c=3_1&q={search}&s=size&o=asc'.lower()
					return link
				else:
					raise Exception("Please insert anime or manga!")
		else:
			def uploaderCheck():
				up = ['[HorribleSubs] ', '[PuyaSubs!] ', '[YnK] ', '[GJM] ', '[BlurayDesuYo] ']
				upl = uploader
				if upl < 4 and upl > -1:
					return up[upl]
				else:
					raise Exception("Please use the correct selections!")
			def userSelection():
				cataChecker = type
				upload = uploaderCheck()
				searc = str(upload) + str(search).replace(' ', '+') + ' ' + episode
				if cataChecker == 'Anime' or cataChecker == 'anime' or cataChecker == 'a':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=1_2&q={searc}{filta}{ud}'.lower()
					return link
				elif cataChecker == 'Manga' or cataChecker == 'manga' or cataChecker == 'm':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=3_1&q={searc}{filta}{ud}'.lower()
					return link
				else:
					raise Exception("Please insert anime or manga!")
	else:
		if uploader == 9999:
			def userSelection():
				cataChecker = type
				searc = str(search).replace(' ', '+') + ' ' + episode
				if cataChecker == 'Anime' or cataChecker == 'anime' or cataChecker == 'a':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=1_2&q={searc}{filta}{ud}'.lower()
					return link
				elif cataChecker == 'Manga' or cataChecker == 'manga' or cataChecker == 'm':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=3_1&q={searc}{filta}{ud}'.lower()
					return link
				else:
					raise Exception("Please insert anime or manga!")
		else:
			def uploaderCheck():
				up = ['[HorribleSubs] ', '[PuyaSubs!] ', '[YnK] ', '[GJM] ', '[BlurayDesuYo] ']
				upl = uploader
				if upl < 4 and upl > -1:
					return up[upl]
				else:
					raise Exception("Please use the correct selections!")
			def userSelection():
				cataChecker = type
				upload = uploaderCheck()
				searc = str(upload) + str(search).replace(' ', '+') + ' ' + episode
				if cataChecker == 'Anime' or cataChecker == 'anime' or cataChecker == 'a':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=1_2&q={searc}{filta}{ud}'.lower()
					return link
				elif cataChecker == 'Manga' or cataChecker == 'manga' or cataChecker == 'm':
					ud = udCheck()
					filta = filterCheck()
					link = f'https://nyaa.si/?f=2&c=3_1&q={searc}{filta}{ud}'.lower()
					return link
				else:
					raise Exception("Please insert anime or manga!")			

			
	def filterCheck():
		filta = ['&s=size','&s=seeders','&s=id']
		if filter < 3 and filter > -1:
			return filta[filter]
		else:
			raise Exception("Please use the correct selections!")

	def udCheck():
		ud = ['&o=desc','&o=asc']
		if sort < 2 and sort > -1:
			return ud[sort]
		else:
			raise Exception("Please use the correct selections!")

	def torrentDownloader(magnet):
		if external == 1:
			os.startfile(magnet)
		elif external == 0:
			def run_command(magnet):
				process = f'aria2c {magnet}'
				process = subprocess.Popen(process, stdout=subprocess.PIPE)
				while True:
					output = process.stdout.readline()
					if output == '' and process.poll() is not None:
						break
					if output:
						print (output.strip())
				rc = process.poll()
				return rc
			run_command(magnet)
		else:
			print('Please only use [0/1] for the --external-downloader')
            

	def searchResults(link):
		Storage = [
			SearchResult(
			title = i.select("a:not(.comments)")[1].get("title"),
			size = i.find_all('td',class_ = 'text-center')[1].text,
			seeders = i.find_all('td',class_= 'text-center')[3].text,
			leechers = i.find_all('td',class_ = 'text-center')[4].text,
			magnet = i.find_all('a',{'href':re.compile(regex)})[0].get('href'))
			for i in link.select("tr.default, tr.success")
		]
		return Storage
	def searcher():
		Link = userSelection()
		page = requests.get(Link).text
		link = bs(page, 'html.parser')
		Storage = searchResults(link)
		table = []
		for i in range(len(Storage)):
			num = str(i)
			name = Storage[i]
			seed = Storage[i].seeders
			size = Storage[i].size
			line = "{} - {} ".format(num, name)
			line = str(line) + ''+ 'seeds: '+ seed+' '+ size
			print(line)
		choice = input('Which one would you like to select? \n')
		magnet = Storage[int(choice)].magnet
		torrentDownloader(magnet)
		recursionCheck = 'n'
		return recursionCheck

	class SearchResult:
		def __init__(self, title, size, seeders, leechers, magnet, poster='', meta=''):
			self.title = title
			self.magnet = magnet
			self.size = size
			self.leechers = leechers
			self.seeders = seeders
			self.poster = poster
			self.meta = meta

		def __repr__(self):
			return '<SearchResult Title: {} Size: {} Seeders: {} Leechers: {} Magnet: {}>'.format(self.title, self.size,
																								self.seeders,
																								self.leechers,
																								self.magnet)
		def __str__(self):
			return self.title

		@property
		def pretty_metadata(self):
			"""
			pretty_metadata is the prettified version of metadata
			"""
			if self.meta:
				return ' | '.join(val for _, val in self.meta.items())
			return ''
	regex = r'(magnet:)+[^"]*'
	recursionCheck = searcher()
	while recursionCheck == 'y' or recursionCheck == 'Y':
		recursionCheck = searcher()
	else:
		pass
if __name__ == '__main__':
	main()
