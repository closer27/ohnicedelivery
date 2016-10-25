class Order:
    recipient_name = ''
    recipient_phone = ''
    zipcode = ''
    address = ''
    order_num = ''
    product_name = ''
    product_option = ''
    caution = ''

    def __init__(self, dictionary):
        self.recipient_name = dictionary['recipient_name']
        self.recipient_phone = dictionary['recipient_phone']
        self.zipcode = dictionary['zipcode']
        self.address = dictionary['address']
        self.order_num = dictionary['order_num']
        self.product_name = dictionary['product_name']
        self.product_option = dictionary['product_option']
        self.caution = dictionary['caution']
