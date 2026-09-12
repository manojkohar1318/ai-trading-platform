'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart3, Bot, Home, MoreHorizontal, Search, Settings, Star, TrendingUp, X } from 'lucide-react';
import { useState } from 'react';

const primary = [
  { label: 'Home', href: '/', Icon: Home },
  { label: 'Markets', href: '/markets', Icon: TrendingUp },
  { label: 'Scanner', href: '/scanner', Icon: Search },
  { label: 'AI', href: '/assistant', Icon: Bot },
];

const more = [
  { label: 'Stocks', href: '/stocks', Icon: BarChart3 },
  { label: 'Backtesting', href: '/backtesting', Icon: TrendingUp },
  { label: 'Watchlist', href: '/watchlist', Icon: Star },
  { label: 'Settings', href: '/settings', Icon: Settings },
];

export default function MobileNav() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <>
      {open && (
        <div className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm" onClick={() => setOpen(false)}>
          <div
            className="absolute bottom-20 left-3 right-3 rounded-2xl border border-white/10 bg-[#10151d] p-3 shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="mb-2 flex items-center justify-between px-2">
              <span className="text-sm font-semibold text-white">More</span>
              <button
                type="button"
                aria-label="Close menu"
                onClick={() => setOpen(false)}
                className="rounded-lg p-2 text-slate-400 hover:bg-white/5 hover:text-white"
              >
                <X size={18} />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {more.map(({ label, href, Icon }) => {
                const active = pathname === href || pathname.startsWith(`${href}/`);
                return (
                  <Link
                    key={href}
                    href={href}
                    onClick={() => setOpen(false)}
                    className={`flex items-center gap-3 rounded-xl px-3 py-3 text-sm ${
                      active
                        ? 'bg-white/10 text-white'
                        : 'text-slate-400 hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <Icon size={18} />
                    {label}
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      )}

      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-white/10 bg-[#080b10]/95 px-2 pb-[max(8px,env(safe-area-inset-bottom))] pt-2 backdrop-blur-xl lg:hidden">
        <div className="mx-auto grid max-w-lg grid-cols-5">
          {primary.map(({ label, href, Icon }) => {
            const active = href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(`${href}/`);
            return (
              <Link
                key={href}
                href={href}
                className={`flex min-h-14 flex-col items-center justify-center gap-1 rounded-xl text-[11px] ${
                  active ? 'text-white' : 'text-slate-500'
                }`}
              >
                <Icon size={20} strokeWidth={active ? 2.4 : 1.8} />
                <span>{label}</span>
              </Link>
            );
          })}

          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            className={`flex min-h-14 flex-col items-center justify-center gap-1 rounded-xl text-[11px] ${
              open ? 'text-white' : 'text-slate-500'
            }`}
          >
            <MoreHorizontal size={20} strokeWidth={open ? 2.4 : 1.8} />
            <span>More</span>
          </button>
        </div>
      </nav>
    </>
  );
}
