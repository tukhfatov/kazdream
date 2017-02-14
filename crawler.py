import bs4
import execjs
import requests


last_id = 132521 # last page id

class Page(object):

	BASE_URL = 'http://joblab.kz/vac'
	EXTENSION = '.html'
	CONTACTS_URL = 'http://joblab.kz/shared/ajax_contacts.php'

	def __init__(self, last_id):
		super(Page, self).__init__()
		self.last_id = last_id
	
	def get_last_page(self):
		self.last_id = self.last_id+1
		return self.BASE_URL+str(self.last_id)+self.EXTENSION

	def get_email(self,c):
		r = requests.post(self.CONTACTS_URL, data={'c':c, 't':'p'})

		if r.status_code == requests.codes.OK:
			return r.text
		return "TBA"

	def parse_page(self, html_data):
		data = bs4.BeautifulSoup(html_data, 'html.parser')
		employer=''
		contact_person=''
		city=''
		salary=''
		working_place=''
		working_hours=''
		condition=''
		responsibility=''
		education=''
		experience=''
		requirements=''

		title = data.h1.string
		table = data.find('table', attrs={'class':'table-to-div'})
		for row in table.find_all('tr'):
			cells = row.find_all('td')
			column = cells[0].select('p')
			if column:
				query = column.pop().string
				if query == 'Прямой работодатель':
					employer = cells[1].b.string
				if query == 'Контактное лицо':
					contact_person = execjs.eval(cells[1].p.string[14:len(cells[1].p.string)-1])
				if query == 'Телефон':
					print('telephone')
				if query == 'E-mail':
					emailstr= data.find_all(string=lambda text:isinstance(text,bs4.Comment))[-1]
					email = self.get_email("m"+emailstr.split()[2][8:-10])
				if query =='Город':
					city = cells[1].b.string+", "+cells[1].font.string
				if query == 'Заработная плата':
					salary=cells[1].b.string
				if query == 'Место работы':
					working_place=cells[1].p.string
				if query == 'График работы':
					working_hours = cells[1].p.string
				if query == 'Условия':
					condition = cells[1].p.text
				if query == 'Обязанности':
					responsibility = cells[1].p.text
				if query == 'Образование':
					education = cells[1].p.text
				if query == 'Опыт работы':
					experience = cells[1].p.text
				if query == 'Требования':
					requirements = cells[1].p.text


# main
page = Page(last_id)
req = requests.get(page.get_last_page())

while req.status_code != requests.codes.NOT_FOUND:
	page.parse_page(req.text)
	print("###################################################")
	req = requests.get(page.get_last_page())
