import ProductCard from "@/components/ProductCard";
import Button from "@/components/Button";

export default function Home() {
  return (
    <>
      <section className="rounded-[14px] bg-[#ecfeff] p-[36px] my-[22px]">
        <h1 className="text-[40px] font-bold text-[#083344]">Goods for slow mornings</h1>
        <p className="mt-2 text-[#6b7280]">Ceramics, textiles and coffee gear.</p>
        <Button className="mt-5">Shop the collection</Button>
      </section>
      <h2 className="mb-[13px] text-[24px] font-semibold">New arrivals</h2>
      <div className="grid grid-cols-2 gap-[18px] md:grid-cols-4">
        <ProductCard title="Stoneware mug" price="€18" />
        <ProductCard title="Linen napkins" price="€24" badge="New" />
        <ProductCard title="Pour-over kettle" price="€65" />
        <ProductCard title="Oak tray" price="€39" />
      </div>
    </>
  );
}
