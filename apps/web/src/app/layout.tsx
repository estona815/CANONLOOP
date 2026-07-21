import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CANONLOOP — Visual continuity for generative media",
  description: "Generate, critique, repair, and archive multi-format media with verifiable provenance."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}

