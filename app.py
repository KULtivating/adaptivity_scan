import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="Adaptivity Maturiteitsscan",
    layout="wide"
)

col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.webp", width=180)

with col2:
    st.title("Adaptivity Maturiteitsscan")
    st.markdown("### Hoe futureproof ben jij?")
    st.markdown("Vul deze korte vragenlijst in en kom het meteen te weten")

# ---------------------------
# GOOGLE SHEETS CONNECTION
# ---------------------------
@st.cache_resource
def connect_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
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
"Ik kan me gemakkelijk aanpassen aan veranderende situaties.": {"pillar": "AZR", "direction": "pos", "block": 2, "code": "Res2"},
"Ik herstel snel wanneer ik te maken krijg met tegenslag.": {"pillar": "AZR", "direction": "pos", "block": 2, "code": "Res3"},
"Ik blijf rustig in situaties waarin ik veel beslissingen moet nemen.": {"pillar": "AZR", "direction": "pos", "block": 2, "code": "IAP_WS1"},
"Ik pas mijn werk gemakkelijk aan nieuwe omstandigheden aan.": {"pillar": "AZR", "direction": "pos", "block": 2, "code": "IAP_R2"},
"Ik pas mijn gedrag graag aan wanneer dat nodig is om goed samen te werken.": {"pillar": "AZR", "direction": "pos", "block": 2, "code": "IAP_I2"},
"Ik volg regelmatig opleidingen op of naast het werk, om mijn vaardigheden up-to-date te houden.": {"pillar": "LO", "direction": "pos", "block": 2, "code": "IAP_T1"},
"Binnen mijn team of afdeling doen mensen een beroep op mij om nieuwe oplossingen aan te reiken.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IAP_C2"},

"Ik ga actief op zoek naar elke kans die mij helpt om mijn functioneren te verbeteren (opleiding, groepsproject, uitwisseling met collega’s, enz.).": {"pillar": "LO", "direction": "pos", "block": 3, "code": "IAP_T2"},
"Ik neem zelf initiatief om te beslissen wat en hoe ik leer.": {"pillar": "LO", "direction": "pos", "block": 3, "code": "LO_A"},

"Ik volg mijn omgeving actief op om te zien wat mijn job of organisatie in de toekomst kan beïnvloeden.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "PB_SS1"},
"Ik denk vooruit over mogelijke veranderingen in mijn job of organisatie als gevolg van ontwikkelingen in de omgeving (bv. markt, technologie).": {"pillar": "TV", "direction": "pos", "block": 4, "code": "PB_SS3"},
"Ik probeer werkwijzen en systemen te ontwikkelen die op lange termijn goed werken, ook als dat in het begin wat meer tijd kost.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "PB_PP1"},
"Ik probeer de echte oorzaak te vinden van problemen die zich voordoen.": {"pillar": "TV", "direction": "pos", "block": 3, "code": "PB_PP2"},

"Ik anticipeer op mogelijke problemen door vooraf scenario’s uit te werken en beslissingsopties klaar te hebben voordat ze nodig zijn.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "IAP_Rx"},
"Ik bouw bewust netwerkrelaties op die mij en anderen helpen om toekomstige veranderingen beter op te vangen of te benutten.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "IAP_Ix"},
"Ik help anderen niet alleen in moeilijke situaties, maar help ook om toekomstige crisissituaties beter te structureren en voorkomen.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "IAP_WSx"},

"Ik bedenk nieuwe manieren om technologie beter te gebruiken in mijn werk.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IBIncr6"},
"Ik ga zelfstandig op zoek naar nieuwe werkwijzen, technieken of hulpmiddelen.": {"pillar": "CI", "direction": "pos", "block": 4, "code": "IBRad4"},
"Ik onderneem acties om verandering in mijn organisatie te realiseren.": {"pillar": "CI", "direction": "pos", "block": 3, "code": "EISB1"},
"Ik bedenk nieuwe manieren van werken voor mijn organisatie.": {"pillar": "CI", "direction": "pos", "block": 3, "code": "EISB4"},
"Ik spreek actief ideeën uit en draag voorstellen aan over hoe mijn organisatie zich kan vernieuwen om met toekomstige veranderingen om te gaan.": {"pillar": "TV", "direction": "pos", "block": 4, "code": "VOICE"},
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

"Ik volg mijn omgeving actief op om te zien wat mijn job of organisatie in de toekomst kan beïnvloeden.": 12,
"Ik denk vooruit over mogelijke veranderingen in mijn job of organisatie als gevolg van ontwikkelingen in de omgeving (bv. markt, technologie).": 8,
"Ik probeer werkwijzen en systemen te ontwikkelen die op lange termijn goed werken, ook als dat in het begin wat meer tijd kost.": 19,
"Ik probeer de echte oorzaak te vinden van problemen die zich voordoen.": 29,

"Ik anticipeer op mogelijke problemen door vooraf scenario’s uit te werken en beslissingsopties klaar te hebben voordat ze nodig zijn.": 9,
"Ik bouw bewust netwerkrelaties op die mij en anderen helpen om toekomstige veranderingen beter op te vangen of te benutten.": 32,
"Ik help anderen niet alleen in moeilijke situaties, maar help ook om toekomstige crisissituaties beter te structureren en voorkomen.": 10,

"Ik bedenk nieuwe manieren om technologie beter te gebruiken in mijn werk.": 22,
"Ik ga zelfstandig op zoek naar nieuwe werkwijzen, technieken of hulpmiddelen.": 31,
"Ik onderneem acties om verandering in mijn organisatie te realiseren.": 11,
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

    all_pillars = ["VA", "AZR", "LO", "TV", "CI"]
    pivot = (
        pivot.set_index("pillar")
        .reindex(all_pillars)
        .fillna(1)
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

### Volgende stappen voor jou:
- weerstand sneller benoemen en bespreekbaar maken
- één kleine verandering bewust uitproberen
- onderzoeken wat een verandering kan opleveren
- minder afwachten, meer verkennen

### Aan de slag!
Kies één kleine verandering deze week en observeer bewust wat er gebeurt wanneer je die volgt in plaats van tegenhoudt.
""",

        1: """
Je accepteert verandering meestal correct en professioneel. Je werkt mee wanneer dat nodig is en zorgt ervoor dat het werk blijft doorlopen. Dat is een belangrijke en vaak onderschatte basis, omdat je stabiliteit en betrouwbaarheid brengt in een veranderende omgeving. Mensen rondom jou kunnen op je rekenen.

Je volgende groeistap ligt in het actiever vormgeven van verandering. Niet alleen uitvoeren wat gevraagd wordt, maar ook nadenken over hoe jij je eigen aanpak kan verbeteren of aanpassen. Door kleine initiatieven te nemen, verschuif je van “meewerken” naar “mee vormgeven”.

### Volgende stappen voor jou:
- bewust reflecteren op je eigen aanpak
- sneller nieuwe werkwijzen uitproberen
- vragen stellen over waarom iets verandert
- kleine verbeteringen zelf voorstellen

### Aan de slag!
Vraag bij één verandering actief door hoe je je werkwijze best kan aanpassen.
""",

        2: """
Je past je goed aan wanneer verandering zich voordoet. Je schakelt wanneer nodig, leert nieuwe situaties kennen en blijft goed functioneren onder druk. Dat toont veerkracht en leervermogen. Je hebt de houding van iemand die zegt: “als het verandert, dan vind ik mijn weg wel.”

De volgende stap is om niet alleen te reageren op verandering, maar ze ook vroeger te zien aankomen. Door signalen sneller op te pikken en je vooraf voor te bereiden, vergroot je je impact en je rust in nieuwe situaties.

### Volgende stappen voor jou:
- sneller alternatieven bedenken
- signalen van verandering vroeger oppikken
- proactiever opleidingen of kennis zoeken
- bewuster vooruitdenken bij nieuwe situaties

### Aan de slag!
Neem in één complexe situatie bewust een stap terug om meerdere opties te overwegen.
""",

        3: """
Je schakelt flexibel tussen situaties en weet goed wat nodig is om resultaat te behalen. Je blijft meestal rustig onder druk, denkt in oplossingen en past je gedrag effectief aan. Dat maakt je een betrouwbare kracht in een dynamische omgeving.

Je groeikans ligt in het nog sterker vooruitdenken in plaats van enkel goed reageren. Door patronen te herkennen en eerder te anticiperen op wat kan komen, kan je meer richting geven in plaats van enkel mee te bewegen.

### Volgende stappen voor jou:
- vaker vooruitdenken in scenario’s
- structurele oorzaken van problemen analyseren
- actief nieuwe vaardigheden ontwikkelen vóór ze nodig zijn
- kansen zien in verandering, niet alleen oplossingen

### Aan de slag!
Kies één ontwikkeling in je werkveld en bekijk wat deze binnen 6 maanden zou kunnen veranderen aan jouw job of taken.
""",

        4: """
Je denkt vooruit en bereidt je bewust voor op toekomstige veranderingen. Je ontwikkelt vaardigheden op voorhand, bouwt sterke netwerken en zoekt duurzame oplossingen. Je wacht niet af, maar helpt verandering mee vorm te geven. Dat toont eigenaarschap, maturiteit en strategisch inzicht.

De volgende stap ligt in nog meer experimenteren zonder directe noodzaak: niet alleen voorbereiden op wat waarschijnlijk komt, maar ook leren en ontwikkelen voor wat nog onbekend is. Zo versterk je je adaptiviteit verder.

### Volgende stappen voor jou:
- experimenteren zonder onmiddellijke aanleiding
- bewust leren buiten de huidige context
- nieuwe mogelijkheden verkennen zonder zeker doel
- anderen inspireren en meenemen in verandering

### Aan de slag!
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

### Aan de slag!
Kies één collega of team en help hen bewust om één verandering beter te begrijpen, aan te pakken of te versnellen.
"""
    }

    return texts.get(level, "Geen feedback beschikbaar voor dit niveau.")

pillar_labels = {
    "VA": "Veranderattitude",
    "AZR": "Adaptieve Zelf-Regulatie",
    "LO": "Leer & Ontwikkelingsoriëntatie",
    "TV": "Toekomstgerichte Voorbereiding",
    "CI": "Creativiteit & Innovatie"
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
        height=500,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

pillar_explanations = {
    "VA": """
### Veranderattitude

**Wat meet dit?**  
Deze pijler toont hoe jij omgaat met verandering in je werk: van eerder afwachtend of terughoudend tot actief ondersteunen of mee sturen van verandering.

**Wat betekent je score?**  
**1–2:** Je vermijdt of ondergaat verandering eerder en houdt vast aan vertrouwde manieren.  
**3–4:** Je werkt mee wanneer het nodig is, maar neemt weinig initiatief.  
**5:** Je bent meestal open en redelijk actief in het ondersteunen van verandering.  
**6–7:** Je bent sterk betrokken en neemt vaak zelf initiatief.
""",

    "AZR": """
### Adaptieve Zelf-Regulatie

**Wat meet dit?**  
Deze pijler gaat over hoe goed je je kan aanpassen aan nieuwe situaties, druk en tegenslagen.

**Wat betekent je score?**  
**1–2:** Verandering of druk voelt vaak zwaar.  
**3–4:** Je kan je aanpassen, maar hebt soms tijd nodig.  
**5:** Je past je meestal vlot aan.  
**6–7:** Je schakelt snel en blijft rustig onder druk.
""",

    "LO": """
### Leer- & Ontwikkelingsoriëntatie

**Wat meet dit?**  
Deze pijler toont hoe actief je bent in leren en jezelf ontwikkelen.

**Wat betekent je score?**  
**1–2:** Je leert vooral wanneer het echt nodig is.  
**3–4:** Je leert regelmatig wanneer kansen zich voordoen.  
**5:** Je bent actief bezig met leren.  
**6–7:** Je zoekt continu leer- en groeikansen.
""",

    "TV": """
### Toekomstgerichte Voorbereiding

**Wat meet dit?**  
Deze pijler toont hoe goed je vooruit denkt en je voorbereidt op toekomstige veranderingen.

**Wat betekent je score?**  
**1–2:** Je reageert vooral op het moment zelf.  
**3–4:** Je denkt soms vooruit.  
**5:** Je bereidt je regelmatig voor.  
**6–7:** Je werkt actief met scenario’s en anticipeert sterk.
""",

    "CI": """
### Creativiteit & Innovatie

**Wat meet dit?**  
Deze pijler toont in welke mate je zelf initiatief neemt om dingen anders of beter te doen.

**Wat betekent je score?**  
**1–2:** Je volgt vooral bestaande manieren.  
**3–4:** Je denkt soms mee over verbeteringen.  
**5:** Je neemt regelmatig initiatief.  
**6–7:** Je bent sterk proactief en zet ideeën om in actie.
"""
}

# ---------------------------
# STEP 1
# ---------------------------
if st.session_state.step == 1:

    st.subheader("Stap 1: Jouw gegevens")

    naam = st.text_input("Naam")
    email = st.text_input("Email")
    organisatie = st.text_input("Organisatie")

    if st.button("Start vragenlijst"):
        st.session_state.naam = naam
        st.session_state.email = email
        st.session_state.organisatie = organisatie

        st.session_state.step = 2
        st.rerun()

# ---------------------------
# STEP 2
# ---------------------------
elif st.session_state.step == 2:

    st.subheader("Stap 2: Vragenlijst")

    answers = st.session_state.answers

    scale_values = list(range(1, 8))

    # ---------------------------
    # SCALE HEADER (SUBTIEL + ALTIJD ALIGNED)
    # ---------------------------
    def scale_header():
        cols = st.columns([5, 4])
        with cols[0]:
            st.empty()
        with cols[1]:
            st.markdown(
                "1 — Nooit  |  2 - Zeer zelden  |  3 - Zelden  |  4 - Soms  |  5 - Regelmatig  |  6 - Vaak  |  7 — Altijd"
            )

    scale_header()
    st.markdown("---")

    # ---------------------------
    # QUESTIONS
    # ---------------------------
    for i, q in enumerate(questions):

        cols = st.columns([5, 4])

        with cols[0]:
            st.write(q)

        with cols[1]:

            selected = st.radio(
                label="",
                options=scale_values,
                horizontal=True,
                key=q
            )

            answers[q] = selected

        st.markdown("---")

        # ---------------------------
        # SCALE REMINDERS (na vraag 10 en 20)
        # ---------------------------
        if i == 5 or i == 10 or i == 15 or i == 20 or i == 25:
            scale_header()
            st.markdown("---")

    # ---------------------------
    # COMPLETENESS CHECK
    # ---------------------------
    if len(answers) < len(questions):
        st.warning("Vul alle vragen in.")
    else:
        st.success("Alle vragen ingevuld.")

        if st.button("Versturen"):

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            rows_to_add = []

            for q, score in answers.items():
                meta = question_map[q]

                raw_score = score
                reversed_flag = meta["direction"] == "neg"

                final_score = 8 - score if reversed_flag else score
                rows_to_add.append([
                    timestamp,
                    st.session_state.naam,
                    st.session_state.email,
                    st.session_state.organisatie,
                    question_map[q]["code"],
                    question_map[q]["pillar"],
                    question_map[q]["direction"],
                    raw_score,
                    final_score,
                    q             
                ])

            sheet.append_rows(rows_to_add)

            st.session_state.step = 3
            st.rerun()

# ---------------------------
# STEP 3
# ---------------------------
elif st.session_state.step == 3:

    st.success("Bedankt voor je deelname 🎉")

    st.subheader("Jouw profiel")

    # ---------------------------
    # SCORE BEREKENEN
    # ---------------------------
    pivot, block_scores = compute_scores(st.session_state.answers)
    level = compute_maturity_level(block_scores)

    # ---------------------------
    # DEBUG: BLOCK SCORE BREAKDOWN
    # ---------------------------
    st.subheader("🔎 Debug: Block scoring details")

    debug_rows = []

    for q, score in st.session_state.answers.items():
        meta = question_map[q]

        raw_score = score
        final_score = 8 - score if meta["direction"] == "neg" else score

        debug_rows.append({
            "Vraag": q,
            "Block": meta["block"],
            "Pillar": meta["pillar"],
            "Direction": meta["direction"],
            "Raw score": raw_score,
            "Final score (na reverse)": final_score,
            "Code": meta["code"]
        })

    debug_df = pd.DataFrame(debug_rows)

    with st.expander("Bekijk alle individuele item-scores per block"):
        st.dataframe(debug_df, use_container_width=True)

    # ---------------------------
    # BLOCK SAMENVATTING
    # ---------------------------
    st.markdown("### 📊 Block gemiddelden")

    st.dataframe(
        block_scores.sort_values("block"),
        use_container_width=True
    )
    # ---------------------------
    # LAYOUT
    # ---------------------------
    col1, col2 = st.columns([1.5, 1.5])

    with col1:
        radar_plot(pivot)

    with col2:
        st.markdown("## Kernpijlers")

        for _, row in pivot.iterrows():
            pillar = row["pillar"]
            score = round(row["score"], 1)

            st.write(pillar_explanations[pillar])
            st.markdown(f"### Score: {score}/7")
            st.markdown("---")

    # ---------------------------
    # MATURITEIT - TIJDELIJK OM NIVEAU TE TESTEN
    # ---------------------------
    st.write(f"Maturiteitsniveau: {level} / 5")

    # ---------------------------
    # FEEDBACK
    # ---------------------------
    st.subheader("Persoonlijke Feedback")
    st.markdown(feedback(level))

    # ---------------------------
    # RESET
    # ---------------------------
    if st.button("Opnieuw invullen"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()
