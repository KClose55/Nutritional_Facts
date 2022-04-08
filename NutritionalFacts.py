import numpy as np
import pandas as pd
import os #view folder contents
from os import system, name 
import shelve
import openpyxl as op
import excel2img
from PIL import Image

#turn off SettingWithCopy warning
pd.options.mode.chained_assignment = None
#nutrient columns
df = pd.read_excel('bakingMAIN.xlsx', index_col='Unnamed: 0')
#ingredient columns
df2 = pd.read_excel('bakingTRANSPOSE.xlsx', index_col='Unnamed: 0')
#daily values
dfdv = pd.read_excel('dailyvalue.xlsx',index_col='nutrient')
#nutrition facts label
dfnf = op.load_workbook('nftemplate.xlsx')
#cost library
s=shelve.open('recipes.db')
try:
    dfct=s['recipes_cost_library']
except KeyError:
    dfct=pd.read_excel('costtemplate.xlsx', index_col='Unnamed: 0')
finally:
    s.close()
#user's personal cost library
s=shelve.open('recipes.db')
try:
    dfct_user=s['recipes_cost_library_user']
except KeyError:
    dfct_user=pd.read_excel('costtemplate.xlsx', index_col='Unnamed: 0')
finally:
    s.close()
#recipe costs library
s=shelve.open('recipes.db')
try:
    dfcr=s['recipes_costs']
except KeyError:
    dfcr=pd.read_excel('recipe_Costs_temp.xlsx', index_col='recipe')
finally:
    s.close()

#different portion sizes used to ensure 2 word entry not mistake when entering recipe
portion_list=['lb','pound','pounds','fl oz', 'fluid ounce', 'fluid ounces', 'cup', 'cups', 'c', 'gram', 'grams', 'g', 'teaspoon', 'teaspoons', 'tablespoon', 'tablespoons', 'tsp', 'tbsp', 'oz', 'ounce', 'ounces']

#gram conversion dict
gram_conv_dict={'oz':28.34952,'lb':453.59237,'ounce':28.34952,'pound':453.59237,'ounces':28.34952,'pounds':453.59237 }

#saved outside any definitions for callback 
s=shelve.open('recipes.db')
try:
    recipe_book=s['recipes_book']
except KeyError:
    recipe_book={}
finally:
    s.close()
    
s=shelve.open('recipes.db')
try:
    recipe_book_user=s['recipes_user']
except KeyError:
    recipe_book_user={}
finally:
    s.close()

s=shelve.open('recipes.db')
try:
    recipe_book_directions=s['recipes_directions']
except KeyError:
    recipe_book_directions={}
finally:
    s.close()

s=shelve.open('recipes.db')
try:
    recipe_dv_dict=s['recipes_dv_dict']
except KeyError:
    recipe_dv_dict={}
finally:
    s.close()

s=shelve.open('recipes.db')
try:
    recipe_nf_dict=s['recipes_nf_dict']
except KeyError:
    recipe_nf_dict={}
finally:
    s.close()

#load main dictionary from cache
s=shelve.open('recipes.db')
try:
    recipe_dict_main=s['recipes_dict']
except KeyError:
    recipe_dict_main={}
finally:
    s.close()

#refresh console
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

#for adding in a new recipe to be used to make label and save in books
def recipe_maker(name1):    
    recipe_book_strings=[]
    recipe_dict_list=[]
    ingred_num=0
    #name1=str(input('Please enter a name for the recipe.: '))
    name_up=name1.upper()
    if name_up in recipe_book.keys():
        rewrite_recipe=input('Would you like to rewrite current '+name1+' recipe? yes/no: ')
        if rewrite_recipe == 'yes':
            name_up=name1.upper()
        elif rewrite_recipe == 'no':
            return clear(),recipe_maker(name1=input('Please enter a name for the recipe.: '))
        else:
            return print('An incorrect choice has been made, please try again.'),clear(),home_screen()    
    while ingred_num==0:        
        ingredient=input('Please enter an ingredient. If you are done, type "done".: ').lower() #######        
        if ingredient == 'done':
            recipe_dict_list2=recipe_dict_list.copy()
            recipe_book_strings2=recipe_book_strings.copy()
            recipe_book[name_up]=recipe_dict_list2 #added dictionary to recipe book dict
            s=shelve.open('recipes.db')
            try:
                s['recipes_book']=recipe_book
            finally:
                s.close()
            recipe_book_user[name_up]=recipe_book_strings2
            s=shelve.open('recipes.db')
            try:
                s['recipes_user']=recipe_book_user
            finally:
                s.close()
            ingred_num+=1
        else:
            recipe_book_strings.append(str(ingredient))
            ingredient_list=ingredient.split()
            recipe_dict={'raw_ingred':"", 'amount':float, 'portion':""}
            #in the instance of > 1 fraction
            if '/' in ingredient_list[1]:
                temp_list=[]
                temp_list.append(ingredient_list[0]+' '+ingredient_list[1])
                print(temp_list)
                ingredient1 =' '.join(temp_list)
                print(ingredient1)
                ingredient_list2=[]
                ingredient_list2.append(ingredient1)
                del ingredient_list[0:2]
                print(ingredient_list)
                for i in ingredient_list:
                    ingredient_list2.append(i)
                    ingredient_list=ingredient_list2
                    print(ingredient_list)
            if len(ingredient_list)< 2:
                print("You made a mistake, please try again.")         
            elif len(ingredient_list)==2 and (ingredient_list[1] not in portion_list):
                try:
                    recipe_dict['amount']=float(ingredient_list[0])
                except ValueError:
                    if len(ingredient_list[0])==3:
                        ing_list2=ingredient_list[0].split('/')
                        ing_list_amt=float(int(ing_list2[0])/int(ing_list2[1]))
                        recipe_dict['amount']=ing_list_amt
                    elif len(ingredient_list[0])>=5:
                        ing_list2=ingredient_list[0].split()
                        ing_list3=float(ing_list2[0])
                        ing_list4=ing_list2[1].split('/')
                        ing_list_amt=float(ing_list3+(float(ing_list4[0])/float(ing_list4[1])))
                        recipe_dict['amount']=ing_list_amt
                recipe_dict['raw_ingred']=str(ingredient_list[1])
                recipe_dict['portion']='unit'
                recipe_dict_list.append(recipe_dict)                
            elif len(ingredient_list)==3:
                try:
                    recipe_dict['amount']=float(ingredient_list[0])
                except ValueError:#insert below the 3/5 options
                    if len(ingredient_list[0])==3:
                        ing_list2=ingredient_list[0].split('/')
                        ing_list_amt=float(int(ing_list2[0])/int(ing_list2[1]))
                        recipe_dict['amount']=ing_list_amt
                    elif len(ingredient_list[0])>=5:
                        ing_list2=ingredient_list[0].split()
                        ing_list3=float(ing_list2[0])
                        ing_list4=ing_list2[1].split('/')
                        ing_list_amt=float(ing_list3+(float(ing_list4[0])/float(ing_list4[1])))
                        recipe_dict['amount']=ing_list_amt
                recipe_dict['raw_ingred']=str(ingredient_list[2])
                recipe_dict['portion']=str(ingredient_list[1])
                recipe_dict_list.append(recipe_dict)                
            elif len(ingredient_list)>3 and ingredient_list[1] in portion_list: #untested after 'and'            
                joined_ingred_list=[]
                for i in range(2, len(ingredient_list)):
                    joined_ingred_list.append(ingredient_list[i])
                joined_ingred=" ".join(joined_ingred_list)
                try:
                    recipe_dict['amount']=float(ingredient_list[0])
                except ValueError:
                    if len(ingredient_list[0])==3:
                        ing_list2=ingredient_list[0].split('/')
                        ing_list_amt=float(int(ing_list2[0])/int(ing_list2[1]))
                        recipe_dict['amount']=ing_list_amt
                    elif len(ingredient_list[0])>=5:
                        ing_list2=ingredient_list[0].split()
                        ing_list3=float(ing_list2[0])
                        ing_list4=ing_list2[1].split('/')
                        ing_list_amt=float(ing_list3+(float(ing_list4[0])/float(ing_list4[1])))
                        recipe_dict['amount']=ing_list_amt
                recipe_dict['portion']=str(ingredient_list[1])
                recipe_dict['raw_ingred']=joined_ingred
                recipe_dict_list.append(recipe_dict)                
            else:
                print("You made a mistake, please try again.")
    return input('Your recipe has been saved in the database. Please press enter to continue.'),clear(),home_screen()

#For doing the math for nutritional facts
def nutrition_math():
    print('Convert a recipe into a Nutrition Facts label.'.center(80))
    print('')
    print('Stored recipes:')
    print('')
    for i in recipe_book.keys():
        print(i.lower())
    if len(recipe_book.keys())==0:
        return input('There are currently no saved recipes in the database. Press enter to return to home screen.'),clear(),home_screen()
    print('')
    #recipe name you're looking for
    reci_name = input('Please enter a recipe name. Enter "home" to return to the home screen.: ').upper()
    if reci_name=='HOME':
        return clear(),home_screen()
    #serving size for nutrition fact
    if reci_name not in recipe_book.keys():
        error_throw=input('You entered an incorrect recipe name. Please press enter to try again or type "home" to return to the home screen.: ')
        if error_throw=='home':
            return clear(), home_screen()
        else:
            return clear(), nutrition_math()
    serv_sz = input('Please enter how many pieces you intend to make from a batch: ')
    try:
        serv_size = float(serv_sz)
    except:
        return input('You entered an invalid serving size. Please press enter to try again.'),clear(),nutrition_math()
    #serv_size = float(input('Please enter how many pieces you intend to make from a batch: '))
    #full ingredient list for that recipe
    ing_list = []
    #dict of floats for multiplying against df3
    ing_mult_list = {}
    #iterate over each ingredient in the recipe pulling it out by pieces
    for i in range(0,len(recipe_book[reci_name])):
        #ingredient of recipe
        dfri = recipe_book[reci_name][i]['raw_ingred']
        #number of the portion size
        dfam = recipe_book[reci_name][i]['amount']
        #portion measurement
        dfpo = recipe_book[reci_name][i]['portion']
        #adding ingredients to a list to be used later
        ing_list.append(dfri)
        #check for instance user uses grams
        if dfpo == 'gram' or dfpo == 'grams' or dfpo == 'g':
            magic_num=float(dfam/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc1']:
            #the number to multiply the nutrition facts by
            magic_num=float((dfam*df2[dfri].loc['gmwt 1'])/100)
            #add to dictionary to call on for each ingredient
            ing_mult_list[dfri]=magic_num
        #can copy paste following "elif" for added portion sizes in graph. change # of gmwt to correspond
        elif dfpo == df2[dfri].loc['gmwt desc2']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 2'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc3']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 3'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc4']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 4'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc5']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 5'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc6']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 6'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc7']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 7'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc8']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 8'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc9']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 9'])/100)
            ing_mult_list[dfri]=magic_num
        elif dfpo == df2[dfri].loc['gmwt desc10']:
            magic_num=float((dfam*df2[dfri].loc['gmwt 10'])/100)
            ing_mult_list[dfri]=magic_num        
        else:
            print('Portion size used does not exist.')
    #make a dataframe using just the ingredients from df2 (ingredient columns)
    df3=df2[ing_list]
    #remove unneccessary indexes
    df3.drop(['gmwt 1', 'gmwt desc1', 'gmwt 2', 'gmwt desc2', 'gmwt 3', 'gmwt desc3', 'gmwt 4', 'gmwt desc4', 'gmwt 5', 'gmwt desc5', 'gmwt 6', 'gmwt desc6', 'gmwt 7', 'gmwt desc7', 'gmwt 8', 'gmwt desc8', 'gmwt 9', 'gmwt desc9', 'gmwt 10', 'gmwt desc10'], inplace=True)
    #multiply each column of dataframe to correspond with each ingredients magic number
    for i in ing_list:
        df3[i]=df3[i]*ing_mult_list[i]
    #add a total column12
    df3['total'] = df3.sum(axis=1)
    #add a total per serving column
    df3['total/serving']=df3['total']/serv_size
    #add a serving size value for access
    df3['servings']=''
    df3['servings'][0]=float(serv_size)
    #add to dictionary of dataframes for recipes
    recipe_dict_main[reci_name]=df3
    s=shelve.open('recipes.db')
    try:
        s['recipes_dict']=recipe_dict_main
    finally:
        s.close()
    df3.to_excel('Recipe Spreadsheets\\recipe_'+str(reci_name)+'.xlsx')
    #start comparison of %dv
    dfdv_ind=[]
    for i in dfdv.index:
        dfdv_ind.append(i)
    df4=dfdv.copy()
    df4['actual value/batch']=''
    df4['actual value/serving']=''
    df4['daily %/serving']=''
    df4['servings']=''
    df4['servings'][0]=serv_size
    #go through just required nutrients
    for i in dfdv_ind:
        try:
            df4['actual value/batch'][i]=df3['total'][i]
        except:
            df4['actual value/batch'][i]=0
    for i in dfdv_ind:
        try:
            df4['actual value/serving'][i]=df3['total/serving'][i]
        except:
            df4['actual value/serving'][i]=0
    if 'sugar' in df3.columns:
        df4['actual value/batch'].loc['added sugars,g']=df3['sugar'].loc['sugar,g']
        df4['actual value/serving'].loc['added sugars,g']=(df3['sugar'].loc['sugar,g'])/serv_size
    #calculate daily percentages
    df4['daily %/serving']=df4['actual value/serving']/df4['daily value']
    #change to actual percentages as opposed to floats ##unneeded
    #df4['daily %/serving']=df4['daily %/serving'].astype(float).round(decimals=1)#exchange .round with this if this fails .map("{:.0%}".format)
    #save to excel file
    df4.to_excel('Recipe Spreadsheets//dailyvalues_'+str(reci_name)+'.xlsx')
    #add to dictionary of daily values
    recipe_dv_dict[reci_name]=df4
    s=shelve.open('recipes.db')
    try:
        s['recipes_dv_dict']=recipe_dv_dict
    finally:
        s.close()
    #turn 'actual value/serving' into float type and round
    df4_av=df4['actual value/serving'].astype(float).round(decimals=1)
    #grab the daily % values from df4
    df4_dv=df4['daily %/serving']
    #fill in the nutrition label
    dfnf_edit = dfnf['Sheet1']
    dfnf_edit['B3']=input('How many servings will be in each container the nutrition facts label will be on?: ')+ ' servings per container'
    dfnf_edit['E4']=input('How much is or what would you refer to a serving as? (ie: 1 cup, 50 pieces, 1 package): ')
    dfnf_edit['D6']=df4['actual value/serving'].loc['energy,Calories'].round()
    dfnf_edit['B10']='Total Fat '+str(df4_av.loc['total fat,g'])+'g'
    dfnf_edit['E10']=df4_dv.loc['total fat,g']
    dfnf_edit['B11']='Saturated Fat '+str(df4_av.loc['fat sat,g'])+'g'
    dfnf_edit['E11']=df4_dv.loc['fat sat,g']
    dfnf_edit['B12']='Trans Fat 0g'
    dfnf_edit['B13']='Cholesterol '+str(df4_av.loc['cholesterol,mg'])+'mg'
    dfnf_edit['E13']=df4_dv.loc['cholesterol,mg']
    dfnf_edit['B14']='Sodium '+str(df4_av.loc['sodium,mg'])+'mg'
    dfnf_edit['E14']=df4_dv.loc['sodium,mg']
    dfnf_edit['B15']='Total Carbohydrate '+str(df4_av.loc['carbohydrates,g'])+'g'
    dfnf_edit['E15']=df4_dv.loc['carbohydrates,g']
    dfnf_edit['B16']='Dietary Fiber '+str(df4_av.loc['fiber,g'])+'g'
    dfnf_edit['E16']=df4_dv.loc['fiber,g']
    dfnf_edit['B17']='Total Sugars '+str(df4_av.loc['sugar,g'])+'g'
    dfnf_edit['C18']='Includes '+str(df4_av.loc['added sugars,g'])+'g Added Sugars'
    dfnf_edit['E18']=df4_dv.loc['added sugars,g']
    dfnf_edit['B19']='Protein '+str(df4_av.loc['protein,g'])+'g'
    dfnf_edit['B21']='Vitamin D '+str(df4_av.loc['vit d,mcg'])+'mcg'
    dfnf_edit['E21']=df4_dv.loc['vit d,mcg']
    dfnf_edit['B22']='Iron '+str(df4_av.loc['iron,mg'])+'mg'
    dfnf_edit['E22']=df4_dv.loc['iron,mg']
    dfnf_edit['B23']='Calcium '+str(df4_av.loc['calcium,mg'])+'mg'
    dfnf_edit['E23']=df4_dv.loc['calcium,mg']
    dfnf_edit['B24']='Potassium '+str(df4_av.loc['potassium,mg'])+'mg'
    dfnf_edit['E24']=df4_dv.loc['potassium,mg']    
    #save nutrition facts spreadsheet
    dfnf.save('Recipe Spreadsheets//NFlabel_'+str(reci_name)+'.xlsx')
    #save as an image
    excel2img.export_img('Recipe Spreadsheets//NFlabel_'+str(reci_name)+'.xlsx','Nutrition Facts Labels//NFlabel_'+str(reci_name)+'.bmp')
    #open image
    imnf=Image.open(r'Nutrition Facts Labels//NFlabel_'+str(reci_name)+'.bmp')
    return imnf.show(),clear(),home_screen()
      
def home_screen():
    print('Welcome to the Serious Baker.'.center(80))
    print('')
    print('What would you like to do?')
    print('')
    print('1. Put in a new recipe.')
    print('2. Generate a nutrition facts label.')
    print('3. View a food cost chart of your current recipes.')
    print('4. Put in cooking directions for an existing recipe.')
    print('5. View a saved recipe.')
    print('6. View an existing Nutrition Facts label.')
    print('7. Add/Change an ingredient cost.') 
    print('8. Change an existing recipe.')
    print('')
    decision=input('Please select an option: ')
    if decision == '1':
        try:
            return clear(),recipe_maker(name1=input('Please enter a name for the recipe.: '))
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '2':
        try:
            return clear(),nutrition_math()
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision =='3':
        try:
            return clear(),cost_math() ##
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '4':
        try:
            return clear(),recipe_directions()  
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '5':
        try:
            return clear(),recipe_user_doc() 
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '6':
        try:
            return clear(),recipe_labels()
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '7':
        try:
            return clear(),recipe_cost_add()  ##
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    elif decision == '8':
        try:
            return clear(),recipe_change()  
        except:
            return input('An error occured. Please enter any key to try again.'),clear(),home_screen()
    else:
        return input('Incorrect selection. Please press enter key to continue...'),clear(),home_screen()

def recipe_user_doc():
    print('View A Saved Recipe.'.center(80))
    print('')
    print('Saved recipes:')
    print('')
    user_reci_ops=[]
    user_reci_ops1=[]
    for i in os.listdir('Recipes'):
        user_reci_ops1.append(i)
    for i in user_reci_ops1:
        user_reci_ops2=i.split('.')
        user_reci_ops3=user_reci_ops2[0].replace('recipe_','')
        user_reci_ops.append(user_reci_ops3.lower())
    for i in user_reci_ops:
        print(i)
    if len(user_reci_ops)==0:
        return input('There are currently no saved recipes in the database. Press enter to return to the home screen.'), clear(),home_screen()
    print('')
    decision=input('Please enter the name of the recipe you would like to view. Type "home" to return to home screen.: ').upper()
    if decision == 'HOME':
        return clear(), home_screen()
    try:
        chosen_rec=open(r'Recipes\recipe_'+decision+'.txt','r')
    except:
        error_throw=input('You entered an incorrect recipe name. Press enter to try again, or type "home" to return to the main screen.: ')
        if error_throw=='home':
            return clear(),home_screen()
        else:
            return clear(),recipe_user_doc()
    for i in chosen_rec.read().splitlines():
        print(i)
    print('')
    chosen_rec_open=input('Would you like to open the recipe outside this program? yes/no: ').lower()
    if chosen_rec_open=='yes':
        return os.startfile(r'Recipes\recipe_'+decision+'.txt'), clear(),home_screen()
    else:
        return input('When finished, press enter to go back to the main screen.'),clear(),home_screen()

def recipe_labels():
    print('View A Saved Nutrition Facts Label.'.center(80))
    print('')
    print('Saved recipe labels:')
    print('')
    user_nf_ops=[]
    user_nf_ops1=[]
    for i in os.listdir('Nutrition Facts Labels'):
        user_nf_ops1.append(i)
    for i in user_nf_ops1:
        user_nf_ops2=i.split('.')
        user_nf_ops3=user_nf_ops2[0].replace('NFlabel_','')
        user_nf_ops.append(user_nf_ops3.lower())
    for i in user_nf_ops:
        print(i)
    if len(user_nf_ops)==0:
        return input('There are currently no Nutrition Facts labels in the database. Press enter to return to the home screen.'),clear(),home_screen()
    print('')
    decision=input('Please enter the name of the recipe recipe you would like to view the nutrition facts label for. Or enter "home" to return to the home screen.: ').upper()
    if decision=='HOME':
        return clear(),home_screen()
    try:
        imnf=Image.open(r'Nutrition Facts Labels//NFlabel_'+decision+'.bmp')
    except:
        error_throw=input('Incorrect recipe name entered. Please press enter to try again or type "home" to return to the home screen.: ')
        if error_throw=='home':
            return clear(), home_screen()
        else:
            return clear(),recipe_labels()
    return imnf.show(),clear(),home_screen()

def recipe_directions():
    print('Add directions to a recipe.'.center(80))
    print('')
    print('Saved recipes.:')
    print('')
    for i in recipe_book.keys():
        print(i.lower())
    if len(recipe_book.keys())==0:
        return input('There are currently no saved recipes in the database. Press enter to return to home screen.: '),clear(),home_screen()
    print('')
    decision=input('Please enter the name of a recipe you want to add directions to. Enter "home" to return to the home screen.: ').upper()
    if decision=='HOME':
        return clear(),home_screen()
    if decision in recipe_book_directions.keys():
        error_throw=input('Directions for that recipe already exist. Overwrite? yes/no: ').lower()
        if error_throw=='no':
            return clear(),recipe_directions()        
    print('Please enter your directions one step at a time, hitting enter between each step.')
    direction_num=1
    direction_done=0
    direction_list=[]
    while direction_done==0:
        direction=input(str(direction_num)+'.: ')
        if direction=='done':
            direction_done+=1
        else:
            direction_list.append(str(direction_num)+'.: '+direction)
            direction_num+=1
    recipe_book_directions[decision]=direction_list
    s=shelve.open('recipes.db')
    try:
        s['recipes_directions']=recipe_book_directions
    finally:
        s.close()
    recipe_file=open(r'Recipes//recipe_'+decision+'.txt','w')
    recipe_file.write(decision+'\n\n')
    recipe_file.write('Ingredients:\n')
    for i in recipe_book_user[decision]:
        recipe_file.write('* '+i+'\n')
    recipe_file.write('\n')
    recipe_file.write('\n')    
    recipe_file.write('Directions:\n')
    for i in direction_list:
        recipe_file.write(i+'\n')
    recipe_file.close()
    return os.startfile(r'Recipes\recipe_'+decision+'.txt'), clear(),home_screen()
    
def recipe_change():
    print('Change an Existing Recipe.'.center(80))
    print('')
    print('Saved recipes.:')
    print('')
    for i in recipe_book.keys():
        print(i.lower())
    if len(recipe_book.keys())==0:
        return input('There are currently no saved recipes in the database. Press enter to return to home screen.: '),clear(),home_screen()
    print('')
    recipe_nm=input('Please enter the recipe name you would like to change.: ').upper()
    if recipe_nm in recipe_book.keys():
        return recipe_maker(name1=recipe_nm)
    else:
        return input('You entered an incorrect recipe name. Please press enter to try again.'),clear(),recipe_change()
    
def cost_math():
    if 'recipe_Costs.xlsx' in os.listdir(r'Cost Spreadsheets'):
        view_update=input('We have a saved recipe cost database in the system. Would you like to view or update it? Type "view" or "update". Please type "home" to return to the home screen.').lower()
        if view_update == 'view':
            view_ch=input('Would you like to view a single recipe\'s cost or all recipes? Type "single" or "all".: ').lower()
            if view_ch == 'all':
                recipe_costs_ss=pd.read_excel(r'Cost Spreadsheets\recipe_Costs.xlsx', index_col='recipe')
                print(recipe_costs_ss)
                choice=input('Would you like to view outside this program? yes/no: ').lower()
                if choice == 'yes':
                    return os.startfile(r'Cost Spreadsheets\recipe_Costs.xlsx'), clear(), home_screen()
                else:
                    return clear(),home_screen()
            elif view_ch == 'single':#
                print('change this')##
            else:
                return input('Incorrect choice entered. Please press enter to continue.'),clear(),cost_math()
        elif view_update == 'home':
            return clear(), home_screen()
        elif view_update == 'update':#
            upd_cost=pd.read_excel(r'Cost Spreadsheets\recipe_Costs.xlsx', index_col='recipe')
            print('change this')##
        else:
            return input('Incorrect choice entered. Please press enter to continue.'), clear(), cost_math()
    else:
        if 'costlibrary_user.xlsx' in os.listdir(r'Cost Spreadsheets'):
            rec_cost_conv=pd.read_excel(r'Cost Spreadsheets\costlibrary_user.xlsx', index_col='Unnamed: 0')
            rec_ing_gram={}
            for i in recipe_book:
                #full ingredient list for that recipe
                ing_list = []
                #dict of floats for multiplying against df3
                ing_gram_list = {}
                for j in range(0,len(recipe_book[i])):##
                #for i in range(0,len(recipe_book[reci_name])):
                    #ingredient of recipe
                    dfri = recipe_book[i][j]['raw_ingred']
                    #number of the portion size
                    dfam = recipe_book[i][j]['amount']
                    #portion measurement
                    dfpo = recipe_book[i][j]['portion']
                    #adding ingredients to a list to be used later
                    ing_list.append(dfri)
                    #check for instance user uses grams
                    if dfpo == 'gram' or dfpo == 'grams' or dfpo == 'g':
                        magic_num=float(dfam)
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc1'].loc[dfri]:
                        #the number to multiply the nutrition facts by
                        magic_num=rec_cost_conv['gmwt 1'].loc[dfri]*dfam
                        #add to dictionary to call on for each ingredient
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc2'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 2'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc3'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 3'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc4'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 4'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc5'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 5'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc6'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 6'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc7'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 7'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc8'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 8'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc9'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 9'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    elif dfpo == rec_cost_conv['gmwt desc10'].loc[dfri]:                        
                        magic_num=rec_cost_conv['gmwt 10'].loc[dfri]*dfam                        
                        ing_gram_list[dfri]=magic_num
                    rec_ing_gram[i]=ing_gram_list
            dfcr2=dfcr.transpose()
            act_rec_ing_cost={}
            for i in rec_ing_gram:
                act_ing_cost={}
                for j in rec_ing_gram[i].keys():
                    act_ing_cost[j]=(rec_ing_gram[i][j])*(rec_cost_conv['cost/g'].loc[j])
                rec_cost_temp=0
                for k in act_ing_cost.keys():
                    rec_cost_temp+=act_ing_cost[k]                    
                act_rec_ing_cost[i]=rec_cost_temp
            for i in act_rec_ing_cost:
                cost_batch=act_rec_ing_cost[i]
                try:
                    dv_cost=pd.read_excel(r'Recipe Spreadsheets\dailyvalues_'+i+'.xlsx', index_col='nutrient')
                    cost_serving=cost_batch/dv_cost['servings'][0]
                except:
                    rec_div=float(input('Please enter the number of servings for the '+i.lower()+' recipe.: '))
                    cost_serving=cost_batch/rec_div
                dfcr2[i]=[cost_batch,cost_serving]##
            dfcr3=dfcr2.transpose()
            dfcr3.to_excel(r'Cost Spreadsheets\recipe_Costs.xlsx')
            s=shelve.open('recipes.db')
            try:
                s['recipes_costs']=dfcr3
            finally:
                s.close()
            finale=input('A database has been created of all your recipes costs. Would you like to view now? yes/no: ').lower()
            if finale == 'yes':
                print(dfcr3)
                true_end=input('Would you like to view outside of this program? yes/no: ').lower()
                if true_end=='yes':
                    return os.startfile('Cost Spreadsheets\recipe_Costs.xlsx'), clear(), home_screen()
                else:
                    return clear(), home_screen()
            else:
                return clear(), home_screen()                        
        else:
            return input('There is currently no record of any costs in the system. Please enter "7" at the home screen to start putting in your food costs. Please press enter to continue.: '), clear(), home_screen()

def recipe_cost_add():
    dfct1=dfct.copy()
    cost_escape=0
    while cost_escape==0:
        cost_ing=input('Please enter an ingredient you would like to add your cost for. If you are done, enter "done". Enter "home" to return to the home screen without saving.: ').lower()
        if cost_ing=='home':
            return clear(),home_screen()
        if cost_ing=='done':
            cost_escape+=1
        if cost_ing in dfct1.index:
            if pd.isnull(dfct1['cost'].loc[cost_ing]):
                ing_cost=float(input('Enter how much the container of '+cost_ing+' cost in USD.(Do not include "$". ie: 10.50): '))
                ing_cost_size=input('Enter the weight of the container of '+cost_ing+' purchased.(Enter number and weight. ie: 16 ounces): ').lower()
                dfct1['cost'].loc[cost_ing]=ing_cost
                dfct1['weight'].loc[cost_ing]=ing_cost_size
                ing_cost_size2=ing_cost_size.split(' ',1)
                if ing_cost_size2[1] == 'grams' or ing_cost_size2[1] == 'gram' or ing_cost_size2[1] == 'g':
                    dfct1['cost/g'].loc[cost_ing]=dfct1['cost'].loc[cost_ing]/float(ing_cost_size2[0])
                elif ing_cost_size2[1] in gram_conv_dict.keys():
                    dfct1['cost/g'].loc[cost_ing]=dfct1['cost'].loc[cost_ing]/(gram_conv_dict[ing_cost_size2[1]]*float(ing_cost_size2[0]))
                elif ing_cost_size2[1] not in gram_conv_dict.keys():
                        add_it=input('The unit of measurement of your container is not in our grams conversion database. Would you like to add it? yes/no: ').lower()
                        if add_it == 'yes':
                            gram_conv_dict[input('Enter the unit of measurement to convert to grams.: ')]=float(input('Enter the number of grams per each unit.: '))
                            input('Conversion added successfully. Press enter to continue.')
                        else:
                            cost_escape+=1
            else:                
                cost_check=input(cost_ing+' has already been entered. Change? yes/no: ').lower()
                if cost_check=='no':
                    cost_escape+=1
                else:
                    ing_cost=float(input('Enter how much the container of '+cost_ing+' cost in USD.(Do not include "$". ie: 10.50): '))
                    ing_cost_size=input('Enter the weight of the container of '+cost_ing+' purchased.(Enter number and weight. ie: 16 ounces): ').lower()
                    dfct1['cost'].loc[cost_ing]=ing_cost
                    dfct1['weight'].loc[cost_ing]=ing_cost_size
                    ing_cost_size2=ing_cost_size.split(' ',1)
                    if ing_cost_size2[1] == 'grams' or ing_cost_size2[1] == 'gram' or ing_cost_size2[1] == 'g':
                        dfct1['cost/g'].loc[cost_ing]=dfct1['cost'].loc[cost_ing]/float(ing_cost_size2[0])
                    elif ing_cost_size2[1] in gram_conv_dict.keys():
                        dfct1['cost/g'].loc[cost_ing]=dfct1['cost'].loc[cost_ing]/(gram_conv_dict[ing_cost_size2[1]]*float(ing_cost_size2[0]))
                    elif ing_cost_size2[1] not in gram_conv_dict.keys():
                        add_it=input('The unit of measurement of your container is not in our grams conversion database. Would you like to add it? yes/no: ').lower()
                        if add_it == 'yes':
                            gram_conv_dict[input('Enter the unit of measurement to convert to grams.: ')]=float(input('Enter the number of grams per each unit.: '))
                            input('Conversion added successfully. Press enter to continue.')
                        else:
                            cost_escape+=1
    dfct1.to_excel(r'Cost Spreadsheets\costlibrary.xlsx')
    s=shelve.open('recipes.db')
    try:
        s['recipes_cost_library']=dfct1
    finally:
        s.close()    
    dfct2=dfct1.dropna(subset=['cost'])
    dfct2.drop(['gmwt 1', 'gmwt desc1', 'gmwt 2', 'gmwt desc2', 'gmwt 3', 'gmwt desc3', 'gmwt 4', 'gmwt desc4', 'gmwt 5', 'gmwt desc5', 'gmwt 6', 'gmwt desc6', 'gmwt 7', 'gmwt desc7', 'gmwt 8', 'gmwt desc8', 'gmwt 9', 'gmwt desc9', 'gmwt 10', 'gmwt desc10'], inplace=True)
    dfct2.to_excel(r'Cost Spreadsheets\costlibrary_user.xlsx')
    s=shelve.open('recipes.db')
    try:
        s['recipes_cost_library_user']=dfct2
    finally:
        s.close()
    finale=input('Everything has been updated and saved. Would you like to view your ingredient cost library? yes/no: ').lower()
    if finale == 'yes':
        return os.startfile(r'Cost Spreadsheets\costlibrary_user.xlsx'),clear(),home_screen()
    else:
        return clear(),home_screen()
    
home_screen()

