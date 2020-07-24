from bs4 import BeautifulSoup
from tabulate import tabulate
import requests
import click
import re

@click.command()
@click.option('--search', '-s', 'search', metavar='QUERY', help='Search the specified string on nyaa.', type=str, required=True)
@click.option('--filter', '-f', 'filte', metavar=['size','seeders','date'], help='Filter the search results using the given filter.', \
	type=click.Choice(['size','seeders','date'], case_sensitive=True), required=False, default='seeders', show_default=True)
@click.option('--sort', 'sort', metavar=['asc','desc'], help='Sort the search result in the given order.', \
	type=click.Choice(['asc','desc'], case_sensitive=True), required=False, default='desc', show_default=True)
@click.option('--media-type', '-mt', 'MediaType', metavar=['anime','manga'], help='Choose what type of media to search for.', \
	type=click.Choice(['anime','manga'], case_sensitive=True), required=False, default='anime', show_default=True)
@click.option('--external-downloader', '-xd', 'external_downloader', help='When used the download will start with the given program. Use "system" as a program value to download with the default torrent program.', required=False, default='')
@click.option('--choice', '-c', 'Choice', help='When used the results will not be printed and the download for the selected result will start.', required=False, default=None, type=int)


def main(search, filte, sort, MediaType, external_downloader, Choice):
	filters = {'seeders': 'seeders', 'size': 'size', 'date': 'id'}
	media_types = {'anime': '1_2', 'manga': '3_1'}
	params = {'c': media_types[MediaType], 'q': search, 's': filters[filte], 'o': sort}
	results = search_results(BeautifulSoup(requests.get('https://nyaa.si', params=params).text, 'html.parser'))
	table, magnets = make_pretty_table(results) # here i map the tuple of the 2 lists to 2 variables
	if not Choice:
		click.echo(table)
		choice = click.prompt('Enter the anime no: ', type=int, default=0)
	else:
		choice = Choice
	download_link = magnets[choice]
	downloader(download_link, external_downloader)


## A class object that will store all info for each result.
class search_result:
	def __init__(self, title, size, seeders, leechers, magnet, link, poster='', meta=''):
		self.title = title.replace('.mkv', '').strip()
		self.link = 'https://nyaa.si' + link
		tmp_soup = BeautifulSoup(requests.get(self.link).text, 'html.parser')
		self.magnet = magnet
		self.size = size
		self.leechers = leechers
		self.seeders = seeders
		self.poster = poster
		self.meta = meta
		self.uploader = tmp_soup.find('a', class_='text-success').text
		self.uploader_safety = tmp_soup.find('a', class_='text-success')['title']
		self.description = tmp_soup.find('div', id='torrent-description').text
		self.total_files = len([x.text for x in tmp_soup.find('div', class_='torrent-file-list panel-body').find('ul').find_all('li')])

	def __str__(self):
		return self.title



## Returns a list where every item of the list is a search_result object with info inside it.
def search_results(html_source):
	regex = r'(magnet:)+[^"]*'
	Storage = [
		search_result(
		title = i.select("a:not(.comments)")[1].get("title"),
		size = i.find_all('td',class_ = 'text-center')[1].text,
		seeders = i.find_all('td',class_= 'text-center')[3].text,
		leechers = i.find_all('td',class_ = 'text-center')[4].text,
		magnet = i.find_all('a',{'href':re.compile(regex)})[0].get('href').replace('\n', ''))
		for i in html_source.select("tr.default, tr.success")
	]
	return Storage

## Makes a table for tabulate and returns the table along the magnet links
def make_pretty_table(list_results):

	results_list = []
	magnet_links = []
	count = -1
	# Creates 2 separate parallel lists, the first one is a 2 dimensional list for the pretty table, 
	# and the 2nd one is to access the magnet link for each item in the 1st list
	for anime in list_results:
		count += 1
		entry = [count, anime.title, anime.seeders, anime.size]
		results_list.append(entry)
		magnet_links.append(anime.magnet)

	# for every header there must be an equivalent item in the list, thats why tables have 2 dimensional lists
	# so that each item can correspond to a header
	headers = ['SlNo', "Title", "Seeders", "Size"]
	table = tabulate(results_list, headers, tablefmt='psql')
	table = '\n'.join(table.split('\n')[::-1])
	return table, magnet_links # here i return a tuple of the two lists

def downloader(magnet_link, external_downloader):
	import subprocess, os
	if not external_downloader:
		command = ['aria2c', magnet_link]
		subprocess.run(command, shell=True)
	elif external_downloader == 'system':
		import subprocess, sys
		if 'win' not in sys.platform:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, magnet_link])
		else:
			os.startfile(magnet_link)
	else:
		command = [external_downloader, magnet_link]
		subprocess.run(command, shell=True)
	
if __name__ == '__main__':
	main()
	print('Finished Downloading!')
