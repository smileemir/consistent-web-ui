export default function Button({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <button className={`rounded-[6px] bg-[#0e7490] px-[18px] py-[10px] text-white transition-colors duration-[250ms] hover:bg-[#155e75] ${className}`}>
      {children}
    </button>
  );
}
