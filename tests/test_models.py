import unittest
from myorm.base_model import BaseModel
from myorm.fields import IntegerField , CharField


class User(BaseModel): 
    table_name = "users"
    id = IntegerField(primary_key = True)
    name = CharField(max_length=100 , null=False)
    email = CharField(unique = True)

class TestUserModel(unittest.TestCase): 
    
        
    def setUp(self):        
        User.cursor.execute("DROP TABLE IF EXISTS users")
        User.create_table()     

    def test_create_user(self): 

        tuser = User()
        tuser.id = 1
        tuser.name = "testAli"
        tuser.email = "testAli@gmail.com"
        tuser.save()

        fch_usr = User.get(id=1) 
        self.assertIsNotNone(fch_usr)
        self.assertEqual(fch_usr.name,"testAli") 
        self.assertEqual(fch_usr.email,"testAli@gmail.com")

    def test_null_name_raises(self):

        tuser = User()
        tuser.id=1
        tuser.name=None 
        
        tuser.email="testAli@gmail.com"

        with self.assertRaises(ValueError): 
            tuser.save()
        

    def test_type_check_fields(self):

        tuser = User()
        tuser.id="alaky" 
        tuser.name="testAli"
        tuser.email="testAli@gmail.com"

        with self.assertRaises(TypeError):
            tuser.save()

    def test_max_len_char(self):

        tuser = User()
        tuser.id=5
        tuser.name= "T" * 101 
        tuser.email="testAli@gmail.com"

        with self.assertRaises(ValueError):
            tuser.save()

    def test_unique_email_raises(self):

        u1=User()
        u1.id=5
        u1.name="ali"
        u1.email="tekrary@gmail.com"
        u1.save()

        u2=User()
        u2.id=7
        u2.name="sara"
        u2.email="tekrary@gmail.com"
        
        with self.assertRaises(ValueError):
            u2.save()


    def test_user_delete(self):
        
        tuser=User()
        tuser.id=9
        tuser.name="delAli"
        tuser.email="delAli@gmail.com"
        tuser.save()

        tuser.delete()
        fch_usr= User.get(id=9)
        self.assertIsNone(fch_usr)
