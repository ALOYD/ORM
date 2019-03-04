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
         if (isinstance(value, list) and any((list, dict in types))):
             rest_tables = str(key)
             attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
             create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
             print(create_classes, '\n', rest_tables, '\n')
         elif (isinstance(value, dict) and any((list, dict in types))):
             try:
                 if (len(types) == 1 and types[0] is list):
                     for k, v in value.items():
                         rest_tables = str(key) + '__' + str(k)
                         attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
                         create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
                         print(create_classes, '\n', rest_tables, '\n')
                 else:
                     rest_tables = str(key)
                     attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
                     create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
                     print(create_classes, '\n', rest_tables, '\n')

             except TypeError:
                if (len(types) == 1 and list(types)[0] is list):
                    for k, v in value.items():
                         rest_tables = str(key) + '__' + str(k)
                         attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
                         create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
                         print(create_classes, '\n', rest_tables, '\n')
                else:
                     rest_tables = str(key)
                     attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
                     create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
                     print(create_classes, '\n', rest_tables, '\n')
                

      self.data.update(create_classes)


    def main_table_dict(self):
#        types={"<class 'str'>":"String","<class 'int'>":"Integer"}
        obj = set(self.data) - set(self.json)
        print('obj ini - ',obj)
        b = list()
        for k in self.data.keys():
            a = list(k.split('__'))
            if len(a) > 1:
                b.append(k)
        d = b
        print('b is ',b)
        print('d is ',d)
        for i in b:
            obj.remove(i)
        print('obj minus b - ',obj)
        obj =  self.data.get(list(obj)[0])


        print('first element of obj ',obj)
#        backpop = str(list(set(self.data) - set(self.json))[0])
        backpop =obj.__name__.lower()
        val_cols = list(set(self.json) - set(self.data))#Columns
#        cols = []
        cols = {}

        print('val_cols is ',val_cols)
        b = set()
        js_update = {}
        for k in self.data.keys():

            a = list(k.split('__'))
            if len(a) > 1:
                if a[0] in js_update:
                    #                js_update[a[0]].append(k)
                    js_update[a[0]].append({k: self.json[a[0]][a[1]]})
                else:
                    #                js_update[a[0]] = [k]
                    js_update[a[0]] = [{k: self.json[a[0]][a[1]]}]
                b.add(a[0])
        print('b set is ',b)
        c = list(b)


        print('c is ')
        val_cols = [x for x in val_cols if x not in c]
        print('val_cols without c is ', val_cols)
        for i in val_cols:
            cols.update({i:self.types[str(type(i))]})
#            if isinstance(i,list):
#                if (len(i)<=1):
#                    cols.update({i})
#        val_rels = list(set(self.json) - set(val_cols))
        val_rels = list((set(self.json) - set(val_cols)- set(c)) ^ set(d))
        print('var_rels is ', val_rels)
        rels = {}
        for i in val_rels:
            print(backpop.lower())
#            rels.update({i:relationship('"'+str(i)+'"',back_populates="'"+backpop.lower()+"'",cascade="all, delete, delete-orphan")})
            rels.update({i:'mock'})
        #rels.append(i)
    #res = [{obj:vals}]
        res ={"table":obj,"cols":cols,"rels":rels}


        for k, v in js_update.items():
            del u[k]
            for i in v:
                u.update(i)
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
            iseq = iter(iterobj.values())
            if (len(iterobj)==0):
                return type('string')
            elif (len(iterobj)==1):
                first_type = type(iterobj[0])
                return first_type
            else:
                first_type = type(next(iseq))
                return first_type if all( (type(x) is first_type) for x in iseq ) else set(type(x) for x in iterobj)


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
u.update({'orders_dist_stats_budik': {'acc_budik': -107.15
                                      , 'this_will_burn':{'ouch':1,'ohhhh':2}
                                      , 'avg_budik': 55.47
                                      , 'var_budik': 53.58}})
#uu = u['contacts_deleted']
#ad = Inthago_dev(uu)
#tdicts = ad.create_tables_dict('Contacts_Deleted')
#w = ad.main_table_dict()

ad = Inthago_dev(u)
tdicts = ad.create_tables_dict('User')
t = ad.create_tables()
w = list()
w.append( ad.main_table_dict())
m = ad.merges()
w[0].update({'data':ad.data,'json':ad.json})
ini_w = 0
for n,i in  enumerate(w):
    for key,attr in i['cols'].items():
        print("trying to set col "+str(key)+" of table "+str(i['table'])+" with attr "+str(attr))
        setattr(i['table'],str(key),Column(attr))
        print("was set col "+str(key)+" of table "+str(i['table'])+" with attr "+ str(attr))

    print("------------- start of " + str(n) + ' rels------------------')
    for key,attr in i['rels'].items():
       print('') 
       print("<><><><><><><><><><><><><><><><><><><>")
       print("<><><><><><><><><><><><><><><><><><><>")
       print("<><><><><><><><><><><><><><><><><><><>")
       setattr(i['table'],str(key),relationship(i['data'][key],back_populates=str(i['table'].__name__.lower()),cascade="all, delete, delete-orphan"))
       print("""setattr({},str({}),relationship({},back_populates=str({}.__name__.lower()),cascade="all, delete, delete-orphan"))""".format(i['table'],key,i['data'][key],i['table']))
       print("=====================================")
       setattr(i['data'][key],str(i['table'].__name__.lower()) ,relationship(str(i['table'].__name__.capitalize()), back_populates=str(key)))
       print("""setattr({},str({}.__name__.lower()) ,relationship(str(i['table'].__name__.capitalize()), back_populates=str({})))""".format(i['data'][key],i['table'],i['table'],key))
       print("=====================================")
       setattr(i['data'][key],str(i['table'].__name__.lower())+'_id',  Column(Integer, ForeignKey(str(i['table'].__name__.capitalize())+'.id'), nullable=False))
       print("""setattr({},str({}.__name__.lower())+'_id',  Column(Integer, ForeignKey(str({}.__name__.capitalize())+'.id'), nullable=False))""".format(i['data'][key],i['table'],i['table'])) 
       print('')
       print('')
       print('')
       
       if isinstance(i['json'][key],dict):
           print('')
           print('')
           print("^^^^^^^^^ bingo it is json of " + str(n) + " key - "+ key +"^^^^^^^^^^^^^")
           print('')
           
           print('')
           nad = None
           nad = Inthago_dev(i['json'][key])
           print("current data is {} and json {}" .format(nad.data, i['json'][key]))
           print("=====================================")
           print("nad = Inthago_dev({})".format(i['json'][key]))
           print("=====================================")
           nad.create_tables_dict(str(key.capitalize()))
           print("nad.create_tables_dict(str({}))".format(key.capitalize()))
           print("=====================================")
           print('')
           print("#extra we need to know what appeared in new data" + str(nad.data))
           print("=====================================")   
           nad.create_tables()
           print("tables created")
           print("================ now len before w append is " + str(len(w) )+ " =====================")
           w.append(nad.main_table_dict())
           print("w.append(nad.main_table_dict())", w[n+1] )
           print("================ now len after w append is " + str(len(w) )+ " =====================")
          
           print("=====================================")
           print('')
           print(" this is w after append {}".format(w[n+1]))
           print('')
           w[len(w) -1  ].update({'data':nad.data,'json':i['json'][key]})
           print("w[{}].update({})".format(str(ini_w),{'data':nad.data,'json':i['json'][key]}))
           print('')
           print(" this is w after UPDATE {}".format(w[n+1]))
           ini_w += 1
           
    print("******************end of " + str(n) + " rels ***************")
           

#
#           
##for i in w:
##    for key,attr in i['rels'].items():
##            
##       print("<><><><><><><><><><><><><><><><><><><>")
##       print("<><><><><><><><><><><><><><><><><><><>")
##       print("<><><><><><><><><><><><><><><><><><><>")
##       print("""setattr({},str({}),relationship({},back_populates=str({}.__name__.lower()),cascade="all, delete, delete-orphan"))""".format(i['table'],key,i['data'][key],i['table']))
##       print("=====================================")
##       print("""setattr({},str({}.__name__.lower()) ,relationship(str(i['table'].__name__.capitalize()), back_populates=str({})))""".format(i['data'][key],i['table'],i['table'],key))
##       print("=====================================")
##       print("""setattr({},str({}.__name__.lower())+'_id',  Column(Integer, ForeignKey(str({}.__name__.capitalize())+'.id'), nullable=False))""".format(i['data'][key],i['table'],i['table']))           
##           #
## def main_table_dict(data,json):
##     types={"<class 'str'>":"String","<class 'int'>":"Integer"}
##     obj = set(data) - set(json)
##     obj =  data.get(list(obj)[0])
##     backpop = str(list(set(data) - set(json))[0])
##     backpop =obj.__name__.lower()
##     val_cols = list(set(json) - set(data))  #Columns
##     cols = []
##     cols = {}
##     for i in val_cols:
##         cols.update({i:types[str(type(i))]})
##         if isinstance(i,list):
##              if (len(i)<=1):
##                  cols.update({i})
##     val_rels = list(set(json) - set(val_cols))
##     rels = {}
##     for i in val_rels:
##         print(backpop.lower())
##         rels.update({i:relationship('"'+str(i)+'"',back_populates="'"+backpop.lower()+"'",cascade="all, delete, delete-orphan")})
##         rels.update({i:'mock'})
##     res =[{"table":obj,"cols":cols,"rels":rels}]
##     return res
## #
## #
##
#def same_type(iterobj):
#    if isinstance(iterobj,list):
#        iseq = iter(iterobj)
#        if (len(iterobj)==0):
#            return type('string')
#        elif (len(iterobj)==1):
#            first_type = type(iterobj[0])
#            return first_type
#        else:
#            first_type = type(next(iseq))
#            return first_type if all( (type(x) is first_type) for x in iseq ) else set(type(x) for x in iterobj)
#    if isinstance(iterobj,dict):
#        iseq = iter(iterobj.values())
#        if (len(iterobj)==0):
#            return type('string')
#        elif (len(iterobj)==1):
#            first_type = type(iterobj[0])
#            return first_type
#        else:
#            first_type = type(next(iseq))
#            return first_type if all( (type(x) is first_type) for x in iseq ) else set(type(x) for x in iterobj)
#
#
#def create_tables_dict(data,json ,main_table_name):
#    create_classes = {}
#    main_table_name = main_table_name
#    main_table = str(main_table_name).capitalize()
#    #      attr_dict = {'__tablename__':main_table.lower(),'id': Column(Integer, primary_key=True), '__table_args__':{'extend_existing': True} }
#    attr_dict = {'__tablename__': main_table.capitalize(), 'id': Column(Integer, primary_key=True),
#                 '__table_args__': {'extend_existing': True}}
#    create_classes[main_table] = type('%s' % main_table, (Bases,), attr_dict)
#    print(create_classes, '\n', main_table, '\n')
#    for key, value in json.items():
#        print('adhasjkhdashdasl!!!!!!!!!', value, type(value), same_type(value))
#        types = same_type(value)
#        ll = []
#        if isinstance(types, type):
#
#            ll.append(types)
#            types = ll
#        else:
#            types = types
##        if ((isinstance(value, list) and any((list, dict in types))) or isinstance(value, dict)):
#        if (isinstance(value, list) and any((list, dict in types))):    
#            rest_tables = str(key)
#            attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
#            create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
#            print(create_classes, '\n', rest_tables, '\n')
#        elif(isinstance(value, dict) and any((list, dict in types))):
#            if (len(types) == 1 and types[0] is list ):
#                for k,v in value.items():
#                    rest_tables = str(key)+'__'+str(k)
#                    attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
#                    create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
#                    print(create_classes, '\n', rest_tables, '\n')
#            else :
#                rest_tables = str(key)
#                attr_dict = {'__tablename__': rest_tables.capitalize(), 'id': Column(Integer, primary_key=True)}
#                create_classes[rest_tables] = type('%s' % rest_tables.capitalize(), (Bases,), attr_dict)
#                print(create_classes, '\n', rest_tables, '\n')
#                    
#                
##asdasd
#    data.update(create_classes)
#    
#    
##underline = '\33[4m' 
##blue = '\x1b[6;30;46m' 
##pink =   '\x1b[7;33;40m'            
##end  =    '\x1b[0m'        
##
##print('<><><><><><><>START<><><><><><><><><><>')                
##for key, value in u.items():
##    print(underline +  str(key) + end ,blue + str(value) + end, '\x1b[6;30;42m' + str(type(value))+end, pink + str(same_type(value)) + end)
##
##    types = same_type(value)
##    lld = {}
##    ll = []
##    if isinstance(types, type):
##        ll.append(types)
##        lld.update({key:types})
##        types = ll
##    else:
##        types = types
##    if (isinstance(value, list) ): 
##        print('list --- ', key,'ll = ' + str(ll),'types = '+ str(types))
##    elif(isinstance(value, dict) ):
##        if (len(types) == 1 and types[0] is list ):
##            print('HERE IT IS ')
##        else:
##            pass
##        print('dict --- ', key,'ll = ' + str(ll),'types = '+ str(types))
##    print('<><><><><><><>END<><><><><><><><><><>')
##    print('                                  ')
##    print('                                  ')    
##    print('                                  ')    
##    print('<><><><><><><>START<><><><><><><><><><>')
#
#def main_table_dict(data,json):
#    types={"<class 'str'>":"String","<class 'int'>":"Integer"}
#    obj = set(data) - set(json)
#    b = list()
#    for k in data.keys():
#    
#        a = list(k.split('__'))
#        if len(a) > 1:
#
#                b.append(k)
#    d= b            
#    for i in b:
#        obj.remove(i)
#    obj =  data.get(list(obj)[0])
#
#    backpop =obj.__name__.lower()
#    val_cols = list(set(json) - set(data))#Columns
#
#    cols = {}
#
#    b = set()
#    js_update = {}
#    for k in data.keys():
#    #js_update.update({k:[]})
#        a = list(k.split('__'))
#        if len(a) > 1:
#            if a[0] in js_update:
##                js_update[a[0]].append(k)
#                js_update[a[0]].append({k:u[a[0]][a[1]]})
#            else:
##                js_update[a[0]] = [k]
#                js_update[a[0]] = [{k:u[a[0]][a[1]]}]
#            b.add(a[0])
#
#    c = list(b)
#
#    val_cols = [x for x in val_cols if x not in c]
#    for i in val_cols:
#        cols.update({i:types[str(type(i))]})
#
#    val_rels = list((set(json) - set(val_cols)- set(c)) ^ set(d))
##    val_rels.append(d)
#    rels = {}
#    for i in val_rels:
#        print(backpop.lower())
#
#        rels.update({i:'mock'})
#
#    res =[{"table":obj,"cols":cols,"rels":rels}]
#    for k,v in js_update.items():
#        del u[k]
#        for i in v:
#            u.update(i)
#    return res
#    
##data_test = {}    
##create_tables_dict(data_test,u,'USIK_PAY_ATTENTION')    
##data = data_test   
##ww = main_table_dict(data,u)
###b = set()
###js_update = {}
###for k,v in data.items():
###    #js_update.update({k:[]})
###    a = list(k.split('__'))
###    if len(a) > 1:
###        if a[0] in js_update:
###            js_update[a[0]].append({k:json[a[0]][a[1]]})
###        else:
###            js_update[a[0]] = [{k:json[a[0]][a[1]]}]
###        b.add(a[0])
###
###c = list(b)    