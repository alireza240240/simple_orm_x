
class Field(): 

    def __init__(self,field_type,primary_key=False,unique=False,null=True,default=None):
        self.field_type=field_type
        self.primary_key=primary_key
        self.unique=unique
        self.null=null
        self.default=default


    def get_field_sql(self,field_name):
        sql =f"{field_name} {self.field_type}"
        if self.primary_key :
            sql += " PRIMARY KEY"
        if self.unique :
            sql += " UNIQUE"
        if not self.null :
            sql += " NOT NULL"
        if self.default is not None:
            
            default_val = f"'{self.default}'" if isinstance(self.default , str) else self.default    
            sql += f" DEFAULT {default_val}"
        return sql




class IntegerField(Field):  
    def __init__(self,**kwargs) :
        super().__init__("INTEGER",**kwargs)



class CharField(Field):
    def __init__(self,max_length=255,**kwargs):     
        super().__init__(f"VARCHAR({max_length})",**kwargs)

        self.max_length = max_length

