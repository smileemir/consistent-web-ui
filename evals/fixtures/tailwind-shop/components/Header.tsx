export default function Header() {
  return (
    <header className="sticky top-0 z-[9999] border-b border-[#e5e7eb] bg-white dark:bg-gray-900">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-[18px] py-[13px]">
        <a href="/" className="text-[22px] font-bold text-[#083344] dark:text-white">Fjord Goods</a>
        <nav className="flex gap-[15px] text-[15px] text-[#374151]">
          <a href="/products">Shop</a><a href="/journal">Journal</a><a href="/cart">Cart</a>
        </nav>
      </div>
    </header>
  );
}
