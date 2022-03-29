import streamlit as st
import numpy as np
import pandas as pd
#from google.colab import drive
#drive.mount('/content/drive/')
############################
# needs openpyxl as well
# Check the version
print('pandas version', pd.__version__)
print('numpy version', np.__version__)

#
st.title('University League Table Omatic - Your University can be the best!')


file_location = r'/content/drive/My Drive/Colab Notebooks/Guardian_University_Guide_2019edited.xlsx'
file_location = r'Guardian_University_Guide_2019editedV2.xlsx'
# number of metrics used by Guardian, there are 9 numbers per University
n=9
#df = pd.read_excel(file_location)
xl = pd.ExcelFile(file_location)
print(xl.sheet_names)  # see all sheet names

df=xl.parse("Institution")  # read a specific sheet to DataFrame
print("Column headings:")
print(df.columns)

# optional to speed code
n_uni=121
#print('running for top ',n_uni,' universities only')
#
# reads in desired set of unis into a dataframe
Guardian_data_df=df.iloc[0:n_uni,4:16]


uni_list=Guardian_data_df.iloc[:,0]
top_uni_name = st.selectbox(
     'Please use the drop down menu to select the UK University [1] you want to be the number one UK University',
     uni_list,index=20)

st.write('You selected:', top_uni_name)#,' please wait a minute while app runs - check the little running icon at top right')
row_num_top=Guardian_data_df[Guardian_data_df['Institution'] == top_uni_name].index[0]
print('row number of selected uni ',row_num_top,Guardian_data_df.iloc[row_num_top,0])


def TScalc(weights):
    for i_uni in range(0,n_uni):
        score_vector=weights[:]*Guardian_data_df.iloc[i_uni,2:2+n]
        Guardian_data_df.iloc[i_uni,1]=np.sum(score_vector)
    return

#
print('getting weights')
LTweights=np.zeros(n)
with open('top_weights.txt') as f:
    lines = f.readlines()
    found_uni_weights=False
    for iline in range(0,len(lines)):
        line_list = lines[iline].split(' ')
#        print(line_list[0])
# extract out name - which may have space in it
        print(len(line_list))
        if(len(line_list) == 11):
            w_uni_name=line_list[0]
            w1=1
            print('found name ',w_uni_name)
        elif(len(line_list) == 12):
            w_uni_name=line_list[0]+' '+line_list[1]
            w1=2
            print('found name ',w_uni_name)
        elif(len(line_list) == 13):
            w_uni_name=line_list[0]+' '+line_list[1]+' '+line_list[2]
            w1=3
            print('found name ',w_uni_name)
        elif(len(line_list) == 14):
            w_uni_name=line_list[0]+' '+line_list[1]+' '+line_list[2]+' '+line_list[3]
            w1=4
            print('found name ',w_uni_name)
        elif(len(line_list) == 15):
            w_uni_name=line_list[0]+' '+line_list[1]+' '+line_list[2]+' '+line_list[3]+' '+line_list[4]
            w1=5
            print('found name ',w_uni_name)
        else:
            print('EEEK!! no name')
#
        if(w_uni_name == top_uni_name):
            LTweights[:]=line_list[w1:w1+9]
            found_uni_weights=True
    if(found_uni_weights): 
        print(top_uni_name,' found weights ',LTweights)      
    else:
        print('EEEEK!, no weights')
#
if(found_uni_weights):
#
    TScalc(LTweights)
# sort
    finalsorted_df=Guardian_data_df.sort_values(by=['Average Teaching Score'],ascending=False)
# set row indices to 1, 2, 3, ...
    finalsorted_df.index = np.arange(1, len(finalsorted_df) + 1)
    final_rank=finalsorted_df[finalsorted_df['Institution'] == top_uni_name].index[0]
    st.write('Congratulations! ',top_uni_name,' has highest league table position of ',final_rank)
    st.write('Full league table is:')
#
    st.dataframe(finalsorted_df.style.format(precision=1))
    st.write("Note that if you flip the signs of all weights you flip the league table, i.e., 'top' university is now 'bottom'.")
#
    st.markdown('This league table for 9 weights $$w_i$$ with values:')
    final_weights=np.round(LTweights,3)
    for i in range(0,n):
        roundedw=str(np.round(LTweights[i],3))
        stringy=finalsorted_df.columns[i+2]+' weight = '+roundedw
        st.write(stringy)
else:
    st.write('Sorry League Table Omatic has failed you ')
#

stringy='This league table uses data from the [2019 Guardian league table](https://www.theguardian.com/education/ng-interactive/2018/may/29/university-league-tables-2019), which uses nine metrics [2] (numbers) $$M_i$$ that are assumed to quantify teaching quality: '
for i in range(0,n-1):
    stringy += Guardian_data_df.columns[i+2]+"; "
stringy += Guardian_data_df.columns[10]+"."

st.markdown(stringy)
st.markdown("This league table web app is just to illustrate how arbitrary is any ranking of institutions as complex and diverse as universities. If you actually want to compare UK universities, please see a [web app that compares and ranks universities based on criteria you choose](https://university-league-tables.herokuapp.com/). That (better) web app was done by Ethan Hinton, a great then-Surrey-student who did a project with me in the first half of 2021. ")

st.markdown('A league table is just a ranking of universities, here this is supposed to be for teaching. To rank using a set of $$n$$ metrics $$M_i$$ with $$i=1,n$$, one number, TS, is computed from the $$n$$ numbers - i.e., the metrics - using')
st.latex(r'{\rm TS}=\sum_{i=1}^nw_iM_i')
st.markdown(r"then the 'top' university is the university with highest value of TS, 'second-best' university has second highest value of TS, ...., 'worst' university has lowest value of TS.")

st.markdown("However TS depends on values of weights $$w_i$$ as well as values of metrics $$M_i$$. This web app exploits the fact that for any set of metrics there are an infinite number of league tables - each one with different set of values for the weights $$w_i$$. The web app varies the values of the $$w_i$$ to try and put the university you select at the top, and so the 'best' university - according to this particular university league table - one of the infinite number of leagure tables you can compute.")

st.markdown("NB does not work for a couple of universities, eg Liverpool John Moores, Queen's Belfast, Sheffield Hallam, Sunderland, Central Lancashire, St Mary's, Twickenham, East London, Worcester, Chester, Birmingham City")
#
#
st.markdown('web app by [Richard Sear](https://richardsear.me/)')
#
st.markdown("[1] NB There are [about 160 Higher Education Institutions (HEI)s in the UK](https://www.universitiesuk.ac.uk/latest/insights-and-analysis/higher-education-numbers). The data used here is from The Guardian 2019 table which has only 121. The Guardian removes some of the 40 HEIs using a rather arbitrary cutoff.")
st.markdown("[2] NB The Guardian does some dodgey things to get some of the metrics. For example, some of the metrics come from National Student Survey results, which are missing for Oxford and Cambridge. The Guardian kind of makes things up here.")
