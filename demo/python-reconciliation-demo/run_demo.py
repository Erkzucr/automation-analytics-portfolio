from pathlib import Path
import csv,json
B=Path(__file__).resolve().parent
def read(p):
 with open(p,newline='',encoding='utf-8') as f:return {r['record_id']:r for r in csv.DictReader(f)}
def reconcile(a,b,t):
 ok=[];ex=[]
 for k in sorted(set(a)|set(b)):
  if k not in a: ex.append([k,'ONLY_B','','UNMATCHED_A'])
  elif k not in b: ex.append([k,'ONLY_A','','UNMATCHED_B'])
  else:
   d=round(float(a[k]['value_amount'])-float(b[k]['value_amount']),2)
   (ok if abs(d)<=t else ex).append([k,'BOTH',d,'WITHIN_TOLERANCE' if abs(d)<=t else 'VARIANCE'])
 return ok,ex
def write(p,rows):
 p.parent.mkdir(exist_ok=True)
 with open(p,'w',newline='',encoding='utf-8') as f:
  x=csv.writer(f);x.writerow(['record_id','match_status','difference','review_reason']);x.writerows(rows)
def main():
 a=read(B/'input/source_a.csv');b=read(B/'input/source_b.csv');t=json.loads((B/'config.json').read_text())['tolerance'];ok,ex=reconcile(a,b,t);write(B/'output/accepted_records.csv',ok);write(B/'output/exception_records.csv',ex);print(f'{len(ok)} accepted, {len(ex)} exceptions')
if __name__=='__main__':main()
