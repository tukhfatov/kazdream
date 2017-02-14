# -*- coding: utf-8 -*-
import bs4
import execjs
import requests
import sqlite3
import time

DB_PATH = "kazdream_api/md_kazdream_db.sqlite3"

class My_DB(object):

	def __init__(self, path):
		super(My_DB, self).__init__()
		self.path = path

	def __connect(self):
		try:
			return sqlite3.connect(self.path)
		except Exception:
			print('ERROR in database. Informing developer...')
		return None

	def get_last_page(self):
		db = self.__connect()
		if db:
			cursor = db.cursor()
			cursor.execute('''SELECT MAX(page) FROM md_vacancy''')
			last = cursor.fetchone()
			db.close()
			if last[0]:
				return last[0]
			else:
				# get latest 10 job descriptions
				return 132520
		return None

	# able to encapsulate into object Vacancy, will do later
	def insert_new_vacancy(self, page, employer, contact_person, telephone, email, title, city, salary, working_place, working_hours, condition, responsibility, education, experience, requirements):

		db = self.__connect()
		if db:
			cursor = db.cursor()

			cursor.execute('''INSERT INTO md_vacancy(page, employer, contact_person, telephone, email, title, city, salary, working_place, working_hours, condition, responsibility, education, experience, requirements) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (page, employer, contact_person, telephone, email, title, city, salary, working_place, working_hours, condition, responsibility, education, experience, requirements))
			return db.commit()


class Page(object):

	BASE_URL = 'http://joblab.kz/vac'
	EXTENSION = '.html'
	CONTACTS_URL = 'http://joblab.kz/shared/ajax_contacts.php'

	def __init__(self, db):
		super(Page, self).__init__()
		self.db = db
		self.last_page_id = self.db.get_last_page()

	def get_last_page(self):
		self.last_page_id = self.last_page_id+1
		return self.BASE_URL+str(self.last_page_id)+self.EXTENSION

	def get_email(self,c):
		r = requests.post(self.CONTACTS_URL, data={'c':c, 't':'p'})

		if r.status_code == requests.codes.OK:
			return r.text
		return "TBA"

	def get_telephone(self,c):
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
		telephone=''
		email=''

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
					telephone=self.get_telephone('')
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

		self.db.insert_new_vacancy(self.last_page_id, employer, contact_person, telephone, email, title, city, salary, working_place, working_hours, condition, responsibility, education, experience, requirements)

		print("Inserted %d"%self.last_page_id)



# main
db = My_DB(DB_PATH)
page = Page(db)
req = requests.get(page.get_last_page())

while req.status_code != requests.codes.NOT_FOUND:
	try:
		page.parse_page(req.text)
	except Exception as e:
		print('ERROR in page %d. Informing developer...'%page.last_page_id)
	req = requests.get(page.get_last_page())
