from .singleton_db import Database
from .fields import Field , IntegerField , CharField

class BaseModel(): 
    
    db = Database.get_instance()
    conn = db.conn
    cursor = db.cursor

    



    @classmethod
    def get_field(cls): 
        fields={}
        for attr_name , attr_val in cls.__dict__.items():
            if isinstance(attr_val,Field): 
                fields[attr_name]=attr_val
        return fields
    

    @classmethod
    def get_table_name(cls):
        return getattr(cls,"table_name",cls.__name__.lower()) 



    @classmethod 
    def create_table(cls): 
        
        list_sql_field=[]
        for field_name , field_obj in cls.get_field().items():  
            list_sql_field.append(field_obj.get_field_sql(field_name))

        fields_str=", ".join(list_sql_field)
        sql = f"CREATE TABLE IF NOT EXISTS {cls.get_table_name()} ({fields_str});"    

        cls.cursor.execute(sql)
        cls.conn.commit()
        print(f"✅ Table '{cls.get_table_name()}' created.")



    def validate(self):
        
        for field_name , field_obj in self.get_field().items():
            value = getattr(self,field_name,field_obj.default)
            
            #check if null=false
            if not field_obj.null and value is None : 
                raise ValueError(f"value of {field_name} shd not be empty !")


            
            if value is None: 
                continue


            #check value type
            if value is not None: 
                if isinstance(field_obj,IntegerField) and not isinstance(value,int):
                    raise TypeError(f"Field {field_name} must be an integer (int) !")
                if isinstance(field_obj,CharField) and not isinstance(value,str):
                    raise TypeError(f"Field {field_name} must be a string -> str !")
                    

            #check length for CharField
            if value is not None: 
                if isinstance(field_obj,CharField) and field_obj.max_length:
                    if len(value) > field_obj.max_length :
                        raise ValueError(f"Field {field_name} must be less than {field_obj.max_length} characters !")


            # check if unique=true
            if field_obj.unique and value is not None: 
        
                sql=f"SELECT COUNT(*) FROM {self.get_table_name()} WHERE {field_name} = ?"

                pk_field = None
                for fn , fo in self.get_field().items():
                    if fo.primary_key :
                        pk_field = fn
                        break

                if pk_field: 
                    pk_value = getattr(self, pk_field, None)
                    sql += f" AND {pk_field} != ?" if pk_value is not None else ""
                    args = (value,pk_value) if pk_value is not None else (value,)
                else : 
                    args = (value,)

                self.cursor.execute(sql,args)
                count=self.cursor.fetchone()[0] 
                if count > 0 :
                    raise ValueError(f"Field '{field_name}': '{value}' already exists (must be unique).")

        print("✅ All validations passed for the current instance.")


    
    def save(self): 
        

        self.validate() 

        list_att_name=[]
        list_att_val=[]
        get_fields = self.get_field().items()
        for att_name , att_val in get_fields:
            list_att_name.append(att_name)
            list_att_val.append(getattr(self,att_name,att_val.default))

        att_name_str=",".join(list_att_name)
        placeholders = ",".join(["?"]*len(list_att_name))
        sql= f"INSERT OR REPLACE INTO {self.get_table_name()} ({att_name_str}) VALUES ({placeholders})"

        self.cursor.execute(sql,list_att_val)
        self.conn.commit()
        print(f"✅ Row saved in '{self.get_table_name()}'")



    @classmethod
    def get(cls,**kwargs): 
        
        if not kwargs :
            raise ValueError("get() requires at least one condition")
        
        key,val=list(kwargs.items())[0]    

       
        
        sql=f"SELECT * FROM {cls.get_table_name()} WHERE {key}=?" # LIMIT 1
        cls.cursor.execute(sql,(val,))
        row = cls.cursor.fetchone()
     

        if not row:
            return None

        instance = cls()  
        for i , field_name in enumerate(list(cls.get_field().keys())): 


            setattr(instance,field_name,row[i])
        return instance
    


    def delete(self): 

        pk_field = None

        for field_nm , field_obj in self.get_field().items():
            if field_obj.primary_key:
                pk_field = field_nm
                break

        if pk_field is None:
            raise ValueError("YOUR MODEL DSNT HV PK !!!")

        pk_val=getattr(self,pk_field,None)

        if pk_val is None:
            raise ValueError("PK VALUE FOR DELETE IS NOT SPECIFIED.")

        sql = f"DELETE FROM {self.get_table_name()} WHERE {pk_field} = ?"
        self.cursor.execute(sql,(pk_val,))
        self.conn.commit()
        print(f"🗑️ row with {pk_field} = {pk_val} from '{self.get_table_name()}' deleted .")
