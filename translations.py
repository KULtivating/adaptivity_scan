"""Taalinhoud voor de Adaptiviteit Maturiteitsscan.

De itemcodes blijven in elke taal identiek. Daardoor veranderen vertalingen
nooit de scoring of de koppeling met historische antwoorden.
"""

TRANSLATIONS_BUILD = "2026-08-06-maturity-compact-interpretations-v1"

LANGUAGE_NAMES = {"nl": "Nederlands", "fr": "Français", "en": "English"}

UI_TEXTS = {
    "nl": {
        "app_title": "Adaptiviteit Maturiteitsscan",
        "app_intro": "Ontdek in enkele minuten hoe jij omgaat met verandering, leren, veerkracht en innovatie.",
        "details_step": "Stap 1 · Je gegevens", "details_title": "Vertel ons kort wie je bent",
        "scan_step": "Stap 2 · Adaptiviteitsscan", "scan_title": "Duid voor elke uitspraak aan hoe vaak dit bij jou voorkomt",
        "name": "Naam", "email": "E-mailadres (optioneel)",
        "email_help": "We bewaren dit alleen zodat we je resultaat later eventueel kunnen bezorgen. Er wordt nu geen e-mail verstuurd.",
        "role": "Functie", "organisation": "Organisatie", "start": "Start vragenlijst",
        "submit": "Toon mijn resultaat", "missing": "Vul alle vragen in om je resultaat te bekijken.",
        "complete": "Alle vragen zijn ingevuld.", "thanks": "Bedankt voor je deelname",
        "profile": "Jouw persoonlijke adaptiviteit",
        "profile_intro": "Adaptiviteit beschrijft hoe je veerkrachtig omgaat met het heden én hoe je je voorbereidt op wat komt.",
        "core_profile": "Jouw kernprofiel", "pillars": "Jouw vijf kernpijlers",
        "interpretation": "Jouw interpretatie", "adaptivity": "Je adaptiviteit", "restart": "Opnieuw invullen",
        "what_stands_out": "Wat valt op?", "strongest": "Sterkste pijler", "development": "Grootste ontwikkelkans",
        "percentile": "Interpretatie", "no_norm": "Geen normdata",
        "percentile_very_low": "Laagste 20%", "percentile_low": "Onder gemiddeld", "percentile_middle": "Gemiddeld",
        "percentile_high": "Boven gemiddeld", "percentile_very_high": "Top 20%",
        "percentile_guide": "Pxx toont je positie ten opzichte van de externe normgroep. P76 betekent bijvoorbeeld dat je hoger scoort dan ongeveer 76% van die normgroep; het is geen percentage juiste antwoorden.",
        "percentile_tooltip": "P{p} betekent dat je hoger scoort dan ongeveer {p}% van de externe normgroep.",
        "scale": ["Nooit", "Zeer zelden", "Zelden", "Soms", "Regelmatig", "Vaak", "Altijd"],
    },
    "fr": {
        "app_title": "Scan de maturité de l’adaptabilité",
        "app_intro": "Découvrez en quelques minutes comment vous abordez le changement, l’apprentissage, la résilience et l’innovation.",
        "details_step": "Étape 1 · Vos informations", "details_title": "Parlez-nous brièvement de vous",
        "scan_step": "Étape 2 · Scan d’adaptabilité", "scan_title": "Pour chaque affirmation, indiquez à quelle fréquence elle vous correspond",
        "name": "Nom", "email": "Adresse e-mail (facultatif)",
        "email_help": "Nous la conservons uniquement afin de pouvoir éventuellement vous envoyer votre résultat ultérieurement. Aucun e-mail n’est envoyé maintenant.",
        "role": "Fonction", "organisation": "Organisation", "start": "Commencer le questionnaire",
        "submit": "Afficher mon résultat", "missing": "Répondez à toutes les questions pour afficher votre résultat.",
        "complete": "Toutes les questions ont été complétées.", "thanks": "Merci pour votre participation",
        "profile": "Votre adaptabilité personnelle",
        "profile_intro": "L’adaptabilité décrit votre capacité à faire face au présent avec résilience et à vous préparer à ce qui vient.",
        "core_profile": "Votre profil en un coup d’œil", "pillars": "Vos cinq piliers clés",
        "interpretation": "Votre interprétation", "adaptivity": "Votre adaptabilité", "restart": "Recommencer",
        "what_stands_out": "Que retenir ?", "strongest": "Pilier le plus fort", "development": "Principale opportunité de développement",
        "percentile": "Interprétation", "no_norm": "Pas de données normatives",
        "percentile_very_low": "20 % les plus faibles", "percentile_low": "Sous la moyenne", "percentile_middle": "Moyenne",
        "percentile_high": "Au-dessus de la moyenne", "percentile_very_high": "Top 20 %",
        "percentile_guide": "Pxx indique votre position par rapport au groupe de référence externe. P76 signifie, par exemple, que votre score est supérieur à celui d’environ 76 % de ce groupe ; il ne s’agit pas d’un pourcentage de bonnes réponses.",
        "percentile_tooltip": "P{p} signifie que votre score est supérieur à celui d’environ {p} % du groupe de référence externe.",
        "scale": ["Jamais", "Très rarement", "Rarement", "Parfois", "Régulièrement", "Souvent", "Toujours"],
    },
    "en": {
        "app_title": "Adaptivity Maturity Scan",
        "app_intro": "Discover in just a few minutes how you approach change, learning, resilience and innovation.",
        "details_step": "Step 1 · Your details", "details_title": "Tell us a little about yourself",
        "scan_step": "Step 2 · Adaptivity scan", "scan_title": "For each statement, indicate how often it applies to you",
        "name": "Name", "email": "Email address (optional)",
        "email_help": "We only store this so that we may send you your result later. No email is sent now.",
        "role": "Role", "organisation": "Organisation", "start": "Start questionnaire",
        "submit": "Show my result", "missing": "Answer all questions to view your result.",
        "complete": "All questions have been answered.", "thanks": "Thank you for taking part",
        "profile": "Your personal adaptivity",
        "profile_intro": "Adaptivity describes how resiliently you deal with the present and how you prepare for what lies ahead.",
        "core_profile": "Your profile at a glance", "pillars": "Your five core pillars",
        "interpretation": "Your interpretation", "adaptivity": "Your adaptivity", "restart": "Start again",
        "what_stands_out": "What stands out?", "strongest": "Strongest pillar", "development": "Main development opportunity",
        "percentile": "Interpretation", "no_norm": "No normative data",
        "percentile_very_low": "Bottom 20%", "percentile_low": "Below average", "percentile_middle": "Average",
        "percentile_high": "Above average", "percentile_very_high": "Top 20%",
        "percentile_guide": "Pxx shows your position relative to the external reference group. P76, for example, means that you scored higher than approximately 76% of that group; it is not a percentage of correct answers.",
        "percentile_tooltip": "P{p} means that you scored higher than approximately {p}% of the external reference group.",
        "scale": ["Never", "Very rarely", "Rarely", "Sometimes", "Regularly", "Often", "Always"],
    },
}

QUESTION_TRANSLATIONS = {
    "fr": {
        "CR_CA1": "J’accepte le changement tel qu’il se présente.",
        "CR_CD1": "Je garde mes réticences face au changement pour moi.",
        "CR_CD3": "Je me tiens à l’écart de tout ce qui concerne le changement.",
        "CR_CA2": "Je collabore efficacement à la mise en œuvre des plans de changement.",
        "CR_CR1": "Je m’oppose activement au changement.",
        "CR_CP1": "Je soutiens activement le changement.",
        "CR_CR3": "J’essaie activement d’influencer ou de freiner les changements.",
        "CR_CD2": "Je tends à remettre à plus tard la mise en œuvre des changements.",
        "CR_CP3": "Je prends moi-même l’initiative de mettre les changements en pratique.",
        "LO_M": "Je suis motivé(e) à apprendre de nouvelles choses.",
        "Res2": "Je peux facilement m’adapter à des situations changeantes.",
        "Res3": "Je récupère rapidement lorsque je suis confronté(e) à des difficultés.",
        "IAP_WS1": "Je reste calme dans les situations où je dois prendre de nombreuses décisions.",
        "IAP_R2": "J’adapte facilement mon travail à de nouvelles circonstances.",
        "IAP_I2": "J’adapte volontiers mon comportement lorsque cela est nécessaire pour bien collaborer avec les autres.",
        "IAP_T1": "Je participe régulièrement à des formations, au travail comme en dehors, afin de maintenir mes compétences à jour.",
        "IAP_C2": "Dans mon équipe ou mon département, les autres font appel à moi pour proposer de nouvelles solutions.",
        "IAP_T2": "Je recherche activement toute opportunité pouvant m’aider à améliorer ma performance (formation, projet de groupe, échanges avec des collègues, etc.).",
        "LO_A": "Je prends moi-même l’initiative de définir ce que j’apprends et la manière dont je l’apprends.",    
        "PB_SS1": "Je suis attentif(ve) aux évolutions de mon environnement afin d’identifier ce qui pourrait influencer mon travail à l’avenir.",
        "PB_SS3": "Je réfléchis de manière proactive aux changements que pourraient connaître mon organisation en raison des évolutions de son environnement (p. ex. le marché, la technologie).",
        "PB_PP1": "J’essaie de développer des méthodes de travail et des systèmes efficaces à long terme, même si cela demande plus de temps au départ. ",
        "PB_PP2": "J’essaie d’identifier la véritable cause des problèmes qui se présentent.",
        "IAP_Rx": "J’anticipe les problèmes potentiels en élaborant à l’avance différents scénarios et options de décision afin d’être préparé(e) lorsque la situation l’exige.",
        "IAP_Ix": "Je développe activement un réseau professionnel qui me permet, ainsi qu’aux autres, de mieux anticiper, gérer et exploiter les changements futurs. ",
        "IAP_WSx": "J’améliore les structures et les processus afin de prévenir les situations de crise et de réduire le stress à l’avenir.",
        "IBIncr6": "Je recherche de nouvelles façons d’utiliser la technologie pour améliorer mon travail.",
        "IBRad4": "Je recherche de manière autonome de nouvelles méthodes de travail, techniques ou outils.",
        "EISB1": "J’entreprends des actions pour concrétiser le changement dans mon travail.",
        "EISB4": "Je propose de nouvelles méthodes de travail pour mon organisation.",
        "VOICE": "Je formule activement des idées et fais des propositions sur la manière dont mon organisation peut se renouveler pour faire face aux changements futurs.",
    },
    "en": {
        "CR_CA1": "I accept change as it is.",
        "CR_CD1": "I keep my resistance to change to myself.",
        "CR_CD3": "I withdraw from anything related to change.",
        "CR_CA2": "I cooperate effectively with plans for change.",
        "CR_CR1": "I actively resist change.",
        "CR_CP1": "I actively support change.",
        "CR_CR3": "I actively try to influence or delay change.",
        "CR_CD2": "I procrastinate when implementing change.",
        "CR_CP3": "I take the initiative to put changes into practice.",
        "LO_M": "I am motivated to learn new things.",
        "Res2": "I adapt easily to changing situations.",
        "Res3": "I recover quickly when I experience a setback.",
        "IAP_WS1": "I remain calm in situations where I have to make many decisions.",
        "IAP_R2": "I adapt my work easily to new circumstances.",
        "IAP_I2": "I readily adapt my behaviour when this is needed to work well with others.",
        "IAP_T1": "I regularly attend training at or outside work to keep my skills up to date.",
        "IAP_C2": "People in my team or department turn to me for new solutions.",
        "IAP_T2": "I actively seek every opportunity to improve how I perform (training, group projects, exchanges with colleagues, etc.).",
        "LO_A": "I take the initiative in deciding what and how I learn.",
        "PB_SS1": "I actively monitor the world around me to identify what may affect my job in the future.",
        "PB_SS3": "I think ahead about possible changes in my organisation resulting from developments in the outside world, such as markets or technology.",
        "PB_PP1": "I try to develop ways of working and systems that are effective in the long term, even if they take more time initially.",
        "PB_PP2": "I try to identify the root cause of problems that occur.",
        "IAP_Rx": "I anticipate potential problems by developing scenarios and decision options before they are needed.",
        "IAP_Ix": "I deliberately build network relationships that help me and others better absorb or benefit from future changes.",
        "IAP_WSx": "I reduce future stress by improving structures and processes and thereby preventing crisis situations.",
        "IBIncr6": "I devise new ways to make better use of technology in my work.",
        "IBRad4": "I independently seek out new working methods, techniques or tools.",
        "EISB1": "I take action to bring about change in my work.",
        "EISB4": "I devise new ways of working for my organisation.",
        "VOICE": "I actively voice ideas and make proposals about how my organisation can renew itself to deal with future changes.",
    },
}

SHORT_DESCRIPTIONS = {
    "nl": {
        "VA": "Positief en constructief omgaan met verandering.", "VZ": "Omgaan met druk en emoties en herstellen bij tegenslag.",
        "LO": "Continu willen leren en jezelf ontwikkelen.", "VV": "Anticiperen op toekomstige veranderingen en je voorbereiden.",
        "CI": "Nieuwe ideeën bedenken en toepassen om vooruit te gaan.",
    },
    "fr": {
        "VA": "Aborder le changement de manière positive et constructive.", "VZ": "Gérer la pression et les émotions et rebondir après un revers.",
        "LO": "Continuer à apprendre et à se développer.", "VV": "Anticiper les changements futurs et s’y préparer.",
        "CI": "Imaginer et appliquer de nouvelles idées pour progresser.",
    },
    "en": {
        "VA": "Approaching change positively and constructively.", "VZ": "Managing pressure and emotions and recovering from setbacks.",
        "LO": "Continuing to learn and develop.", "VV": "Anticipating future changes and preparing for them.",
        "CI": "Developing and applying new ideas to move forward.",
    },
}


PILLAR_RADAR_LABELS = {'nl': {'VA': 'Veranderattitude',
        'VZ': 'Veerkracht<br>& Zelfregulatie',
        'LO': 'Leermotivatie<br>& Ontwikkeling',
        'VV': 'Vooruitzien<br>& Voorbereiden',
        'CI': 'Creativiteit<br>& Innovatie'},
 'fr': {'VA': 'Attitude face<br>au changement',
        'VZ': 'Résilience<br>& Autorégulation',
        'LO': 'Motivation à apprendre<br>& Développement',
        'VV': 'Anticipation<br>& Préparation',
        'CI': 'Créativité<br>& Innovation'},
 'en': {'VA': 'Change<br>Attitude',
        'VZ': 'Resilience<br>& Self-regulation',
        'LO': 'Learning Motivation<br>& Development',
        'VV': 'Anticipating<br>& Preparing',
        'CI': 'Creativity<br>& Innovation'}}

PILLAR_INTERPRETATIONS = {'nl': {'VA': {'low': 'Voor deze dimensie scoor je bij de laagste 20% van de benchmarkgroep. Verandering roept vaak '
                      'terughoudendheid of weerstand op, waardoor nieuwe werkwijzen verkennen en mee richting geven '
                      'meer energie kost. Dit is een duidelijke ontwikkelkans.',
               'below_average': 'Voor deze dimensie scoor je onder het gemiddelde van de benchmarkgroep. Je staat '
                                'eerder afwachtend of kritisch tegenover verandering. Je ziet mogelijk de noodzaak, '
                                'maar vertaalt die nog niet altijd in actieve steun of eigenaarschap.',
               'average': 'Voor deze dimensie scoor je rond het gemiddelde van de benchmarkgroep. Je houding tegenover '
                          'verandering is meestal werkbaar: bij duidelijke meerwaarde beweeg je mee, terwijl '
                          'onzekerheid of weinig inspraak je kritischer of terughoudender kan maken.',
               'above_average': 'Voor deze dimensie scoor je boven het gemiddelde van de benchmarkgroep. Je benadert '
                                'verandering meestal constructief, denkt mee en neemt initiatief. Die open houding '
                                'helpt ook bij onzekerheid beweging te creëren.',
               'high': 'Voor deze dimensie behoor je tot de hoogste 20% van de benchmarkgroep. Je gaat actief en '
                       'constructief met verandering om, geeft ze betekenis en neemt gemakkelijk eigenaarschap. Met je '
                       'houding neem je vaak ook anderen mee.'},
        'VZ': {'low': 'Voor deze dimensie scoor je bij de laagste 20% van de benchmarkgroep. Druk, tegenslag of '
                      'onverwachte gebeurtenissen verstoren je functioneren relatief sterk en herstel vraagt vaak tijd '
                      'of ondersteuning. Dit is een belangrijke ontwikkelkans.',
               'below_average': 'Voor deze dimensie scoor je onder het gemiddelde van de benchmarkgroep. Je vangt '
                                'moeilijke situaties op, maar je evenwicht en herstel zijn niet altijd stabiel. Bij '
                                'aanhoudende druk wordt het lastiger om aandacht, emoties en energie gericht te '
                                'reguleren.',
               'average': 'Voor deze dimensie scoor je rond het gemiddelde van de benchmarkgroep. Je blijft meestal '
                          'voldoende functioneren en herstelt doorgaans na tegenslag. Bij langdurige druk of meerdere '
                          'veranderingen kan extra structuur of steun nodig zijn.',
               'above_average': 'Voor deze dimensie scoor je boven het gemiddelde van de benchmarkgroep. Je blijft '
                                'meestal rustig en doelgericht onder druk en herstelt vlot na tegenslag. Zo blijf je '
                                'ook in complexe situaties keuzes maken en je aanpak bijsturen.',
               'high': 'Voor deze dimensie behoor je tot de hoogste 20% van de benchmarkgroep. Je blijft uitzonderlijk '
                       'stabiel onder druk, herstelt snel en reguleert je aandacht en energie sterk. In moeilijke '
                       'omstandigheden bied je vaak ook anderen rust en houvast.'},
        'LO': {'low': 'Voor deze dimensie scoor je bij de laagste 20% van de benchmarkgroep. Je zoekt momenteel weinig '
                      'actief naar feedback, oefenkansen of nieuwe kennis. Daardoor zet je ervaringen minder '
                      'vanzelfsprekend om in ontwikkeling. Dit is een duidelijke groeikans.',
               'below_average': 'Voor deze dimensie scoor je onder het gemiddelde van de benchmarkgroep. Je leert '
                                'vooral wanneer de taak of situatie dat vraagt. Zelf leerdoelen kiezen, feedback '
                                'ophalen en inzichten toepassen gebeurt nog minder consequent.',
               'average': 'Voor deze dimensie scoor je rond het gemiddelde van de benchmarkgroep. Je staat open voor '
                          'leren en gebruikt relevante feedback wanneer die beschikbaar is. Hoe gericht je oefent en '
                          'ontwikkeling volhoudt, verschilt nog per context.',
               'above_average': 'Voor deze dimensie scoor je boven het gemiddelde van de benchmarkgroep. Je zoekt '
                                'actief kennis, feedback en kansen om te groeien. Nieuwe inzichten vertaal je meestal '
                                'naar je werk en zo versterk je gericht je vermogen om met verandering om te gaan.',
               'high': 'Voor deze dimensie behoor je tot de hoogste 20% van de benchmarkgroep. Leren en ontwikkelen '
                       'zijn een sterke motor in je werk. Je zoekt systematisch feedback en nieuwe perspectieven, past '
                       'inzichten toe en stimuleert vaak ook het leren van anderen.'},
        'VV': {'low': 'Voor deze dimensie scoor je bij de laagste 20% van de benchmarkgroep. Je aandacht ligt vooral '
                      'bij wat vandaag speelt, waardoor je vroege signalen en toekomstige gevolgen minder snel '
                      'opmerkt. Je voorbereiding is vaak reactief en vormt een duidelijke ontwikkelkans.',
               'below_average': 'Voor deze dimensie scoor je onder het gemiddelde van de benchmarkgroep. Je kijkt soms '
                                'vooruit, maar vertaalt signalen nog niet consequent naar scenario’s of voorbereiding. '
                                'Daardoor kunnen veranderingen je vaker verrassen dan nodig.',
               'average': 'Voor deze dimensie scoor je rond het gemiddelde van de benchmarkgroep. Je houdt rekening '
                          'met wat eraan komt en bereidt je voor zodra signalen duidelijk zijn. Bij meer onzekerheid '
                          'of een langere tijdshorizon wordt vooruitdenken minder systematisch.',
               'above_average': 'Voor deze dimensie scoor je boven het gemiddelde van de benchmarkgroep. Je merkt '
                                'relevante signalen vroeg op en vertaalt ze naar haalbare voorbereidingen. Zo houd je '
                                'opties open en hoef je minder reactief te handelen.',
               'high': 'Voor deze dimensie behoor je tot de hoogste 20% van de benchmarkgroep. Vooruitkijken is een '
                       'duidelijke sterkte: je verbindt signalen, verkent scenario’s en bereidt je tijdig voor. Zo '
                       'help je vaak ook anderen om toekomstige verandering concreet te maken.'},
        'CI': {'low': 'Voor deze dimensie scoor je bij de laagste 20% van de benchmarkgroep. Je grijpt vaak terug naar '
                      'bekende oplossingen en experimenteert weinig met alternatieven. Daardoor blijven mogelijke '
                      'verbeteringen sneller onbenut. Dit is een duidelijke ontwikkelkans.',
               'below_average': 'Voor deze dimensie scoor je onder het gemiddelde van de benchmarkgroep. Je ziet soms '
                                'nieuwe mogelijkheden, maar zet ze nog weinig om in concrete tests of verbeteringen. '
                                'Bij onzekerheid krijgt de vertrouwde aanpak meestal voorrang.',
               'average': 'Voor deze dimensie scoor je rond het gemiddelde van de benchmarkgroep. Je komt met '
                          'bruikbare ideeën wanneer de situatie daarom vraagt. Of je ermee experimenteert en ze '
                          'realiseert, hangt nog sterk af van tijd, ruimte en steun.',
               'above_average': 'Voor deze dimensie scoor je boven het gemiddelde van de benchmarkgroep. Je ontwikkelt '
                                'geregeld nieuwe ideeën en test alternatieven doelgericht. Zo verbind je creativiteit '
                                'meestal met praktische verbetering in je werk.',
               'high': 'Voor deze dimensie behoor je tot de hoogste 20% van de benchmarkgroep. Creatief vernieuwen is '
                       'een duidelijke sterkte: je ziet onverwachte mogelijkheden, experimenteert doelgericht en zet '
                       'ideeën om in zichtbare verbetering. Daarmee stimuleer je vaak ook anderen.'}},
 'fr': {'VA': {'low': 'Pour cette dimension, votre score se situe parmi les 20 % les plus faibles du groupe de '
                      'référence. Le changement suscite souvent réserve ou résistance, ce qui demande davantage '
                      'd’énergie pour explorer de nouvelles méthodes et contribuer à l’orientation. C’est une occasion '
                      'de développement claire.',
               'below_average': 'Pour cette dimension, votre score se situe sous la moyenne du groupe de référence. '
                                'Vous adoptez plus souvent une attitude prudente ou critique face au changement. Vous '
                                'en voyez peut-être la nécessité, sans toujours la traduire en soutien actif ou en '
                                'prise de responsabilité.',
               'average': 'Pour cette dimension, votre score se situe autour de la moyenne du groupe de référence. '
                          'Votre attitude face au changement est généralement constructive : vous avancez lorsque la '
                          'valeur ajoutée est claire, tandis que l’incertitude ou le manque de participation peuvent '
                          'vous rendre plus critique ou réservé.',
               'above_average': 'Pour cette dimension, votre score se situe au-dessus de la moyenne du groupe de '
                                'référence. Vous abordez généralement le changement de manière constructive, '
                                'contribuez à la réflexion et prenez des initiatives. Cette ouverture aide aussi à '
                                'créer du mouvement dans l’incertitude.',
               'high': 'Pour cette dimension, votre score se situe parmi les 20 % les plus élevés du groupe de '
                       'référence. Vous abordez le changement de manière active et constructive, lui donnez du sens et '
                       'prenez facilement vos responsabilités. Votre attitude entraîne souvent aussi les autres.'},
        'VZ': {'low': 'Pour cette dimension, votre score se situe parmi les 20 % les plus faibles du groupe de '
                      'référence. La pression, les revers ou les imprévus perturbent relativement fortement votre '
                      'fonctionnement, et la récupération demande souvent du temps ou du soutien. C’est une occasion '
                      'de développement importante.',
               'below_average': 'Pour cette dimension, votre score se situe sous la moyenne du groupe de référence. '
                                'Vous faites face aux situations difficiles, mais votre équilibre et votre '
                                'récupération ne sont pas toujours stables. Sous une pression prolongée, il devient '
                                'plus difficile de réguler votre attention, vos émotions et votre énergie.',
               'average': 'Pour cette dimension, votre score se situe autour de la moyenne du groupe de référence. '
                          'Vous restez généralement opérationnel et récupérez après un revers. En cas de pression '
                          'prolongée ou de changements multiples, davantage de structure ou de soutien peut être '
                          'utile.',
               'above_average': 'Pour cette dimension, votre score se situe au-dessus de la moyenne du groupe de '
                                'référence. Vous restez généralement calme et concentré sous pression et récupérez '
                                'rapidement après un revers. Vous continuez ainsi à décider et à ajuster votre '
                                'approche dans les situations complexes.',
               'high': 'Pour cette dimension, votre score se situe parmi les 20 % les plus élevés du groupe de '
                       'référence. Vous restez exceptionnellement stable sous pression, récupérez rapidement et '
                       'régulez fortement votre attention et votre énergie. Dans les situations difficiles, vous '
                       'apportez souvent calme et repères aux autres.'},
        'LO': {'low': 'Pour cette dimension, votre score se situe parmi les 20 % les plus faibles du groupe de '
                      'référence. Vous recherchez actuellement peu de feedback, d’occasions de pratiquer ou de '
                      'nouvelles connaissances. Vos expériences se transforment donc moins spontanément en '
                      'développement. C’est une occasion de croissance claire.',
               'below_average': 'Pour cette dimension, votre score se situe sous la moyenne du groupe de référence. '
                                'Vous apprenez surtout lorsque la tâche ou la situation l’exige. Définir vous-même des '
                                'objectifs d’apprentissage, demander du feedback et appliquer les acquis reste moins '
                                'régulier.',
               'average': 'Pour cette dimension, votre score se situe autour de la moyenne du groupe de référence. '
                          'Vous êtes ouvert à l’apprentissage et utilisez le feedback pertinent lorsqu’il est '
                          'disponible. La régularité avec laquelle vous vous exercez et poursuivez votre développement '
                          'varie encore selon le contexte.',
               'above_average': 'Pour cette dimension, votre score se situe au-dessus de la moyenne du groupe de '
                                'référence. Vous recherchez activement des connaissances, du feedback et des occasions '
                                'de progresser. Vous transposez généralement les nouveaux acquis dans votre travail et '
                                'renforcez ainsi votre capacité à faire face au changement.',
               'high': 'Pour cette dimension, votre score se situe parmi les 20 % les plus élevés du groupe de '
                       'référence. L’apprentissage et le développement sont un moteur puissant dans votre travail. '
                       'Vous recherchez systématiquement du feedback et de nouvelles perspectives, appliquez les '
                       'acquis et stimulez souvent l’apprentissage des autres.'},
        'VV': {'low': 'Pour cette dimension, votre score se situe parmi les 20 % les plus faibles du groupe de '
                      'référence. Votre attention porte surtout sur le présent, si bien que vous repérez moins vite '
                      'les signaux précoces et les conséquences futures. Votre préparation reste souvent réactive et '
                      'constitue une occasion de développement claire.',
               'below_average': 'Pour cette dimension, votre score se situe sous la moyenne du groupe de référence. '
                                'Vous regardez parfois vers l’avenir, mais ne traduisez pas encore systématiquement '
                                'les signaux en scénarios ou en préparation. Les changements peuvent donc vous '
                                'surprendre plus souvent que nécessaire.',
               'average': 'Pour cette dimension, votre score se situe autour de la moyenne du groupe de référence. '
                          'Vous tenez compte de ce qui arrive et vous préparez dès que les signaux deviennent clairs. '
                          'Lorsque l’incertitude augmente ou que l’horizon s’allonge, votre anticipation devient moins '
                          'systématique.',
               'above_average': 'Pour cette dimension, votre score se situe au-dessus de la moyenne du groupe de '
                                'référence. Vous repérez tôt les signaux pertinents et les traduisez en préparations '
                                'réalisables. Vous gardez ainsi plusieurs options ouvertes et devez moins souvent agir '
                                'de manière réactive.',
               'high': 'Pour cette dimension, votre score se situe parmi les 20 % les plus élevés du groupe de '
                       'référence. L’anticipation est une force claire : vous reliez les signaux, explorez des '
                       'scénarios et vous préparez à temps. Vous aidez ainsi souvent les autres à concrétiser les '
                       'changements futurs.'},
        'CI': {'low': 'Pour cette dimension, votre score se situe parmi les 20 % les plus faibles du groupe de '
                      'référence. Vous revenez souvent à des solutions connues et expérimentez peu d’alternatives. Des '
                      'améliorations possibles restent donc plus vite inexploitées. C’est une occasion de '
                      'développement claire.',
               'below_average': 'Pour cette dimension, votre score se situe sous la moyenne du groupe de référence. '
                                'Vous voyez parfois de nouvelles possibilités, mais les transformez encore peu en '
                                'tests ou en améliorations concrètes. Dans l’incertitude, l’approche habituelle garde '
                                'généralement la priorité.',
               'average': 'Pour cette dimension, votre score se situe autour de la moyenne du groupe de référence. '
                          'Vous proposez des idées utiles lorsque la situation le demande. Le fait de les tester et de '
                          'les réaliser dépend encore fortement du temps, de l’espace et du soutien disponibles.',
               'above_average': 'Pour cette dimension, votre score se situe au-dessus de la moyenne du groupe de '
                                'référence. Vous développez régulièrement de nouvelles idées et testez des '
                                'alternatives de manière ciblée. Vous reliez ainsi le plus souvent la créativité à des '
                                'améliorations pratiques dans votre travail.',
               'high': 'Pour cette dimension, votre score se situe parmi les 20 % les plus élevés du groupe de '
                       'référence. Innover de manière créative est une force claire : vous voyez des possibilités '
                       'inattendues, expérimentez de manière ciblée et transformez les idées en améliorations '
                       'visibles. Vous stimulez ainsi souvent aussi les autres.'}},
 'en': {'VA': {'low': 'For this dimension, your score is in the bottom 20% of the benchmark group. Change often '
                      'triggers hesitation or resistance, so exploring new ways of working and helping shape direction '
                      'takes more energy. This is a clear development opportunity.',
               'below_average': 'For this dimension, your score is below the benchmark group average. You tend to be '
                                'more cautious or critical about change. You may recognise the need, but do not yet '
                                'always translate it into active support or ownership.',
               'average': 'For this dimension, your score is around the benchmark group average. Your attitude towards '
                          'change is generally workable: you move with clear added value, while uncertainty or limited '
                          'involvement can make you more critical or hesitant.',
               'above_average': 'For this dimension, your score is above the benchmark group average. You generally '
                                'approach change constructively, contribute ideas and take initiative. This openness '
                                'also helps create movement under uncertainty.',
               'high': 'For this dimension, your score is in the top 20% of the benchmark group. You deal with change '
                       'actively and constructively, give it meaning and readily take ownership. Your attitude often '
                       'brings others along as well.'},
        'VZ': {'low': 'For this dimension, your score is in the bottom 20% of the benchmark group. Pressure, setbacks '
                      'or unexpected events disrupt your functioning relatively strongly, and recovery often takes '
                      'time or support. This is an important development opportunity.',
               'below_average': 'For this dimension, your score is below the benchmark group average. You cope with '
                                'difficult situations, but your balance and recovery are not always stable. Under '
                                'sustained pressure, it becomes harder to regulate attention, emotions and energy.',
               'average': 'For this dimension, your score is around the benchmark group average. You generally '
                          'continue to function adequately and recover after setbacks. Prolonged pressure or several '
                          'simultaneous changes may require extra structure or support.',
               'above_average': 'For this dimension, your score is above the benchmark group average. You usually '
                                'remain calm and focused under pressure and recover quickly after setbacks. This helps '
                                'you keep making decisions and adjusting your approach in complex situations.',
               'high': 'For this dimension, your score is in the top 20% of the benchmark group. You remain '
                       'exceptionally stable under pressure, recover quickly and regulate your attention and energy '
                       'strongly. In difficult circumstances, you often provide calm and direction to others.'},
        'LO': {'low': 'For this dimension, your score is in the bottom 20% of the benchmark group. You currently make '
                      'limited active use of feedback, practice opportunities or new knowledge. Experiences are '
                      'therefore less readily turned into development. This is a clear growth opportunity.',
               'below_average': 'For this dimension, your score is below the benchmark group average. You mainly learn '
                                'when the task or situation requires it. Setting your own learning goals, seeking '
                                'feedback and applying insights still happens less consistently.',
               'average': 'For this dimension, your score is around the benchmark group average. You are open to '
                          'learning and use relevant feedback when it is available. How deliberately you practise and '
                          'sustain development still varies by context.',
               'above_average': 'For this dimension, your score is above the benchmark group average. You actively '
                                'seek knowledge, feedback and opportunities to grow. You usually apply new insights in '
                                'your work, strengthening your ability to deal with change.',
               'high': 'For this dimension, your score is in the top 20% of the benchmark group. Learning and '
                       'development are a strong driver in your work. You systematically seek feedback and new '
                       'perspectives, apply insights and often encourage others to learn as well.'},
        'VV': {'low': 'For this dimension, your score is in the bottom 20% of the benchmark group. Your attention is '
                      'mainly on what is happening today, so you notice early signals and future consequences less '
                      'quickly. Preparation is often reactive and is a clear development opportunity.',
               'below_average': 'For this dimension, your score is below the benchmark group average. You sometimes '
                                'look ahead, but do not yet consistently translate signals into scenarios or '
                                'preparation. Changes may therefore surprise you more often than necessary.',
               'average': 'For this dimension, your score is around the benchmark group average. You consider what is '
                          'coming and prepare once signals are clear. With greater uncertainty or a longer time '
                          'horizon, your forward thinking becomes less systematic.',
               'above_average': 'For this dimension, your score is above the benchmark group average. You notice '
                                'relevant signals early and translate them into practical preparation. This keeps '
                                'options open and reduces the need to act reactively.',
               'high': 'For this dimension, your score is in the top 20% of the benchmark group. Looking ahead is a '
                       'clear strength: you connect signals, explore scenarios and prepare in time. This often helps '
                       'others make future change concrete.'},
        'CI': {'low': 'For this dimension, your score is in the bottom 20% of the benchmark group. You often fall back '
                      'on familiar solutions and experiment little with alternatives. Potential improvements are '
                      'therefore more likely to remain unused. This is a clear development opportunity.',
               'below_average': 'For this dimension, your score is below the benchmark group average. You sometimes '
                                'see new possibilities, but do not yet turn them into concrete tests or improvements '
                                'very often. Under uncertainty, the familiar approach usually takes priority.',
               'average': 'For this dimension, your score is around the benchmark group average. You generate useful '
                          'ideas when the situation calls for them. Whether you test and realise them still depends '
                          'strongly on available time, space and support.',
               'above_average': 'For this dimension, your score is above the benchmark group average. You regularly '
                                'develop new ideas and test alternatives deliberately. This usually connects '
                                'creativity with practical improvement in your work.',
               'high': 'For this dimension, your score is in the top 20% of the benchmark group. Creative renewal is a '
                       'clear strength: you see unexpected possibilities, experiment deliberately and turn ideas into '
                       'visible improvements. This often encourages others as well.'}}}

PILLAR_TRANSLATIONS = {
    "fr": {
        "VA": {"title": "Ouverture au changement", "description": "Ce pilier décrit votre réaction émotionnelle, cognitive et comportementale au changement dans votre environnement de travail.", "score_meaning": {
            "low": "Votre score est plutôt faible. Le changement peut vous sembler difficile ou menaçant, et vous avez tendance à vous appuyer sur des méthodes familières.",
            "mid": "Votre score se situe dans la moyenne. Vous adoptez généralement une attitude neutre à ouverte et vous coopérez lorsque le changement est demandé.",
            "good": "Votre score est plutôt élevé. Vous abordez généralement le changement de façon ouverte et constructive et vous contribuez activement à sa mise en œuvre.",
            "high": "Votre score est très élevé. Vous ne vous contentez pas d’accepter le changement : vous l’initiez et contribuez activement à le façonner.",
        }},
        "VZ": {"title": "Résilience & Autorégulation", "description": "Ce pilier décrit votre capacité à fonctionner sous pression, à vous adapter et à rebondir après un revers.", "score_meaning": {
            "low": "Votre score est plutôt faible. La pression ou les situations inattendues peuvent peser sur votre fonctionnement et l’adaptation vous demande du temps.",
            "mid": "Votre score se situe dans la moyenne. Vous vous adaptez dans la plupart des situations, parfois avec un besoin de temps, de structure ou de soutien.",
            "good": "Votre score est plutôt élevé. Vous restez généralement stable sous pression et vous vous adaptez aisément aux nouvelles circonstances.",
            "high": "Votre score est très élevé. Vous gérez très bien la pression et le changement et vous passez rapidement d’une situation à l’autre.",
        }},
        "LO": {"title": "Apprentissage et développement continu", "description": "Ce pilier décrit dans quelle mesure vous investissez activement dans l’apprentissage et votre développement.", "score_meaning": {
            "low": "Votre score est plutôt faible. Vous apprenez surtout lorsque votre travail l’exige et votre développement reste principalement réactif.",
            "mid": "Votre score se situe dans la moyenne. Vous saisissez régulièrement les occasions d’apprendre, sans toujours piloter votre développement de façon systématique.",
            "good": "Votre score est plutôt élevé. Vous investissez activement dans votre apprentissage et recherchez régulièrement des moyens d’améliorer vos compétences.",
            "high": "Votre score est très élevé. Votre motivation intrinsèque à apprendre est forte et vous recherchez continuellement de nouvelles occasions de vous développer.",
        }},
        "VV": {"title": "Anticipation & Préparation", "description": "Ce pilier décrit votre orientation vers l’avenir et la manière dont vous anticipez les changements possibles.", "score_meaning": {
            "low": "Votre score est plutôt faible. Vous vous concentrez surtout sur le présent et réagissez aux problèmes lorsqu’ils surviennent.",
            "mid": "Votre score se situe dans la moyenne. Vous pensez parfois à l’avenir, mais pas encore toujours de manière structurelle.",
            "good": "Votre score est plutôt élevé. Vous anticipez régulièrement et vous vous préparez consciemment aux évolutions et risques futurs.",
            "high": "Votre score est très élevé. Vous travaillez de façon très proactive avec des scénarios et anticipez systématiquement les changements futurs.",
        }},
        "CI": {"title": "Créativité & Innovation", "description": "Ce pilier décrit dans quelle mesure vous développez et mettez en pratique de nouvelles idées, méthodes et solutions.", "score_meaning": {
            "low": "Votre score est plutôt faible. Vous vous appuyez surtout sur les méthodes existantes et prenez peu d’initiatives pour les renouveler.",
            "mid": "Votre score se situe dans la moyenne. Vous contribuez parfois à des améliorations, mais l’innovation n’est pas encore systématique.",
            "good": "Votre score est plutôt élevé. Vous prenez régulièrement l’initiative d’améliorer les processus et contribuez activement au renouvellement.",
            "high": "Votre score est très élevé. Vous développez activement des idées innovantes et les transformez en améliorations concrètes.",
        }},
    },
    "en": {
        "VA": {"title": "Change Attitude", "description": "This pillar describes how you respond emotionally, cognitively and behaviourally to change in your work environment.", "score_meaning": {
            "low": "Your score is rather low. Change may feel difficult or threatening, and you tend to rely on familiar ways of working.",
            "mid": "Your score is around the middle. You generally take a neutral to open stance and cooperate when change is requested.",
            "good": "Your score is rather high. You generally approach change openly and constructively and actively support its implementation.",
            "high": "Your score is very high. You not only accept change, but often initiate it and actively help shape it.",
        }},
        "VZ": {"title": "Resilience & Self-regulation", "description": "This pillar describes how well you function under pressure, adapt to changing circumstances and recover from setbacks.", "score_meaning": {
            "low": "Your score is rather low. Pressure or unexpected situations can affect how you function, and adapting may take time.",
            "mid": "Your score is around the middle. You adapt in most situations, although you may need time, structure or support.",
            "good": "Your score is rather high. You generally remain stable under pressure and adapt smoothly to new circumstances.",
            "high": "Your score is very high. You deal very effectively with pressure and change and switch quickly between situations.",
        }},
        "LO": {"title": "Learning Motivation & Development", "description": "This pillar describes the extent to which you actively invest in learning and personal development.", "score_meaning": {
            "low": "Your score is rather low. You mainly learn when your work requires it, so development tends to be reactive.",
            "mid": "Your score is around the middle. You regularly use learning opportunities, but do not always steer your development systematically.",
            "good": "Your score is rather high. You actively invest in learning and regularly seek ways to strengthen your skills.",
            "high": "Your score is very high. You are strongly motivated to learn and continually seek new opportunities to develop.",
        }},
        "VV": {"title": "Anticipating & Preparing", "description": "This pillar describes how future-oriented you are and how systematically you anticipate possible changes.", "score_meaning": {
            "low": "Your score is rather low. You mainly focus on the present and respond to problems when they arise.",
            "mid": "Your score is around the middle. You sometimes think ahead, although not yet consistently or systematically.",
            "good": "Your score is rather high. You regularly think ahead and consciously prepare for future developments and risks.",
            "high": "Your score is very high. You work proactively with scenarios and systematically anticipate future change.",
        }},
        "CI": {"title": "Creativity & Innovation", "description": "This pillar describes the extent to which you develop and implement new ideas, ways of working and solutions.", "score_meaning": {
            "low": "Your score is rather low. You mainly rely on existing methods and take little initiative to renew them.",
            "mid": "Your score is around the middle. You sometimes contribute ideas for improvement, but innovation is not yet systematic.",
            "good": "Your score is rather high. You regularly initiate improvements and actively contribute to renewal in your work environment.",
            "high": "Your score is very high. You actively develop innovative ideas and turn them into concrete improvements.",
        }},
    },
}

SUMMARY_TRANSLATIONS = {
    "fr": {
        0: "Votre adaptabilité se trouve encore au début de son développement.", 1: "Vous coopérez correctement au changement lorsque cela est nécessaire.",
        2: "Vous vous adaptez bien lorsque le changement se présente.", 3: "Vous réagissez avec souplesse et cherchez des solutions dans les situations changeantes.",
        4: "Vous anticipez et vous préparez consciemment aux changements futurs.", 5: "Vous créez activement le changement et aidez les autres à progresser.",
    },
    "en": {
        0: "Your adaptivity is still at an early stage of development.", 1: "You cooperate reliably with change when needed.",
        2: "You adapt well when change occurs.", 3: "You respond flexibly and focus on solutions in changing situations.",
        4: "You think ahead and consciously prepare for future change.", 5: "You actively create change and help others grow with it.",
    },
}

FEEDBACK_TRANSLATIONS = {
    "fr": {
        0: """Vous privilégiez clairement les façons de travailler familières. C’est compréhensible : le changement demande de l’énergie et peut créer de l’incertitude. Votre regard critique reste précieux, car il vous aide à repérer ce qui n’est pas encore suffisamment réfléchi.\n\n### Prochaines étapes\n- exprimer plus rapidement vos réserves\n- tester consciemment un petit changement\n- explorer ce que le changement peut vous apporter\n- moins attendre et davantage explorer\n\n### Premier petit pas\nChoisissez cette semaine un petit changement et observez ce qui se passe lorsque vous l’accompagnez plutôt que de le freiner.""",
        1: """Vous acceptez généralement le changement de manière correcte et professionnelle. Vous coopérez lorsque cela est nécessaire et apportez de la stabilité. Votre prochaine étape consiste à ne plus seulement exécuter le changement, mais à contribuer davantage à le façonner.\n\n### Prochaines étapes\n- réfléchir consciemment à votre propre approche\n- tester plus rapidement de nouvelles méthodes\n- questionner les raisons du changement\n- proposer vous-même de petites améliorations\n\n### Premier petit pas\nLors d’un changement, demandez activement comment adapter au mieux votre façon de travailler.""",
        2: """Vous vous adaptez bien lorsque le changement survient. Vous savez passer à une nouvelle situation et continuer à fonctionner sous pression. La prochaine étape est de repérer les changements plus tôt et de vous y préparer de manière plus proactive.\n\n### Prochaines étapes\n- imaginer plus rapidement plusieurs options\n- détecter plus tôt les signaux de changement\n- rechercher des connaissances avant qu’elles ne deviennent nécessaires\n- penser plus consciemment à l’avenir\n\n### Premier petit pas\nDans une situation complexe, prenez du recul et examinez consciemment plusieurs options.""",
        3: """Vous passez avec souplesse d’une situation à l’autre, restez généralement calme sous pression et cherchez des solutions. Votre opportunité de croissance consiste à renforcer encore votre capacité d’anticipation et à reconnaître plus tôt les tendances.\n\n### Prochaines étapes\n- réfléchir plus souvent en scénarios\n- analyser les causes structurelles\n- développer des compétences avant d’en avoir besoin\n- voir les opportunités dans le changement\n\n### Premier petit pas\nChoisissez une évolution dans votre domaine et examinez son impact possible sur votre travail dans six mois.""",
        4: """Vous anticipez et vous préparez consciemment aux changements futurs. Vous développez des compétences à l’avance et recherchez des solutions durables. Votre prochaine étape est d’expérimenter davantage, même sans nécessité immédiate.\n\n### Prochaines étapes\n- expérimenter sans raison immédiate\n- apprendre en dehors de votre contexte actuel\n- explorer sans objectif fixé à l’avance\n- inspirer et accompagner les autres\n\n### Premier petit pas\nSuivez une formation dont l’utilité immédiate n’est pas encore certaine et évaluez ce qu’elle vous apprend.""",
        5: """Vous ne vous contentez pas de suivre le changement : vous contribuez activement à le créer. Vous apprenez en continu et utilisez le changement comme moteur de croissance. Votre plus grand impact futur réside dans le renforcement des autres.\n\n### Pour aller plus loin\n- accompagner les autres dans le changement\n- partager explicitement vos apprentissages\n- créer de l’espace pour expérimenter\n- contribuer au changement organisationnel\n\n### Premier petit pas\nChoisissez une personne ou une équipe et aidez-la à mieux comprendre ou accélérer un changement concret.""",
    },
    "en": {
        0: """You clearly prefer familiar ways of working. This is understandable: change takes energy and can create uncertainty. Your critical perspective is valuable because it helps you notice when something has not yet been thought through sufficiently.\n\n### Next steps\n- voice concerns sooner\n- consciously test one small change\n- explore what a change could offer\n- spend less time waiting and more time exploring\n\n### First small step\nChoose one small change this week and observe what happens when you go along with it rather than hold it back.""",
        1: """You generally accept change correctly and professionally. You cooperate when needed and bring stability. Your next step is to move beyond implementing change and play a more active part in shaping it.\n\n### Next steps\n- reflect consciously on your own approach\n- try new ways of working sooner\n- ask why a change is taking place\n- propose small improvements yourself\n\n### First small step\nFor one change, actively ask how you could best adapt your way of working.""",
        2: """You adapt well when change occurs. You switch when needed and continue to function in new situations and under pressure. Your next step is to spot change earlier and prepare for it more proactively.\n\n### Next steps\n- generate alternatives more quickly\n- notice signals of change earlier\n- seek knowledge before it is required\n- think ahead more consciously\n\n### First small step\nIn one complex situation, deliberately step back and consider several options.""",
        3: """You move flexibly between situations, generally remain calm under pressure and focus on solutions. Your growth opportunity is to strengthen your forward thinking and recognise patterns earlier.\n\n### Next steps\n- think in scenarios more often\n- analyse structural causes\n- develop skills before they are needed\n- look for opportunities in change\n\n### First small step\nChoose one development in your field and consider how it could affect your work six months from now.""",
        4: """You think ahead and consciously prepare for future change. You develop skills in advance and seek sustainable solutions. Your next step is to experiment more, even when there is no immediate need.\n\n### Next steps\n- experiment without an immediate trigger\n- learn outside your current context\n- explore without a fixed goal\n- inspire and involve others\n\n### First small step\nTake one course whose immediate usefulness is not yet certain and evaluate what you learn from it.""",
        5: """You do not merely move with change; you actively help create it. You learn continuously and use change as a driver for growth. Your greatest further impact lies in strengthening others.\n\n### Areas for further development\n- coach others through change and growth\n- share learning processes explicitly\n- create room for experimentation\n- help steer change at organisational level\n\n### First small step\nChoose one colleague or team and help them understand, address or accelerate one concrete change.""",
    },
}
