from dataclasses import dataclass
@dataclass
class BacktestConfig:
    transaction_cost_bps:float=10.0; slippage_bps:float=2.0; position_size_pct:float=1.0

def run_backtest(candles,config=BacktestConfig()):
    trades=[]; equity=1.0; peak=1.0; max_dd=0.0
    for i in range(1,len(candles)):
        prev=candles[i-1].close; cur=candles[i].close
        if prev==0: continue
        ret=(cur/prev)-1-(config.transaction_cost_bps+config.slippage_bps)/10000
        pnl=ret*config.position_size_pct; equity*=1+pnl
        if pnl: trades.append(pnl)
        peak=max(peak,equity); max_dd=max(max_dd,(peak-equity)/peak)
    wins=[x for x in trades if x>0]; losses=[x for x in trades if x<0]
    return {"total_return":equity-1,"win_rate":len(wins)/len(trades) if trades else 0,"average_win":sum(wins)/len(wins) if wins else 0,"average_loss":sum(losses)/len(losses) if losses else 0,"profit_factor":sum(wins)/abs(sum(losses)) if losses else None,"maximum_drawdown":max_dd,"number_of_trades":len(trades)}
