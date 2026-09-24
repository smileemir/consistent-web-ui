import ProductCard from "@/components/ProductCard";

export default function Products() {
  return (
    <div className="py-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-[30px] font-bold text-gray-900">All products</h1>
        <select className="rounded-md border border-[#d1d5db] px-3 py-2 text-sm">
          <option>Newest</option><option>Price</option>
        </select>
      </div>
      <div className="grid grid-cols-2 gap-5 md:grid-cols-4">
        <ProductCard title="Stoneware mug" price="€18" />
        <ProductCard title="Linen napkins" price="€24" />
      </div>
    </div>
  );
}
