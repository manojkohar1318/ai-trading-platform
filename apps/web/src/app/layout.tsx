import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata={title:'Indian Trading AI',description:'Quantitative Indian market analysis terminal'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
