import pandas as pd
#baraie tabdile "now" be tarikhe shamsi
from persiantools.jdatetime import JalaliDate
import datetime
import csv
import os #to remove some temporary files

#########################################################
root='/users/shahabkiani/desktop/test_project/'


file_not_divided=root+'DATAss_notdivided.csv'

file_divided=root+'DATAss.csv'

file_information=root+'data1.xlsx'
#tarakonesh
#########################################################
df=pd.read_excel(file_information)
list_names=list(df.name)

all_vahed=[]  #hazineie taghsim shode tarakonesh, baraie pardazeshe rahate gozaresh , jolo tar ba etelate taghsim shode por mishe
for  i in range(len(list_names)):
    all_vahed.append([])


def reset_all_vahed(l:list): #por kardane list be tedad vahed ha, jolo tar por mishe
    l.clear()
    for i in range(len(list_names)):
        l.append([])


parking=list(df.parkings)
surface=list(df.area)
sakenin=list(df.residents)
not_divided_data=[]

best_div_for_each_category={'other':'e',('ghabz','avarez'):'e',('ghabz','ab'):'r',('ghabz','bargh'):'r',('ghabz','gas'):'a','nezafat':'e','asansoor':'e','hazine_parking':'p','tamirat':'e','sharj':'r'}    # {...,'category':'default div',...}

def convert_relatedUnits_all_to_numbers(relatedUnits:str): #tabdil input e all be adade vahed baraie method haie badi
    relatedUnits_str = ''
    for i in range(len(sakenin)):
        relatedUnits_str += f',{i+1}'
    relatedUnits_str = relatedUnits_str[1:]
    relatedUnits=relatedUnits_str
    return relatedUnits
#nahve haie taghsim bandi

def e_div(amount:str,relatedUnits:str):         
    if relatedUnits=='all':
        relatedUnits=convert_relatedUnits_all_to_numbers(relatedUnits)
    relatedUnits=relatedUnits.split(',')
    amount_per_num=float(amount)/len(relatedUnits)
    amount_per={}
    for i in relatedUnits:
        amount_per[i]=amount_per_num
    return amount_per

def r_div(amount:str,relatedUnits:str):
    if relatedUnits=='all':
        relatedUnits=convert_relatedUnits_all_to_numbers(relatedUnits)
    relatedUnits = relatedUnits.split(',')
    amount_per={}
    sakenin_kol_relatedUnits=0
    for  i in relatedUnits:
        sakenin_kol_relatedUnits+=sakenin[int(i)-1]
    for i in relatedUnits:
        amount_per[i]=(sakenin[int(i)-1]/sakenin_kol_relatedUnits)*float(amount)
    return amount_per

def a_div(amount:str,relatedUnits:str):
    if relatedUnits=='all':
        relatedUnits=convert_relatedUnits_all_to_numbers(relatedUnits)
    relatedUnits = relatedUnits.split(',')
    amount_per = {}
    surface_kol_relatedUnits=0
    for i in relatedUnits:
        surface_kol_relatedUnits+=surface[int(i)-1]
    for i in relatedUnits:
        amount_per[i]=(surface[int(i)-1]/surface_kol_relatedUnits)*float(amount)
    return amount_per

def p_div(amount:str,relatedUnits:str):
    if relatedUnits=='all':
        relatedUnits=convert_relatedUnits_all_to_numbers(relatedUnits)
    relatedUnits = relatedUnits.split(',')
    amount_per = {}
    parking_kol_relatedUnits=0
    for i in relatedUnits:
        parking_kol_relatedUnits+=parking[int(i)-1]
    for i in relatedUnits:
        amount_per[i]=(parking[int(i)-1]/parking_kol_relatedUnits)*float(amount)
    return amount_per


def reshte_adad_div(amount:str,relatedUnits:str,reshte_adad:str):  ###input be soorate darsad : vahed haie 1,3,6 ba darsade 10-20-70
    if relatedUnits=='all':
        relatedUnits=convert_relatedUnits_all_to_numbers(relatedUnits)
    relatedUnits = relatedUnits.split(',')
    amount_per = {}
    reshte_adad=reshte_adad.split('-')
    for i in relatedUnits:
        amount_per[i]=(float(reshte_adad[relatedUnits.index(i)])/100)*float(amount)
    return amount_per

def portal_userstr_to_div(div:str,relatedUnits:str,amount:str,category:str,subCategory:str): #method baraie entekhabe divtype
    if div=='e':
        return e_div(amount,relatedUnits)

    elif div=='r':
        return r_div(amount,relatedUnits)
    elif div=='p':
        return p_div(amount,relatedUnits)
    elif div=='a':
        return a_div(amount,relatedUnits)
    if div=='default' or div=='d': #peida kardane divtype default
        if category=='ghabz':
            div = best_div_for_each_category[(category,subCategory)] #ghabz tanha category ba subcategory
        else:
            div=best_div_for_each_category[category]
        return portal_userstr_to_div(div,relatedUnits,amount,category,subCategory) #dar in metohd divtype 'd' be (e,r,p,a) mishe va dobare hesab mishe
    else: #age divtype barhasbe darsad bood
        return reshte_adad_div(amount=amount,relatedUnits=relatedUnits,reshte_adad=div)







def append_input(y:list):
    if y[1]=='now':
        #time=f'{datetime.datetime.now()}'.split()[0]  #date like: 2021-1-26     (year-month-day) miladi bood in ;)
        #tabdil be shamsi
        time = JalaliDate.today()
        time = str(time).replace("-", "/")

    else:
        time=y[1].replace("-", "/")
    amount=y[2]
    category=y[3]
    subCategory=y[4]
    responsibleUnit=y[5]
    relatedUnits=y[6]
    div = y[7]
    description_splited=y[8:]
    description=''
    #tabdile list description be string
    for i in description_splited:
        description+=' '+i
    description=description[1:]
    #####
    not_divided_data.append([time,amount,category,subCategory,responsibleUnit,relatedUnits,div,description])
    #####
    if relatedUnits!='all' and len(relatedUnits.split(','))==1: #dar in soorat dashtane divType mani nadare
        all_vahed[int(relatedUnits)-1].append([amount,time,category,subCategory,'NA',description,responsibleUnit])   
    else:
        result=portal_userstr_to_div(div,relatedUnits,amount,category,subCategory) # result yek dict ba moshakhasate tarakonesh taghsim shode
        for i in result:
            all_vahed[int(i) - 1].append([result[i], time, category, subCategory, div, description, responsibleUnit])
    


def save():
    header_csv_file_divided=['vahed','amount','time','category','subCategory','div','description','responsibleUnit']
    try:
        fi=open(file_divided,'r',newline='')
        fi.close()
        #output as a csv file
        fi=open(file_divided,'a',newline='')
        file=csv.writer(fi)
        for i in range(len(all_vahed)):
            for j in all_vahed[i]:
                file.writerow([f'vahed{i+1}']+j)
        fi.close()
    except:
        fi = open(file_divided, 'a', newline='')
        file = csv.writer(fi)
        file.writerow(header_csv_file_divided)
        for i in range(len(all_vahed)):
            for j in all_vahed[i]:
                file.writerow([f'vahed{i + 1}'] + j)
        fi.close()

    
    header_csv_file_notdivided=['date','amount','category','subcategory','resunit','relateunit','divtype','des']
    try:
        fi=open(file_not_divided,'r',newline='')
        fi.close()
        #output as a csv file
        fi=open(file_not_divided,'a',newline='')
        file=csv.writer(fi)
        for i in not_divided_data:
            file.writerow(i)
        fi.close()
    except:
        fi = open(file_not_divided, 'a', newline='')
        file = csv.writer(fi)
        file.writerow(header_csv_file_notdivided)
        for i in not_divided_data:
            file.writerow(i)
        fi.close()
#  some input examples::
# append now 2910000 ghabz ab 3 4,2,3 e descripton
# append now 3000000 ghabz gas 1 all p garmayesh parking
# append now 900 ghabz gas 4 all d hazine in mah
# append 1397-12-20 500 hazine_parking undefined 4 1,4 default
# append now 3000000 ghabz gas 1 all a garmayesh parking
# append 1398-12-13 2910000 ghabz bargh 3 2 a 
# append 1399-12-04 2910000 ghabz bargh 3 2 r 

#gozaresh
####################################################################################################
import csv
import pandas as pd
from matplotlib import pyplot

class gozaresh():
    def taraz_vahed(self,state):

        units_balance = dict()
        # creating keys
        with open(file_divided) as file:
            file.readline()
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if len(row)==1:
                    row=''.join(row).split(",") #to solve some problems reformating creates
                    
                units_balance[row[0]]=0 
        # calculating balances
        with open(file_divided) as file:
            file.readline()
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                
                if len(row)==1:
                    row=''.join(row).split(",") #to solve some problems reformating creates
                #checking the category
                if len(row)==8:#to solve some problems reformating creates
                    if row[3]!="sharj" :
                        units_balance[row[0]]-=float(row[1])
                    else:
                        units_balance[row[0]] += float(row[1])
        #iterating trough the dict
        if state==1: #later used
            return (sum(units_balance.values()))
        else:
            for key in units_balance:
                print("{} : {}".format(key,units_balance[key]))

    def tarikh_tarakonesh(self,start_time:str,end_time:str):
        col_names = ['time', 'amount', 'category', 'subcategory', 'resunit', 'relateunit','divtype','des']

        #tranforming csv to pandas dataframe
        df = pd.read_csv(file_not_divided,
                 skiprows=1,
                 names=col_names,
                 )
        start=start_time.split('-')
        end=end_time.split('-')
        df[['year', 'month', 'day']] = pd.DataFrame([ x.split("/") for x in df['time'].tolist() ])
        df['day'] = df['day'].str.lstrip('0')
        df['month'] = df['month'].str.lstrip('0')
        df['value']=(df['day'].astype('int32')+df['month'].astype('int32')*100+df['year'].astype('int32')*10000)  #to determine value of the date
        df=df.loc[(df['value'] >int(start[2])+int(start[1])*100+int(start[0])*10000 )  #pandas doesnt support shamsi calender because it uses 
                  & (df['value'] <int(end[2])+int(end[1])*100+int(end[0])*10000 )]     #nanoseconds as time units and uses 64bit integers
        df.set_index('value', inplace=True)                                            #so we used a system to filter for time(for some reason,this problem occurs only when uusing csv  :|)
        df.sort_index()
        
        df.drop('year', axis=1, inplace=True)
        df.drop('month', axis=1, inplace=True)
        df.drop('day', axis=1, inplace=True)
                          
        df.to_csv('Tarakonesh ha az {} ta {}.csv'.format(start_time,end_time), sep=',' , encoding='utf-8',index=False)
        
            #print("please close the created csv file")

    class tahlil_hazine:
        def category(self):
            category_cost = dict()
            #creating keys
            with open(file_not_divided) as file:
                file.readline()
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    category_cost[row[2]] = 0
            #calculating cost for each category
            with open(file_not_divided) as file:
                file.readline()
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    category_cost[row[2]] += float(row[1])
            #creating list out of keys and values
            values=list(category_cost.values())
            keys = list(category_cost.keys())
            #creating the piechart
            pyplot.pie([float(v) for v in values], labels=[str(k) for k in keys],
                       autopct=None)
            pyplot.show()
        def subcategory(self,category):
            #like the category part
            subcategory_cost = dict()
            with open(file_not_divided) as file:
                file.readline()
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    if row[2]==category:
                        subcategory_cost[row[3]] = 0
            with open(file_not_divided) as file:
                file.readline()
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    #checking if category is the desired category
                    if row[2] == category:
                        subcategory_cost[row[3]] += float(row[1])
            values=list(subcategory_cost.values())
            keys = list(subcategory_cost.keys())
            pyplot.pie([float(v) for v in values], labels=[str(k) for k in keys],
                       autopct=None)
            pyplot.show()

        def balance(self):
            gozaresh_object = gozaresh()
            print("balance : "+ str(gozaresh_object.taraz_vahed(1))) # 1 is the state of called function. in state 1 the function will return sum of the balance of all units
    class tajmii:
        def vahed(self,entered_vahed_list,start,end,category,subcategory):

            for i in range(len(entered_vahed_list)):
                    entered_vahed_list[i]="vahed"+entered_vahed_list[i]
            
            col_names = ['vahed', 'amount', 'time', 'category', 'subcategory', 'div', 'des', 'res']

            #tranforming csv to pandas dataframe
            df = pd.read_csv(file_divided,
                 skiprows=1,
                 names=col_names,
                 )
            start=start.split('-')
            end=end.split('-')
            #print(df)
            df[['year', 'month', 'day']] = pd.DataFrame([ x.split("/") for x in df['time'].tolist() ])
            df['day'] = df['day'].str.lstrip('0')
            df['month'] = df['month'].str.lstrip('0')
            df['value']=(df['day'].astype('int32')+df['month'].astype('int32')*100+df['year'].astype('int32')*10000)  #to determine value of the date
            df=df.loc[(df['value'] >int(start[2])+int(start[1])*100+int(start[0])*10000 )  #pandas doesnt support shamsi calender because it uses 
                      & (df['value'] <int(end[2])+int(end[1])*100+int(end[0])*10000 )]     #nanoseconds as time units and uses 64bit integers
            df.set_index('value', inplace=True)                                            #so we used a system to filter for time (for some reason,this problem occurs only when uusing csv  :|)
            df.sort_index()
            
            df.drop('year', axis=1, inplace=True)
            df.drop('month', axis=1, inplace=True)
            df.drop('day', axis=1, inplace=True)
            

            try:
                #creating a file to read from
                df.to_csv('temp_result.csv', sep=',', encoding='utf-8')
            except:
                print("Something went wrong, please close all csv files and try again")
            vahed_list=df['vahed'].unique()
            #checking if file is empty
            if len(vahed_list)==0:
                print("hich tarkoneshi dar in tarikh anjam nashode")
                return
            else:
                vahed_dict=dict()
                for element in vahed_list:
                    #checking if the unit is needed
                    if element in entered_vahed_list:
                        vahed_dict[element]=dict()

            #adding the values
            for key in vahed_dict:
                # creating a dict to fill it with time as key and cost as value 
                temp_dict=dict()
                with open('temp_result.csv') as file:
                    file.readline()
                    reader = csv.reader(file, delimiter=',')
                    for row in reader:
                        temp_dict[row[3]] = 0
                with open('temp_result.csv') as file:
                    file.readline()
                    reader = csv.reader(file, delimiter=',')
                    for row in reader:

                        if row[1]==key:
                            if row[3]!="sharj": #checking if category and subcategory match
                                if (row[4]==category or category=="") and (row[5]==subcategory or subcategory==""):
                                    temp_dict[row[3]] += float(row[2])


                    #this is a nested dictinory. the outer dictionary keys are units name and the inner keys are
                    #times with values of cost for that time
                    vahed_dict[key]=temp_dict
            
            for key_vahed in vahed_dict:

                temp_dict=vahed_dict[key_vahed]
                b=0
                temp_list=[]
                for key in temp_dict:
                    #creating data for cumulative graph
                    b+=temp_dict[key]
                    temp_list.append(b)
                #creating plot charts for each unit
                zarib = len(list(temp_dict.keys())) // 10
                fig, ax = pyplot.subplots(1)

                ax.plot(list(temp_dict.keys()), temp_list)
                ax.set_xticks(list(temp_dict.keys())[::zarib])
                ax.set_xticklabels(list(temp_dict.keys())[::zarib], rotation=45)
                ax.locator_params(nbins=10)
                ax.set_ylabel('Hazine ' + category + " " + subcategory)
                ax.set_title(key_vahed)

                pyplot.show()

        def subcategory(self,entered_sub_list,start,end):
            
            #sorting based on required time

            #tranforming csv to pandas dataframe
            col_names = ['vahed', 'amount', 'time', 'category', 'subcategory', 'div', 'des', 'res']

            #tranforming csv to pandas dataframe
            df = pd.read_csv(file_divided,
                 skiprows=1,
                 names=col_names,
                 )
            start=start.split('-')
            end=end.split('-')
            
            df[['year', 'month', 'day']] = pd.DataFrame([ x.split("/") for x in df['time'].tolist() ])
            df['day'] = df['day'].str.lstrip('0')
            df['month'] = df['month'].str.lstrip('0')
            df['value']=(df['day'].astype('int32')+df['month'].astype('int32')*100+df['year'].astype('int32')*10000)  #to determine value of the date
            df=df.loc[(df['value'] >int(start[2])+int(start[1])*100+int(start[0])*10000 )  #pandas doesnt support shamsi calender because it uses 
                      & (df['value'] <int(end[2])+int(end[1])*100+int(end[0])*10000 )]     #nanoseconds as time units and uses 64bit integers
            df.set_index('value', inplace=True)                                            #so we used a system to filter for time(for some reason,this problem occurs only when uusing csv  :|)
            df.sort_index()
            
            df.drop('year', axis=1, inplace=True)
            df.drop('month', axis=1, inplace=True)
            df.drop('day', axis=1, inplace=True)

            #print(df)

            try:
                #creating a file to read from
                df.to_csv('temp_result.csv', sep=',', encoding='utf-8')
            except:
                print("Something went wrong, please close all csv files and try again")
            #ignoring all nan values in datframe
            df=df[df['subcategory'].notna()]
            sub_list=df['subcategory'].unique()
            if len(sub_list)==0:
                print("hich tarkoneshi dar in tarikh anjam nashode ba vahed haie zekr shode tain nashode")
                return
            else:
                sub_dict=dict()
                for element in sub_list:
                    

                    if element in entered_sub_list:
                        sub_dict[element]=dict()
            #creating key based on time
            #like vahed() method
            for key in sub_dict:

                temp_dict=sub_dict[key]
                with open('temp_result.csv') as file:
                    file.readline()
                    reader = csv.reader(file, delimiter=',')
                    for row in reader:
                        temp_dict[row[3]] = 0
                with open('temp_result.csv') as file:
                    file.readline()
                    reader = csv.reader(file, delimiter=',')
                    for row in reader:
                        if row[5]==key:
                            temp_dict[row[3]] += float(row[2])



                    sub_dict[key]=temp_dict
            
            for key_sub in sub_dict:

                temp_dict=sub_dict[key_sub]
                b=0
                temp_list=[]
                for key in temp_dict:
                    #creating data for cumulative graph
                    b+=temp_dict[key]
                    temp_list.append(b)

                pyplot.plot(list(temp_dict.keys()), temp_list)
                zarib = len(list(temp_dict.keys())) // 10
                fig, ax = pyplot.subplots(1)

                ax.plot(list(temp_dict.keys()), temp_list)
                ax.set_xticks(list(temp_dict.keys())[::zarib])
                ax.set_xticklabels(list(temp_dict.keys())[::zarib], rotation=45)
                ax.locator_params(nbins=10)
                ax.set_ylabel('Hazine ' + key_sub)
                ax.set_title(key_sub)

    def takhmin_hazine(self,year):
        col_names = ['time', 'amount', 'category', 'subcategory', 'resunit', 'relunit', 'div', 'des']
        df = pd.read_csv(file_not_divided,
                skiprows=1,
                names=col_names)
        
        
        
        #to calculate sharj
        #removing all other years
        for index, row in df.iterrows():
            temp_string=row[0]
            
            if temp_string[0:4]!=str(year):
                df.drop(index, inplace=True)

        
                
        
        inflation_dict={'90':1.215 , "91":1.3, "92":1.34 , "93":1.15 ,"94":1.119,
                        "95":1.09 , "96":1.09 , "97":1.212 , "98":1.412 ,"99":1 } #no inflation information for year 99
        #removing sharj category
        yearly_cost=df.loc[df['category'] != 'sharj', 'amount'].sum() #ignoring sharj category and calculating sum of others
        
        print("sharj sale bad baraie har mah : " +str(yearly_cost*inflation_dict[str(year)[2:4]]/len(list_names)))


#reformatting
########################################
def reformat(file_not_divided,file_divided):
#reformate file divide shode
    mm=pd.read_excel(file_divided)
    df=pd.DataFrame(mm)
    df.columns=['vahed','amount','time','category','subCategory','div','description','responsibleUnit']
    #taviz bazi az stoona ha
    df.vahed=df.time
    df.time=df.category
    df.amount=df.responsibleUnit
    df.category=df.subCategory
    df.responsibleUnit=''
    df.description=''
    df.time=df.time.str.replace('-','/')
    df.vahed=df.vahed.str.replace('id','vahed')
    df.subCategory=df['div'].astype(str)
    df=df.drop('div',1)
    df['div']=''
    #tavize category ha 
    a=['ghabz','nezafat','asansoor','hazine_parking','tamirat','sharj','other']
    b=['ab','bargh','gas','avarez']                                    
    aa=['Ghabz','nezafat','asansor','parking','tamirat','sharj','other']     # sharj nabud too dataset jadid  
    bb=['Water','bargh','gaz','avarez'] # ghabz avarez ham dare!
    ###
    for i in range(len(a)):
        df['category']=df['category'].str.replace(aa[i],a[i])
        
    for i in range(len(b)):
        df['subCategory']=df['subCategory'].str.replace(bb[i],b[i])                                                                                                          
    df=df.drop('description',1)
    df=df.drop('responsibleUnit',1)
    
    df['description']=''
    df['responsibleUnit']=''

    file_divided_new=file_divided.replace('xlsx','csv') #avaz kardane format be csv chon bishtare barname ba csv kar mikone
    
    
    df.to_csv(file_divided_new,index=False)
    df = pd.read_csv(file_divided_new, #bazi error be khatere reformat pish miomad ke in haleshoon mikone
                 lineterminator='\n')
    df.to_csv(file_divided_new,index=False)


#reformate file divide nashode    
    mm=pd.read_excel(file_not_divided)
    df=pd.DataFrame(mm)
    #taghire bazi sotoonha
    df=df.drop(list(df.columns)[0],1)
    df.date=df.date.str.replace('-','/')
    df=df.drop('id',1)
    df.zirdaste,df.mablagh=df.mablagh,df.zirdaste
    df.daste,df.zirdaste=df.zirdaste,df.daste
    df.rename(columns = {'daste':'amount'}, inplace = True)
    df.rename(columns = {'zirdaste':'category'}, inplace = True)
    df.rename(columns={'mablagh':'subcategory'},inplace=True)
    df['resunit']=''
    #taghir bazi category ha
    a=['ghabz','nezafat','asansoor','hazine_parking','tamirat','sharj','other']
    b=['ab','bargh','gas','avarez']                                    
    aa=['Ghabz','nezafat','asansor','parking','tamirat','sharj','other']     # sharj nabud too excel
    bb=['Water','bargh','gaz','avarez'] # ghabz avarez ham dare!
    ###
    for i in range(len(a)):
        df['category']=df['category'].str.replace(aa[i],a[i])
        
    for i in range(len(b)):
        df['subcategory']=df['subcategory'].str.replace(bb[i],b[i])
        
    def reformate(x): #taghir format related uint
        ans=''
        for i in eval(x):
            ans+=i[2:]+','
        ans=ans[:-1]
        return ans
    
    df['relateunit']=df.name.apply(reformate)
    df=df.drop('name',1)
    df['divtype']=''
    df['des']=''

    file_not_divided_new=file_not_divided.replace('xlsx','csv') #avaz kardane format be csv chon bishtare barname ba csv kar mikone
    
    
    df.to_csv(file_not_divided_new,index=False)
    df = pd.read_csv(file_not_divided_new, #bazi error be khatere reformat pish miomad ke in haleshoon mikone
                 lineterminator='\n')
    df.to_csv(file_not_divided_new,index=False)
    return file_not_divided_new,file_divided_new #baraie taghire masire file ha be csv sakhte shode


#main
########################################
try:
    df_check_format=pd.read_csv(file_divided) #baz kardane file ba har do formate xlsx va csv
    
except:
    
    df_check_format=pd.read_excel(file_divided) 

if df_check_format.columns[0] !='vahed': #check kardane format
                            # !=vahed neshoon dahandeie formate jadide va baiad reformat she.
    file_not_divided,file_divided=reformat(file_not_divided,file_divided)
print('''1.Append
2.Report
3.Help
4.Exit''')
x = int(input('-> '))
while x != 4:

    if x == 1:  # append
        y = input('Tarakonesh -> ')
        append_input(y.split())
        save()
        reset_all_vahed(all_vahed) #pak kardane list tarakonesh taghsim shode
        not_divided_data.clear()

    if x == 3:
        print('''append-date-amount-category-subcategory-responsibleUnit-relatedunits-divtype-description
date:yyyy/mm/dd
amount:10000
category:
        ghabz
        hazine_parking
        nezafat
        asansoor
        tamirat
        sharj
        other
subcategory:
        ab
        gas
        bargh
        avarez
responsibleUnit:2
relatedunits:
        all
        2,3,7
        9
divtype:
        e
        d
        default
        a
        r
        p
        50-20-30 (% for 3 units example)
description:
        <anything>
Example:
    append 1397-01-13 2900000 ghabz bargh 3 2 a
    append 1397-01-28 3000000 ghabz avarez 3 2,4,5,3,8 10-10-20-30-30 bi dalil haminjoori
    
        ''')

    if x == 2:
        print('''1.taraz_vahed
2.tarikh_tarakonesh
3.tahlil_hazine
4.tajmi
5.takhmin_hazine''')
        y = int(input('-> '))

        gozaresh_obj = gozaresh()
        if y == 1:
            gozaresh_obj.taraz_vahed(0)
        if y == 2:
            start = input("start date(ex:1398-1-10,1399-10-10):\n-> ")
            end = input("end date(ex:1398-1-10,1399-10-10):\n-> ")
            gozaresh_obj.tarikh_tarakonesh(start, end)
        if y == 3:
            print('''1.category
            2.subcategory
            3.balance''')
            x = int(input('->'))
            tahlil_hazine_obj = gozaresh_obj.tahlil_hazine()
            if x == 1:
                tahlil_hazine_obj.category()
            if x == 2:
               
                category = 'ghabz'
                tahlil_hazine_obj.subcategory(category)
            if x == 3:
                tahlil_hazine_obj.balance()
        if y == 4:
            print('''1.vahed
            2.subcategory''')
            tajmi_obj = gozaresh_obj.tajmii()
            x = int(input('-> '))
            if x == 1:
                vahed_string = input("which units? ex: 1 4 6 ...\n-> ")
                vahed_list = vahed_string.split()

                start = input("start date(ex:1398-1-10,1399-10-10):\n-> ")
                end = input("end date(ex:1398-1-10,1399-10-10):\n-> ")
                category = input("which category?(empty for all)\n-> ")
                subcategory = input("which subcategory?(empty for all)\n-> ")
                tajmi_obj.vahed(vahed_list, start, end, category, subcategory)
            if x == 2:
                sub_string = input("which subcategory? ex: ab avarez... \n-> ")
                sub_list = sub_string.split()
                start = input("start date(ex:1398-1-10,1399-10-10):\n-> ")
                end = input("end date(ex:1398-1-10,1399-10-10):\n-> ")
                tajmi_obj.subcategory(sub_list, start, end)
        if y == 5:
            year = int(input("year?{yyyy):\n-> "))
            gozaresh_obj.takhmin_hazine(year)

    x = int(input('-> '))







