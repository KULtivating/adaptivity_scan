import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import gspread
import streamlit.components.v1 as components
from google.oauth2.service_account import Credentials
        
# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="Adaptivity Maturiteitsscan",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown('<div id="top"></div>', unsafe_allow_html=True)

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

# De technische logica gebruikt stabiele itemcodes, niet de zichtbare tekst.
# Voeg later per taal een extra mapping toe (bv. "fr" en "en") zonder scoring
# of historische data te wijzigen.
QUESTION_TEXTS = {
    "nl": {question_map[text]["code"]: text for text in questions},
}
QUESTION_META = {
    question_map[text]["code"]: {
        **question_map[text],
        "order": question_order[text],
    }
    for text in questions
}
QUESTION_CODES = sorted(QUESTION_META, key=lambda code: QUESTION_META[code]["order"])

UI_TEXTS = {
    "nl": {
        "app_title": "Adaptiviteit Maturiteitsscan",
        "app_intro": "Ontdek in enkele minuten hoe jij omgaat met verandering, leren, veerkracht en innovatie.",
        "details_step": "Stap 1 · Je gegevens",
        "scan_step": "Stap 2 · Adaptiviteitsscan",
        "name": "Naam",
        "email": "E-mailadres (optioneel)",
        "email_help": "We bewaren dit alleen zodat we je resultaat later eventueel kunnen bezorgen. Er wordt nu geen e-mail verstuurd.",
        "role": "Functie",
        "organisation": "Organisatie",
        "start": "Start vragenlijst",
        "submit": "Toon mijn resultaat",
        "missing": "Vul alle vragen in om je resultaat te bekijken.",
        "complete": "Alle vragen zijn ingevuld.",
        "thanks": "Bedankt voor je deelname",
        "profile": "Jouw persoonlijke adaptiviteit",
        "profile_intro": "Adaptiviteit beschrijft hoe je veerkrachtig omgaat met het heden én hoe je je voorbereidt op wat komt.",
        "core_profile": "Jouw kernprofiel",
        "pillars": "Jouw vijf kernpijlers",
        "interpretation": "Jouw interpretatie",
        "adaptivity": "Je adaptiviteit",
        "restart": "Opnieuw invullen",
    }
}

LANGUAGE = "nl"  # Voeg hier later een taalkeuze aan toe zodra vertalingen klaar zijn.
T = UI_TEXTS[LANGUAGE]

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

    for code, score in answers.items():
        meta = QUESTION_META[code]
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


def compute_maturity_level(block_scores_df, pillar_scores_df):
    """
    block_scores_df: dataframe met kolommen:
    [block, score]
    """

    scores = dict(zip(block_scores_df["block"], block_scores_df["score"]))

    b1 = scores.get(1, 0)
    b2 = scores.get(2, 0)
    b3 = scores.get(3, 0)
    b4 = scores.get(4, 0)
    pillar_scores = dict(zip(pillar_scores_df["pillar"], pillar_scores_df["score"]))
    vv = pillar_scores.get("VV", 0)
    ci = pillar_scores.get("CI", 0)

    # -------------------------
    # BLOCK 1
    # -------------------------
    if b1 < 3.5:
        return 0

    # -------------------------
    # BLOCK 2
    # -------------------------
    if b2 < 4.5:
        return 1
    elif b2 <= 5.5:
        return 2
    # alleen als b2 > 5.5 ga je verder

    # -------------------------
    # BLOCK 3
    # -------------------------
    if b3 < 4.5:
        return 2
    elif b3 <= 5.5:
        return 3
    # alleen als b3 > 5.5 ga je verder

    # -------------------------
    # BLOCK 4
    # -------------------------
    if b4 < 4.5:
        return 3
    elif b4 < 6 or vv < 5.75 or ci < 5.75:
        return 4
    else:
        return 5

# ---------------------------
# FEEDBACK FORMATTING (NIEUW)
# ---------------------------
def format_feedback(text):
    return (
        text
        .replace("### Volgende stappen:", "<br><br><b>Volgende stappen:</b><br>")
        .replace("### Eerste kleine stap", "<br><br><b>Eerste kleine stap</b><br>")
        .replace("- ", "• ")
        .replace("\n", "<br>")
    )

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

PERCENTILE_DATA = {
    "Veranderattitude": [(4.56, 2.50), (4.78, 5.00), (4.89, 10.00), (5.00, 20.00), (5.11, 22.50), (5.22, 40.00), (5.44, 42.50), (5.56, 47.50), (5.67, 62.50), (5.78, 65.00), (5.89, 72.50), (6.00, 80.00), (6.11, 87.50), (6.22, 97.50), (6.67, 100.00)],
    "Veerkracht & Zelfregulatie": [(2.40, 0.66), (2.60, 3.29), (2.80, 5.92), (3.00, 8.55), (3.20, 12.50), (3.40, 16.45), (3.60, 21.71), (3.80, 37.50), (4.00, 48.03), (4.20, 57.89), (4.40, 67.11), (4.60, 72.37), (4.80, 75.00), (5.00, 75.66), (5.20, 77.63), (5.40, 80.92), (5.60, 82.24), (5.80, 88.16), (6.00, 92.11), (6.20, 94.74), (6.40, 98.68), (6.60, 99.34), (6.80, 100.00)],
    "Leermotivatie & Ontwikkeling": [(2.25, 0.66), (2.50, 1.97), (2.75, 3.29), (3.00, 3.95), (3.25, 8.55), (3.50, 11.84), (3.75, 15.13), (4.00, 19.74), (4.25, 28.29), (4.50, 38.16), (4.75, 50.66), (5.00, 62.50), (5.25, 71.71), (5.50, 78.95), (5.75, 87.50), (6.00, 95.39), (6.25, 96.71), (6.50, 98.03), (6.75, 100.00)],
    "Vooruitzien & Voorbereiden": [(4.00, 2.50), (4.12, 5.00), (4.25, 15.00), (4.38, 17.50), (4.50, 20.00), (4.62, 22.50), (4.75, 25.00), (4.88, 27.50), (5.00, 37.50), (5.12, 45.00), (5.25, 47.50), (5.38, 50.00), (5.50, 67.50), (5.71, 70.00), (5.75, 75.00), (5.88, 82.50), (6.00, 87.50), (6.25, 97.50), (6.50, 100.00)],
    "Creativiteit & Innovatie": [(3.60, 5.00), (3.80, 7.50), (4.00, 10.00), (4.20, 15.00), (4.40, 22.50), (4.80, 32.50), (5.00, 45.00), (5.20, 57.50), (5.60, 65.00), (5.80, 77.50), (6.00, 85.00), (6.20, 92.50), (6.40, 95.00), (6.60, 97.50), (7.00, 100.00)],
}


def get_percentile(title, score):
    """Interpoleer de score lineair binnen de externe normgroep."""
    values = PERCENTILE_DATA.get(title, [])
    if not values:
        return None
    if score < values[0][0]:
        return 0.0
    if score >= values[-1][0]:
        return 100.0
    for index in range(1, len(values)):
        lower_score, lower_percentile = values[index - 1]
        upper_score, upper_percentile = values[index]
        if score <= upper_score:
            position = (score - lower_score) / (upper_score - lower_score)
            return lower_percentile + position * (upper_percentile - lower_percentile)
    return 100.0


def percentile_label(percentile):
    if percentile is None:
        return "Geen normdata"
    if percentile < 10:
        return "Zeer laag"
    if percentile < 30:
        return "Eerder laag"
    if percentile <= 70:
        return "Rond het midden"
    if percentile <= 90:
        return "Eerder hoog"
    return "Zeer hoog"


def short_summary(level):
    summaries = {
        0: "Je adaptiviteit staat nog aan het begin van haar ontwikkeling.",
        1: "Je werkt correct mee met verandering wanneer dat nodig is.",
        2: "Je past je goed aan wanneer verandering zich voordoet.",
        3: "Je schakelt flexibel en oplossingsgericht in veranderende situaties.",
        4: "Je denkt vooruit en bereidt je bewust voor op toekomstige verandering.",
        5: "Je creëert actief verandering en helpt anderen daarin mee te groeien.",
    }
    return summaries.get(level, "")


PILLAR_ICONS = {
    "VA": '<svg viewBox="0 0 64 64"><path d="M18 17a19 19 0 0 1 28 5"/><path d="M46 14v10H36"/><path d="M46 47a19 19 0 0 1-28-5"/><path d="M18 50V40h10"/></svg>',
    "VZ": '<svg viewBox="0 0 64 64"><path d="M32 8 50 15v14c0 12-8 21-18 27-10-6-18-15-18-27V15z"/><path d="m23 31 6 6 12-14"/></svg>',
    "LO": '<svg viewBox="0 0 64 64"><path d="M10 16c8-3 15-1 22 4v30c-7-5-14-7-22-4z"/><path d="M54 16c-8-3-15-1-22 4v30c7-5 14-7 22-4z"/><path d="M32 20v30"/></svg>',
    "VV": '<svg viewBox="0 0 64 64"><path d="m12 25 29-10 4 9-29 10z"/><path d="m42 24 10 7M27 32 18 54M35 29 45 54"/></svg>',
    "CI": '<svg viewBox="0 0 64 64"><path d="M21 28a11 11 0 1 1 22 0c0 6-3 8-6 12H27c-3-4-6-6-6-12z"/><path d="M27 45h10M29 50h6M32 5v7M10 28H3M61 28h-7"/></svg>',
}

PILLAR_SHORT_DESCRIPTIONS = {
    "VA": "Positief en constructief omgaan met verandering.",
    "VZ": "Omgaan met druk en emoties en herstellen bij tegenslag.",
    "LO": "Continu willen leren en jezelf ontwikkelen.",
    "VV": "Anticiperen op toekomstige veranderingen en je voorbereiden.",
    "CI": "Nieuwe ideeën bedenken en toepassen om vooruit te gaan.",
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
:root {
    --primary: #0f566b;
    --blue: #2aa5ca;
    --yellow: #ffc271;
    --light-blue: #eef8fb;
    --text: #17313b;
    --muted: #667985;
    --line: #cfe1e7;
}
html, body, [data-testid="stAppViewContainer"] {
    scroll-behavior: smooth;
    color: var(--text);
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f5fbfd 0, #ffffff 300px);
}
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
h1, h2, h3 { color: var(--primary) !important; }
.app-header {
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
    border-radius: 0 42px 42px 0;
    background: var(--primary);
    color: white;
}
.app-header h1 { color: white !important; margin: 0; font-size: 2.2rem; }
.app-header p { margin: .45rem 0 0; color: white; max-width: 760px; }
.section-pill {
    display: inline-block;
    margin-bottom: .55rem;
    padding: .28rem .75rem;
    border-radius: 999px;
    background: var(--primary);
    color: white;
    font-size: .78rem;
    font-weight: 800;
    letter-spacing: .05em;
    text-transform: uppercase;
}
[data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--line) !important;
    border-radius: 16px !important;
}
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 1rem;
    align-items: stretch;
}
.pillar-card {
    grid-column: span 2;
    min-height: 100%;
    padding: 1.1rem;
    border: 1px solid var(--line);
    border: 1.5px solid var(--primary);
    border-radius: 16px;
    background: white;
    box-shadow: 0 8px 22px rgba(15, 86, 107, .07);
    display: flex;
    flex-direction: column;
}
.pillar-card:nth-child(4) { grid-column: 2 / span 2; }
.pillar-card:nth-child(5) { grid-column: 4 / span 2; }
.pillar-header { display:grid; grid-template-columns:48px 1fr; gap:.75rem; align-items:start; }
.pillar-icon {
    width:46px; height:46px; border-radius:50%; background:var(--primary); color:white;
    display:grid; place-items:center; flex:none;
}
.pillar-icon svg { width:68%; height:68%; fill:none; stroke:currentColor; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }
.pillar-card h3 { font-size: 1.04rem; line-height:1.18; margin:0 0 .4rem; }
.pillar-card p { font-size: .88rem; line-height:1.42; margin:0; }
.score-row { display:flex; align-items:center; gap:.75rem; margin:.9rem 0; }
.score-track { flex:1; height:9px; border-radius:999px; background:#e5f0f3; overflow:hidden; }
.score-fill { height:100%; border-radius:999px; background:linear-gradient(90deg, var(--blue), var(--primary)); }
.score-value { color:var(--primary); font-weight:800; white-space:nowrap; }
.percentile-badge { display:inline-grid; grid-template-columns:auto auto; gap:.1rem .45rem; align-items:center; width:max-content; padding:.4rem .65rem; border-radius:10px; background:#fff7eb; color:var(--primary); margin-bottom:.75rem; }
.percentile-badge b { font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; }
.percentile-badge strong { font-size:1rem; }
.percentile-badge small { grid-column:1 / -1; color:var(--muted); font-weight:700; }
.interpretation-box { padding:.8rem; border-radius:10px; background:var(--light-blue); margin-top:auto; }
.interpretation-box strong { color:var(--primary); }
.profile-summary-card { padding:1.15rem; border:1px solid var(--line); border-left:5px solid var(--primary); border-radius:16px; background:var(--light-blue); min-height:100%; }
.profile-summary-card h3 { margin-top:0; }
.summary-stat { padding:.7rem 0; border-bottom:1px solid rgba(15,86,107,.16); }
.summary-stat:last-of-type { border-bottom:0; }
.summary-stat b { color:var(--primary); }
.summary-stat strong { display:block; margin-top:.15rem; font-size:1.02rem; }
.summary-copy { margin-top:.85rem; padding:.75rem; border-radius:10px; background:white; color:var(--text); }
div[data-testid="stRadio"] label p { font-size: .86rem; }
@media (min-width: 900px) {
    div[data-testid="stRadio"] div[role="radiogroup"] {
        flex-wrap: nowrap;
        gap: .55rem;
    }
}
.stButton > button {
    border: 0;
    border-radius: 999px;
    background: var(--primary);
    color: white;
    font-weight: 700;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
}
.stButton > button:hover { background:#0a4455; color:white; }
@media (max-width: 700px) {
    .block-container { padding: 1rem; }
    .app-header { border-radius: 0 28px 28px 0; margin-left:-1rem; }
    .app-header h1 { font-size:1.65rem; }
    .pillar-grid { grid-template-columns:1fr; }
    .pillar-card, .pillar-card:nth-child(4), .pillar-card:nth-child(5) { grid-column:1; }
}
@media (min-width: 701px) and (max-width: 980px) {
    .pillar-grid { grid-template-columns:repeat(2, minmax(0, 1fr)); }
    .pillar-card, .pillar-card:nth-child(4), .pillar-card:nth-child(5) { grid-column:auto; }
    .pillar-card:last-child { grid-column:1 / -1; }
}
</style>
""", unsafe_allow_html=True)

header_left, header_right = st.columns([5, 1.35], vertical_alignment="center")
with header_left:
    st.markdown(
        f'<div class="app-header"><h1>{T["app_title"]}</h1><p>{T["app_intro"]}</p></div>',
        unsafe_allow_html=True,
    )
with header_right:
    logo_left, logo_right = st.columns(2, vertical_alignment="center")
    with logo_left:
        st.image("assets/logo Coliberate.png", use_container_width=True)
    with logo_right:
        st.image("assets/logo KULtivating.webp", use_container_width=True)

# ---------------------------
# STEP 1
# ---------------------------
if st.session_state.step == 1:
    st.markdown(f'<span class="section-pill">{T["details_step"]}</span>', unsafe_allow_html=True)
    st.subheader("Vertel ons kort wie je bent")

    naam = st.text_input(T["name"])
    email = st.text_input(T["email"], help=T["email_help"], placeholder="naam@organisatie.be")
    functie = st.text_input(T["role"])
    organisatie = st.text_input(T["organisation"])
    st.caption(T["email_help"])

    if st.button(T["start"]):
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

    st.markdown(f'<span class="section-pill">{T["scan_step"]}</span>', unsafe_allow_html=True)
    st.subheader("Duid voor elke uitspraak aan hoe vaak dit bij jou voorkomt")

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
    for code in QUESTION_CODES:
        q = QUESTION_TEXTS[LANGUAGE][code]
        with st.container():
            # Geef de zeven antwoordopties voldoende ruimte om op één regel te blijven.
            col_q, col_a = st.columns([4, 8], gap="large")

            with col_q:
                st.markdown(f"**{q}**")

            with col_a:
                selected = st.radio(
                    label="",
                    options=list(scale_map.keys()),
                    horizontal=True,
                    key=f"question_{code}",
                    index=None,
                    label_visibility="collapsed"
                )

                # 🔴 BELANGRIJK: expliciet opslaan
                if selected:
                    answers[code] = scale_map[selected]

        st.markdown(
            "<hr style='margin:8px 0; opacity:0.6;'>",
            unsafe_allow_html=True
        )

    # ---------------------------
    # COMPLETENESS CHECK
    # ---------------------------
    missing = [code for code in QUESTION_CODES if code not in answers]
    if missing:
        st.warning(T["missing"])
    else:
        st.success(T["complete"])

    # ---------------------------
    # SUBMIT
    # ---------------------------
    if st.button(T["submit"], disabled=bool(missing)):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        rows_to_add = []

        for code, score in answers.items():
            meta = QUESTION_META[code]
            q = QUESTION_TEXTS[LANGUAGE][code]

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

    # ---------------------------
    # SCORES (ALTIJD BINNEN STEP 3)
    # ---------------------------
    pivot, block_scores = compute_scores(st.session_state.answers)
    level = compute_maturity_level(block_scores, pivot)

    # ---------------------------
    # LAYOUT
    # ---------------------------
    st.markdown(f'<span class="section-pill">{T["profile"]}</span>', unsafe_allow_html=True)
    st.title(T["thanks"])
    st.markdown(f"### {T['profile']}")
    st.write(T["profile_intro"])

    profile_rows = []
    for _, row in pivot.iterrows():
        title = pillar_data[row["pillar"]]["title"]
        score = float(row["score"])
        percentile = get_percentile(title, score)
        profile_rows.append({
            "code": row["pillar"],
            "title": title,
            "score": score,
            "percentile": percentile,
            "percentile_label": percentile_label(percentile),
        })
    strongest = max(profile_rows, key=lambda item: item["score"])
    weakest = min(profile_rows, key=lambda item: item["score"])

    radar_column, summary_column = st.columns([1.2, .8], gap="large", vertical_alignment="top")
    with radar_column:
        st.subheader(T["core_profile"])
        radar_plot(pivot)
    with summary_column:
        summary_html = f"""
        <article class="profile-summary-card">
            <h3>Wat valt op?</h3>
            <div class="summary-stat">
                <b>Sterkste pijler</b>
                <strong>{strongest['title']}: {strongest['score']:.1f} / 7</strong>
                <small>P{strongest['percentile']:.0f} · {strongest['percentile_label']}</small>
            </div>
            <div class="summary-stat">
                <b>Grootste ontwikkelkans</b>
                <strong>{weakest['title']}: {weakest['score']:.1f} / 7</strong>
                <small>P{weakest['percentile']:.0f} · {weakest['percentile_label']}</small>
            </div>
            <p class="summary-copy">{short_summary(level)}</p>
        </article>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

    st.markdown(f"## {T['pillars']}")
    cards = []
    for _, row in pivot.iterrows():
        pillar = row["pillar"]
        raw_score = float(row["score"])
        score = round(raw_score, 1)
        title = pillar_data[pillar]["title"]
        description = PILLAR_SHORT_DESCRIPTIONS[pillar]
        explanation = get_score_explanation(round(score), pillar_data[pillar]["score_meaning"])
        score_percentage = max(0, min(100, (raw_score / 7) * 100))
        percentile = get_percentile(title, raw_score)
        percentile_text = percentile_label(percentile)

        # Zonder regeleindes: anders kan Markdown ingesprongen HTML na kaart 1
        # als een codeblok tonen in plaats van als onderdeel van hetzelfde grid.
        card_html = (
            '<article class="pillar-card">'
            '<header class="pillar-header">'
            f'<span class="pillar-icon">{PILLAR_ICONS[pillar]}</span>'
            f'<div><h3>{title}</h3><p>{description}</p></div>'
            '</header>'
            '<div class="score-row">'
            f'<div class="score-track"><div class="score-fill" style="width:{score_percentage:.1f}%"></div></div>'
            f'<span class="score-value">{score} / 7</span>'
            '</div>'
            f'<span class="percentile-badge" title="P{percentile:.0f} betekent dat je hoger scoort dan ongeveer {percentile:.0f}% van de externe normgroep.">'
            f'<b>Interpretatie</b><strong>P{percentile:.0f}</strong><small>{percentile_text}</small>'
            '</span>'
            '<div class="interpretation-box">'
            f'<strong>{T["interpretation"]}</strong><p>{explanation}</p>'
            '</div>'
            '</article>'
        )
        cards.append(card_html)
    st.markdown(f'<div class="pillar-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
    st.caption(
        "Pxx toont je positie ten opzichte van de externe normgroep. "
        "P76 betekent bijvoorbeeld dat je hoger scoort dan ongeveer 76% van die normgroep; "
        "het is geen percentage juiste antwoorden."
    )

    # ---------------------------
    # EXTRA FEEDBACK ONDERAAN
    # ---------------------------
    st.subheader(T["adaptivity"])
    st.markdown(feedback(level))
    st.markdown("---")

    # ---------------------------
    # RESET
    # ---------------------------
    if st.button(T["restart"]):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()
