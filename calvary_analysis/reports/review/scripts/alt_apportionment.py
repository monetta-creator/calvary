"""Review check: how sensitive are the M2 stress-test losses to the way FY25 government revenue is split across streams?
Reads only calvary_funding_data/clean/. Run from anywhere; ROOT is the project root."""
# Review script. Paths resolve from this file: calvary_analysis/reports/review/scripts/ -> project root three levels up.
import os as _os, pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
PROJECT_ROOT = str(_pl.Path(_os.environ.get("CALVARY_ROOT", _HERE.parents[3])))
REVIEW_OUT = _os.environ.get("REVIEW_OUT", str(_HERE.parent / "evidence"))
from pathlib import Path
import pandas as pd, yaml
ROOT = Path(__file__).resolve()
while ROOT.name != 'calvary' and ROOT.parent != ROOT: ROOT = ROOT.parent
ROOT = Path(PROJECT_ROOT)
C = ROOT / 'calvary_funding_data' / 'clean'
CAL = '521307706'
g = pd.read_csv(C / 'fact_gov_awards.csv', dtype={'recipient_ein': str}, low_memory=False)
g = g[g.recipient_ein == CAL]
fin = pd.read_csv(C / 'fact_org_financials.csv', dtype={'ein': str}, low_memory=False)
f = fin[(fin.ein == CAL) & (fin.preferred == 1)].set_index('fiscal_year')
cfg = yaml.safe_load(open(ROOT / 'calvary_analysis' / 'config' / 'scenarios.yaml'))

def ovsjg(fy):
    s = g[(g.source_type == 'dc_ovsjg') & (g.fiscal_year == fy) & (g.amount != 3680675)]
    return s.amount.sum()
def coc(comp_year):
    return g[(g.source_type == 'hud_coc') & (g.fiscal_year == comp_year)].amount.sum()
def coc_nf2(comp_year):
    s = g[(g.source_type == 'hud_coc') & (g.fiscal_year == comp_year)]
    return s[s.program_name.str.contains('New Foundations 2')].amount.sum()
dhs = g[(g.source_type == 'dc_oversight') & (g.fiscal_year == 2024)].amount.sum()
sisters = g[(g.source_type == 'dc_oversight') & (g.program_name.str.contains('Sisters Rise'))].amount.sum()
sefa_coc = {fy: g[(g.source_type == 'audit_sefa') & (g.fiscal_year == fy) & (g.program_name.str.contains('Supportive Housing'))].amount.sum() for fy in (2022, 2023)}
other = g[(g.source_type == 'audit_sefa') & (g.fiscal_year == 2023) & (~g.program_name.str.contains('Supportive Housing|Fiscal Recovery'))].amount.sum()

print('--- CoC: audited SEFA expenditure vs award ceilings (lag 1 = competition year t-1; lag 0 = same year)')
for fy in (2022, 2023):
    print(f'FY{fy}: SEFA CoC {sefa_coc[fy]:,.0f} | lag-1 ceiling {coc(fy-1):,.0f} ({sefa_coc[fy]/coc(fy-1):.0%}) | lag-0 ceiling {coc(fy):,.0f} ({sefa_coc[fy]/coc(fy):.0%})')
draw = sum(sefa_coc.values()) / (coc(2021) + coc(2022))
print(f'two-year CoC draw rate vs lag-1 ceilings: {draw:.0%}')

rev25 = f.loc[2025, 'total_revenue']; exp25 = f.loc[2025, 'total_expenses']; cash25 = f.loc[2025, 'cash_savings_eoy']; gov25 = f.loc[2025, 'government_grants']
ceil = {'ovsjg': ovsjg(2025), 'coc': coc(2024), 'dhs': dhs, 'other': other}
print('\nFY25 ceilings', {k: f'{v:,.0f}' for k, v in ceil.items()}, 'sum', f'{sum(ceil.values()):,.0f}', '| recognized', f'{gov25:,.0f}')
print(f"TCP share of 2024 base ({ovsjg(2024)+coc(2024)+dhs:,.0f}): {(coc(2024)+dhs)/(ovsjg(2024)+coc(2024)+dhs):.1%};  of FY25 ceiling base: {(coc(2024)+dhs)/sum(ceil.values()):.1%}")

def scenarios(split, label):
    nf2_share = coc_nf2(2024) / coc(2024)
    S = {'S1 OVSJG -10%': 0.10*split['ovsjg'], 'S2 OVSJG -25%': 0.25*split['ovsjg'], 'S3 CoC -15%': 0.15*split['coc'],
         'S4 NF2 lost': nf2_share*split['coc'], 'S5 DHS lost': split['dhs'], 'S6 combined': 0.25*split['ovsjg']+0.15*split['coc']+split['dhs']}
    rows = []
    for k, loss in S.items():
        net = loss * (1 - cfg['cost_avoidance_share'])
        deficit_net = -(exp25 - rev25) - net
        months_net = (cash25 + deficit_net) / ((exp25 - loss*cfg['cost_avoidance_share']) / 12)
        rows.append((label, k, round(loss), f'{loss/rev25:.0%}', round(months_net, 1)))
    return rows

splits = {}
tot = sum(ceil.values()); splits['A team: ceiling share'] = {k: gov25*v/tot for k, v in ceil.items()}
# B: OVSJG and other fully recognized; CoC at the audited two-year draw rate; DHS = residual
b = {'ovsjg': ceil['ovsjg'], 'other': ceil['other'], 'coc': ceil['coc']*draw}; b['dhs'] = gov25 - sum(b.values()); splits['B: OVSJG full, CoC at SEFA draw rate, DHS residual'] = b
# C: Sisters Rise ended in FY25 (ceiling base without it), ceiling share
ceil_c = dict(ceil); ceil_c['dhs'] = dhs - sisters; tot_c = sum(ceil_c.values()); splits['C: Sisters Rise gone, ceiling share'] = {k: gov25*v/tot_c for k, v in ceil_c.items()}
# D: OVSJG full, CoC full, DHS residual (floor case for DHS)
d = {'ovsjg': ceil['ovsjg'], 'other': ceil['other'], 'coc': ceil['coc']}; d['dhs'] = gov25 - sum(d.values()); splits['D: OVSJG and CoC fully drawn, DHS residual'] = d
out = []
for label, sp in splits.items():
    print(f"\n{label}: split", {k: f'{v:,.0f}' for k, v in sp.items()})
    out += scenarios(sp, label)
df = pd.DataFrame(out, columns=['apportionment', 'scenario', 'revenue_loss', 'pct_revenue', 'months_cash_after_12m_net'])
piv = df.pivot(index='scenario', columns='apportionment', values='revenue_loss')
print('\n', piv.to_string())
base = piv['A team: ceiling share']
print('\nchange vs team (%):'); print(((piv.sub(base, axis=0)).div(base, axis=0)*100).round(0).to_string())
df.to_csv(Path(__file__).with_name('alt_apportionment.csv'), index=False)
