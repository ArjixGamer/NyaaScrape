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
@click.option('--external-downloader', '-xd', 'external_downloader', help='If used the download will start with the given program.', required=False, default='')
@click.option('--choice', '-c', 'Choice', help='If used the results will not be printed and the download for the selected result will start.', required=False, default=None, type=int)


def main(search, filte, sort, MediaType, external_downloader, Choice):
	filters = {'seeders': 's=seeders', 'size': 's=size', 'date': 's=id'}
	media_types = {'anime': 'c=1_2', 'manga': 'c=3_1'}
	link = f'https://nyaa.si/?{media_types[MediaType]}&q={search}&{filters[filte]}&o={sort}'
	results = searchResults(BeautifulSoup(requests.get(link).text, 'html.parser'))
	table, magnets = make_pretty_table(results)
	if not Choice:
		click.echo(table)
		choice = click.prompt('Enter the anime no: ', type=int, default=0)
	else:
		choice = Choice
	download_link = magnets[choice]
	downloader(download_link, external_downloader)


## Result object
class SearchResult:
	def __init__(self, title, size, seeders, leechers, magnet, poster='', meta=''):
		self.title = title.replace('.mkv', '').strip()
		self.magnet = magnet
		self.size = size
		self.leechers = leechers
		self.seeders = seeders
		self.poster = poster
		self.meta = meta

	def __str__(self):
		return self.title



## Returns a list with all the search results
def searchResults(html_source):
	regex = r'(magnet:)+[^"]*'
	Storage = [
		SearchResult(
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
	for anime in list_results:
		count += 1
		entry = [count, anime.title, anime.seeders, anime.size]
		results_list.append(entry)
		magnet_links.append(anime.magnet)


	headers = ['SlNo', "Title", "Seeders", "Size"]
	table = tabulate(results_list, headers, tablefmt='psql')
	table = '\n'.join(table.split('\n')[::-1])
	return table, magnet_links

def downloader(magnet_link, external_downloader):
	import subprocess
	if not external_downloader:
		command = ['aria2c', magnet_link]
	else:
		command = [external_downloader, magnet_link]
	subprocess.run(command, shell=True)
	print('Finished Downloading!')

if __name__ == '__main__':
	main()
