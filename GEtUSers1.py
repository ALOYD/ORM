# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:17:25 2019

@author: UKR0020792
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:05:32 2018

@author: fuand
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, Integer, String, DateTime,Float
import json
#cd C:\Users\fuand\OneDrive\Документы\work\Python
#from sqlalchemy import Column, Integer, DateTime
engine = create_engine('sqlite:///orderman7.db')



Session = sessionmaker(bind=engine)
Bases = declarative_base()


#Base.metadata.create_all(engine)



############################start record adding###############################
session = Session()


##########################GEn classes###################

########################Inthago################################### 
class Inthago_dev(object):
    
    
    def __init__(self,json):
         self.json = json
         self.data = {}
         self.obj = Bases()
         self.vals=[]
         self.d={}
         self.types={"<class 'str'>":"String","<class 'int'>":"Integer"}
    
    def create_tables_dict(self,main_table_name):
      create_classes={}
      self.main_table_name = main_table_name
      main_table = str(main_table_name).capitalize()
#      attr_dict = {'__tablename__':main_table.lower(),'id': Column(Integer, primary_key=True), '__table_args__':{'extend_existing': True} }
      attr_dict = {'__tablename__':main_table.capitalize(),'id': Column(Integer, primary_key=True), '__table_args__':{'extend_existing': True} }
      create_classes[main_table]= type('%s' % main_table,(Bases,),attr_dict)
      print(create_classes,'\n',main_table,'\n')
      for key,value in self.json.items():
         print('adhasjkhdashdasl!!!!!!!!!',value,type(value),self.same_type(value))
         types = self.same_type(value) 
         ll = []
         if isinstance( types,type):
             
             ll.append(types)
             types = ll
         else:
             types = types
         if ((isinstance(value,list) and any((list,dict in types))) or isinstance(value,dict)):
             rest_tables=str(key)
             attr_dict = {'__tablename__':rest_tables.capitalize(),'id': Column(Integer, primary_key=True)}
             create_classes[rest_tables]= type('%s' % rest_tables.capitalize(),(Bases,),attr_dict)
             print(create_classes,'\n',rest_tables,'\n')

      self.data.update(create_classes)
      

    def main_table_dict(self):
#        types={"<class 'str'>":"String","<class 'int'>":"Integer"}
        obj = set(self.data) - set(self.json)
        obj =  self.data.get(list(obj)[0])
#        backpop = str(list(set(self.data) - set(self.json))[0])
        backpop =obj.__name__.lower()
        val_cols = list(set(self.json) - set(self.data))#Columns
#        cols = []
        cols = {}
        for i in val_cols:
            cols.update({i:self.types[str(type(i))]})
#            if isinstance(i,list):
#                if (len(i)<=1):
#                    cols.update({i})
        val_rels = list(set(self.json) - set(val_cols))
        rels = {}
        for i in val_rels:
            print(backpop.lower())
#            rels.update({i:relationship('"'+str(i)+'"',back_populates="'"+backpop.lower()+"'",cascade="all, delete, delete-orphan")})
            rels.update({i:'mock'})
        #rels.append(i)
    #res = [{obj:vals}]
        res =[{"table":obj,"cols":cols,"rels":rels}]
        return res
    
    def create_tables(self):
        table_dict=globals().update(self.data)
        return table_dict
    
    
    def merges(self):
        d1 = self.data
        d2 = self.json
        merged={}
        for k,v in d1.items():
            try:
                merged.update({v:d2[k]})
            except KeyError:
                pass
        return merged    
    
    def sign_skel(self,l):
        
        for k,v in l.items():
            i=0
            self.d.update({k:{}})
            for listval in v:
                i +=1
                key_l = str(k)+'_'+str(i)
                key =str(k)
                if isinstance(listval,list):
                    new_l={key_l+'_child':listval}
#                    print(new_l,' this is list')
                #d.update(new_l)
                    self.sign_skel(new_l,self.d)
                elif isinstance(listval,dict):
                    new_l2={key+'_child':listval}
#                    print(new_l2,' this is dict')
                    self.d.update(new_l2)
#sign_skel(new_l,d)
                else:
               # print('this is rest')
               # print (d[k], ' this is d[k]')
#                    print ({key:listval},' this is {key:listval}')
                    self.d[k].update({key_l:type(listval)})
        return self.d 
    
    
    def max_depth(self,iter_obj,ii,di):

         list_arr = []
         for i in iter_obj:
             if isinstance(i,list):
                 ii += 1
                 for element in i:
                #print(element,i,type(element))
                     if isinstance(element,list):
                 #   ii += 1
                         list_arr.append(element)
                         print(element,i)

         if (len(list_arr)>0):
       # ii += 1  
             di.append({ii:list_arr})      
             return self.max_depth(list_arr,ii,di)
         else:
             di.append({ii:list_arr})
             return di[-1]    
        

    def same_type(self,iterobj):
        if isinstance(iterobj,list):
            iseq = iter(iterobj)
            if (len(iterobj)==0):
                return type('string')
            elif (len(iterobj)==1): 
                first_type = type(iterobj[0])
                return first_type
            else:    
                first_type = type(next(iseq))
                return first_type if all( (type(x) is first_type) for x in iseq ) else set(type(x) for x in iterobj)
        if isinstance(iterobj,dict):
            pass

    def __len__(self):
        return len(self.coordinate_row)
        
        
    def rest_tables_dict(self,merged):
        depth=[]
        future_dict=[]
        for k,v in merged.items():
            if isinstance(v,list):
                if (list(self.max_depth(v,0,depth).keys())[0]>0):
                
                    future_dict.append({k:self.sign_skel(v)})
                else:
                    if (len(v)>1):
                        try:
                            if(len(self.same_type(v))==1):
                                future_dict.append({k:v})
                            else:
                                if (str in self.same_type):
                                    future_dict.append({k:v})
                                else:
                                    pass
                        except TypeError:
                            print (k,v,type(v))
                    else:
                        future_dict.append({k:v})
            if isinstance(v,dict):
                pass
        return future_dict                          
                                
                            
                            
    
    def add_cols(self,obj_dict):
        for k,v in obj_dict.items():
            for i in v:
                setattr(k,i,Column(String))






f = open('u.json')

u = json.loads(f.read())
f.close()
#uu = u['contacts_deleted']
#ad = Inthago_dev(uu)
#tdicts = ad.create_tables_dict('Contacts_Deleted')
#w = ad.main_table_dict()

ad = Inthago_dev(u)
tdicts = ad.create_tables_dict('User')
t = ad.create_tables()
w = ad.main_table_dict()
m = ad.merges()

for i in w:
    for key,attr in i['cols'].items():
        print("trying to set col "+str(key)+" of table "+str(i['table'])+" with attr "+str(attr))
        setattr(i['table'],str(key),Column(attr))
        print("was set col "+str(key)+" of table "+str(i['table'])+" with attr "+ str(attr))


    for key,attr in i['rels'].items():
       setattr(i['table'],str(key),relationship(ad.data[key],back_populates=str(i['table'].__name__.lower()),cascade="all, delete, delete-orphan"))
       setattr(ad.data[key],str(i['table'].__name__.lower()) ,relationship(str(i['table'].__name__.capitalize()), back_populates=str(key)))
       setattr(ad.data[key],str(i['table'].__name__.lower())+'_id',  Column(Integer, ForeignKey(str(i['table'].__name__.capitalize())+'.id'), nullable=False))
       
#       if isinstance(ad.json[key],dict):
#           nad = Inthago_dev(ad.json[key])
#           nad.create_tables_dict(str(key.capitalize()))
#           nad.create_tables()
#           w.append(nad.main_table_dict())
#       
#       