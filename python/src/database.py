database = {
    "tours": {
        "PQ": {"name": "Phú Quốc", "transport": "airplane"},
        "DN": {"name": "Đà Nẵng", "transport": "airplane"},
        "NT": {"name": "Nha Trang", "transport": "train"}
    },
    "schedule": {
        "PQ": [
            {"departure": "HCMC", "departure_time": "7AM 1/7", "arrival": "PQ", "arrival_time": "9AM 1/7", "runtime": "2:00 HR"},
            {"departure": "HCMC", "departure_time": "8AM 5/7", "arrival": "PQ", "arrival_time": "10AM 5/7", "runtime": "2:00 HR"}
        ],
        "DN": [
            {"departure": "HCMC", "departure_time": "7AM 1/7", "arrival": "DN", "arrival_time": "9AM 1/7", "runtime": "2:00 HR"},
            {"departure": "HCMC", "departure_time": "7AM 4/7", "arrival": "DN", "arrival_time": "9AM 4/7", "runtime": "2:00 HR"}
        ],
        "NT": [
            {"departure": "HCMC", "departure_time": "7AM 1/7", "arrival": "NT", "arrival_time": "12AM 1/7", "runtime": "5:00 HR"},
            {"departure": "HCMC", "departure_time": "7AM 5/7", "arrival": "NT", "arrival_time": "12AM 5/7", "runtime": "5:00 HR"}
        ]
    }
}

def expand_database(new_entry, database):
    new_entry_parts = new_entry.strip("()").split()
    departure = new_entry_parts[1]
    destination = new_entry_parts[2]
    departure_time = new_entry_parts[3]
    arrival_time = new_entry_parts[5]
    runtime = str(int(arrival_time.split(':')[0]) - int(departure_time.split(':')[0])) + ':' + str(int(arrival_time.split(':')[1]) - int(departure_time.split(':')[1])) + ' HR'

    # Update the schedule in the database
    if destination in database["schedule"]:
        database["schedule"][destination].append({
            "departure": departure,
            "departure_time": departure_time,
            "arrival": destination,
            "arrival_time": arrival_time,
            "runtime": runtime
        })
    else:
        database["schedule"][destination] = [{
            "departure": departure,
            "departure_time": departure_time,
            "arrival": destination,
            "arrival_time": arrival_time,
            "runtime": runtime
        }]

# new_data = "(DTIME NT HCMC '9AM 5/7') (ATIME NT NT '15AM 5/7')"
# expand_database(new_data, database)

lexicon = {
    'em': {'type': 'N', 'agr': '2s', 'sem': 'EM1'},
    'có': {'type': 'V', 'subcat': 'np', 'subj': '?subj', 'obj': '?obj', 'sem': '(CO1)'},
    'tất cả': {'type': 'DET', 'agr': '3p', 'sem': 'TATCA1'},
    'các': {'type': 'ART', 'agr': '3p', 'sem': 'CAC1'},
    'tour': {'type': 'N', 'agr': '3s', 'sem': 'TOUR1'},
    'được không': {'type': 'YN', 'sem': 'DUOCKHONG1'},
    'đi': {'type': 'V', 'subcat': 'np', 'subj': '?subj', 'obj': '?obj', 'sem': '(DI1)'},
    'từ': {'type': 'P', 'pform': 'TU', 'sem': 'TU1'},
    'hồ chí minh': {'type': 'NAME', 'agr': '3s', 'sem': 'HCM1'},
    'tới': {'type': 'P', 'pform': 'TOI', 'sem': 'TOI'},
    'nha trang': {'type': 'NAME', 'agr': '3s', 'sem': 'NT1'},
    'hết': {'type': 'V', 'subcat': 'np', 'subj': '?subj', 'obj': '?obj', 'sem': '(HET1)'},
    'bao lâu': {'type': 'WH', 'agr': '3s', 'sem': 'BAOLAU1'},
    'đà nẵng': {'type': 'NAME', 'agr': '3s', 'sem': 'DN1'},
    'bao nhiêu': {'type': 'WH', 'agr': '3s', 'sem': 'BAONHIEU1'},
    'phú quốc': {'type': 'NAME', 'agr': '3s', 'sem': 'PQ1'},
    'vậy': {'type': 'INES' ,'sem': 'VAY1'},
    'bạn': {'type': 'PRO', 'agr': '2s', 'sem': 'BAN1'},
    'bằng': {'type': 'P', 'pform': 'BANG', 'sem': 'BY'},
    'phương tiện': {'type': 'N', 'agr': '3s', 'sem': 'PHUONGTIEN1'},
    'gì': {'type': 'WH', 'agr': '3s', 'sem': 'GI1'},
    'những': {'type': 'ART', 'agr': '3p', 'sem': 'CAC1'},
    'ngày nào': {'type': 'WH', 'agr': '3s', 'sem': 'NGAYNAO1'},
    'nhỉ': {'type': 'INES' ,'sem': 'NHI1'},
    'có thể': {'type': 'AUX', 'subcat': 'v', 'sem': 'COTHE1'},
    'nhắc lại': {'type': 'V', 'subcat': 'np', 'subj': '?subj', 'obj': '?obj', 'sem': '(NHACLAI1)'}
}



rules ={
    ('VP','VP')     :'S',
    ('NP','VP','YN'):'S',
    ('NP','VP')     :'S',
    ('S','INESP')   :'S',
    ('NP','NP')     :'NP',
    ('INES', 'PRO') :'INESP',
    ('V','NP')      :'VP',
    ('WH',)         :'NP',
    ('AUX','VP')    :'VP',
    ('V','PP')      :'VP',
    ('PP','PP')     :'PP',
    ('P','NP')      :'PP',
    ('DET', 'NP')   :'NP',
    ('ART','NP')     :'NP',
    ('NAME',)       :'NP',
    ('N',)          :'NP',
    ('PRO',)        :'NP',
    ('INES',)       :'INESP'
}

# NP VAR ?v SEM(PRO v ?sempro) -> (PRO SEM? sempro ) 1
def np_pro(pro):
    return {'type': 'NP' ,'agr': pro['agr'] , 'sem' : '('+'PRO ' +pro['sem']+')', 'inv' : False}

# NP VAR ?v SEM(N v ?semn) -> (N SEM ?semn) 2
def np_n(n):
    return {'type': 'NP', 'agr': n['agr'], 'sem': '(' +'N '+ n['sem']+')', 'inv': False}

# NP VAR ?v SEM( NAME v ?semname) -> NAME SEM ?semname 3
def np_name(name):
    return {'type': 'NP', 'agr': name['agr'], 'sem':'(' +'NAME' + ' '+name['sem']+')', 'inv': False}

# NP VAR ?v SEM(?semant v (?semn)) -> (ART SEM ?semart) (N SEM ?semn ) 4
def np_art_np(art, np):
    return {'type': 'NP', 'agr': art['agr'], 'sem': '('+art['sem'] + np['sem']+')', 'inv': False}

# NP VAR ?v SEM(?sendet v (?semnp)) -> (DET SEM ?sendet) ( NP SEM? semnp) 5
def np_det_np(det, np):
    return {'type': 'NP', 'agr': det['agr'], 'sem': '('+det['sem']  + np['sem']+')', 'inv': np['inv']}

#PP PFORM ?pform SEM(lambda x (?semp x ?semnp)) -> ( P SEM ?semp ) ( NP SEM ?semnp) 6
def pp_p_np(p,np):
    return { 'agr': np['agr'] , 'inv': np['inv'] , 'sem': '('+p['sem']  +np['sem']+')' }

# PP SEM (&(?sempp1 ?sempp2 ))-> (PP SEM ?semp) (PP SEM ?sempp ) 7
def pp_pp_pp(pp1,pp2):
    return {'sem' : '('+'&(' + pp1['sem']  +pp2['sem'] +')'+')','inv': pp1['inv'],'agr' : pp1['agr']}

# VP  SEM(lambda x(?semv ?v x ?sempp)) -> (V_np_pp: on SEM ?semv) ( PP PROM SEM ?semp) 8
def vp_v_pp(v, pp):
    return {'inv' : pp['inv'], 'agr' : pp['agr'], 'sem' : '('+v['sem'] + pp['sem']+')'}

# VP SEM(lambda x(?semaux(?semvp x ))) -> ( AUX SUBCAT ?v SEM ?semaux ) ( VP VFORM ?s SEM ?semvp ) 9
def vp_aux_vp(aux, vp):
    return {'inv': vp['inv'], 'agr': vp['agr'], 'sem': '('+aux['sem'] + vp['sem']+')' }

# NP INV+ WH ?q VAR ?v SEM(WH ?v semwh ) -> (WH SEM ?semwh) 10
def np_wh(wh):
    return {'inv': True, 'sem': '(WH '  + wh['sem']+')','agr' : wh['agr']}

# VP VAR ?v SEM(lambda x (?semv x ?semnp))-> (V_np SEM ?semv) ( NP SEM ?semnp)
def vp_v_np(v, np):
    return {'sem': '(' +v['sem']  + np['sem']+')', 'agr' : np['agr'] , 'inv' : np['inv']}

def np_np_np(np1,np2):
    return {'sem' : "(" + np1['sem'] + np2['sem']  + ")", 'agr' : '3p', 'inv' : True if np1['inv']+np2['inv'] else False }

# S SEM (?semvp ?semnp ) -> (NP SEM ?semnp ) (UP SEM ?semvp ) 11
def s_np_vp(np, vp):
    return {'sem': '('+ vp['sem'] + np['sem']+')','agr': np['agr'], 'inv': True if np['inv'] + vp['inv'] else False}

# S INV+ SEM (?semwh ( Semup Semnp )) -> (NP SEM ?semnp) ( VP SEM ?Semvp) ( WH SEM ?semwh ) 12
def s_np_vp_yn(np,vp,yn):
    return {'inv': True,'agr': np['agr'], 'sem': '('+yn['sem'] + '('+vp['sem']  + np['sem'] + ')'+')'}

# S SEM (semvp2? semvp2 ?) -> (VP SEM ?semvp ) (VP SEM ?semvp) 13
def s_vp_vp(vp1,vp2):
    return {'sem': '('+vp1['sem'] + vp2['sem']+')','agr': '3s', 'inv': True if vp1['inv'] + vp2['inv'] else False}