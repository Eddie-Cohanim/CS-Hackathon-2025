# -*- coding: UTF‑8 -*-
from typing import Dict, List

def get_subject_keywords() -> dict[str, List[str]]:
    SUBJECT_KEYWORDS: Dict[str, List[str]] = {
        # ── Governance & politics ──────────────────────────────────────────────
        "politics": [
            "politics","political","policy","governance","government","administration",
            "public administration","public policy","regulation","regulatory","legislation",
            "legislative","bill","act","statute","ordinance","lawmaker","lobby","lobbying",
            "parliament","congress","senate","house of representatives","committee",
            "minister","cabinet","secretary","governor","mayor","president","prime minister",
            "election","campaign","ballot","vote","referendum","diplomacy","diplomatic",
            "foreign policy","geopolitics","constitution","democracy","republican","democratic"
        ],

        # ── Finance & economy ──────────────────────────────────────────────────
        "finance": [
            "finance","financial","finances","fiscal","budget","budgetary","appropriation",
            "economy","economic","macroeconomic","microeconomic","gdp","gni","inflation",
            "deflation","cpi","pricing index","interest","interest rate","deficit","surplus",
            "revenue","tax","taxes","taxation","income tax","property tax","tariff","customs",
            "trade","export","import","balance of trade","monetary","bank","banking","central bank",
            "federal reserve","credit","debit","loan","mortgage","bond","treasury","equity",
            "stock","share","market","stock market","exchange","dow","nasdaq","s&p","index",
            "investment","invest","investor","venture capital","vc","private equity","fund",
            "fintech","insurance","pension","retirement fund","accounting","audit","auditing",
            "subsidy","grant","stimulus","bailout","crypto","cryptocurrency","bitcoin",
            "ethereum","blockchain","statistics","data series","textiles"        # ← kept your extra words
        ],

        # ── Health & medicine ──────────────────────────────────────────────────
        "health": [
            "health","healthcare","public health","medical","medicine","clinical","clinic",
            "hospital","emergency room","er","icu","nurse","physician","doctor","surgeon",
            "pharmacy","pharmaceutical","drug","medication","prescription","vaccine",
            "vaccination","immunization","therapy","treatment","diagnosis","diagnose",
            "disease","illness","condition","symptom","infection","virus","viral","bacteria",
            "bacterial","pandemic","epidemic","outbreak","covid","sars‑cov‑2","flu",
            "influenza","cancer","oncology","cardiology","neurology","mental health",
            "psychology","psychiatry","depression","anxiety","wellness","nutrition",
            "diet","obesity","fitness","exercise","rehabilitation","mortality","life expectancy"
        ],

        # ── Science & technology ───────────────────────────────────────────────
        "technology": [
            "technology","tech","high‑tech","information technology","it","software","hardware",
            "computer","computing","cpu","gpu","semiconductor","chip","microchip","algorithm",
            "code","coding","programming","developer","engineering","data","dataset","database",
            "big data","data science","analytics","analysis","cloud","cloud computing","saas",
            "iaas","paas","cyber","cybersecurity","security breach","hack","hacking","malware",
            "virus","worm","phishing","ai","artificial intelligence","machine learning",
            "deep learning","neural network","nlp","llm","chatbot","robot","robotics","automation",
            "iot","internet of things","smart device","sensor","blockchain","ledger",
            "cryptography","augmented reality","ar","virtual reality","vr","mixed reality",
            "quantum","quantum computing","startup","innovation","research","r&d","patent",
            "gadget","smartphone","mobile app","app","app store","api","open source","opensource"
        ],

        # ── Sports & recreation ────────────────────────────────────────────────
        "sports": [
            "sport","sports","sporting","game","match","fixture","tournament","league","cup",
            "championship","playoff","final","semi‑final","competition","contest","athlete",
            "player","team","club","coach","manager","referee","umpire","stadium","arena",
            "score","scored","goal","points","win","loss","draw","record","medal","podium",
            "olympic","olympics","paralympic","athletics","track","field","marathon",
            "football","soccer","nba","basketball","baseball","mlb","cricket","hockey",
            "nhl","rugby","tennis","golf","cycling","swimming","gymnastics","skiing",
            "snowboard","surf","motorsport","formula 1","nascar","boxing","mma","ufc",
            "wrestling","esports","gaming","fitness","workout"
        ],

        # ── Education ──────────────────────────────────────────────────────────
        "education": [
            "education","educational","school","primary school","elementary","middle school",
            "high school","secondary","college","university","campus","student","pupil",
            "undergraduate","postgraduate","graduate","doctoral","phd","professor","teacher",
            "instructor","faculty","staff","curriculum","syllabus","course","class","lesson",
            "lecture","seminar","tutorial","lab","laboratory","exam","examination","test",
            "assessment","grading","homework","assignment","degree","diploma","certificate",
            "scholarship","loan forgiveness","tuition","enrollment","admission","literacy",
            "numeracy","stem","science education","distance learning","e‑learning","online course"
        ],

        # ── Environment & climate ──────────────────────────────────────────────
        "environment": [
            "environment","environmental","ecology","ecosystem","climate","climate change",
            "global warming","carbon","co2","greenhouse","emission","carbon dioxide",
            "methane","pollution","air quality","water quality","waste","garbage","recycling",
            "compost","plastic","biodiversity","wildlife","species","conservation",
            "endangered","forest","forestry","deforestation","reforestation","tree planting",
            "habitat","wetland","river","lake","ocean","marine","sustainability","sustainable",
            "renewable","renewables","renewable energy","solar","wind","hydro","geothermal",
            "clean energy","energy efficiency","electric vehicle","ev","carbon offset"
        ],

        # ── Transportation & infrastructure ────────────────────────────────────
        "transportation": [
            "transport","transportation","transit","traffic","road","highway","bridge",
            "tunnel","rail","railway","train","metro","subway","tram","bus","station",
            "airport","flight","airline","aviation","runway","port","harbor","shipping",
            "freight","logistics","cargo","supply chain","truck","vehicle","car","automobile",
            "motor","motorway","bike","bicycle","scooter","pedestrian","commute","commuting",
            "rideshare","uber","lyft","public transport","infrastructure"
        ],

        # ── Energy ─────────────────────────────────────────────────────────────
        "energy": [
            "energy","power","electricity","power plant","grid","utility","generation",
            "distribution","transmission","oil","petroleum","gas","natural gas","lng",
            "coal","fossil fuel","nuclear","nuclear power","uranium","reactor",
            "renewable","renewables","solar","photovoltaic","pv","wind","onshore wind",
            "offshore wind","hydro","hydroelectric","dam","geothermal","biofuel","biomass",
            "battery","storage","energy storage","smart grid","efficiency","demand response"
        ],

        # ── Agriculture & food ────────────────────────────────────────────────
        "agriculture": [
            "agriculture","agricultural","farm","farming","farmer","farmland","ranch",
            "field","crop","crops","harvest","yield","irrigation","soil","fertile","fertilizer",
            "pesticide","herbicide","seed","grain","wheat","corn","maize","rice","soy",
            "soybean","barley","oat","livestock","cattle","cow","beef","dairy","milk",
            "goat","sheep","lamb","pig","pork","poultry","chicken","turkey","egg","fishery",
            "aquaculture","horticulture","greenhouse","organic","agribusiness","food security"
        ],

        # ── Labour & employment ───────────────────────────────────────────────
        "labor": [
            "labor","labour","employment","employ","employee","employer","job","jobs",
            "workforce","worker","work","occupation","profession","industry","sector",
            "wage","salary","pay","minimum wage","income","earning","overtime","benefit",
            "union","trade union","collective bargaining","strike","layoff","redundancy",
            "unemployment","jobless","hiring","recruit","recruitment","vacancy","training",
            "skills","skill development","productivity","workplace","occupational safety"
        ],

        # ── Crime & justice ───────────────────────────────────────────────────
        "crime": [
            "crime","criminal","criminology","law enforcement","police","policing",
            "sheriff","constable","officer","detective","investigation","arrest","custody",
            "charge","indictment","prosecution","prosecutor","district attorney","court",
            "trial","hearing","judge","jury","verdict","sentence","sentencing","prison",
            "jail","inmate","correction","parole","probation","felony","misdemeanor",
            "homicide","murder","manslaughter","assault","battery","theft","larceny",
            "robbery","burglary","fraud","embezzlement","corruption","bribery","money laundering",
            "drug trafficking","narcotic","terrorism","cybercrime","violence","violent crime",
            "victim","forensic","dna evidence"
        ],

        # ── Immigration & population ──────────────────────────────────────────
        "immigration": [
            "immigration","immigrant","migrant","migration","emigration","visa",
            "residency","residence","citizenship","naturalization","refugee","asylum",
            "asylum seeker","border","border control","customs","deportation","detention",
            "green card","passport","work permit","labor migration","undocumented"
        ],

        # ── Social welfare ────────────────────────────────────────────────────
        "social_welfare": [
            "welfare","social welfare","social security","benefit","benefits","allowance",
            "subsidy","public assistance","assistance","aid","grant","pension","retirement",
            "disability","disability benefit","snap","food stamp","food assistance",
            "medicaid","medicare","health insurance","insurance coverage","affordable housing",
            "housing","homeless","homelessness","poverty","low income","income support",
            "child care","day care","family support","universal credit","basic income"
        ],

        # ── Defence & military ────────────────────────────────────────────────
        "defence": [
            "defense","defence","military","armed forces","army","navy","air force",
            "marine","marines","coast guard","national guard","soldier","troop","veteran",
            "weapon","arms","armament","missile","rocket","drone","fighter jet","tank",
            "artillery","war","conflict","battle","operation","mission","counterterrorism",
            "nato","alliance","security","homeland security","intelligence","surveillance",
            "espionage","cyberwarfare","peacekeeping"
        ],

        # ── Culture & entertainment ───────────────────────────────────────────
        "culture": [
            "culture","cultural","art","arts","painting","sculpture","gallery","museum",
            "exhibition","heritage","history","historical","theatre","theater","drama","play",
            "film","movie","cinema","screening","television","tv","series","show","streaming",
            "netflix","disney+","hulu","amazon prime","music","concert","festival","song",
            "album","record","band","orchestra","opera","dance","ballet","literature",
            "book","novel","poetry","poem","author","writer","celebrity","pop culture",
            "video game","gaming","esports","comic","animation"
        ]
    }
    return SUBJECT_KEYWORDS
