class Equipment:

    def __init__(self, ID, IMEI, ProductPtr):
        self.ID = ID
        self.IMEI = IMEI
        self.ProductPtr = ProductPtr

    def add_product(self, product):
    	self.product = product