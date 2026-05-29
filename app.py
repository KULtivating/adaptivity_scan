import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import gspread
import streamlit.components.v1 as components
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
import markdown

# ---------------------------
# EMAIL FUNCTIE (MUST BE GLOBAL)
# ---------------------------
def send_email(to_email, subject, body):
    sender_email = st.secrets["gmail_user"]
    sender_password = st.secrets["gmail_password"]

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        
# ---------------------------
# APP CONFIG
# ---------------------------
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Adaptivity Maturiteitsscan",
    layout="wide"
)

col1, col2 = st.columns([4, 1])

with col1:
    st.title("Adaptiviteit Maturiteitsscan")
#   st.markdown("### Hoe futureproof ben jij?")

with col2:
    st.image("logo Coliberate.png", width=100)
    st.image("logo KULtivating.webp", width=100)

# ---------------------------
# GOOGLE SHEETS CONNECTION
# ---------------------------
@st.cache_resource
def connect_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )


    client = gspread.authorize(creds)

    sheet = client.open("Adaptivity Maturiteitsscan").sheet1

    return sheet


sheet = connect_sheet()

# ---------------------------
# SESSION STATE
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------------------
# QUESTION MAP
# ---------------------------
question_map = {
"Ik aanvaard verandering zoals die is.": {"pillar": "VA", "direction": "pos", "block": 2, "code": "CR_CA1"},
"Ik houd mijn weerstand tegen verandering voor mijzelf.": {"pillar": "VA", "direction": "neg", "block": 2, "code": "CR_CD1"},
"Ik trek mij terug uit alles wat met verandering te maken heeft.": {"pillar": "VA", "direction": "neg", "block": 1, "code": "CR_CD3"},
"Ik werk goed mee met plannen voor verandering.": {"pillar": "VA", "direction": "pos", "block": 2, "code": "CR_CA2"},
"Ik verzet mij actief tegen verandering.": {"pillar": "VA", "direction": "neg", "block": 1, "code": "CR_CR1"},
"Ik steun verandering actief.": {"pillar": "VA", "direction": "pos", "block": 2, "code": "CR_CP1"},
"Ik probeer actief om verandering te beïnvloeden of te vertragen.": {"pillar": "VA", "direction": "neg", "block": 1, "code": "CR_CR3"},
"Ik toon uitstelgedrag bij het uitvoeren van verandering.": {"pillar": "VA", "direction": "neg", "block": 1, "code": "CR_CD2"},
"Ik neem zelf initiatief om veranderingen in de praktijk te brengen.": {"pillar": "VA", "direction": "pos", "block": 2, "code": "CR_CP3"},

"Ik ben gemotiveerd om nieuwe dingen te leren.": {"pillar": "LO", "direction": "pos", "block": 2, "code": "LO_M"},
"Ik kan me gemakkelijk aanpassen aan veranderende situaties.": {"pillar": "VZ", "direction": "pos", "block": 2, "code": "Res2"},
"Ik herstel snel wanneer ik te maken krijg met tegenslag.": {"pillar": "VZ", "direction": "pos", "block": 2, "code": "Res3"},
"Ik blijf rustig in situaties waarin ik veel beslissingen moet nemen.": {"pillar": "VZ", "direction": "pos", "block": 2, "code": "IAP_WS1"},
"Ik pas mijn werk gemakkelijk aan nieuwe omstandigheden aan.": {"pillar": "VZ", "direction": "pos", "block": 2, "code": "IAP_R2"},
"Ik pas mijn gedrag graag aan wanneer dat nodig is om goed samen te werken.": {"pillar": "VZ", "direction": "pos", "block": 2, "code": "IAP_I2"},
"Ik volg regelmatig opleidingen op of naast het werk, om mijn vaardigheden up-to-date te houden.": {"pillar": "LO", "direction": "pos", "block": 2, "code": "IAP_T1"},
"Binnen mijn team of afdeling doen mensen een beroep op mij om nieuwe oplossingen aan te reiken.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IAP_C2"},

"Ik ga actief op zoek naar elke kans die mij helpt om mijn functioneren te verbeteren (opleiding, groepsproject, uitwisseling met collega’s, enz.).": {"pillar": "LO", "direction": "pos", "block": 3, "code": "IAP_T2"},
"Ik neem zelf initiatief om te beslissen wat en hoe ik leer.": {"pillar": "LO", "direction": "pos", "block": 3, "code": "LO_A"},

"Ik volg de wereld rondom mij actief op om te zien wat mijn job in de toekomst kan beïnvloeden.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "PB_SS1"},
"Ik denk vooruit over mogelijke veranderingen in mijn organisatie als gevolg van ontwikkelingen in de wereld rondom mij (bv. markt, technologie).": {"pillar": "VV", "direction": "pos", "block": 4, "code": "PB_SS3"},
"Ik probeer werkwijzen en systemen te ontwikkelen die op lange termijn goed werken, ook als dat in het begin wat meer tijd kost.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "PB_PP1"},
"Ik probeer de echte oorzaak te vinden van problemen die zich voordoen.": {"pillar": "VV", "direction": "pos", "block": 3, "code": "PB_PP2"},

"Ik anticipeer op mogelijke problemen door vooraf scenario’s uit te werken en beslissingsopties klaar te hebben voordat ze nodig zijn.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "IAP_Rx"},
"Ik bouw bewust netwerkrelaties op die mij en anderen helpen om toekomstige veranderingen beter op te vangen of te benutten.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "IAP_Ix"},
"Ik zorg voor minder stress in de toekomst door structuren en processen te verbeteren en zo crisis situaties te voorkomen.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "IAP_WSx"},

"Ik bedenk nieuwe manieren om technologie beter te gebruiken in mijn werk.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IBIncr6"},
"Ik ga zelfstandig op zoek naar nieuwe werkwijzen, technieken of hulpmiddelen.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IBRad4"},
"Ik onderneem acties om verandering in mijn werk te realiseren.": {"pillar": "CI", "direction": "pos", "block": 3, "code": "EISB1"},
"Ik bedenk nieuwe manieren van werken voor mijn organisatie.": {"pillar": "CI", "direction": "pos", "block": 3, "code": "EISB4"},
"Ik spreek actief ideeën uit en draag voorstellen aan over hoe mijn organisatie zich kan vernieuwen om met toekomstige veranderingen om te gaan.": {"pillar": "VV", "direction": "pos", "block": 4, "code": "VOICE"},
}

# ---------------------------
# ORDERED QUESTIONS (GECORRIGEERD)
# ---------------------------
question_order = {
"Ik aanvaard verandering zoals die is.": 1,
"Ik houd mijn weerstand tegen verandering voor mijzelf.": 14,
"Ik trek mij terug uit alles wat met verandering te maken heeft.": 24,
"Ik werk goed mee met plannen voor verandering.": 15,
"Ik verzet mij actief tegen verandering.": 2,
"Ik steun verandering actief.": 25,
"Ik probeer actief om verandering te beïnvloeden of te vertragen.": 16,
"Ik toon uitstelgedrag bij het uitvoeren van verandering.": 26,
"Ik neem zelf initiatief om veranderingen in de praktijk te brengen.": 3,

"Ik ben gemotiveerd om nieuwe dingen te leren.": 17,
"Ik kan me gemakkelijk aanpassen aan veranderende situaties.": 4,
"Ik herstel snel wanneer ik te maken krijg met tegenslag.": 13,
"Ik blijf rustig in situaties waarin ik veel beslissingen moet nemen.": 27,
"Ik pas mijn werk gemakkelijk aan nieuwe omstandigheden aan.": 5,
"Ik pas mijn gedrag graag aan wanneer dat nodig is om goed samen te werken.": 28,
"Ik volg regelmatig opleidingen op of naast het werk, om mijn vaardigheden up-to-date te houden.": 6,
"Binnen mijn team of afdeling doen mensen een beroep op mij om nieuwe oplossingen aan te reiken.": 18,

"Ik ga actief op zoek naar elke kans die mij helpt om mijn functioneren te verbeteren (opleiding, groepsproject, uitwisseling met collega’s, enz.).": 7,
"Ik neem zelf initiatief om te beslissen wat en hoe ik leer.": 23,

"Ik volg de wereld rondom mij actief op om te zien wat mijn job in de toekomst kan beïnvloeden.": 12,
"Ik denk vooruit over mogelijke veranderingen in mijn organisatie als gevolg van ontwikkelingen in de wereld rondom mij (bv. markt, technologie).": 8,
"Ik probeer werkwijzen en systemen te ontwikkelen die op lange termijn goed werken, ook als dat in het begin wat meer tijd kost.": 19,
"Ik probeer de echte oorzaak te vinden van problemen die zich voordoen.": 29,

"Ik anticipeer op mogelijke problemen door vooraf scenario’s uit te werken en beslissingsopties klaar te hebben voordat ze nodig zijn.": 9,
"Ik bouw bewust netwerkrelaties op die mij en anderen helpen om toekomstige veranderingen beter op te vangen of te benutten.": 32,
"Ik zorg voor minder stress in de toekomst door structuren en processen te verbeteren en zo crisis situaties te voorkomen.": 10,

"Ik bedenk nieuwe manieren om technologie beter te gebruiken in mijn werk.": 22,
"Ik ga zelfstandig op zoek naar nieuwe werkwijzen, technieken of hulpmiddelen.": 31,
"Ik onderneem acties om verandering in mijn werk te realiseren.": 11,
"Ik bedenk nieuwe manieren van werken voor mijn organisatie.": 30,
"Ik spreek actief ideeën uit en draag voorstellen aan over hoe mijn organisatie zich kan vernieuwen om met toekomstige veranderingen om te gaan.": 21
}

# ---------------------------
# ORDER QUESTIONS (single source of truth)
# ---------------------------

questions = sorted(question_order, key=question_order.get)

scale_labels = [
    "1 - Nooit",
    "2 - Zeer zelden",
    "3 - Zelden",
    "4 - Soms",
    "5 - Regelmatig",
    "6 - Vaak",
    "7 - Altijd"
]

scale_values = list(range(1, 8))

# ---------------------------
# SCORING
# ---------------------------
def compute_scores(answers):
    rows = []

    for q, score in answers.items():
        meta = question_map[q]
        pillar = meta["pillar"]
        block = meta["block"]
        direction = meta["direction"]

        if direction == "neg":
            score = 8 - score

        rows.append({
            "pillar": pillar,
            "block": block,
            "score": score
        })

    df = pd.DataFrame(rows)

    # PILLARS
    pivot = df.groupby("pillar")["score"].mean().reset_index()

    all_pillars = ["VA", "VZ", "LO", "VV", "CI"]
    pivot = (
        pivot.set_index("pillar")
        .reindex(all_pillars)
        .fillna(df["score"].mean())
        .reset_index()
    )
    # BLOCKS
    block_scores = df.groupby("block")["score"].mean().reset_index()

    return pivot, block_scores


def compute_maturity_level(block_scores_df):
    """
    block_scores_df: dataframe met kolommen:
    [block, score]
    """

    scores = dict(zip(block_scores_df["block"], block_scores_df["score"]))

    b1 = scores.get(1, 0)
    b2 = scores.get(2, 0)
    b3 = scores.get(3, 0)
    b4 = scores.get(4, 0)

    # -------------------------
    # BLOCK 1
    # -------------------------
    if b1 < 3.5:
        return 0

    # -------------------------
    # BLOCK 2
    # -------------------------
    if b2 < 4:
        return 1
    elif 4 <= b2 <= 6:
        return 2
    # alleen als b2 > 6 ga je verder

    # -------------------------
    # BLOCK 3
    # -------------------------
    if b3 < 4:
        return 2
    elif 4 <= b3 <= 6:
        return 3
    # alleen als b3 > 6 ga je verder

    # -------------------------
    # BLOCK 4
    # -------------------------
    if b4 < 4:
        return 3
    elif 4 <= b4 <= 6:
        return 4
    else:
        return 5


def feedback(level):
    texts = {
        0: """
Je hebt een duidelijke voorkeur voor vertrouwde manieren van werken en dat is heel begrijpelijk. Verandering vraagt energie, brengt onzekerheid mee en kan soms voelen alsof je grip verliest. Jouw kritische blik is daarbij ook waardevol: je voelt vaak snel aan wanneer iets nog niet klopt of onvoldoende doordacht is. Dat helpt om veranderingen niet zomaar blind te volgen.

Verandering kan echter ook kansen bieden en is vaak noodzakelijk om vooruit te kunnen. Een volgende stap kan zijn om vaker te onderzoeken wat een verandering jou of je werk kan opleveren. Kleine experimenten helpen hierbij: eerst voorzichtig proberen, daarna evalueren wat het effect is. Door je bezorgdheden iets sneller bespreekbaar te maken, vergroot je ook je invloed op hoe verandering vorm krijgt.

### Volgende stappen:
- weerstand sneller benoemen en bespreekbaar maken
- één kleine verandering bewust uitproberen
- onderzoeken wat een verandering kan opleveren
- minder afwachten, meer verkennen

### Eerste kleine stap
Kies één kleine verandering deze week en observeer bewust wat er gebeurt wanneer je die volgt in plaats van tegenhoudt.
""",

        1: """
Je accepteert verandering meestal correct en professioneel. Je werkt mee wanneer dat nodig is en zorgt ervoor dat het werk blijft doorlopen. Dat is een belangrijke en vaak onderschatte basis, omdat je stabiliteit en betrouwbaarheid brengt in een veranderende omgeving. Mensen rondom jou kunnen op je rekenen.

Je volgende groeistap ligt in het actiever vormgeven van verandering. Niet alleen uitvoeren wat gevraagd wordt, maar ook nadenken over hoe jij je eigen aanpak kan verbeteren of aanpassen. Door kleine initiatieven te nemen, verschuif je van “meewerken” naar “mee vormgeven”.

### Volgende stappen:
- bewust reflecteren op je eigen aanpak
- sneller nieuwe werkwijzen uitproberen
- vragen stellen over waarom iets verandert
- kleine verbeteringen zelf voorstellen

### Eerste kleine stap
Vraag bij één verandering actief door hoe je je werkwijze best kan aanpassen.
""",

        2: """
Je past je goed aan wanneer verandering zich voordoet. Je schakelt wanneer nodig, leert nieuwe situaties kennen en blijft goed functioneren onder druk. Dat toont veerkracht en leervermogen. Je hebt de houding van iemand die zegt: “als het verandert, dan vind ik mijn weg wel.”

De volgende stap is om niet alleen te reageren op verandering, maar ze ook vroeger te zien aankomen. Door signalen sneller op te pikken en je vooraf voor te bereiden, vergroot je je impact en je rust in nieuwe situaties.

### Volgende stappen:
- sneller alternatieven bedenken
- signalen van verandering vroeger oppikken
- proactiever opleidingen of kennis zoeken
- bewuster vooruitdenken bij nieuwe situaties

### Eerste kleine stap
Neem in één complexe situatie bewust een stap terug om meerdere opties te overwegen.
""",

        3: """
Je schakelt flexibel tussen situaties en weet goed wat nodig is om resultaat te behalen. Je blijft meestal rustig onder druk, denkt in oplossingen en past je gedrag effectief aan. Dat maakt je een betrouwbare kracht in een dynamische omgeving.

Je groeikans ligt in het nog sterker vooruitdenken in plaats van enkel goed reageren. Door patronen te herkennen en eerder te anticiperen op wat kan komen, kan je meer richting geven in plaats van enkel mee te bewegen.

### Volgende stappen:
- vaker vooruitdenken in scenario’s
- structurele oorzaken van problemen analyseren
- actief nieuwe vaardigheden ontwikkelen vóór ze nodig zijn
- kansen zien in verandering, niet alleen oplossingen

### Eerste kleine stap
Kies één ontwikkeling in je werkveld en bekijk wat deze binnen 6 maanden zou kunnen veranderen aan jouw job of taken.
""",

        4: """
Je denkt vooruit en bereidt je bewust voor op toekomstige veranderingen. Je ontwikkelt vaardigheden op voorhand, bouwt sterke netwerken en zoekt duurzame oplossingen. Je wacht niet af, maar helpt verandering mee vorm te geven. Dat toont eigenaarschap, maturiteit en strategisch inzicht.

De volgende stap ligt in nog meer experimenteren zonder directe noodzaak: niet alleen voorbereiden op wat waarschijnlijk komt, maar ook leren en ontwikkelen voor wat nog onbekend is. Zo versterk je je adaptiviteit verder.

### Volgende stappen:
- experimenteren zonder onmiddellijke aanleiding
- bewust leren buiten de huidige context
- nieuwe mogelijkheden verkennen zonder zeker doel
- anderen inspireren en meenemen in verandering

### Eerste kleine stap
Volg één opleiding waarvan je op voorhand nog niet weet of ze direct bruikbaar is voor je huidige taken en evalueer wat je ervan leert.
""",

        5: """
Je beweegt niet alleen mee met verandering, je helpt ze actief creëren. Je leert continu, ook zonder directe aanleiding, en denkt in mogelijkheden eerder dan in beperkingen. Je hebt een hoge tolerantie voor onzekerheid en gebruikt verandering als motor voor groei. Daarmee ben je vaak ook een inspirerend voorbeeld voor anderen.

Jouw verdere ontwikkeling ligt hier niet zozeer in “meer”, maar in verdieping: hoe kan jouw aanpak nog meer anderen versterken? Jouw grootste impact zit vaak in het begeleiden, inspireren en versterken van de omgeving rond jou.

### Werkpunten voor verdere verdieping:
- anderen coachen in verandering en groei
- leerprocessen explicieter delen met collega’s
- ruimte creëren voor experiment binnen het team
- verandering op organisatieniveau helpen sturen

### Eerste kleine stap
Kies één collega of team en help hen bewust om één verandering beter te begrijpen, aan te pakken of te versnellen.
"""
    }

    return texts.get(level, "Geen feedback beschikbaar voor dit niveau.")

pillar_labels = {
    "VA": "Veranderattitude",
    "VZ": "Veerkracht<br>& Zelfregulatie",
    "LO": "Leermotivatie<br>& Ontwikkeling",
    "VV": "Vooruitzien<br>& Voorbereiden",
    "CI": "Creativiteit<br>& Innovatie"
}

def radar_plot(pivot):

    pivot = pivot.copy()
    pivot["pillar_label"] = pivot["pillar"].map(pillar_labels)

    fig = px.line_polar(
        pivot,
        r="score",
        theta="pillar_label",
        line_close=True,
        range_r=[1, 7]
    )

    fig.update_traces(fill="toself")

    fig.update_layout(
        margin=dict(l=100, r=100, t=40, b=40),
        polar=dict(
            angularaxis=dict(
                tickangle=0  # or -45 for long labels
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)

pillar_data = {
    "VA": {
        "title": "Veranderattitude",
        "description": (
            "Deze pijler beschrijft hoe jij emotioneel, cognitief en gedragsmatig reageert op verandering in je werkomgeving. "
            "Het gaat niet alleen om of je verandering accepteert, maar ook in welke mate je deze actief ondersteunt, beïnvloedt of net probeert te vermijden. "
            "Dit varieert van weerstand en terughoudendheid tot actieve betrokkenheid en het zelf mee vormgeven van verandering."
        ),
         "score_meaning": {
            "low": (
                "Je scoort eerder laag op Veranderattitude. Dit betekent dat je verandering vaak als lastig, onzeker of bedreigend ervaart "
                "en dat je de neiging hebt om vast te houden aan vertrouwde werkwijzen. In verandertrajecten neem je meestal een afwachtende of terughoudende houding aan "
                "en je vermijdt of vertraagt verandering eerder dan dat je ze actief ondersteunt."
            ),
            "mid": (
                "Je scoort gemiddeld op Veranderattitude. Dit betekent dat je doorgaans een neutrale tot redelijk open houding hebt tegenover verandering. "
                "Je werkt mee wanneer verandering gevraagd of opgelegd wordt, maar je neemt zelf zelden het initiatief om verandering actief te ondersteunen of te versnellen."
            ),
            "good": (
                "Je scoort eerder hoog op Veranderattitude. Dit betekent dat je meestal open en constructief staat tegenover verandering en deze actief ondersteunt wanneer ze zich voordoet. "
                "Je denkt mee over hoe verandering kan worden uitgevoerd en draagt regelmatig bij aan een vlotte implementatie."
            ),
            "high": (
                "Je scoort zeer hoog op Veranderattitude. Dit betekent dat je verandering niet alleen accepteert, maar vaak ook actief initieert en mee vormgeeft. "
                "Je neemt regelmatig een trekkersrol op in veranderprocessen en probeert verandering te stimuleren, versnellen of verbeteren."
            )
        }
    },
 "VZ": {
        "title": "Veerkracht & Zelfregulatie",
        "description": (
            "Deze pijler beschrijft hoe goed je functioneert onder druk, in veranderende omstandigheden en bij tegenslagen. "
            "Het gaat zowel over emotionele veerkracht (hoe je stress en druk verwerkt) als over gedragsmatige flexibiliteit (hoe snel je je aanpast in concrete situaties)."
        ),
        "score_meaning": {
            "low": (
                "Je scoort eerder laag op Veerkracht & Zelfregulatie. Dit betekent dat je verandering, druk of onverwachte situaties vaak als belastend ervaart "
                "en dat het je tijd kost om je opnieuw aan te passen. Stress kan een duidelijke impact hebben op je functioneren."
            ),
            "mid": (
                "Je scoort gemiddeld op Veerkracht & Zelfregulatie. Dit betekent dat je je in de meeste situaties kan aanpassen, "
                "maar dat je soms bewust tijd, structuur of ondersteuning nodig hebt om goed te blijven functioneren onder druk."
            ),
            "good": (
                "Je scoort eerder hoog op Veerkracht & Zelfregulatie. Dit betekent dat je doorgaans stabiel blijft functioneren onder druk "
                "en je je vlot kan aanpassen aan veranderende omstandigheden en verwachtingen."
            ),
            "high": (
                "Je scoort zeer hoog op Veerkracht & Zelfregulatie. Dit betekent dat je erg goed kan omgaan met druk en verandering, "
                "en dat je snel en flexibel schakelt zonder dat dit je functioneren of emotionele stabiliteit negatief beïnvloedt."
            )
        }
    },

    "LO": {
        "title": "Leermotivatie & Ontwikkeling",
        "description": (
            "Deze pijler beschrijft in welke mate je actief investeert in leren en persoonlijke ontwikkeling. "
            "Dit omvat zowel formele leeractiviteiten zoals opleidingen als informele ontwikkeling zoals feedback gebruiken, zelfstudie en leren in de praktijk."
        ),
        "score_meaning": {
            "low": (
                "Je scoort eerder laag op Leermotivatie & Ontwikkeling. Dit betekent dat je vooral leert wanneer het noodzakelijk is voor je werk "
                "en dat leren eerder een reactieve dan een proactieve activiteit is."
            ),
            "mid": (
                "Je scoort gemiddeld op Leermotivatie & Ontwikkeling. Dit betekent dat je regelmatig gebruikmaakt van leerkansen wanneer ze zich voordoen, "
                "maar dat je ontwikkeling niet altijd actief of systematisch aanstuurt."
            ),
            "good": (
                "Je scoort eerder hoog op Leermotivatie & Ontwikkeling. Dit betekent dat je actief bezig bent met leren en je ontwikkeling "
                "en dat je regelmatig bewust zoekt naar mogelijkheden om je vaardigheden te verbeteren."
            ),
            "high": (
                "Je scoort zeer hoog op Leermotivatie & Ontwikkeling. Dit betekent dat je sterk intrinsiek gemotiveerd bent om te leren "
                "en voortdurend actief op zoek gaat naar nieuwe kansen om jezelf professioneel en persoonlijk te ontwikkelen."
            )
        }
    },

    "VV": {
        "title": "Vooruitzien & Voorbereiden",
        "description": (
            "Deze pijler beschrijft hoe sterk je gericht bent op de toekomst, hoe goed je trends en ontwikkelingen opvolgt "
            "en in welke mate je je systematisch voorbereidt op mogelijke veranderingen en uitdagingen."
        ),
        "score_meaning": {
            "low": (
                "Je scoort eerder laag op Vooruitzien & Voorbereiden. Dit betekent dat je vooral focust op de huidige situatie "
                "en meestal reageert op problemen wanneer ze zich voordoen, eerder dan ze vooraf te anticiperen."
            ),
            "mid": (
                "Je scoort gemiddeld op Vooruitzien & Voorbereiden. Dit betekent dat je soms vooruitdenkt en rekening houdt met mogelijke veranderingen, "
                "maar dat dit niet altijd structureel of systematisch gebeurt."
            ),
            "good": (
                "Je scoort eerder hoog op Vooruitzien & Voorbereiden. Dit betekent dat je regelmatig vooruitdenkt en je bewust voorbereidt op toekomstige ontwikkelingen en mogelijke risico’s."
            ),
            "high": (
                "Je scoort zeer hoog op Vooruitzien & Voorbereiden. Dit betekent dat je sterk proactief werkt met scenario’s, trends en analyses "
                "en dat je structureel anticipeert op toekomstige veranderingen en uitdagingen."
            )
        }
    },

    "CI": {
        "title": "Creativiteit & Innovatie",
        "description": (
            "Deze pijler beschrijft in welke mate je actief nieuwe ideeën, werkwijzen en oplossingen ontwikkelt en implementeert. "
            "Het gaat zowel om creatief denken als om het daadwerkelijk realiseren van verbeteringen en vernieuwing in je werkcontext."
        ),
        "score_meaning": {
            "low": (
                "Je scoort eerder laag op Creativiteit & Innovatie. Dit betekent dat je vooral werkt volgens bestaande methodes "
                "en weinig initiatief neemt om dingen te verbeteren of te vernieuwen."
            ),
            "mid": (
                "Je scoort gemiddeld op Creativiteit & Innovatie. Dit betekent dat je soms meedenkt over verbeteringen "
                "en af en toe ideeën aanbrengt, maar dat je niet structureel vernieuwend bezig bent."
            ),
            "good": (
                "Je scoort eerder hoog op Creativiteit & Innovatie. Dit betekent dat je regelmatig initiatief neemt om processen, werkwijzen of ideeën te verbeteren "
                "en dat je actief bijdraagt aan vernieuwing in je werkomgeving."
            ),
            "high": (
                "Je scoort zeer hoog op Creativiteit & Innovatie. Dit betekent dat je sterk innovatief ingesteld bent en actief nieuwe ideeën ontwikkelt én realiseert "
                "om je werk en organisatie te verbeteren of te vernieuwen."
            )
        }
    }
}

def get_score_explanation(score, meanings):
    if score <= 2:
        return meanings["low"]
    elif score <= 4:
        return meanings["mid"]
    elif score == 5:
        return meanings["good"]
    else:
        return meanings["high"]

st.markdown("""
<style>
div[data-testid="stRadio"] label {
    font-size: 0px; /* verbergt default label maar breekt layout niet */
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    scroll-behavior: smooth;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# STEP 1
# ---------------------------
if st.session_state.step == 1:
    st.subheader ("Vul deze korte vragenlijst (3') in en kom te weten hoe matuur jouw adaptiviteit is")

    st.subheader("Stap 1: Je gegevens")

    naam = st.text_input("Naam")
    email = st.text_input("Email - hierop ontvang je jouw persoonlijke feedbackrapport")
    functie = st.text_input("Functie")
    organisatie = st.text_input("Organisatie")

    if st.button("Start vragenlijst"):
        st.session_state.naam = naam
        st.session_state.email = email
        st.session_state.functie = functie
        st.session_state.organisatie = organisatie

        st.session_state.step = 2
        st.rerun()


# ---------------------------
# STEP 2
# ---------------------------
elif st.session_state.step == 2:

    st.subheader("Stap 2: Adaptiviteitsscan")

    answers = st.session_state.answers

    # ---------------------------
    # SCALE MAP
    # ---------------------------
    scale_map = {
        "Nooit": 1,
        "Zeer zelden": 2,
        "Zelden": 3,
        "Soms": 4,
        "Regelmatig": 5,
        "Vaak": 6,
        "Altijd": 7
    }

    # ---------------------------
    # QUESTIONS
    # ---------------------------
    for q in questions:
        with st.container():
            col_q, col_a = st.columns([5, 5])

            with col_q:
                st.markdown(f"**{q}**")

            with col_a:
                selected = st.radio(
                    label="",
                    options=list(scale_map.keys()),
                    horizontal=True,
                    key=q,
                    index=None,
                    label_visibility="collapsed"
                )

                # 🔴 BELANGRIJK: expliciet opslaan
                if selected:
                    answers[q] = scale_map[selected]

        st.markdown(
            "<hr style='margin:8px 0; opacity:0.6;'>",
            unsafe_allow_html=True
        )

    # ---------------------------
    # COMPLETENESS CHECK
    # ---------------------------
    missing = [q for q in questions if q not in answers]
    if missing:
        st.warning("Vul alle vragen in.")
    else:
        st.success("Alle vragen ingevuld.")

    # ---------------------------
    # SUBMIT
    # ---------------------------
    if st.button("Versturen"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        rows_to_add = []

        for q, score in answers.items():
            meta = question_map[q]

            raw_score = score
            final_score = 8 - score if meta["direction"] == "neg" else score

            rows_to_add.append([
                timestamp,
                st.session_state.naam,
                st.session_state.email,
                st.session_state.functie,
                st.session_state.organisatie,
                meta["code"],
                meta["pillar"],
                meta["direction"],
                raw_score,
                final_score,
                q
            ])

        sheet.append_rows(rows_to_add)

        st.session_state.step = 3
        st.session_state.scroll_top = True
        st.rerun()

# ---------------------------
# STEP 3 - DEBUG
# ---------------------------
    # ---------------------------
    # DEBUG: BLOCK SCORE BREAKDOWN
    # ---------------------------
  #  st.subheader("🔎 Debug: Block scoring details")

 #   debug_rows = []

  #  for q, score in st.session_state.answers.items():
  #      meta = question_map[q]

   #     raw_score = score
   #     final_score = 8 - score if meta["direction"] == "neg" else score

 #       debug_rows.append({
   #         "Vraag": q,
    #        "Block": meta["block"],
     #       "Pillar": meta["pillar"],
      #      "Direction": meta["direction"],
       #     "Raw score": raw_score,
       #     "Final score (na reverse)": final_score,
       #     "Code": meta["code"]
      #  })

  #  debug_df = pd.DataFrame(debug_rows)

  #  with st.expander("Bekijk alle individuele item-scores per block"):
  #      st.dataframe(debug_df, use_container_width=True)

    # ---------------------------
    # BLOCK SAMENVATTING
    # ---------------------------
 #   st.markdown("### 📊 Block gemiddelden")

 #   st.dataframe(
  #      block_scores.sort_values("block"),
  #      use_container_width=True
  #  )

# ---------------------------
# STEP 3
# ---------------------------
elif st.session_state.step == 3:

    st.markdown('<div id="top"></div>', unsafe_allow_html=True)

    # scroll to top
    components.html(
        """
        <script>
            setTimeout(() => {
                const el = window.parent.document.getElementById("top");
                if (el) {
                    el.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }, 200);
        </script>
        """,
        height=0
    )

    st.success("Bedankt voor je deelname 🎉")
    st.subheader("Je profiel")

    # ---------------------------
    # SCORES (ALTIJD BINNEN STEP 3)
    # ---------------------------
    pivot, block_scores = compute_scores(st.session_state.answers)
    level = compute_maturity_level(block_scores)

    # ---------------------------
    # HTML REPORT BUILDER (MAIL + EVENTUEEL PDF)
    # ---------------------------
    def build_report_html(level, pivot):
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #222;
                    line-height: 1.6;
                }}
                h2 {{
                    color: #2E86C1;
                }}
                .box {{
                    padding: 10px;
                    margin-bottom: 10px;
                    border-left: 4px solid #2E86C1;
                    background: #f5f9fc;
                }}
                .pillar {{
                    margin-bottom: 15px;
                    padding: 10px;
                    border-left: 3px solid #999;
                    background: #fafafa;
                }}
            </style>
        </head>
        <body>

        <table style="width:100%; margin-bottom:20px;">
        <tr>
        <td>
            <img src="https://YOUR_LOGO_URL/logo_coliberate.png" height="50">
        </td>
        <td style="text-align:right;">
            <img src="https://YOUR_LOGO_URL/logo_kultivating.png" height="50">
        </td>
        </tr>
        </table>

        <h2>Jouw Adaptiviteitsscan resultaat</h2>
        <p>
        Bedankt voor je deelname aan de Adaptiviteitsscan.
        In deze mail vind je jouw persoonlijke resultaat, inclusief de verschillende pijlers van je adaptief gedrag,
        en enkele concrete groeistappen.
        </p>
        
        <hr>
        <h3>Overzicht kernpijlers</h3>
        """
    
        # ---------------------------
        # PILLARS (zoals in app + extra uitleg)
        # ---------------------------
        for _, row in pivot.iterrows():
    
            pillar = row["pillar"]
            score = round(row["score"], 1)
    
            title = pillar_data[pillar]["title"]
            description = pillar_data[pillar]["description"]
            meanings = pillar_data[pillar]["score_meaning"]
    
            # simpele interpretatie
            if score <= 2:
                interp = meanings["low"]
            elif score <= 4:
                interp = meanings["mid"]
            elif score <= 5:
                interp = meanings["good"]
            else:
                interp = meanings["high"]
    
            html += f"""
            <div class="pillar">
                <h4>{title}</h4>
                <p><b>Score:</b> {score} / 7</p>
                <p>{description}</p>
                <p><b>Interpretatie:</b></p>
                <p>{interp}</p>
            </div>
            """      
        # ---------------------------
        # ADAPTIVITEIT (JOUW BESTAANDE FEEDBACK)
        # ---------------------------
        html += f"""
        <hr>
        
        <h3>Je adaptiviteit</h3>
        
        <div style="white-space: pre-line;">
        {feedback(level)
            .replace("### Volgende stappen:", "<b>Volgende stappen:</b>")
            .replace("### Eerste kleine stap", "<b>Eerste kleine stap</b>")
            .replace("- ", "• ")
        }
        </div>
        
        <hr>
        """
    
        # ---------------------------
        # COMMERCIËLE + TWEEDE SCAN SECTIE
        # ---------------------------
        html += """
        <hr>
        <h3>Verder verdiepen in adaptiviteit?</h3>
    
        <p>
        Deze scan geeft je inzicht in je <b>persoonlijke adaptiviteit</b>: hoe jij zelf omgaat met verandering, leren, veerkracht en innovatie.
        </p>
    
        <p>
        Er is ook een tweede perspectief: de <b>context</b> waarin dit gedrag ontstaat.
        Die scan helpt je begrijpen welke factoren in je omgeving jouw adaptief gedrag versterken of net belemmeren.
        </p>
    
        <p>
        Ontdek de organisatiescan hier:<br>
        <a href="https://organisatiescan.streamlit.app/" target="_blank">
        Organisatiescan
        </a>
        </p>
    
        <hr>
    
        <h3>Vragen of samen verder aan de slag?</h3>
    
        <p>
        Heb je vragen over de resultaten of wil je dit vertalen naar je team of organisatie,
        dan gaan we graag met je in gesprek om de inzichten verder te duiden en te vertalen naar actie.
        </p>
    
        <p>
        Daarnaast begeleiden we organisaties in het breder uitrollen van deze scan en het omzetten van inzichten naar concrete interventies op team- en organisatieniveau.
        </p>
    
        <p><b>Dank je wel voor je deelname.</b></p>
    
        </body>
        </html>
        """
    
        return html



    result_html = build_report_html(level, pivot)

    # ---------------------------
    # EMAIL (SAFE: 1X ONLY)
    # ---------------------------
    if "email_sent" not in st.session_state:

        try:
            send_email(
                st.session_state.email,
                "Jouw Adaptiviteitsscan resultaat",
                result_html
            )
            st.success("Resultaat is ook naar je e-mail gestuurd 📧")
        except Exception as e:
            st.error(f"E-mail kon niet verzonden worden: {e}")

        st.session_state.email_sent = True

    # ---------------------------
    # LAYOUT
    # ---------------------------
    col1, col2 = st.columns([2, 2], gap="large")

    with col1:
        radar_plot(pivot)

    with col2:
        with st.container(height=700):

            st.markdown("## Kernpijlers")

            for _, row in pivot.iterrows():
                pillar = row["pillar"]
                score = round(row["score"], 1)

                title = pillar_data[pillar]["title"]
                description = pillar_data[pillar]["description"]
                meanings = pillar_data[pillar]["score_meaning"]

                explanation = get_score_explanation(round(score), meanings)

                st.markdown(f"### {title} — {score}/7")

                st.markdown(f"""
{description}

**Wat betekent mijn score?**  
{explanation}
""")

                st.markdown("<hr style='margin:8px 0; opacity:0.3;'>",
                            unsafe_allow_html=True)

    # ---------------------------
    # EXTRA FEEDBACK ONDERAAN
    # ---------------------------
    st.subheader("Je adaptiviteit")
    st.markdown(feedback(level))
    st.markdown("---")

    # ---------------------------
    # RESET
    # ---------------------------
    if st.button("Opnieuw invullen"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.session_state.email_sent = False
        st.rerun()
