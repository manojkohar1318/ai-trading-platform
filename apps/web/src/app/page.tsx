import Terminal from "@/components/Terminal";
import Metric from "@/components/Metric";
import StockTable from "@/components/StockTable";
import PriceChart, { VolumeChart } from "@/components/PriceChart";
import { chart, stocks } from "@/lib/demo";
import MarketSession from "@/components/MarketSession";
export default function Home() {
  return (
    <Terminal>
      <div className="mb-4"><MarketSession /></div>
      <div className="flex items-end justify-between mb-6">
        <div>
          <h1 className="text-2xl font-semibold">Market Command Center</h1>
          <p className="muted text-sm mt-1">
            A quantitative snapshot for Indian equities.
          </p>
        </div>
        <span className="text-xs px-2 py-1 border border-amber-500/30 text-amber-300 rounded">
          All figures are DEMO
        </span>
      </div>
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3 mb-4">
        <Metric label="NIFTY 50" value="24,912.40" change="+0.62%" />
        <Metric label="BANK NIFTY" value="54,182.15" change="+0.41%" />
        <Metric label="Advances" value="1,267" change="Breadth 1.35×" />
        <Metric
          label="Market Status"
          value="CLOSED"
          change="Next session 09:15 IST"
        />
      </div>
      <div className="grid xl:grid-cols-[1.5fr_1fr] gap-4">
        <div className="card p-4">
          <div className="flex justify-between">
            <div>
              <div className="text-sm font-medium">
                NIFTY intraday structure
              </div>
              <div className="text-xs muted mt-1">
                Synthetic price path · DEMO
              </div>
            </div>
            <div className="text-sm up">+0.62%</div>
          </div>
          <PriceChart data={chart} />
          <VolumeChart data={chart} />
        </div>
        <div className="card p-4">
          <div className="flex justify-between mb-3">
            <div className="text-sm font-medium">AI Market Brief</div>
            <span className="text-[10px] muted">PLACEHOLDER</span>
          </div>
          <p className="text-sm leading-6 text-[#aeb9ca]">
            Market breadth is constructive in this demo snapshot. Quantitative
            signals are mixed-to-positive; wait for validated live data before
            acting.
          </p>
          <div className="mt-4 grid grid-cols-2 gap-2">
            <div className="bg-[#0c121c] rounded-lg p-3">
              <div className="text-xs muted">Bias</div>
              <div className="mt-1 up">Constructive</div>
            </div>
            <div className="bg-[#0c121c] rounded-lg p-3">
              <div className="text-xs muted">Risk</div>
              <div className="mt-1">Moderate</div>
            </div>
          </div>
        </div>
      </div>
      <div className="grid xl:grid-cols-2 gap-4 mt-4">
        <div>
          <div className="flex justify-between mb-3">
            <h2 className="font-medium">Strongest Stocks</h2>
            <span className="text-xs muted">Quant score</span>
          </div>
          <StockTable rows={stocks.slice(0, 5)} />
        </div>
        <div>
          <div className="flex justify-between mb-3">
            <h2 className="font-medium">Top Movers</h2>
            <span className="text-xs muted">Demo universe</span>
          </div>
          <StockTable rows={stocks.slice(3)} />
        </div>
      </div>
    </Terminal>
  );
}
