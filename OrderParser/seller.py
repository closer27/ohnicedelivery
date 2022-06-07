class Seller:
    idx_recipient_name = 0
    idx_recipient_phone = 0
    idx_zipcode = 0
    idx_address = 0
    idx_order_num = 0
    idx_product_name = 0
    idx_product_option = 0
    idx_caution = 0

    def description(self):
        pass


class TenByTen(Seller):
    idx_recipient_name = 6
    idx_recipient_phone = 8
    idx_zipcode = 9
    idx_address = 10
    idx_order_num = 0
    idx_product_name = 14
    idx_product_option = 15
    idx_caution = 11

    def description(self):
        return "TenByTen"


class Book(Seller):
    idx_recipient_name = 7
    idx_recipient_phone = 8
    idx_zipcode = 10
    idx_address = 11
    idx_order_num = 0
    idx_product_name = 2
    idx_product_option = 5
    idx_caution = 12

    def description(self):
        return "Book"


class StoreFarm(Seller):
    idx_recipient_name = 11
    idx_recipient_phone = 42
    idx_zipcode = 46
    idx_address = 44
    idx_order_num = 1
    idx_product_name = 17
    idx_product_option = 20
    idx_caution = 47

    def description(self):
        return "Storefarm"


class Uniqmoment(Seller):
    idx_recipient_name = 2
    idx_recipient_phone = 10
    idx_zipcode = 8
    idx_address = 9
    idx_order_num = 0
    idx_product_name = 4
    idx_product_option = 3
    idx_caution = 11

    def description(self):
        return "Uniqmoment"


class Biskit(Seller):
    idx_recipient_name = 9
    idx_recipient_phone = 14
    idx_zipcode = 10
    idx_address = 11
    idx_order_num = 0
    idx_product_name = 2
    idx_product_option = 4
    idx_caution = 15

    def description(self):
        return "Biskit"


class Aland(Seller):
    idx_recipient_name = 0
    idx_recipient_phone = 1
    idx_zipcode = 3
    idx_address = 4
    idx_order_num = 6
    idx_product_name = 7
    idx_product_option = 9  # No mean. just index of blank
    idx_caution = 11

    def description(self):
        return "Aland"


class Hottracks(Seller):
    idx_recipient_name = 7
    idx_recipient_phone = 8
    idx_zipcode = 12
    idx_address = 13
    idx_order_num = 6
    idx_product_name = 16
    idx_product_option = 17  # No mean. just index of blank
    idx_caution = 9

    def description(self):
        return "Hottracks"
