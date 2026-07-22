# Adaptiviteit Maturiteitsscan

Streamlit-app die antwoorden opslaat in Google Sheets en het persoonlijke
resultaat onmiddellijk op het scherm toont.

## Lokaal starten

```bash
pip install -r requirements.txt
streamlit run app.py
```

De Google-serviceaccountconfiguratie blijft nodig via
`.streamlit/secrets.toml`. Gmail- of SMTP-secrets zijn niet meer nodig.

## Meertaligheid

De app bevat Nederlands, Frans en Engels. De taal kan bovenaan worden gekozen
en rechtstreeks via `?lang=nl`, `?lang=fr` of `?lang=en` worden ingesteld.
Alle vertalingen staan centraal in `translations.py`.

De scoring gebruikt stabiele vraagcodes (`QUESTION_META`) en is daardoor niet
gekoppeld aan de zichtbare vertaling. Bij de eerste nieuwe inzending voegt de
app automatisch de kolom `taal` toe aan Google Sheets. Elke opgeslagen
antwoordregel bevat daarin `nl`, `fr` of `en`.

## Interpretatie

De resultaatpagina gebruikt de externe percentielreeksen uit het persoonlijke
adaptiviteitsrapport. Waarden tussen twee normpunten worden lineair
geïnterpoleerd. De maturiteitsberekening gebruikt de bijgewerkte grenzen van
4,5 en 5,5 voor blok 2 en 3. Niveau 5 vereist blok 4 van minstens 6 én minstens
5,75 op zowel Vooruitzien & Voorbereiden als Creativiteit & Innovatie.
