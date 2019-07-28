from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import os
from fuzzywuzzy import fuzz
import re

# Create your views here.



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tsv_path = os.path.join(base_dir,"word_search.tsv")


#Home page for search box
def home(request):
    return render(request,"home.html")


#calling the logic function for autocompletion of words
def search(request):
    Input_word = request.GET['word']
    df = pd.read_csv(tsv_path,delimiter='\t',encoding='utf-8',header=None)
    df.dropna(inplace = True)
    df = df.reset_index()
    del df['index']
    df.columns=['Words','Frequency']
    res_data = fuzzy_ratio(Input_word,df)
    res_data = res_data.sort_values('Ratio_count',ascending=False)
    result = res_data[:25]['Words']
    
    return JsonResponse( {"Autocorrected_words":result.tolist()})



# using fuzzywuzzy logic to get the autocompletion words
def fuzzy_ratio(Input_word,df):
    res_data = pd.DataFrame(columns = ["Words","Frequency","Ratio_count"])
    filtered_data = pd.DataFrame(columns=["Words","Frequency"])
    z = 0
    
    #using regular expression to filter the words for efficiency
    for i in range(len(df)):
        print(i)
        res = re.findall(Input_word,df['Words'][i])
        if len(res)!=0:
            filtered_data.loc[z]= [df['Words'][i],df['Frequency'][i]]
            z+=1
            
    #using fuzz library to rank the similarity of words for auto completion
    for i in range(0,len(filtered_data)):
        ratio_val = fuzz.ratio(Input_word,filtered_data['Words'][i])
        res_data.loc[i] = [filtered_data['Words'][i],filtered_data['Frequency'][i],ratio_val]
    return res_data        