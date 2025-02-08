
class Voters():
    def __init__(self, db): 
        self.db = db
        
    def get_by_id(self, id):
        self.db.ensure_connection()
        return None
        # with self.db.conn.cursor() as cursor:
        #     query = """
        #     SELECT id, name, phone, user_level_id, shop_id
        #     FROM users 
        #     WHERE id = %s 
        #     """
        #     cursor.execute(query, (id,))
        #     data = cursor.fetchone()
        #     if data:
        #         user_level = self.get_user_level_id(data[3])
        #         shop = MyShops(self.db).get_by_id(data[4])
        #         company = self.db.get_company_by_id(shop.company_id)
        #         license = self.db.get_license_by_id(company.license_id)   
        #         return User(data[0], data[1], data[2], user_level, shop, company, license)
        #     else:
        #         return None   