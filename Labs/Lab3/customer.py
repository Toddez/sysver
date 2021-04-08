class Customer:

	def __init__(self, ID, Firstname, Lastname, Age, Sex, Street, Zip, City, Nationality='', IMSIPtr='', IMEIPtr='', SubscriptionPtr='', Email='', Password=''):
		self.ID = ID
		self.Firstname = Firstname
		self.Lastname = Lastname
		self.Age = Age
		self.Sex = Sex
		self.Street = Street
		self.Zip = Zip
		self.City = City
		self.Nationality = Nationality
		self.IMSIPtr = IMSIPtr
		self.IMEIPtr = IMEIPtr
		self.SubscriptionPtr = SubscriptionPtr
		self.Email = Email
		self.Password = Password

	def add_equipment(self, equipment):
		self.equipment = equipment

	def add_sim(self, sim):
		self.sim = sim