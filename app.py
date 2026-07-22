from datetime import datetime, timedelta
from hmac import compare_digest
from zoneinfo import ZoneInfo

import gspread
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from google.oauth2.service_account import Credentials
from analytics import percentile, percentile_band, respondent_maturity, spread_band

st.set_page_config(page_title="Live groepsdashboard · Adaptiviteit", page_icon="↗", layout="wide", initial_sidebar_state="collapsed")

LANGUAGES = {"nl": "Nederlands", "fr": "Français", "en": "English"}
TEXT = {
    "nl": {
        "title":"Live groepsdashboard","subtitle":"Adaptiviteit van de groep","intro":"Volg de groepsresultaten rechtstreeks vanuit de scan. Het dashboard toont alleen gemiddelden en nooit individuele antwoorden.","access":"Toegangscode","access_help":"Vul de gedeelde toegangscode in om de groepsresultaten te bekijken.","access_wrong":"De toegangscode is niet correct.",
        "language":"Taal","period":"Welke antwoorden wil je tonen?","session":"Sinds opening van deze dashboardsessie","hour":"Laatste uur","day":"Laatste 24 uur","all":"Volledige dataset","refresh":"Nu verversen","updated":"Laatst ververst","responses":"Deelnemers","answers":"Antwoorden","average":"Groepsgemiddelde","pillars":"De vijf kernpijlers","strongest":"Sterkste pijler","opportunity":"Grootste ontwikkelkans","no_data":"Voor deze periode zijn nog geen antwoorden beschikbaar.","privacy":"Resultaten worden als groepsgemiddelden getoond. Deel geen conclusies over individuele deelnemers.","source_error":"De Google Sheet kon niet worden gelezen. Controleer de secrets, de naam van de spreadsheet en de deelrechten.","scale":"Score op 7","live":"LIVE","organisation_filter":"Organisatie (optioneel)","all_orgs":"Alle organisaties","period_note":"Getoond venster","from":"vanaf","full":"alle beschikbare antwoorden",
    },
    "fr": {
        "title":"Tableau de bord collectif en direct","subtitle":"Adaptabilité du groupe","intro":"Suivez les résultats du groupe directement depuis le scan. Le tableau de bord n’affiche que des moyennes, jamais de réponses individuelles.","access":"Code d’accès","access_help":"Saisissez le code partagé pour consulter les résultats collectifs.","access_wrong":"Le code d’accès est incorrect.",
        "language":"Langue","period":"Quelles réponses afficher ?","session":"Depuis l’ouverture de cette session","hour":"Dernière heure","day":"Dernières 24 heures","all":"Ensemble des données","refresh":"Actualiser maintenant","updated":"Dernière actualisation","responses":"Participants","answers":"Réponses","average":"Moyenne du groupe","pillars":"Les cinq piliers clés","strongest":"Pilier le plus fort","opportunity":"Principale opportunité de développement","no_data":"Aucune réponse n’est encore disponible pour cette période.","privacy":"Les résultats sont présentés sous forme de moyennes collectives. Ne tirez pas de conclusions sur des participants individuels.","source_error":"Impossible de lire la feuille Google. Vérifiez les secrets, le nom de la feuille de calcul et les droits de partage.","scale":"Score sur 7","live":"EN DIRECT","organisation_filter":"Organisation (facultatif)","all_orgs":"Toutes les organisations","period_note":"Période affichée","from":"depuis","full":"toutes les réponses disponibles",
    },
    "en": {
        "title":"Live group dashboard","subtitle":"Group adaptability","intro":"Follow group results directly from the scan. The dashboard only shows averages and never individual answers.","access":"Access code","access_help":"Enter the shared access code to view the group results.","access_wrong":"The access code is incorrect.",
        "language":"Language","period":"Which responses should be shown?","session":"Since this dashboard session opened","hour":"Last hour","day":"Last 24 hours","all":"Full dataset","refresh":"Refresh now","updated":"Last refreshed","responses":"Participants","answers":"Answers","average":"Group average","pillars":"The five core pillars","strongest":"Strongest pillar","opportunity":"Main development opportunity","no_data":"No responses are available for this period yet.","privacy":"Results are shown as group averages. Do not draw conclusions about individual participants.","source_error":"The Google Sheet could not be read. Check the secrets, spreadsheet name and sharing permissions.","scale":"Score out of 7","live":"LIVE","organisation_filter":"Organisation (optional)","all_orgs":"All organisations","period_note":"Displayed window","from":"from","full":"all available responses",
    },
}

PILLARS = ["VA", "VZ", "LO", "VV", "CI"]
PILLAR_TEXT = {
    "nl": {"VA":("Veranderattitude","Hoe de groep verandering benadert en mee vormgeeft."),"VZ":("Veerkracht & zelfregulatie","Hoe de groep onder druk blijft functioneren en herstelt."),"LO":("Leermotivatie & ontwikkeling","Hoe actief de groep leert, feedback benut en groeit."),"VV":("Vooruitzien & voorbereiden","Hoe sterk de groep signalen oppikt en vooruitdenkt."),"CI":("Creativiteit & innovatie","Hoe de groep nieuwe ideeën en verbeteringen realiseert.")},
    "fr": {"VA":("Attitude face au changement","La manière dont le groupe aborde et façonne le changement."),"VZ":("Résilience & autorégulation","La manière dont le groupe fonctionne sous pression et récupère."),"LO":("Motivation à apprendre & développement","La manière dont le groupe apprend, utilise le feedback et progresse."),"VV":("Anticipation & préparation","La capacité du groupe à capter les signaux et anticiper."),"CI":("Créativité & innovation","La manière dont le groupe développe des idées et améliorations.")},
    "en": {"VA":("Change attitude","How the group approaches and helps shape change."),"VZ":("Resilience & self-regulation","How the group keeps functioning under pressure and recovers."),"LO":("Learning motivation & development","How actively the group learns, uses feedback and grows."),"VV":("Anticipation & preparation","How well the group picks up signals and thinks ahead."),"CI":("Creativity & innovation","How the group develops new ideas and improvements.")},
}

SUBTITLE={"nl":"Jullie adaptief gedrag","fr":"Votre comportement adaptatif","en":"Your adaptive behaviour"}
INTRO={"nl":"Dit dashboard toont enkel gemiddelden, geen individuele antwoorden.","fr":"Ce tableau de bord présente uniquement des moyennes, jamais de réponses individuelles.","en":"This dashboard only shows averages, never individual answers."}
COPY={
"nl":{"overview":"De vijf pijlers van adaptief gedrag","overview_intro":"De vijf pijlers tonen hoe deelnemers vandaag met verandering omgaan en hoe zij zich voorbereiden op wat nog komt.","stands":"Wat valt op?","largest":"Meeste individuele spreiding","smallest":"Minste individuele spreiding","radar_band":"10e–90e percentiel","group_mean":"Groepsgemiddelde","benchmark":"Gemiddelde","spread":"Individuele spreiding","benchmark_help":"Het groepsgemiddelde, geduid tegenover de externe benchmark.","spread_help":"Hoe sterk antwoorden van deelnemers onderling verschillen.","p_very_low":"Zeer laag","p_low":"Laag","p_middle":"Rond het midden","p_high":"Hoog","p_very_high":"Zeer hoog","s_low":"Lage spreiding","s_moderate":"Matige spreiding","s_high":"Hoge spreiding","s_unavailable":"Nog niet beschikbaar","spread_guide":"Objectieve duiding van spreiding (7-puntsschaal)","spread_low":"Laag: SD ≤ 0,72 · antwoorden liggen dicht bij elkaar.","spread_mid":"Matig: SD 0,73–1,32 · merkbare verschillen tussen deelnemers.","spread_high":"Hoog: SD > 1,32 · sterk uiteenlopende ervaringen.","distribution":"Verdeling over de antwoordcategorieën","distribution_intro":"De balken tonen welk aandeel deelnemers per pijler gemiddeld in elke scorecategorie valt.","maturity":"Van reactief naar proactief veranderen","maturity_intro":"De maturiteitsniveaus beschrijven welk gedrag vandaag het meest herkenbaar is wanneer verandering zich aandient. Ze vormen geen oordeel of vast label.","dominant":"Vaakst voorkomend profiel","respondents":"respondenten","progress":"Van reactief naar proactief","privacy_small":"Toon groepsresultaten bij voorkeur vanaf minstens drie deelnemers."},
"fr":{"overview":"Les cinq piliers du comportement adaptatif","overview_intro":"Les cinq piliers montrent comment les participants abordent aujourd’hui le changement et se préparent à ce qui vient.","stands":"Que retenir ?","largest":"Plus grande dispersion individuelle","smallest":"Plus faible dispersion individuelle","radar_band":"10e–90e percentile","group_mean":"Moyenne du groupe","benchmark":"Moyenne","spread":"Dispersion individuelle","benchmark_help":"La moyenne du groupe, située par rapport à la référence externe.","spread_help":"La mesure dans laquelle les réponses diffèrent entre participants.","p_very_low":"Très faible","p_low":"Faible","p_middle":"Dans la moyenne","p_high":"Élevé","p_very_high":"Très élevé","s_low":"Faible dispersion","s_moderate":"Dispersion modérée","s_high":"Forte dispersion","s_unavailable":"Pas encore disponible","spread_guide":"Interprétation objective de la dispersion (échelle à 7 points)","spread_low":"Faible : ET ≤ 0,72 · réponses proches.","spread_mid":"Modérée : ET 0,73–1,32 · différences perceptibles.","spread_high":"Forte : ET > 1,32 · expériences très différentes.","distribution":"Répartition des catégories de réponse","distribution_intro":"Les barres montrent la part des participants dont la moyenne par pilier relève de chaque catégorie.","maturity":"Passer du changement réactif au changement proactif","maturity_intro":"Les niveaux décrivent le comportement actuellement le plus reconnaissable face au changement. Ils ne constituent ni un jugement ni une étiquette fixe.","dominant":"Profil le plus fréquent","respondents":"répondants","progress":"Du réactif au proactif","privacy_small":"Présentez de préférence les résultats collectifs à partir de trois participants."},
"en":{"overview":"The five pillars of adaptive behaviour","overview_intro":"The five pillars show how participants currently deal with change and prepare for what comes next.","stands":"What stands out?","largest":"Greatest individual spread","smallest":"Smallest individual spread","radar_band":"10th–90th percentile","group_mean":"Group average","benchmark":"Average","spread":"Individual spread","benchmark_help":"The group average interpreted against the external benchmark.","spread_help":"How strongly participants’ answers differ from one another.","p_very_low":"Very low","p_low":"Low","p_middle":"Around the middle","p_high":"High","p_very_high":"Very high","s_low":"Low spread","s_moderate":"Moderate spread","s_high":"High spread","s_unavailable":"Not yet available","spread_guide":"Objective interpretation of spread (7-point scale)","spread_low":"Low: SD ≤ 0.72 · answers are close together.","spread_mid":"Moderate: SD 0.73–1.32 · noticeable differences.","spread_high":"High: SD > 1.32 · strongly differing experiences.","distribution":"Distribution across response categories","distribution_intro":"The bars show the share of participants whose average per pillar falls in each category.","maturity":"From reactive to proactive change","maturity_intro":"The maturity levels describe which behaviour is currently most recognisable when change occurs. They are not a judgement or fixed label.","dominant":"Most common profile","respondents":"respondents","progress":"From reactive to proactive","privacy_small":"Preferably present group results from at least three participants."}}
MATURITY={
"nl":[("Kritisch & terughoudend","Verandering vraagt veel energie; kritische signalen en onzekerheid staan voorop."),("Stabiel meewerkend","Deelnemers werken professioneel mee, maar nemen beperkt initiatief."),("Reactief aanpassend","Deelnemers passen zich aan wanneer verandering zich voordoet."),("Wendbaar responsief","Deelnemers schakelen snel en effectief in wisselende situaties."),("Proactief anticiperend","Deelnemers zien verandering vroeger aankomen en bereiden zich bewust voor."),("Anticiperende leer- en transformatiekracht","Deelnemers blijven leren en creëren actief nieuwe mogelijkheden.")],
"fr":[("Critique & réservé","Le changement demande beaucoup d’énergie ; signaux critiques et incertitude dominent."),("Coopération stable","Les participants coopèrent de manière professionnelle, avec peu d’initiative."),("Adaptation réactive","Les participants s’adaptent lorsque le changement survient."),("Réactivité agile","Les participants s’ajustent rapidement et efficacement."),("Anticipation proactive","Les participants voient le changement venir et s’y préparent."),("Apprentissage anticipatif & transformation","Les participants continuent d’apprendre et créent de nouvelles possibilités.")],
"en":[("Critical & reserved","Change requires considerable energy; critical signals and uncertainty dominate."),("Stable cooperation","Participants cooperate professionally but take limited initiative."),("Reactive adaptation","Participants adapt when change occurs."),("Agile responsiveness","Participants adjust quickly and effectively in changing situations."),("Proactive anticipation","Participants see change coming and prepare deliberately."),("Anticipatory learning & transformation","Participants keep learning and actively create new possibilities.")]
}
PATTERN_LEGEND={"nl":["Volle lijn = vaakst voorkomend profiel","Stippellijn = ander voorkomend niveau","Transparant = niet aanwezig"],"fr":["Ligne pleine = profil le plus fréquent","Pointillés = autre niveau présent","Transparent = niveau absent"],"en":["Solid line = most common profile","Dashed line = other level present","Transparent = level not present"]}
LEVEL_LABEL={"nl":"NIVEAU","fr":"NIVEAU","en":"LEVEL"}
PILLAR_ICONS={
"VA":'<svg viewBox="0 0 64 64"><path d="M14 22a20 20 0 0 1 34-5l5 6M50 10l3 13-13-2M50 42a20 20 0 0 1-34 5l-5-6M14 54l-3-13 13 2"/></svg>',
"VZ":'<svg viewBox="0 0 64 64"><path d="M32 7l19 8v14c0 13-8 22-19 28-11-6-19-15-19-28V15z"/><path d="m22 31 7 7 14-16"/></svg>',
"LO":'<svg viewBox="0 0 64 64"><path d="M8 15c9-3 17-1 24 5v34c-7-6-15-8-24-5zM56 15c-9-3-17-1-24 5v34c7-6 15-8 24-5z"/></svg>',
"VV":'<svg viewBox="0 0 64 64"><path d="M10 51 26 20l9 14 8-11 11 28M20 51h38M13 17h19M25 10l7 7-7 7"/></svg>',
"CI":'<svg viewBox="0 0 64 64"><path d="M21 29a11 11 0 1 1 22 0c0 6-3 8-6 12H27c-3-4-6-6-6-12zM27 47h10M29 53h6M32 5v8M9 29h7M48 29h7"/></svg>'}
MATURITY_ICONS=[
'<svg viewBox="0 0 64 64"><path d="M47 12a24 24 0 1 1-8-3"/><path d="M25 22v20M39 22v20"/></svg>',
'<svg viewBox="0 0 64 64"><path d="M32 7l6 4 7-1 4 6 7 3v7l4 6-4 6v7l-7 3-4 6-7-1-6 4-6-4-7 1-4-6-7-3v-7l-4-6 4-6v-7l7-3 4-6 7 1z"/><path d="m21 32 7 7 15-16"/></svg>',
'<svg viewBox="0 0 64 64"><path d="M8 18h18M38 18h18M8 32h34M50 32h6M8 46h8M28 46h28"/><circle cx="32" cy="18" r="5"/><circle cx="46" cy="32" r="5"/><circle cx="22" cy="46" r="5"/></svg>',
'<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="23"/><path d="m39 25-5 11-11 5 5-11z"/><circle cx="32" cy="32" r="2"/><path d="M32 6v5M32 53v5M6 32h5M53 32h5"/></svg>',
'<svg viewBox="0 0 64 64"><path d="M32 32 50 17M13 48a26 26 0 1 1 38 0M20 42a17 17 0 1 1 24 0M27 36a8 8 0 1 1 10 0"/><circle cx="47" cy="20" r="3.5"/><path d="M10 50h44"/></svg>',
'<svg viewBox="0 0 64 64"><path d="M32 55C24 55 20 52 20 49C20 45 26 43 33 43C42 43 48 40 48 36C48 31 40 28 30 29C19 30 13 27 13 23C13 18 23 14 36 15C49 16 56 12 56 8M25 49c4 2 11 2 16 0M20 39c8 3 20 2 27-2M14 27c10 4 27 3 37-2M10 16c12 5 31 4 43-1m40-7 6 0-1 7"/></svg>'
]

ALIASES = {
    "timestamp":["timestamp","tijdstip","datum","datetime"], "name":["naam","name","nom"], "email":["email","e-mail","e-mailadres"],
    "organisation":["organisatie","organisation","organization"], "code":["code","itemcode","item_code"], "pillar":["pillar","pijler"], "score":["final_score","gecorrigeerde score","score_final","score"],
}

def now_local(): return datetime.now(ZoneInfo("Europe/Brussels")).replace(tzinfo=None)

@st.cache_resource
def worksheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.readonly"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    config = st.secrets.get("dashboard", {})
    book = client.open(config.get("spreadsheet_name", "Adaptivity Maturiteitsscan"))
    tab = config.get("worksheet_name", "")
    return book.worksheet(tab) if tab else book.sheet1

@st.cache_data(ttl=15, show_spinner=False)
def load_rows(): return worksheet().get_all_records()

def column(df, key, fallback_position=None):
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for alias in ALIASES[key]:
        if alias in normalized: return normalized[alias]
    if fallback_position is not None and len(df.columns) > fallback_position: return df.columns[fallback_position]
    return None

def prepare(rows):
    df = pd.DataFrame(rows)
    if df.empty: return df
    cols = {"timestamp":column(df,"timestamp",0),"name":column(df,"name",1),"email":column(df,"email",2),"organisation":column(df,"organisation",4),"code":column(df,"code",5),"pillar":column(df,"pillar",6),"score":column(df,"score",9)}
    if not cols["timestamp"] or not cols["pillar"] or not cols["score"]: raise ValueError("Required columns missing")
    out = pd.DataFrame({k: df[v] if v is not None else "" for k,v in cols.items()})
    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce")
    out["score"] = pd.to_numeric(out["score"], errors="coerce")
    out["pillar"] = out["pillar"].astype(str).str.strip()
    out["code"] = out["code"].astype(str).str.strip()
    out["respondent"] = out["timestamp"].astype(str) + "|" + out["name"].astype(str) + "|" + out["email"].astype(str)
    return out.dropna(subset=["timestamp","score"])

st.markdown("""<style>
:root{--primary:#0f566b;--blue:#2aa5ca;--yellow:#ffc271;--light:#eef8fb;--cream:#fff7eb;--line:#cfe1e7;--text:#17313b}
.block-container{max-width:1220px;padding-top:2.2rem;padding-bottom:4rem}.hero{padding:1.6rem 1.8rem;border-radius:0 44px 44px 0;background:#0f566b;color:white;margin:0 0 1.2rem}.hero h1{margin:0;color:white;font-size:2.25rem}.hero h2{margin:.25rem 0;color:#ffc271;font-size:1.25rem}.hero p{max-width:850px;margin:.6rem 0 0}.live{display:inline-block;padding:.25rem .65rem;border-radius:99px;background:#cf256c;color:white;font-weight:800;font-size:.72rem;letter-spacing:.08em}.metric-row{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0}.metric{padding:1rem 1.1rem;border-left:5px solid #2aa5ca;border-radius:14px;background:#eef8fb}.metric b{display:block;font-size:.78rem}.metric strong{font-size:1.8rem;color:#0f566b}.cards{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.85rem}.card{padding:1rem;border:1.5px solid #0f566b;border-radius:16px;background:white;display:flex;flex-direction:column;min-height:275px}.card h3{font-size:1rem;color:#0f566b;margin:.2rem 0 .5rem}.card p{font-size:.82rem;line-height:1.4}.score{font-size:1.45rem;font-weight:800;color:#0f566b;margin-top:auto}.track{height:9px;background:#e3eff2;border-radius:99px;overflow:hidden;margin:.55rem 0}.track i{display:block;height:100%;background:linear-gradient(90deg,#2aa5ca,#0f566b)}.insight{padding:1rem;border-radius:14px;background:#fff7eb;border-left:5px solid #ffc271}.logos{display:flex;justify-content:flex-end;align-items:center;gap:1rem}.logos img{max-height:42px;max-width:130px}.privacy{margin-top:1rem;color:#667985;font-size:.8rem}@media(max-width:900px){.cards{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.cards,.metric-row{grid-template-columns:1fr}.hero{margin-left:-1rem}.card{min-height:0}}
</style>""", unsafe_allow_html=True)
st.markdown("""<style>
.metric-row{grid-template-columns:repeat(2,1fr)}.metric .badge{display:inline-flex;margin:.45rem 0 0;padding:.35rem .6rem;border-radius:9px;background:#fff7eb;color:#0f566b;font-size:.78rem;font-weight:800}.section-lead{padding:.8rem 1rem;margin:.5rem 0 1rem;border-left:5px solid #0f566b;border-radius:12px;background:#eef8fb}.overview-grid{display:grid;grid-template-columns:1.3fr .7fr;gap:1rem;align-items:stretch}.stands{padding:1rem 1.15rem;border-radius:16px;background:#eef8fb;border-left:6px solid #0f566b}.stands h3{margin-top:0}.stands ul{padding-left:1.1rem}.stands li{margin:.55rem 0}.spread-guide,.badge-guide{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin:1rem 0;padding:.8rem 1rem;border:1px solid #cfe1e7;border-radius:13px;background:#f7fbfc;font-size:.78rem}.badge-guide{grid-template-columns:repeat(2,1fr)}.behaviour-cards{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:1rem}.behaviour-card{grid-column:span 2;padding:1rem;border:1.5px solid #0f566b;border-radius:16px;background:#fff;display:flex;flex-direction:column;min-height:300px}.behaviour-card:nth-child(4){grid-column:2/span 2}.behaviour-head{display:grid;grid-template-columns:48px 1fr;gap:.75rem;min-height:112px}.pillar-icon{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:#0f566b;color:white}.pillar-icon svg{width:30px;height:30px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}.behaviour-card h3{margin:.1rem 0 .35rem;color:#0f566b;font-size:1rem}.behaviour-card p{font-size:.78rem;line-height:1.35}.card-score{display:flex;align-items:center;gap:.6rem;margin:.65rem 0}.card-score .track{flex:1}.badges{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.45rem}.status{padding:.45rem .55rem;border-radius:9px;font-size:.7rem;line-height:1.25}.status b{display:block}.status.mean{background:#fff7eb}.status.spread-low{background:#eaf6f0;color:#247c5c}.status.spread-moderate{background:#fff7eb;color:#8b641d}.status.spread-high{background:#fff0f3;color:#b33b55}.chart-shell{padding:.8rem;border:1.5px solid #cfe1e7;border-radius:18px;background:white}.maturity-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:.7rem;align-items:end;margin:1.2rem 0}.maturity-card{--level:#2aa5ca;min-height:var(--height);padding:.8rem;border:2px solid transparent;border-radius:26px 26px 14px 14px;background:linear-gradient(180deg,#fff,var(--soft));display:flex;flex-direction:column;text-align:center}.maturity-card.dominant-stage{border:4px solid var(--level);box-shadow:0 8px 24px rgba(15,86,107,.14)}.maturity-card.present-stage{border:3px dashed var(--level)}.maturity-card.absent-stage{opacity:.42;border:1px solid color-mix(in srgb,var(--level) 30%,white);background:#fbfcfd}.maturity-card .circle{width:68px;height:68px;margin:-2.1rem auto .6rem;border:6px solid var(--level);border-radius:50%;background:white;display:grid;place-items:center;color:var(--level)}.maturity-card .circle svg{width:42px;height:42px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}.maturity-card small{font-weight:800;color:var(--level)}.maturity-card h3{font-size:.86rem;color:var(--level);min-height:3.2rem}.maturity-card p{font-size:.7rem;line-height:1.35}.maturity-count{margin-top:auto;padding-top:.7rem;border-top:1px solid var(--level);font-size:.72rem}.maturity-count b{font-size:1.45rem}.share-track{height:10px;margin:.5rem 0 .25rem;border-radius:99px;background:rgba(255,255,255,.8);border:1px solid color-mix(in srgb,var(--level) 30%,white);overflow:hidden}.share-track i{display:block;height:100%;background:var(--level)}.pattern-legend{display:flex;justify-content:center;flex-wrap:wrap;gap:1rem;margin:.8rem 0 1.7rem;font-size:.75rem}.pattern-legend span{display:inline-flex;align-items:center;gap:.4rem}.pattern-legend i{display:inline-block;width:30px;border-top:3px solid #0f566b}.pattern-legend i.dashed{border-top-style:dashed}.pattern-legend i.muted{border-top:2px solid #b9c5ca;opacity:.5}.dominant{display:inline-block;padding:.3rem .7rem;border-radius:99px;background:#ffc271;color:#0f566b;font-size:.74rem;font-weight:800}.progression{padding:.8rem 1rem;border:1px solid #cfe1e7;border-radius:13px;background:#f7fbfc;display:flex;justify-content:space-between;font-size:.75rem;font-weight:800}.privacy-warning{padding:.7rem 1rem;border-radius:10px;background:#fff7eb;color:#8b641d;font-size:.78rem}@media(max-width:900px){.overview-grid{grid-template-columns:1fr}.behaviour-cards{grid-template-columns:1fr 1fr}.behaviour-card,.behaviour-card:nth-child(4){grid-column:auto}.maturity-grid{grid-template-columns:1fr 1fr;align-items:stretch}.maturity-card{min-height:300px;margin-top:2rem}}@media(max-width:600px){.behaviour-cards,.maturity-grid,.spread-guide,.badge-guide{grid-template-columns:1fr}.maturity-card{min-height:0}.progression{flex-direction:column;gap:.35rem}}
</style>""", unsafe_allow_html=True)

if "dashboard_started" not in st.session_state: st.session_state.dashboard_started = now_local()
top_left, top_right = st.columns([5,2], vertical_alignment="center")
with top_right:
    logo1, logo2 = st.columns(2, vertical_alignment="center")
    with logo1: st.image("assets/logo Coliberate.png", use_container_width=True)
    with logo2: st.image("assets/logo KULtivating.webp", use_container_width=True)
    lang = st.selectbox("Language · Taal · Langue", LANGUAGES, format_func=LANGUAGES.get, label_visibility="collapsed")
t = TEXT[lang]
with top_left: st.markdown(f'<div class="hero"><span class="live">{t["live"]}</span><h1>{t["title"]}</h1><h2>{SUBTITLE[lang]}</h2><p>{INTRO[lang]}</p></div>', unsafe_allow_html=True)

expected_code = str(st.secrets.get("dashboard", {}).get("access_code", "")).strip()
if expected_code:
    entered_code = st.text_input(t["access"], type="password", help=t["access_help"])
    if not entered_code: st.stop()
    if not compare_digest(entered_code, expected_code): st.error(t["access_wrong"]); st.stop()

control1, control2, control3 = st.columns([2.2,1.5,1])
period_keys = ["session","hour","day","all"]
with control1: period = st.selectbox(t["period"], period_keys, format_func=lambda x:t[x])
with control3:
    st.write("")
    if st.button(t["refresh"], use_container_width=True): st.cache_data.clear(); st.rerun()

try:
    data = prepare(load_rows())
except Exception:
    st.error(t["source_error"]); st.stop()

with control2:
    orgs = sorted(x for x in data.get("organisation", pd.Series(dtype=str)).dropna().astype(str).str.strip().unique() if x)
    selected_org = st.selectbox(t["organisation_filter"], [""] + orgs, format_func=lambda x: t["all_orgs"] if x == "" else x)

now = now_local()
cutoffs = {"session":st.session_state.dashboard_started,"hour":now-timedelta(hours=1),"day":now-timedelta(days=1)}
filtered = data.copy()
if period != "all": filtered = filtered[filtered["timestamp"] >= cutoffs[period]]
if selected_org: filtered = filtered[filtered["organisation"].astype(str).str.strip() == selected_org]

st.caption(f'{t["updated"]}: {now:%d/%m/%Y %H:%M:%S} · {t["period_note"]}: ' + (t["full"] if period == "all" else f'{t["from"]} {cutoffs[period]:%d/%m/%Y %H:%M}'))
if filtered.empty:
    st.info(t["no_data"]); st.stop()

n_people = filtered["respondent"].nunique()
respondent_pillars = filtered[filtered["pillar"].isin(PILLARS)].groupby(["respondent","pillar"])["score"].mean().unstack().reindex(columns=PILLARS)
means = respondent_pillars.mean().dropna()
sds = respondent_pillars.std(ddof=1).reindex(means.index)
low_band = respondent_pillars.quantile(.10).reindex(means.index)
high_band = respondent_pillars.quantile(.90).reindex(means.index)
overall = means.mean()
pillar_percentiles = pd.Series({code:percentile(code,score) for code,score in means.items()})
overall_percentile = pillar_percentiles.mean()
c=COPY[lang]
p_labels={"very_low":c["p_very_low"],"low":c["p_low"],"middle":c["p_middle"],"high":c["p_high"],"very_high":c["p_very_high"]}
s_labels={"low":c["s_low"],"moderate":c["s_moderate"],"high":c["s_high"],"unavailable":c["s_unavailable"]}
overall_label=p_labels[percentile_band(overall_percentile)]
st.markdown(f'<div class="metric-row"><div class="metric"><b>{t["responses"]}</b><strong>{n_people}</strong></div><div class="metric"><b>{t["average"]}</b><strong>{overall:.2f} / 7</strong><span class="badge">P{overall_percentile:.0f} · {overall_label}</span></div></div>',unsafe_allow_html=True)
if n_people < 3: st.markdown(f'<div class="privacy-warning">{c["privacy_small"]}</div>',unsafe_allow_html=True)

st.subheader(c["overview"])
st.markdown(f'<div class="section-lead">{c["overview_intro"]}</div>',unsafe_allow_html=True)
chart_col,stands_col=st.columns([1.3,.7],gap="large",vertical_alignment="top")
labels=[PILLAR_TEXT[lang][code][0] for code in means.index]
closed_labels=labels+[labels[0]]; closed_mean=list(means)+[means.iloc[0]]; closed_low=list(low_band)+[low_band.iloc[0]];closed_high=list(high_band)+[high_band.iloc[0]]
radar=go.Figure()
radar.add_trace(go.Scatterpolar(r=closed_low,theta=closed_labels,line=dict(color="rgba(42,165,202,0)"),hoverinfo="skip",showlegend=False))
radar.add_trace(go.Scatterpolar(r=closed_high,theta=closed_labels,fill="tonext",fillcolor="rgba(42,165,202,.16)",line=dict(color="rgba(42,165,202,.25)"),name=c["radar_band"]))
radar.add_trace(go.Scatterpolar(r=closed_mean,theta=closed_labels,line=dict(color="#0f566b",width=3),marker=dict(size=7,color="#0f566b"),name=c["group_mean"]))
radar.update_layout(height=440,margin=dict(l=45,r=45,t=35,b=35),paper_bgcolor="rgba(0,0,0,0)",polar=dict(bgcolor="white",radialaxis=dict(range=[1,7],tickvals=[1,2,3,4,5,6,7],gridcolor="#cfe1e7"),angularaxis=dict(gridcolor="#dce9ed")),legend=dict(orientation="h",y=-.12,x=.15))
with chart_col: st.plotly_chart(radar,use_container_width=True,config={"displayModeBar":False})
high,low=means.idxmax(),means.idxmin();largest=sds.idxmax() if sds.notna().any() else high;smallest=sds.idxmin() if sds.notna().any() else low
largest_sd="—" if pd.isna(sds[largest]) else f'{sds[largest]:.2f}';smallest_sd="—" if pd.isna(sds[smallest]) else f'{sds[smallest]:.2f}'
with stands_col:
    st.markdown(f'''<div class="stands"><h3>{c["stands"]}</h3><ul>
    <li><b>{t["strongest"]}</b><br>{PILLAR_TEXT[lang][high][0]} · {means[high]:.2f}/7 · P{pillar_percentiles[high]:.0f}</li>
    <li><b>{t["opportunity"]}</b><br>{PILLAR_TEXT[lang][low][0]} · {means[low]:.2f}/7 · P{pillar_percentiles[low]:.0f}</li>
    <li><b>{c["largest"]}</b><br>{PILLAR_TEXT[lang][largest][0]} · SD {largest_sd}</li>
    <li><b>{c["smallest"]}</b><br>{PILLAR_TEXT[lang][smallest][0]} · SD {smallest_sd}</li></ul></div>''',unsafe_allow_html=True)

st.markdown(f'<div class="spread-guide"><div><b>{c["spread_guide"]}</b></div><div>{c["spread_low"]}</div><div>{c["spread_mid"]}<br>{c["spread_high"]}</div></div>',unsafe_allow_html=True)
cards=[]
for code,score in means.items():
    title,desc=PILLAR_TEXT[lang][code];pct=pillar_percentiles[code];p_label=p_labels[percentile_band(pct)];sd=sds[code];s_band=spread_band(sd);s_label=s_labels[s_band];sd_text="—" if pd.isna(sd) else f'{sd:.2f}'
    cards.append(f'''<article class="behaviour-card"><div class="behaviour-head"><span class="pillar-icon">{PILLAR_ICONS[code]}</span><div><h3>{title}</h3><p>{desc}</p></div></div><div class="card-score"><b>{c["group_mean"]}</b><div class="track"><i style="width:{score/7*100:.1f}%"></i></div><strong>{score:.2f}/7</strong></div><div class="badges"><div class="status mean"><b>{c["benchmark"]}</b>{p_label} · P{pct:.0f}</div><div class="status spread-{s_band}"><b>{c["spread"]}</b>{s_label} · SD {sd_text}</div></div></article>''')
st.markdown(f'<div class="behaviour-cards">{"".join(cards)}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="badge-guide"><div><b>{c["benchmark"]}</b><br>{c["benchmark_help"]}</div><div><b>{c["spread"]}</b><br>{c["spread_help"]}</div></div>',unsafe_allow_html=True)

st.subheader(c["distribution"]);st.markdown(f'<div class="section-lead">{c["distribution_intro"]}</div>',unsafe_allow_html=True)
category_labels={"nl":["Zeer beperkt","Beperkt","Eerder beperkt","Midden","Eerder sterk","Sterk","Zeer sterk"],"fr":["Très limité","Limité","Plutôt limité","Milieu","Plutôt fort","Fort","Très fort"],"en":["Very limited","Limited","Rather limited","Middle","Rather strong","Strong","Very strong"]}[lang]
colors=["#edf7f9","#dceff3","#c6e6ed","#9ed5e1","#69bed1","#2aa5ca","#0f566b"]
dist=go.Figure()
rounded=respondent_pillars.round().clip(1,7)
for value,label,color in zip(range(1,8),category_labels,colors):
    percentages=[(rounded[code].eq(value).sum()/rounded[code].notna().sum()*100 if rounded[code].notna().sum() else 0) for code in means.index]
    dist.add_trace(go.Bar(y=labels,x=percentages,name=label,orientation="h",marker_color=color,text=[f"{v:.0f}%" if v>=5 else "" for v in percentages],textposition="inside"))
dist.update_layout(barmode="stack",height=380,margin=dict(l=10,r=10,t=30,b=30),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white",xaxis=dict(range=[0,100],title="%"),yaxis=dict(autorange="reversed"),legend=dict(orientation="h",y=1.18,x=0))
st.plotly_chart(dist,use_container_width=True,config={"displayModeBar":False})

levels=respondent_maturity(filtered)
if not levels.empty:
    counts=levels.value_counts().reindex(range(6),fill_value=0);dominant=int(counts.idxmax());total=int(counts.sum())
    st.subheader(c["maturity"]);st.markdown(f'<div class="section-lead">{c["maturity_intro"]}</div><span class="dominant">{c["dominant"]}: {MATURITY[lang][dominant][0]}</span>',unsafe_allow_html=True)
    level_colors=["#cf256c","#eb8500","#199fa7","#118b8d","#0879bd","#0c447f"];softs=["#fff0f3","#fff7eb","#eefafa","#edf8f5","#eef6fb","#edf2f8"];heights=[330,350,370,390,410,430]
    maturity_cards=[]
    for level,(label,desc) in enumerate(MATURITY[lang]):
        count=int(counts[level]);percentage=count/total*100
        stage_class="dominant-stage" if level==dominant else "present-stage" if count>0 else "absent-stage"
        maturity_cards.append(f'<article class="maturity-card {stage_class}" style="--level:{level_colors[level]};--soft:{softs[level]};--height:{heights[level]}px"><div class="circle">{MATURITY_ICONS[level]}</div><small>{LEVEL_LABEL[lang]} {level}</small><h3>{label}</h3><p>{desc}</p><div class="maturity-count"><b>{count}</b> {c["respondents"]}<div class="share-track"><i style="width:{percentage:.1f}%"></i></div><strong>{percentage:.0f}%</strong></div></article>')
    legend=PATTERN_LEGEND[lang]
    st.markdown(f'<div class="maturity-grid">{"".join(maturity_cards)}</div><div class="pattern-legend"><span><i></i>{legend[0]}</span><span><i class="dashed"></i>{legend[1]}</span><span><i class="muted"></i>{legend[2]}</span></div><div class="progression"><span>{c["progress"]}</span><span>→</span><span>{MATURITY[lang][2][0]}</span><span>→</span><span>{MATURITY[lang][4][0]}</span><span>→</span><span>{MATURITY[lang][5][0]}</span></div>',unsafe_allow_html=True)
st.markdown(f'<p class="privacy">{t["privacy"]}</p>',unsafe_allow_html=True)
