class Client:
    def __init__(self, client_id, name , gender, phone, address):
        self.client_id = client_id
        self.name = name
        self.gender = gender 
        self.phone = phone
        self.address = address

    def serialize(self):
        return {
            'client_id':self.client_id,
            'name':self.name,
            'gender':self.gender,
            'phone' : self.phone,
            'address': self.address,

        }
        