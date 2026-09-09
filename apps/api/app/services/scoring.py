from dataclasses import dataclass
@dataclass
class ScoreWeights:
    trend:float=.20; momentum:float=.20; volume:float=.15; structure:float=.15; volatility:float=.10; risk_reward:float=.20
    def validate(self):
        vals=[self.trend,self.momentum,self.volume,self.structure,self.volatility,self.risk_reward]
        if any(v<0 for v in vals) or abs(sum(vals)-1)>1e-9: raise ValueError("weights must be non-negative and sum to 1")

def score_stock(components:dict,weights:ScoreWeights=ScoreWeights()):
    weights.validate(); vals={k:float(components.get(k,0)) for k in vars(weights)}
    total=sum(vals[k]*getattr(weights,k) for k in vals)
    reasons=[]; warnings=[]
    for k,v in vals.items():
        if v>=75: reasons.append(f"Strong {k.replace('_',' ')}")
        if v<40: warnings.append(f"Weak {k.replace('_',' ')}")
    return {"total_score":round(total,1),"component_scores":vals,"reasons":reasons,"warnings":warnings}
