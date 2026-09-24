export default function ProductCard({ title, price, badge }: { title: string; price: string; badge?: string }) {
  return (
    <article className="rounded-[10px] border border-[#e5e7eb] bg-white p-[13px] hover:shadow-lg">
      <div className="aspect-[4/3] rounded-[8px] bg-[#f3f4f6]" />
      {badge && <span className="mt-2 inline-block rounded bg-[#fef3c7] px-2 text-[12px] text-[#b45309]">{badge}</span>}
      <h3 className="mt-[10px] text-[15px] font-medium text-[#333]">{title}</h3>
      <p className="font-semibold text-[#111827]">{price}</p>
      <button className="mt-3 w-full rounded-full bg-cyan-600 py-2 text-white">Add to cart</button>
    </article>
  );
}
