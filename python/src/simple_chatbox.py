import codecs
from itertools import product
from database import *


queries = ["em có thể nhắc lại tất cả các tour được không",
             "đi từ Hồ Chí Minh tới Nha Trang hết bao lâu",
             "đi từ Hồ Chí Minh tới Đà Nẵng hết bao lâu",
             "có bao nhiêu tour đi Phú Quốc vậy bạn",
             "tour Nha Trang đi bằng phương tiện gì vậy",
             "đi Nha Trang có những ngày nào nhỉ"]

def translate_sentence(sentence, lexicon):
    words = sentence.lower().split()
    def word_definition(words):
        if len(words) > 1:
            single_word = words[0]
            s1 = []
            s2 = []
            s3 = []
            if single_word in lexicon:
                s = word_definition(words[1:])
                if s:
                    s1 = [lexicon[single_word]['type']]
                    s1 = [[(a,single_word)] for a in s1]
                    s1 = [x + y for x, y in product(s1, s)]
            if len(words) > 1:
                compound_word = str(words[0] + ' ' + words[1])
                if compound_word in lexicon:
                    s = word_definition(words[2:])
                    if not words[2:]: s =[[]]
                    if s:
                        s2 = [lexicon[compound_word]['type']]
                        s2 = [[(a,compound_word)] for a in s2]
                        s2 = [x + y for x, y in product(s2, s)]
            if len(words) > 2:
                compound_word = str(words[0] + ' ' + words[1] + ' ' + words[2])
                if compound_word in lexicon:
                    s = word_definition(words[3:])
                    if not words[3:]: s =[[]]
                    if s:
                        s3 = [lexicon[compound_word]['type']]
                        s3 = [[(a,compound_word)] for a in s3]
                        s3 = [x + y for x, y in product(s3, s)]
            x = s1 + s2 + s3
            return x
        if len(words) == 1 and words[0] in lexicon:
            return [[(a,words)] for a in [lexicon[words[0]]['type']]]
        return []
    return word_definition(words)



# s = translate_sentence(queries[1],lexicon)
# print(s)

##########################################################

def get_rule_list(x,rules = rules):
    # return type [[rule],...]
    return_value =[]
    for rule in rules:
        if rule[0] == x:
            return_value.append(rule)
    return return_value


def current_agenda_check(current_agenda,rules = rules):
    new_agenda = []
    for i in range(0,len(current_agenda)):
        start , word , end ,rule_lst,history = current_agenda[i]
        new_history = [current_agenda[i]]
        for rule in rule_lst:
            if len(rule)==1:
                new_agenda+= [(start, rules[rule],end,get_rule_list(rules[rule]),new_history)]
            else:
                en = end
                key = False
                past_list = []
                for j in range(1,len(rule)):
                    key = False
                    for k in range(i,len(current_agenda)):
                        s,w,e,r,h = current_agenda[k]
                        if s == en and w == rule[j]:
                            en = e
                            key = True
                            past_list += [current_agenda[k]]
                            break
                if key:
                    new_agenda+= [(start,rules[rule],en,get_rule_list(rules[rule]),new_history + past_list)]
    return new_agenda

def past_agenda_check(current_agenda,past_agenda,rules = rules):
    new_agenda = []
    for i in range(0,len(past_agenda)):
        start,word,end, rule_lst,history = past_agenda[i]
        new_history = [past_agenda[i]]
        for rule in rule_lst:
            if len(rule)!=1:
                en =end 
                key= False
                past_list = []
                for j in range(1,len(rule)):
                    key = False
                    for s,w,e,r,h in current_agenda + past_agenda:
                        if s == en and w == rule[j]:
                            en = e
                            key = True
                            past_list += [(s,w,e,r,h)]
                            break
                if key:
                    new_agenda+= [(start,rules[rule],en, get_rule_list(rules[rule]) ,new_history + past_list)]
    for i in range(0,len(current_agenda)):
        start,word,end,rule_lst, history = current_agenda[i]
        new_history = [current_agenda[i]]
        for rule in rule_lst:
            if len(rule)!= 1:
                en =end 
                key= False
                past_list = []
                for j in range(1,len(rule)):
                    key = False
                    for s,w,e,r,h in past_agenda +current_agenda:
                        if s == en and w == rule[j]:
                            en = e
                            key = True
                            past_list += [(s,w,e,r,h)]
                            break
                if key:
                    new_agenda+= [(start,rules[rule],en, get_rule_list(rules[rule]) ,new_history + past_list)]
    return new_agenda

def bottom_up_parser(sentence):
    past_agenda = []
    current_agenda = []
    length_sentence = len(sentence)
    for c, word in enumerate(sentence,start=0):
        current_agenda.append((c,word,c+1,get_rule_list(word),[]))
        
    while True:
        new_agenda = []
        new_agenda += current_agenda_check(current_agenda)
        new_agenda += past_agenda_check(current_agenda,past_agenda)
        past_agenda += current_agenda
        current_agenda = new_agenda
        for a in new_agenda:
            s,w,e,r,h = a
            if (s,w,e) == (0,'S',length_sentence):
                return a
        if not new_agenda:
                break
    return []


def semantic_relationship(queries = queries,lexicon = lexicon,rules=rules):
    def redundant_tree(node):
        if node:
            s,w,e,r,h = node
            new_h = []
            for c_node in h:
                new_h += [redundant_tree(c_node)]
            return (w,new_h)
        return []
            
    def adding_sematric(node):
        query, n = node
        s,w,e,r,h = n
        if len(h) == 0:
            letter = query[s][1]
            if w == 'N':
                x = {'agr' : lexicon[letter]['agr'] ,'sem': lexicon[letter]['sem']}
                return x
            if w == 'V':
                x = {'sem': lexicon[letter]['sem']}
                return x
            if w == 'P':
                x = {'sem': lexicon[letter]['sem'] }
                return x
            if w == 'NAME':
                x = {'sem': lexicon[letter]['sem'], 'agr' :  lexicon[letter]['agr']}
                return x
            if w=='WH':
                x = {'agr' : lexicon[letter]['agr'] ,'sem': lexicon[letter]['sem']}
                return x
            if w == 'P':
                x = {'sem': lexicon[letter]['sem']}
                return x
            if w == 'AUX':
                x = {'sem': lexicon[letter]['sem']}
                return x
            if w == 'DET':
                x = {'agr': lexicon[letter]['agr'],'sem': lexicon[letter]['sem']}
                return x
            if w == 'ART':
                x = {'agr': lexicon[letter]['agr'],'sem': lexicon[letter]['sem']}
                return x
            if w == 'YN':
                x = {'sem': lexicon[letter]['sem']}
                return x
        if len(h) == 1:
            if h[0][1] == 'NP':
                x = np_n(adding_sematric((query,h[0])))
                return x
            if h[0][1] == 'PP':
                x = pp_p_np(adding_sematric((query,h[0])))
                return x
            if h[0][1] == 'NAME':
                x = np_name(adding_sematric((query,h[0])))
                return x
            if h[0][1] == 'PRO':
                x = np_pro(adding_sematric((query,h[0])))
                return x
            if h[0][1] == 'N':
                x = np_n(adding_sematric((query,h[0])))
                return x
            if h[0][1] == 'WH':
                x = np_wh(adding_sematric((query,h[0])))
                return x
        if len(h) == 2:
            if h[0][1] == 'VP' and h[1][1] == 'VP':
                x,y = adding_sematric((query,h[0])),adding_sematric((query,h[1]))
                z= s_vp_vp(x,y)
                return z
            if h[0][1] == 'NP' and h[1][1] == 'NP':
                x,y = adding_sematric((query,h[0])),adding_sematric((query,h[1]))
                z= np_np_np(x,y)
                return z
            if h[0][1] == 'NP' and h[1][1] == 'VP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z= s_np_vp(x,y)
                return z
            if h[0][1] == 'S' and h[1][1] == 'INESP':
                return adding_sematric((query,h[0]))
            if h[0][1] == 'V' and h[1][1] == 'NP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = vp_v_np(x,y)
                return z
            if h[0][1] == 'V' and h[1][1] == 'PP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = vp_v_pp(x,y)
                return z
            if h[0][1] == 'AUX' and h[1][1] == 'VP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = vp_aux_vp(x,y)
                return z
            if h[0][1] == 'P' and h[1][1] == 'NP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = pp_p_np(x,y)
                return z
            if h[0][1] == 'PP' and h[1][1] == 'PP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = pp_pp_pp(x,y)
                return z
            if h[0][1] == 'DET' and h[1][1] == 'NP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = np_det_np(x,y)
                return z
            if h[0][1] == 'ART' and h[1][1] == 'NP':
                x,y = adding_sematric((query,h[0])) , adding_sematric((query,h[1]))
                z = np_art_np(x,y)
                return z
           
        if len(h)==3:
            x,y,z = adding_sematric((query,h[0])) , adding_sematric((query,h[1])),adding_sematric((query,h[2]))
            za = s_np_vp_yn(x,y,z)
            return za
            
    queries_sematric= []
    for q in queries:
        translate_s = translate_sentence(q,lexicon)[0]
        s = [a[0] for a in translate_s]
        root = bottom_up_parser(s)
        a = adding_sematric((translate_s,root))
        queries_sematric+=[[q,translate_s,root,a]]
    return queries_sematric

def print_tree(tree,write_txt):
    if tree:
        samelevel = []
        newlevel = []
        for s,w,e,r,h in tree:
            samelevel += [s,w,e]
            newlevel += h
        print_tree((newlevel),write_txt)
        write_txt.write(str(samelevel) + '\n')

queries_semantic = semantic_relationship()

p2= './output/p2-p-p2.txt'
codecs.open(p2,mode ='w')
write_p2 = codecs.open(p2, encoding= 'utf-8' ,mode ='a')

p4= './output/p2-p-p4.txt'
codecs.open(p4,mode ='w')

write_p4 = codecs.open(p4, encoding= 'utf-8' ,mode ='a')
for c, query in enumerate(queries_semantic):
    q ,s ,root , a = query
    write_p4.write(str(c+1) + '. '+str(q) + '\n')
    write_p4.write(str(s)+ '\n')
    write_p4.write(str(a)+ '\n')
    write_p4.write('-------------------------------------------------------------------------------\n')
    write_p2.write(str(c+1)+'. ' + str(q) +'\n')
    write_p2.write(str(s) +'\n')
    print_tree(root[4],write_p2)
    write_p2.write(str([root[0],root[1],root[2]])+'\n')
    write_p2.write('-------------------------------------------------------------------------------\n')

def string_to_list(s):
    stack = [[]]
    i = 0
    while i < len(s):
        if s[i] == '(':
            stack.append([])
            i += 1
        elif s[i] == ')':
            sublist = stack.pop()
            if stack:
                stack[-1].append(sublist)
            i += 1
        else:
            # Extracting name
            name = ''
            while i < len(s) and s[i] != '(' and s[i] != ')':
                name += s[i]
                i += 1
            stack[-1].append(name.strip())
    return stack[0][0]

# def handle_r(r, answer):
#     if isinstance(r,list):
#         return 
#     else:

# def query_answer(data,query_semantic):
#     tour = False
#     departure = False
#     departure_time = False
#     arrival = False
#     arrival_time = False
#     run_time = False
    
#     answer = [tour,departure,departure_time,arrival,arrival_time,run_time]
#     r,l =queries_semantic
            
            
    

# for q in queries_semantic:
#     if q[3]['inv'] :
#         sem_list = string_to_list(q[3]['sem'])
#         query_answer(database, sem_list)
#     else:
#         print("That was not a query.")
    
