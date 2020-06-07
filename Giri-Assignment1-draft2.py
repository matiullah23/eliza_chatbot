# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:24:21 2020

@author: 2018-Giri-Dell
# AIT 590 NLP - Team 2 Assignment 1

#Team (alphatecially listed):
#    
#   Matiullah Hasher
#   Faysal Mowdud
#   Giri Nanduru
#   Asad Zaheer
"""
# Include the all the libraries we need for our ChatBot Application
from nltk import word_tokenize # for word tokenization
from nltk.tag import pos_tag # to get the part of speech for each token
from nltk import RegexpParser #parse input for the pattern in the grammar string
from nltk.corpus import wordnet #for finding stem word and noun lemmatization

import random
import re
import sys

#Use the user provided line and extract the Name token from it
def GetName(sentence):
    
    #Parse either Proper Noun Singular or Noun because RegexpParser is inaccurate at times
    grammar = 'NAME: {<NNP>*|<NN?>*}'
    
    #Create the Parser Object
    cp = RegexpParser(grammar)
    
    common_words = {'hi', 'name', 'hello', 'thank', 'you', 'i', 'am', 'oh', 'hey', 'sure', 'yes', 'named', 'known'}
    
    #Tokenize the input
    word_tokens = word_tokenize(sentence)
    
    #Eliminate the greeting words and get straight to discerning the Name as NNP or NN
    word_tokens = [x for x in word_tokens if x.lower() not in common_words]
    
    #Obtain parts of speech for each token and run through parser
    pos = pos_tag(word_tokens)
    result = cp.parse(pos)
    
    #print statements for debugging 
    #print(result)
    #result.draw()
    
    #Loop through the tree datastructure and pull the x (actual name), if the Root is 'NAME'
    #we created for the result
    
    output = "" 
    for tree in result.subtrees():
        if tree.label() == 'NAME':
            name_match = ' '.join([x for x,y in tree.leaves()])
            output = output + ' ' + name_match
    
    return output.replace("  ", " ").strip()


#Randomize method simply takes a noun token and formats it is a response for followup using a 
#canned list, injecting the noun token appropriately for context
def randomize(token, user_name):
    
    a1 = 'Why are you interested in ' + token + '?\n'
    a2 = 'Thanks for sharing about ' + token + '. Tell me more.\n'
    a3 = 'Why dont you tell me more about ' + token + '?\n'
    a4 = 'Most people relate to ' + token + ' in some form.  Why are you curious about it?\n'
    a5 = 'There is a lot of research about ' + token + '. Are you aware of it?\n'
    
    #Create a list object with above values
    Custom_fillers = [a1, a2, a3, a4, a5]
    
    if len(token) > 0:
            return random.choice(Custom_fillers)
    
    #print('randomize is called')
    Random_fillers = {'question': [user_name + ", that is a very interesting question. What made you ask that?\n", 
                    user_name + ', before I answer, can you give me your thoughts?\n', 
                    user_name + ', that is a complicated question. Can you provide me some more details?\n', 
                    'Hmm. Where do I begin?\n'],
                    'statement': ['How does that make you feel?\n',
                    'Why do you think that?\n',
                    'How long have you felt this way?\n',
                    'I find that extremely interesting. I would like to know why you feel this way.\n',
                    'Thanks for sharing that with me. Tell me more.\n',
                    'Do you feel in touch with your inner self?\n',
                    'Do you really believe that?\n']}
       
    if user_text.strip().endswith("?"):
        return random.choice(Random_fillers["question"])
    else:
        return random.choice(Random_fillers["statement"])   

    
    #Return randomly one of the list values that includes token passed in


#This method captures the main part of speech composed of verb, determinant, noun
#This can then be used to form a question to the user with that phrase
def GetVerbDetNounPhrase(sentence):
    
    #print('GetNounPhrase is called')
    output = ''
    
    #Parse either Proper Noun Singular or Noun because RegexpParser is inaccurate at times    
    grammar = 'DNP: {<(VB |VBP)><DT>?<NN>}'

    #Create the Parser Object 
    cp = RegexpParser(grammar)
 
    #Tokenize the input and get part of speech
    pos = pos_tag(word_tokenize(sentence))
    
    result = cp.parse(pos)
    
    #result.draw()
    #print(result)

    #Loop through the tree datastructure and pull the values under DNP node
    #we created for the result
    for tree in result.subtrees():
        if tree.label() == 'DNP':
            name_match = ' '.join([x for x,y in tree.leaves()])
            output = output + name_match
    
    return output

#This method pulls Noun from the sentence and returns it
def GetNounPhrase(sentence):
    
    #print('GetNounPhrase is called')
    output = ''

    #Parse either Proper Noun Singular or Noun because RegexpParser is inaccurate at times     
    grammar = 'NP: {<DT>?<JJ>*<NN.*>+}'
 
    #Create the Parser Object 
    cp = RegexpParser(grammar)
    
    #Tokenize the input and get part of speech
    pos = pos_tag(word_tokenize(sentence))
    
    result = cp.parse(pos)

    #for debugging    
    #result.draw()    
    #print(result)
    
    #Loop through the tree datastructure and pull the values under DNP node
    #we created for the result 
    for subtree in result.subtrees(filter=lambda t: t.label() == 'NP'):
        output = ' '.join(item[0] for item in subtree.leaves()) # 'abc\nghi\nmno'
    
    return output

#This method searches to see if there's a verb embedded somewhere in
#in the sentence and tries to convert into a Noun form and return it
def GetVerbPhrase(sentence):
       
    #print('GetNounPhrase is called')
    output = ''
    verb_token = ''

    #Parse either Proper Noun Singular or Noun because RegexpParser is inaccurate at times    
    grammar = 'VP: {<VB> | <VBP>}'

    #Create the Parser Object     
    cp = RegexpParser(grammar)
    
    #Tokenize the input and get part of speech  
    pos = pos_tag(word_tokenize(sentence))
    
    result = cp.parse(pos)
    
    #Debug: look at the tree formed
    #result.draw()
    #print(result)

    #Loop through the tree datastructure and pull the values under DNP node
    #we created for the result  
    for subtree in result.subtrees(filter=lambda t: t.label() == 'VP'):
        verb_token = ' '.join(item[0] for item in subtree.leaves()) 
    
    #print('verb found:' + verb_token)
    misclassified_verbs  = ['is', 'are', 'am', 'do']
    if verb_token in misclassified_verbs:
        return ''; #if it is a verb that cannot be converted just return blank
    
    if (len(verb_token.strip()) == 0):
        return verb_token.strip()  #if there's no verb just return blank

    #Second half of the program
    #Begin with creating a wordnet library object
    wn = wordnet        
    #debugging
    #wl = WordNetLemmatizer()
    #wn.lemma('give.v.01.give').derivationally_related_forms()

    #Use try catch loop because some verbs do not have a noun form and result
    #in exception error
    try:
        #create a lemma word of hte form verb + v.01 + verb => this is what wordnet lemma method takes
        lemma_word = verb_token + '.v.01.' + verb_token
 
        #debug to try
        # wn.lemma('perform.v.01.perform').derivationally_related_forms()
        
        #Call the lemma function and then derivationally_related_forms() to get all the applicable
        #word forms wordnet can give us
        lemma_output = wn.lemma(lemma_word).derivationally_related_forms()
        
        #debug
        #print(lemma_output)
        
        #if we find a noun form ending with ing, ial, ion we want it!
        for x in lemma_output:
            #print (x.name())
            if (re.search(r'ing$|ial$|ion$', x.name())):
                return x.name()
  
        #if its not one of the three above, return the first noun form found
        output = lemma_output[0].name()
    except:
        output = ''
        #Ideally handle the exception, in this case we return a blank
        #print("Oops!", sys.exc_info()[0], "occurred.")
    
    return output 

#As self-explanatory name suggests, convert the words so they are not misdiagnosed in parsing step
def ConvertApostrophe(token):
    # specific
    token = re.sub(r"won't", "will not", token)
    token = re.sub(r"can\'t", "can not", token)
    token = re.sub(r"n\'t", " not", token)
    token = re.sub(r"\'re", " are", token)
    token = re.sub(r"\'s", " is", token)
    token = re.sub(r"\'d", " would", token)
    token = re.sub(r"\'ll", " will", token)
    token = re.sub(r"\'t", " not", token)
    token = re.sub(r"\'ve", " have", token)
    token = re.sub(r"\'m", " am", token)
    return token

user_name = ""  #name we want to extract from user input

flag=True # Flag to break our loops processing user input

#Debug
#print('Jai Ganesh!')


prompt = "Hi, I'm a AIT 590 Psychotherapist. What is your name?\n"

while True:
    #Begin with welcome message after stripping the single quotes to form standard words
    user_input = ConvertApostrophe(input(prompt))
    
    #User wants to quit, time to break the loop already
    if (user_input.strip().lower() == 'quit' or user_input.strip().lower() == 'exit'):
        flag = False
        break
    
    if(user_input.strip() == ''):
        prompt = "Sorry couldn't get your name, can you try one more time?"
        continue  
    else:
        user_name = GetName(user_input)
        prompt = 'Hi ' + user_name + '. You can type quit to end our conversation anytime. How can I help you today?\n'
        break
    
while(flag == True):
    
    user_text = input(prompt)
    
    if (len(user_text) == 0):
        prompt = "No input received, please try again"
        continue
    #user_response=user_response.lower()
    
    #print('user text on line 275 is ' + user_text)
    user_text = ConvertApostrophe(user_text)
    if(user_text.strip().lower() =='quit' or user_text.strip().lower() == 'exit'):
        flag=False
        break
    elif(re.search(r'\byou\b', user_text, re.IGNORECASE)):
         prompt = user_name + ", thank you for that response. let's focus on you :) \n"
         continue #if the question is for the chatbot, turn it around to the user
    else:
           
        # ATTEMPT 1: Try the grammar format "verb determinant noun"
        # for example, rule-the-world.
        # If user enters "I like to play the piano", method should return "play the piano"
        
        user_response = GetVerbDetNounPhrase(user_text).strip()
 
        #print("GetVerbDetNounPhrase returned" + user_response) #debug      
        if (len(user_response) > 2):
            #Found a response, build the string for the next prompt
            prompt = user_name + ", why do you want to " + user_response + "?\n"
            continue #go back to the top of the while loop
       
        #ATTEMPT 2: Try the grammar format Noun first (with or without verb later)
        user_response = GetNounPhrase(user_text).strip()
        
        #Debug
        #print("GetNounPhrase returned" + user_response)
        if (len(user_response) > 2):
            prompt = randomize(user_response, user_name)
            continue;
            
        # ATTEMPT 3: Try the grammar format verb without a noun
        # for example, deny.
        # If user enters "I like to play the piano", method should return "play the piano"
        
        #try to capture the essential verb-det-noun, if not found, try just the verb
        #I warn, the function returns warning
        user_response = GetVerbPhrase(user_text).strip()
        #print("GetVerbPhrase returned " + user_response)
        if (len(user_response) > 2):
            prompt = user_name + ", " + randomize(user_response, user_name)
            continue
        
        #All 3 Attempts above did not result in us learning the context satisfactorily
        #Try random responses
  
        prompt = randomize('', user_name)
#User has indicated they want to quit
print("Good bye " + user_name + ". See you in your next appointment!")
