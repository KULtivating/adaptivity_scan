import pandas as pd

PERCENTILE_DATA = {
    "VA": [(4.56,2.5),(4.78,5),(4.89,10),(5,20),(5.11,22.5),(5.22,40),(5.44,42.5),(5.56,47.5),(5.67,62.5),(5.78,65),(5.89,72.5),(6,80),(6.11,87.5),(6.22,97.5),(6.67,100)],
    "VZ": [(2.4,.66),(2.6,3.29),(2.8,5.92),(3,8.55),(3.2,12.5),(3.4,16.45),(3.6,21.71),(3.8,37.5),(4,48.03),(4.2,57.89),(4.4,67.11),(4.6,72.37),(4.8,75),(5,75.66),(5.2,77.63),(5.4,80.92),(5.6,82.24),(5.8,88.16),(6,92.11),(6.2,94.74),(6.4,98.68),(6.6,99.34),(6.8,100)],
    "LO": [(2.25,.66),(2.5,1.97),(2.75,3.29),(3,3.95),(3.25,8.55),(3.5,11.84),(3.75,15.13),(4,19.74),(4.25,28.29),(4.5,38.16),(4.75,50.66),(5,62.5),(5.25,71.71),(5.5,78.95),(5.75,87.5),(6,95.39),(6.25,96.71),(6.5,98.03),(6.75,100)],
    "VV": [(4,2.5),(4.12,5),(4.25,15),(4.38,17.5),(4.5,20),(4.62,22.5),(4.75,25),(4.88,27.5),(5,37.5),(5.12,45),(5.25,47.5),(5.38,50),(5.5,67.5),(5.71,70),(5.75,75),(5.88,82.5),(6,87.5),(6.25,97.5),(6.5,100)],
    "CI": [(3.6,5),(3.8,7.5),(4,10),(4.2,15),(4.4,22.5),(4.8,32.5),(5,45),(5.2,57.5),(5.6,65),(5.8,77.5),(6,85),(6.2,92.5),(6.4,95),(6.6,97.5),(7,100)],
}

ITEM_BLOCKS = {'CR_CA1':2,'CR_CD1':2,'CR_CD3':1,'CR_CA2':2,'CR_CR1':1,'CR_CP1':2,'CR_CR3':1,'CR_CD2':1,'CR_CP3':2,'LO_M':2,'Res2':2,'Res3':2,'IAP_WS1':2,'IAP_R2':2,'IAP_I2':2,'IAP_T1':2,'IAP_C2':4,'IAP_T2':3,'LO_A':3,'PB_SS1':4,'PB_SS3':4,'PB_PP1':4,'PB_PP2':3,'IAP_Rx':4,'IAP_Ix':4,'IAP_WSx':4,'IBIncr6':4,'IBRad4':4,'EISB1':3,'EISB4':3,'VOICE':4}

def percentile(code, score):
    points = PERCENTILE_DATA.get(code, [])
    if not points: return None
    if score < points[0][0]: return 0.0
    if score >= points[-1][0]: return 100.0
    for (x0,p0),(x1,p1) in zip(points, points[1:]):
        if score <= x1:
            return p0 + (score-x0)/(x1-x0)*(p1-p0)
    return 100.0

def percentile_band(value):
    if value < 10: return "very_low"
    if value < 30: return "low"
    if value <= 70: return "middle"
    if value <= 90: return "high"
    return "very_high"

def spread_band(sd):
    if pd.isna(sd): return "unavailable"
    if sd <= .72: return "low"
    if sd <= 1.32: return "moderate"
    return "high"

def maturity_level(blocks, pillars):
    b1,b2,b3,b4 = (blocks.get(i) for i in range(1,5))
    if any(pd.isna(x) for x in (b1,b2,b3,b4)): return None
    if b1 < 3.5: return 0
    if b2 < 4.5: return 1
    if b2 <= 5.5: return 2
    if b3 < 4.5: return 2
    if b3 <= 5.5: return 3
    if b4 < 4.5: return 3
    if b4 < 6 or pillars.get("VV",0) < 5.75 or pillars.get("CI",0) < 5.75: return 4
    return 5

def respondent_maturity(data):
    work=data[data["code"].isin(ITEM_BLOCKS)].copy()
    if work.empty:return pd.Series(dtype="Int64")
    work["block"]=work["code"].map(ITEM_BLOCKS)
    block_scores=work.groupby(["respondent","block"])["score"].mean().unstack()
    pillar_scores=data.groupby(["respondent","pillar"])["score"].mean().unstack()
    levels={}
    for respondent,row in block_scores.iterrows():
        blocks={int(k):v for k,v in row.dropna().items()}
        pillars=pillar_scores.loc[respondent].dropna().to_dict() if respondent in pillar_scores.index else {}
        level=maturity_level(blocks,pillars)
        if level is not None:levels[respondent]=level
    return pd.Series(levels,dtype="Int64")
