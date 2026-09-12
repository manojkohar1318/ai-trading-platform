import Sidebar from './Sidebar';
import MobileNav from './MobileNav';

export default function Terminal({
  children,
  title = 'Dashboard',
}: {
  children: React.ReactNode;
  title?: string;
}) {
  return (
    <div className="min-h-screen bg-[#080b10] text-slate-100">
      <div className="flex min-h-screen">
        <Sidebar />

        <main className="min-w-0 flex-1 pb-20 lg:pb-0">
          <header className="sticky top-0 z-30 border-b border-white/10 bg-[#080b10]/95 backdrop-blur-xl">
            <div className="flex min-h-16 items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
              <div className="min-w-0">
                <h1 className="truncate text-base font-semibold text-white sm:text-lg">
                  {title}
                </h1>
                <p className="hidden text-xs text-slate-500 sm:block">
                  Indian market analysis
                </p>
              </div>

              <div className="flex shrink-0 items-center gap-2">
                <span className="rounded-full border border-amber-500/20 bg-amber-500/10 px-2.5 py-1 text-[10px] font-semibold tracking-wide text-amber-300">
                  DEMO
                </span>
                <span className="hidden text-xs text-slate-500 sm:inline">
                  Market closed
                </span>
                <div className="grid h-8 w-8 place-items-center rounded-full bg-white/5 text-xs font-bold text-slate-300">
                  AI
                </div>
              </div>
            </div>
          </header>

          <section className="mx-auto w-full max-w-7xl px-4 py-4 sm:px-6 sm:py-6 lg:px-8 lg:py-8">
            {children}
          </section>
        </main>
      </div>

      <MobileNav />
    </div>
  );
}
