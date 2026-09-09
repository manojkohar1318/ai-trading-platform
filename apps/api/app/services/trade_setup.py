def build_trade_setup(price,support,resistance,atr_value,score,trend):
    if not atr_value or score<65 or trend not in {"bullish","bearish"}: return None
    direction="bullish" if trend=="bullish" else "bearish"
    risk=max(float(atr_value)*1.2, price*0.005)
    if direction=="bullish":
        entry=(max(support or price-risk,price-risk*.5),price+risk*.2); stop=price-risk; target=price+risk*2
    else:
        entry=(price-risk*.2,min(resistance or price+risk,price+risk*.5)); stop=price+risk; target=price-risk*2
    rr=abs(target-price)/abs(price-stop) if price!=stop else 0
    return {"direction":direction,"entry_zone":[round(entry[0],2),round(entry[1],2)],"target":round(target,2),"stop_loss":round(stop,2),"risk_reward":round(rr,2),"estimated_probability":round(min(0.8,max(.5,score/100*.85)),2),"confidence_score":round(min(95,max(50,score)),1),"is_estimate":True}
