import yaml
import os

class InsuranceCompany:

	def __init__(self, data:dict, id: int = None):
		self.title = data['title']
		self.description = data['description']
		self.logo = data['logo']
		self.webpage = data['webpage']
		self.price = data['price']
		self.insurance_types = data['insurance_types']
		self.id = id
		self.calculated_price = None
		self.price = 3000

class Companies:

	def __init__(self):
		self.yaml_file = 'templates/companies/companies.yaml'
		self.companies = self.__create_companies()

	def __create_companies(self):
		# here but database retrieval code
		data = None
		companies = []
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_path = os.path.join(BASE_DIR, 'templates', 'companies', 'companies.yaml')
		with open(file_path) as file:
			data = yaml.safe_load(file)
		for i, elem in enumerate(data):
			company = InsuranceCompany(elem, i)
			companies.append(company)
		return companies
