# -*- coding: utf-8 -*-
import json
import re
import urllib.request 
from urllib.parse import quote

# variables to help formatting of input url
core = 'CovidTweets'
or_seperator = "%20OR%20"
and_seperator = "%20AND%20"
pois = ["CDCgov", "JoeBiden", "KamalaHarris", "BarackObama", "tedcruz","HHSGov",
"MoHFW_INDIA", "narendramodi", "RahulGandhi", "AmitShah", "ArvindKejriwal",
"SSalud_mx", "lopezobrador_", "m_ebrard", "PRI_Nacional", "PRDMexico", "rodrigobocardi"]

covid_keywords = ["quarentena", "hospital", "covidresources", "rt-pcr", "वैश्विकमहामारी", "oxygen", "सुरक्षित रहें", "stayhomestaysafe", 
"covid19", "quarantine", "मास्क", "face mask", "covidsecondwaveinindia", "flattenthecurve", "corona virus", "wuhan", "cierredeemergencia", "autoaislamiento", 
"sintomas", "covid positive", "casos", "कोविड मृत्यु", "स्वयं चुना एकांत", "stay safe", "#deltavariant", "covid symptoms", "sarscov2", "covidiots", "brote", 
"alcohol en gel", "disease", "asintomático", "टीकाकरण", "encierro", "covidiot", "covidappropriatebehaviour", "fever", 
"pandemia de covid-19", "wearamask", "flatten the curve", "oxígeno", "desinfectante", 
"super-spreader", "ventilador", "coronawarriors", "quedate en casa", "mascaras", "mascara facial", 
"trabajar desde casa", "संगरोध", "immunity", "स्वयं संगरोध", "डेल्टा संस्करण", "mask mandate", "health", 
"dogajkidoori", "travelban", "cilindro de oxígeno", "covid", "staysafe", "variant", 
"yomequedoencasa", "doctor", "एंटीबॉडी", "दूसरी लहर", "distancia social", "मुखौटा", "covid test", 
"अस्पताल", "covid deaths", "कोविड19", "muvariant", "susanadistancia", "personal protective equipment", "remdisivir", "quedateencasa", "asymptomatic", 
"social distancing", "distanciamiento social", "cdc", "transmission", "epidemic", "social distance", "herd immunity", "transmisión", "सैनिटाइज़र", "indiafightscorona", 
"surgical mask", "facemask", "desinfectar", "वायरस", "संक्रमण", "symptoms", "सामाजिक दूरी", "covid cases", "ppe", "sars", "autocuarentena", "प्रक्षालक", "breakthechain", 
"stayhomesavelives", "coronavirusupdates", "sanitize", "covidinquirynow", "कोरोना", "workfromhome", "outbreak", "flu", "sanitizer", "distanciamientosocial", "variante", 
"कोविड 19", "कोविड-19", "covid pneumonia", "कोविड", "pandemic", "icu", "वाइरस", "contagios", "वेंटिलेटर", "washyourhands", "n95", "stayhome", "lavadodemanos", "fauci", 
"रोग प्रतिरोधक शक्ति", "maskmandate", "डेल्टा", "कोविड महामारी", "third wave", "epidemia", "fiebre", "मौत", "travel ban", "फ़्लू", "muerte", "स्वच्छ", "washhands", "enfermedad", 
"contagio", "infección", "faceshield", "self-quarantine", "remdesivir", "oxygen cylinder", "mypandemicsurvivalplan", "कोविड के केस", "delta variant", "wuhan virus", "लक्षण", "corona", "maskup", "gocoronago", "death", "curfew","socialdistance", "second wave", "máscara", "stayathome", "positive", "lockdown", "propagación en la comunidad", "तीसरी लहर", "aislamiento", "rtpcr", "coronavirus", "variante delta", "distanciasocial", "cubrebocas", "घर पर रहें", "socialdistancing", "covidwarriors", "प्रकोप", "covid-19", "stay home","संक्रमित", "jantacurfew", "cowin", "कोरोनावाइरस", "virus", "distanciamiento", "cuarentena", "indiafightscovid19", "healthcare", "natocorona", "मास्क पहनें", "delta", "ऑक्सीजन", "wearmask", "कोरोनावायरस", "ventilator", "pneumonia", "maskupindia", "ppe kit", "sars-cov-2", "testing", "fightagainstcovid19", "महामारी", "नियंत्रण क्षेत्र", "who", "mask", "pandemia", "deltavariant", "वैश्विक महामारी", "रोग", "síntomas", "work from home", "antibodies", "masks", "confinamiento", "flattening the curve", "मुखौटा जनादेश", "thirdwave", "mascarilla", "usacubrebocas", "covidemergency", "inmunidad", "cierre de emergencia", "self-isolation", "स्वास्थ्य सेवा", "सोशल डिस्टन्सिंग", "isolation", "cases", "community spread", "unite2fightcorona", "oxygencrisis", "containment zones", "homequarantine", "स्पर्शोन्मुख", "लॉकडाउन", "hospitalización", "incubation period",
"anticuerpos", "vaccine mandate", "eficacia de la vacuna", "vacuna covid", "covidvaccine", 
"vaccination","booster shot", "dosis de vacuna", "moderna", "campaña de vacunación",  "vacunar", 
"कोविशील्ड",  "टीकाकरण", "वैक्सीनेशन","inyección de refuerzo", "efecto secundario", "inmunización",
"टीका",  "unvaccinated", "खुराक",  "side effect", "रोग प्रतिरोधक शक्ति","कोवैक्सीन", "कोविन", 
"fully vaccinated", "वैक्सीन",  "दुष्प्रभाव", "pfizer","second dose","vacunado","mandato de vacuna",
"remdesivir", "la inmunidad de grupo","एस्ट्राजेनेका","टीका लगवाएं"]

url_prefix = "http://3.21.190.202:8983/solr/{core}/select?q=".format(core = core)
url_suffix = "&wt=json&indent=true&rows=2147483647"
for poi in pois:
    query_string = "poi_name:"+ poi

    inurl = url_prefix + query_string + url_suffix
    data = urllib.request.urlopen(inurl)
    tweets = json.load(data)['response']['docs']
    covid_tweet_count = 0
    non_covid_tweet_count = 0
    for tweet in tweets:
        is_covid_tweet = False;
        for keyword in covid_keywords:
            if keyword in tweet['tweet_text']:
                is_covid_tweet = True
                break
        if(is_covid_tweet):
            covid_tweet_count+=1
        else:
            non_covid_tweet_count+=1
    print(poi, covid_tweet_count, non_covid_tweet_count)

            
        
# final_tweets = []
# result= json.dumps(data)
# for tweet in tweets:
#     #collecting replies
#     replies = json.load(data)['response']['docs']



#context={"text":"test text"}
# return JsonResponse(request,'home.htm',tweets[0],safe=False)
#return render(request,'home.htm',context)