from collections import deque
from bs4 import BeautifulSoup
import os
import requests
import re
import urllib.parse

os.system('clear')
user_url = str(input('[+] Please enter url: '))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] Enter Limit: '))

try:
	while True:
		count += 1
		if count > limit:
			break

		url = urls.popleft()
		scraped_urls.add(url)
		parts = urllib.parse.urlsplit(url)
		base_url = f'{parts.scheme}://{parts.netloc}'
		path = url[:url.rfind('/')+1] if '/' in parts.path else url

		print(f'{[count]} Process {url}')

		try:
			response = requests.get(url)
		except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
			continue

		new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
		emails.update(new_emails)

		soup = BeautifulSoup(response.text, 'html.parser')
		for anchor in soup.find_all('a'):
			link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
			if link.startswith('/'):
				link = base_url + link
			elif not link.startswith('http'):
				link = path + link

			if not link in urls and not link in scraped_urls:
				urls.append(link)

except KeyboardInterrupt:
	print('[-] Closing!')

print('\nProcess Complete!')
print(f'\n{len(emails)} Emails found: \n=========================================')

for mail in emails:
	print('  '+mail)
print('\n')
