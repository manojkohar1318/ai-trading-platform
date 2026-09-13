import Terminal from "@/components/Terminal";
import Link from "next/link";

const stocks = ["RELIANCE", "ICICIBANK", "SBIN", "INFY", "TCS", "HDFCBANK", "ITC"];

export default function Stocks() {
  return (
    <Terminal title="Stocks">
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-semibold">Stock Analyzer</h1>
          <p className="muted mt-2">
            Select an instrument to view quantitative analysis, technical indicators,
            market structure and trade setup.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stocks.map((symbol) => (
            <Link
              key={symbol}
              href={`/stocks/${symbol}`}
              className="card p-5 hover:border-[#5365a5] transition-colors"
            >
              <div className="font-semibold">{symbol}</div>
              <div className="text-sm muted mt-2">Open analysis →</div>
            </Link>
          ))}
        </div>
      </div>
    </Terminal>
  );
}
