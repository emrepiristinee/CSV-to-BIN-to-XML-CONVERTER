# -- coding: utf-8 --
import csv
import json


#checks if the command is in correct format
def checkCommand(command):
    flag = True
    if (command[0] == "select"):
        if (len(command) == 11 or len(command) == 15):
            cmmd_len = len(command)
            column_name = command[1].split(",")
            for i in range(len(column_name)):
                if (column_name[i] != "id" and column_name[i] != "name" and column_name[i] != "lastname" and column_name[i] != "email" and column_name[i] != "grade" and column_name[i] != "all"):
                    flag = False
                    break

            if (command[2] == "from" and command[3] == "students" and command[4] == "where" and command[cmmd_len-3] == "order" and command[cmmd_len-2] == "by" and (command[cmmd_len-1] == "asc" or command[cmmd_len-1] == "dsc")):
               
                if(command[5] == "name" or command[5] == "lastname" or command[5] == "email"):
                    if(command[6]!="=" and command[6]!="!="):
                        flag=False
                    
                    command7str = command[7]
                    if(command7str[0] != "'" or command7str[-1] != "'"):
                        flag=False
                
                if (command[5] != "id" and command[5] != "name" and command[5] != "lastname" and command[5] != "email" and command[5] != "grade"):
                    flag = False

                elif (command[6] != "=" and command[6] != "!=" and command[6] != "<" and command[6] != ">" and command[6] != "<=" and command[6] != ">=" and command[6] != "!<" and command[6] != "!>" and command[6] != "and" and command[6] != "or"):
                    flag = False
            else:
                flag=False

            if (len(command) == 15):
                if(command[9] == "name" or command[9] == "lastname" or command[9] == "email"):
                    if(command[10]!="=" and command[10]!="!="):
                          flag=False  
                    
                    command11str = command[11]
                    if(command11str[0] != "'" or command11str[-1] != "'"):
                        flag=False
                          
                if (command[8] != "and" and command[8] != "or"):
                    flag = False
                elif (command[9] != "id" and command[9] != "name" and command[9] != "lastname" and command[9] != "email" and command[9] != "grade"):
                    flag = False

                elif (command[10] != "=" and command[10] != "!=" and command[10] != "<" and command[10] != ">" and command[10] != "<=" and command[10] != ">=" and command[10] != "!<" and command[10] != "!>" and command[10] != "and" and command[10] != "or"):
                    flag = False
        else:
            flag = False

    elif(command[0] == "delete"):
        if (len(command) == 7 or len(command) == 11):
            if(command[4] == "name" or command[4] == "lastname" or command[4] == "email"):
                 if(command[5]!="=" and command[5]!="!="):
                     flag=False 
                     
                 command6str = command[6]
                 if(command6str[0] != "'" or command6str[-1] != "'"):
                     flag=False    
                     
            if (command[1] == "from" and command[2] == "students" and command[3] == "where"):
                if (command[4] != "id" and command[4] != "name" and command[4] != "lastname" and command[4] != "email" and command[4] != "grade"):
                      flag = False                     

                elif (command[5] != "=" and command[5] != "!=" and command[5] != "<" and command[5] != ">" and command[5] != "<=" and command[5] != ">=" and command[5] != "!<" and command[5] != "!>" and command[5] != "and" and command[5] != "or"):
                      flag = False  
                 
            else:
                flag = False

            if (len(command) == 11):
                
                if(command[8] == "name" or command[8] == "lastname" or command[8] == "email"):
                     if(command[9]!="=" and command[9]!="!="):
                         flag=False 
                         
                     command10str = command[10]
                     if(command10str[0] != "'" or command10str[-1] != "'"):
                         flag=False    
                         
                if (command[7] != "and" and command[7] != "or"):
                    flag = False
                         
                elif (command[8] != "id" and command[8] != "name" and command[8] != "lastname" and command[8] != "email" and command[8] != "grade"):
                    flag = False

                elif (command[9] != "=" and command[9] != "!=" and command[9] != "<" and command[9] != ">" and command[9] != "<=" and command[9] != ">=" and command[9] != "!<" and command[9] != "!>" and command[9] != "and" and command[9] != "or"):
                    flag = False
        else:
             flag=False

    
    elif (command[0] == "insert" and len(command)==4 ):
        
        values_control = str(command[3])
        if(values_control[6]=="(" and values_control[-1]==")" ):
            values_str = values_control[7:-1].split(",")
            
            if (command[1] != "into" and command[2] != "students" and values_control[0:6] != "values" and len(values_str) != 5):               
                flag = False
                
        else:
            flag=False
        

    else:
        flag = False

    return flag

#finds command type (select/insert/delete)
def findType(command, sorted_dict):
    
    output_dict={}
 
    if (command[0] == "select"):
        select(command, sorted_dict)
        output_dict= sorted_dict 
        
    elif (command[0] == "insert"):
       output_dict=  insert(command, sorted_dict)

    elif (command[0] == "delete"):
       output_dict=  delete(command, sorted_dict)
        
    return output_dict

#select operation
def select(command, sorted_dict):    
    command[7] = command[7].replace("'", "")
    printOut = ""
    printInfo = {}
    column_name = command[1].split(",")
    
    if(command[5]=="grade"):
        for key in sorted_dict:
            if(command[6]=='='):
                if(sorted_dict[key]['grade'] == command[7]):
                   printOut += selectOutput(key,column_name, sorted_dict) #printOut= holds selected data as string
                   printInfo[key] = getInfo(key, sorted_dict) #printInfo= holds selected data as dictionary
                  
            elif(command[6]=='!='):
                if( sorted_dict[key]['grade'] != command[7]):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='<'):
                if( int(sorted_dict[key]['grade']) < int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='>'):
                if( int(sorted_dict[key]['grade']) > int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='<=' or command[6]=='!>'):
                if( int(sorted_dict[key]['grade']) <= int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='>=' or command[6]=='!<'):
                if(int(sorted_dict[key]['grade']) >= int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)
     
                    
    elif(command[5] == "name" or command[5] == "lastname" or command[5] == "email"):
        for key in sorted_dict:
            if(command[6]=='='):
                if(sorted_dict[key][command[5]] == command[7]):
                   printOut += selectOutput(key, column_name, sorted_dict)
                   printInfo[key] = getInfo(key, sorted_dict)
                  
            elif(command[6]=='!='):
                if(sorted_dict[key][command[5]] != command[7]):
                    printOut += selectOutput(key, column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)
                    
    elif(command[5] == "id"):
        for key in sorted_dict:
            if(command[6]=='='):
                if(key == int(command[7])):
                   printOut += selectOutput(key,column_name, sorted_dict)
                   printInfo[key] = getInfo(key, sorted_dict)
                  
            elif(command[6]=='!='):
                if(key != int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='<'):
                if( key < int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='>'):
                if(key > int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='<=' or command[6]=='!>'):
                if(key <= int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[6]=='>=' or command[6]=='!<'):
                if(key >= int(command[7])):
                    printOut += selectOutput(key,column_name, sorted_dict)
                    printInfo[key] = getInfo(key, sorted_dict)
                    
    
                    
    printOutWith15 = "" #If command has 15 elements, string to be sent to selectOutput
    if(len(command) == 15):
            command[11] = command[11].replace("'", "")
            
            #if there is an "and" in command
            if(command[8] == "and"):
                    if(command[9]=="grade"):
                        for key in printInfo:
                            if(command[10]=='='):
                                if(sorted_dict[key]['grade'] == command[11]):
                                   printOutWith15 += selectOutput(key,column_name, sorted_dict)
                                  
                            elif(command[10]=='!='):
                                if( sorted_dict[key]['grade'] != command[11]):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='<'):
                                if( int(sorted_dict[key]['grade']) < int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='>'):
                                if( int(sorted_dict[key]['grade']) > int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='<=' or command[10]=='!>'):
                                if( int(sorted_dict[key]['grade']) <= int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='>=' or command[10]=='!<'):
                                if(int(sorted_dict[key]['grade']) >= int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)
                     
                                    
                    elif(command[9] == "name" or command[9] == "lastname" or command[9] == "email"):
                        for key in printInfo:
                            if(command[10]=='='):
                                if(sorted_dict[key][command[9]] == command[11]):
                                   printOutWith15 += selectOutput(key, column_name, sorted_dict)
                                  
                            elif(command[10]=='!='):
                                if(sorted_dict[key][command[9]] != command[11]):
                                    printOutWith15 += selectOutput(key, column_name, sorted_dict)
                                    
                    elif(command[9] == "id"):
                        for key in printInfo:
                            if(command[10]=='='):
                                if(key == int(command[11])):
                                   printOutWith15 += selectOutput(key,column_name, sorted_dict)
                                  
                            elif(command[10]=='!='):
                                if(key != int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='<'):
                                if( key < int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='>'):
                                if(key > int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='<=' or command[10]=='!>'):
                                if(key <= int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)

                            elif(command[10]=='>=' or command[10]=='!<'):
                                if(key >= int(command[11])):
                                    printOutWith15 += selectOutput(key,column_name, sorted_dict)
                                    
            #if there is an "or" in command
            elif (command[8] == "or"):
                if(command[9]=="grade"):
                    for key in sorted_dict:
                        if(command[10]=='='):
                            if(sorted_dict[key]['grade'] == command[11]):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)
                              
                        elif(command[10]=='!='):
                            if( sorted_dict[key]['grade'] != command[11]):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='<'):
                            if( int(sorted_dict[key]['grade']) < int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='>'):
                            if( int(sorted_dict[key]['grade']) > int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='<=' or command[10]=='!>'):
                            if( int(sorted_dict[key]['grade']) <= int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='>=' or command[10]=='!<'):
                            if(int(sorted_dict[key]['grade']) >= int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)
                 
                                
                elif(command[9] == "name" or command[9] == "lastname" or command[9] == "email"):
                    for key in sorted_dict:
                        if(command[10]=='='):
                            if(sorted_dict[key][command[9]] == command[11]):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)
                              
                        elif(command[10]=='!='):
                            if(sorted_dict[key][command[9]] != command[11]):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)
                                
                elif(command[9] == "id"):
                    for key in sorted_dict:
                        if(command[10]=='='):
                            if(key == int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)
                              
                        elif(command[10]=='!='):
                            if(key != int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='<'):
                            if( key < int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='>'):
                            if(key > int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='<=' or command[10]=='!>'):
                            if(key <= int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)

                        elif(command[10]=='>=' or command[10]=='!<'):
                            if(key >= int(command[11])):
                               printOut += selectOutput_OR(key,column_name, sorted_dict, printInfo)           
                
    print_SelectOutput(command, printOut, printOutWith15)
                           

def print_SelectOutput(command, printOut, printOutWith15):
          
    if(len(command) == 11):
        printOut = printOut.split(",")
        if(command[-1] == "asc"):
            for i in range(len(printOut)-1):
                print(printOut[i])
            
        elif(command[-1] == "dsc"):
            for i in range(len(printOut)):
                print(printOut[-(i+1)])
                
    elif (len(command) == 15):
        if(command[8] == "and"):
            printOutWith15 = printOutWith15.split(",")
            if(command[-1] == "asc"):
                for i in range(len(printOutWith15)-1):
                    print(printOutWith15[i])
                
            elif(command[-1] == "dsc"):
                for i in range(len(printOutWith15)):
                    print(printOutWith15[-(i+1)])
                    
        elif(command[8] == "or"):
            printOut = printOut.split(",")
            if(command[-1] == "asc"):
                for i in range(len(printOut)-1):
                    print(printOut[i])
                
            elif(command[-1] == "dsc"):
                for i in range(len(printOut)):
                    print(printOut[-(i+1)])
    
    
#creates output of select func with AND#creates output of select func with and
def selectOutput(key, column_name, sorted_dict):
    out_str=""
    for i in range(len(column_name)):   
        if(column_name[i]=="id"):
            out_str+= str(key) +" "
        else:   
            out_str+= sorted_dict[key][column_name[i]] +" "
                                       
    return out_str + ","

#creates output of select func with OR
def selectOutput_OR(key, column_name, sorted_dict, printInfo):
    out_str=""
    flag=True
    for a in printInfo:
        if(key==a):
            flag= False
    if(flag):  
        for i in range(len(column_name)):   
            if(column_name[i]=="id"):
                out_str+= str(key) +" "
            else:   
                out_str+= sorted_dict[key][column_name[i]] +" "                                  
    return out_str + ","    
    

#insert operation
def insert(command, sorted_dict):
    
    values_control = str(command[3])
    values_str = values_control[7:-1].split(",")
    
    sorted_dict[int(values_str[0])]= {'name': values_str[1], 'lastname': values_str[2], 'email': values_str[3], 'grade': values_str[4]}
    print(values_str[0]+" "+values_str[1]+" "+values_str[2]+" "+values_str[3]+" "+values_str[4])
    
  
    return sorted_dict
    
#delete operation 
def delete(command, sorted_dict):
    command[6] = command[6].replace("'", "")
    printInfo = {}
    
    if(command[4]=="grade"):
        for key in sorted_dict:
            if(command[5]=='='):
                if(sorted_dict[key]['grade'] == command[6]):                   
                   printInfo[key] = getInfo(key, sorted_dict) #printInfo= holds matching data as dictionary
                  
            elif(command[5]=='!='):
                if( sorted_dict[key]['grade'] != command[6]):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='<'):
                if( int(sorted_dict[key]['grade']) < int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='>'):
                if( int(sorted_dict[key]['grade']) > int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='<=' or command[6]=='!>'):
                if( int(sorted_dict[key]['grade']) <= int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='>=' or command[6]=='!<'):
                if(int(sorted_dict[key]['grade']) >= int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)
     
                    
    elif(command[4] == "name" or command[4] == "lastname" or command[4] == "email"):
        for key in sorted_dict:
            if(command[5]=='='):
                if(sorted_dict[key][command[4]] == command[6]):
                   printInfo[key] = getInfo(key, sorted_dict)
                  
            elif(command[5]=='!='):
                if(sorted_dict[key][command[4]] != command[6]):
                    printInfo[key] = getInfo(key, sorted_dict)
                    
    elif(command[4] == "id"):
        for key in sorted_dict:
            if(command[5]=='='):
                if(key == int(command[6])):
                   printInfo[key] = getInfo(key, sorted_dict)
                  
            elif(command[5]=='!='):
                if(key != int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='<'):
                if( key < int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='>'):
                if(key > int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='<=' or command[5]=='!>'):
                if(key <= int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)

            elif(command[5]=='>=' or command[5]=='!<'):
                if(key >= int(command[6])):
                    printInfo[key] = getInfo(key, sorted_dict)
    
    
    delete_dict={}  #If command has 11 elements, holds the data of second condition(and/or)
    if(len(command) == 11):
           command[10] = command[10].replace("'", "")
           if(command[7] == "and"):
                   if(command[8]=="grade"):
                       for key in printInfo:
                           if(command[9]=='='):
                               if(sorted_dict[key]['grade'] == command[10]):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                                   
                           elif(command[9]=='!='):
                               if( sorted_dict[key]['grade'] != command[10]):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='<'):
                               if( int(sorted_dict[key]['grade']) < int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='>'):
                               if( int(sorted_dict[key]['grade']) > int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='<=' or command[9]=='!>'):
                               if( int(sorted_dict[key]['grade']) <= int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='>=' or command[9]=='!<'):
                               if(int(sorted_dict[key]['grade']) >= int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                    
                                   
                   elif(command[8] == "name" or command[8] == "lastname" or command[8] == "email"):
                       for key in printInfo:
                           if(command[9]=='='):
                               if(sorted_dict[key][command[8]] == command[10]):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                                 
                           elif(command[9]=='!='):
                               if(sorted_dict[key][command[8]] != command[10]):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                                   
                   elif(command[8] == "id"):
                       for key in printInfo:
                           if(command[9]=='='):
                               if(key == int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                                 
                           elif(command[9]=='!='):
                               if(key != int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='<'):
                               if( key < int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='>'):
                               if(key > int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='<=' or command[9]=='!>'):
                               if(key <= int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)

                           elif(command[9]=='>=' or command[9]=='!<'):
                               if(key >= int(command[10])):
                                   delete_dict[key]= getInfo(key, sorted_dict)
                                   
                   
           elif (command[7] == "or"):
               if(command[8]=="grade"):
                   for key in sorted_dict:
                       if(command[9]=='='):
                           if(sorted_dict[key]['grade'] == command[10]):                              
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)
                               
                       elif(command[9]=='!='):
                           if( sorted_dict[key]['grade'] != command[10]):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='<'):
                           if( int(sorted_dict[key]['grade']) < int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='>'):
                           if( int(sorted_dict[key]['grade']) > int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='<=' or command[9]=='!>'):
                           if( int(sorted_dict[key]['grade']) <= int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='>=' or command[9]=='!<'):
                           if(int(sorted_dict[key]['grade']) >= int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)
                
                               
               elif(command[8] == "name" or command[8] == "lastname" or command[8] == "email"):
                   for key in sorted_dict:
                       if(command[9]=='='):
                           if(sorted_dict[key][command[8]] == command[10]):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)
                             
                       elif(command[9]=='!='):
                           if(sorted_dict[key][command[8]] != command[10]):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)
                               
               elif(command[8] == "id"):
                   for key in sorted_dict:
                       if(command[9]=='='):
                           if(key == int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)
                             
                       elif(command[9]=='!='):
                           if(key != int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='<'):
                           if( key < int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='>'):
                           if(key > int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='<=' or command[9]=='!>'):
                           if(key <= int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)

                       elif(command[9]=='>=' or command[9]=='!<'):
                           if(key >= int(command[10])):
                               delete_dict[key]= tempDeleteDict(key, sorted_dict, delete_dict)                          
                               
    if(len(command)==7):     
         print(printInfo)
         for key in printInfo:
             sorted_dict.pop(key)
                
             
    elif(len(command)==11):
         print(delete_dict)
         for key in delete_dict:            
             sorted_dict.pop(key)
                     
    return sorted_dict

# if the person hasn't been selected, adds it to delete_dict(for OR)
def tempDeleteDict(key,sorted_dict,delete_dict):
    flag=True
    d_dict = {}
    for a in delete_dict:
        if(key==a):
            flag= False           
    if(flag):
        d_dict[key] = getInfo(key, sorted_dict)
    return d_dict
              
def getInfo(key, sorted_dict):
    temp_dict = {'name': sorted_dict[key]['name'], 'lastname': sorted_dict[key]['lastname'], 'email': sorted_dict[key]['email'], 'grade': sorted_dict[key]['grade']}
    return temp_dict
     

#reads csv file and writes into dictionary
def CSVtoDict():
    with open('students.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        tempDict={}

        #got index names in first line
        for line in csv_reader:
            strline = ''.join(line)
            listTitle = strline.split(";")
            break

        
        for line2 in csv_reader:
            thisdict = {}
            strline2 = ''.join(line2).lower()
            listInfo = strline2.split(";")
            for a in range(len(listInfo)):
                thisdict[listTitle[a]] = listInfo[a]
                if (a == len(listInfo) - 1):
                    break
            tempDict[int(listInfo[0])] = thisdict
        
        #data sorted by id num
        myKeys= sorted(tempDict.keys())
        sorted_dict = {i: tempDict[i] for i in myKeys}

        return sorted_dict



def main():
    sorted_dict = CSVtoDict()  
    while (True):
        command = input("\nEnter your command: ").lower()
        
        if(command=="exit"):
            print("Exit.")
            with open('Output.json', 'w') as json_file:
              json.dump(sorted_dict, json_file, indent = 4, ensure_ascii=False)
            break
        
        else:
            command = command.split(" ")
            flag = checkCommand(command) #check user input

            if(flag==False):
                print("Invalid command type.")
                
            else:
               sorted_dict = findType(command, sorted_dict) #operations

    
main()
