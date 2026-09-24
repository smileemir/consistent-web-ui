import "./globals.css";
import Header from "@/components/Header";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <Header />
        <main className="mx-auto max-w-6xl px-[18px]">{children}</main>
        <footer className="mt-16 bg-[#111827] py-8 text-center text-[13px] text-[#9ca3af]">© 2026 Fjord Goods (fictional)</footer>
      </body>
    </html>
  );
}
