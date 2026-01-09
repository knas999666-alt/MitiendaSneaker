import React, { useState, useEffect, useMemo } from 'react';
import { ShoppingBag, Search, X, ChevronRight, Check, Trash2, ShieldCheck, Zap, MessageCircle, Menu, Filter, Share2, Heart, DollarSign } from 'lucide-react';

// --- CONFIGURACIÓN DE CONTACTO ---
const WHATSAPP_NUMBER = "525565647493"; 
const PAYPAL_USER = "https://paypal.me/knas99"; // Tu usuario de paypal.me

// --- UI COMPONENTS ---

const Navbar = ({ cartCount, toggleCart }) => (
  <nav className="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
    <div className="container mx-auto px-4 h-16 flex justify-between items-center">
        <div className="flex items-center gap-2 cursor-pointer">
            <div className="w-9 h-9 bg-black flex items-center justify-center text-white font-black italic text-xl tracking-tighter rounded-lg shadow-md transform -rotate-3">W</div>
            <span className="font-black text-2xl tracking-tighter uppercase hidden md:block">WERA<span className="text-[#006340]">STOCK</span></span>
        </div>
        <div className="hidden md:flex flex-1 max-w-xl mx-8 relative">
            <input type="text" placeholder="Buscar: Jordan 4, Travis Scott..." className="w-full bg-gray-50 border border-gray-200 h-11 pl-11 pr-4 rounded-full text-sm font-bold focus:ring-2 focus:ring-[#006340] focus:bg-white outline-none transition-all placeholder-gray-400"/>
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18}/>
        </div>
        <button onClick={toggleCart} className="relative flex items-center gap-2 p-2 hover:bg-gray-100 rounded-full transition-colors">
            <ShoppingBag size={24} className="text-black" />
            {cartCount > 0 && <span className="absolute -top-1 -right-1 bg-[#006340] text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full border-2 border-white shadow-sm">{cartCount}</span>}
        </button>
    </div>
  </nav>
);

const FilterBar = ({ activeCategory, setActiveCategory }) => {
    const categories = ["Todos", "Retro 1", "Retro 3", "Retro 4", "Retro 5", "Retro 6", "Retro 11", "Otros Retro"];
    return (
        <div className="bg-white border-b border-gray-100 sticky top-16 z-40 shadow-sm">
            <div className="max-w-[1600px] mx-auto px-4 overflow-x-auto no-scrollbar">
                <div className="flex gap-3 h-14 items-center">
                    {categories.map(cat => (
                        <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-5 py-2 rounded-full text-xs font-black uppercase tracking-wide whitespace-nowrap transition-all border ${activeCategory === cat ? 'bg-black text-white border-black shadow-md' : 'bg-white text-gray-500 border-gray-200 hover:border-black hover:text-black'}`}>{cat}</button>
                    ))}
                </div>
            </div>
        </div>
    );
};

const ProductCard = ({ product, onClick }) => {
    const minPrice = product.price || 0;
    return (
        <div onClick={() => onClick(product)} className="group cursor-pointer bg-white border border-transparent hover:border-gray-200 hover:shadow-xl transition-all duration-300 p-4 rounded-xl flex flex-col h-full">
            <div className="aspect-square mb-4 flex items-center justify-center relative bg-[#F9F9F9] rounded-lg overflow-hidden">
                {product.badge && <span className="absolute top-2 left-2 bg-[#006340] text-white text-[9px] font-black px-2 py-1 uppercase rounded-sm shadow-sm z-10">{product.badge}</span>}
                <img src={product.image} alt={product.name} className="w-[90%] h-auto object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-500 ease-out" loading="lazy" onError={(e) => { e.target.src = "https://images.stockx.com/images/Air-Jordan-1-Retro-High-OG-Chicago-Reimagined-Lost-and-Found-Product.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color"; }}/>
            </div>
            <div className="mt-auto">
                <h3 className="font-black text-gray-900 text-xs uppercase leading-tight line-clamp-2 mb-1">{product.name}</h3>
                <p className="text-gray-500 text-[10px] truncate mb-3 font-medium">{product.model}</p>
                <div className="flex justify-between items-end border-t border-dashed border-gray-200 pt-3">
                    <div><p className="font-black text-lg text-black">${minPrice.toLocaleString('es-MX')}</p><p className="text-[10px] text-gray-400 font-bold uppercase">Envío Incluido</p></div>
                    <div className="bg-black text-white p-1.5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"><ChevronRight size={14}/></div>
                </div>
            </div>
        </div>
    );
};

const ProductDetail = ({ product, onClose, onAddToCart }) => {
  const [selectedSize, setSelectedSize] = useState(null);
  const pricingData = product.pricing || {};
  const sizes = Object.keys(pricingData).sort((a, b) => parseFloat(a) - parseFloat(b));
  const currentPrice = selectedSize ? pricingData[selectedSize] : null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex justify-center items-center p-4 animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-5xl h-full md:h-auto md:max-h-[85vh] shadow-2xl flex flex-col md:flex-row relative rounded-2xl overflow-hidden">
        <button onClick={onClose} className="absolute top-4 right-4 p-2 bg-gray-100 hover:bg-gray-200 rounded-full z-20"><X size={20}/></button>
        <div className="w-full md:w-3/5 bg-white flex items-center justify-center p-8 md:p-12 border-r border-gray-100 relative">
             <div className="absolute top-6 left-6 flex flex-col gap-2"><span className="inline-flex items-center gap-1 bg-[#006340] text-white px-3 py-1 text-[10px] font-bold uppercase rounded-full shadow-md"><ShieldCheck size={12}/> Verificado</span></div>
             <img src={product.image} className="w-full h-auto max-h-[400px] object-contain drop-shadow-xl" />
        </div>
        <div className="w-full md:w-2/5 p-8 flex flex-col bg-white overflow-y-auto">
             <div className="mb-8">
                 <h2 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 flex items-center gap-1">{product.brand} / {product.category}</h2>
                 <h1 className="text-3xl font-black text-black leading-tight mb-2 uppercase">{product.name}</h1>
                 <p className="text-lg text-[#006340] font-bold">{product.model}</p>
             </div>
             <div className="mb-8 flex-1">
                 <p className="text-xs font-bold text-black uppercase mb-4">Selecciona Talla (MX)</p>
                 <div className="grid grid-cols-3 gap-2">
                     {sizes.map(size => (
                         <button key={size} onClick={() => setSelectedSize(size)} className={`py-3 px-2 border rounded flex flex-col items-center justify-center transition-all ${selectedSize === size ? 'border-black bg-black text-white shadow-lg scale-105' : 'border-gray-200 text-gray-700 hover:border-black'}`}>
                             <span className="text-sm font-bold">{size.replace(' MX', '')}</span>
                             <span className={`text-[10px] font-bold mt-0.5 ${selectedSize === size ? 'text-gray-400' : 'text-[#006340]'}`}>${pricingData[size].toLocaleString()}</span>
                         </button>
                     ))}
                 </div>
             </div>
             <div className="mt-auto pt-6 border-t border-gray-100">
                 <div className="flex justify-between items-end mb-4"><p className="text-sm font-bold text-gray-500">Precio Final:</p><p className="text-4xl font-black tracking-tight">${currentPrice ? currentPrice.toLocaleString('es-MX') : "--"}</p></div>
                 <button disabled={!selectedSize} onClick={() => { onAddToCart({...product, selectedSize, price: currentPrice}); onClose(); }} className="w-full bg-black text-white h-14 font-bold text-lg uppercase tracking-wide hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 shadow-lg">Comprar Ahora</button>
             </div>
        </div>
      </div>
    </div>
  );
};

const CartDrawer = ({ isOpen, onClose, cart, setCart }) => {
    const total = cart.reduce((acc, item) => acc + item.price, 0);
    const handleWhatsApp = () => {
        if(cart.length === 0) return;
        const msg = `Hola WeraStock! Quiero comprar: ${cart.map(i => `${i.name} (${i.model}) [${i.selectedSize}]`).join(', ')}. Total: $${total}`;
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
    };
    const handlePayPal = () => {
        // Genera link de PayPal.me
        window.open(`https://paypal.me/${PAYPAL_USER}/${total}`, '_blank');
    };
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex justify-end animate-in fade-in duration-200">
            <div className="absolute inset-0" onClick={onClose}></div>
            <div className="relative w-full max-w-md bg-white h-full flex flex-col shadow-2xl animate-in slide-in-from-right duration-300">
                <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-white"><h2 className="font-black text-xl uppercase tracking-tighter">Tu Pedido</h2><button onClick={onClose}><X size={20}/></button></div>
                <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
                    {cart.map((item, i) => (
                        <div key={i} className="flex gap-4 mb-4 bg-white p-4 border border-gray-100 rounded-xl shadow-sm">
                            <div className="w-20 h-20 flex items-center justify-center p-2 flex-shrink-0 bg-gray-50 rounded-lg"><img src={item.image} className="w-full h-auto object-contain mix-blend-multiply"/></div>
                            <div className="flex-1"><h4 className="font-bold text-xs uppercase leading-tight mb-1">{item.name}</h4><p className="text-[10px] text-gray-500 mb-2">{item.model}</p><div className="flex justify-between items-end"><div className="bg-black text-white px-2 py-1 text-[10px] font-bold rounded">Talla: {item.selectedSize.replace(' MX', '')}</div><p className="font-black text-sm">${item.price.toLocaleString('es-MX')}</p></div><button onClick={() => setCart(cart.filter((_, idx) => idx !== i))} className="text-[10px] text-red-500 font-bold mt-2 hover:underline uppercase">Eliminar</button></div>
                        </div>
                    ))}
                </div>
                <div className="p-6 bg-white border-t border-gray-100 shadow-lg">
                    <div className="flex justify-between mb-6 text-2xl font-black"><span>Total</span><span>${total.toLocaleString('es-MX')}</span></div>
                    <div className="flex flex-col gap-3">
                        <button onClick={handleWhatsApp} className="w-full bg-[#25D366] text-white py-3 rounded-lg font-bold uppercase hover:opacity-90 flex justify-center items-center gap-2"><MessageCircle size={18}/> Pedir por WhatsApp</button>
                        <button onClick={handlePayPal} className="w-full bg-[#0070BA] text-white py-3 rounded-lg font-bold uppercase hover:opacity-90 flex justify-center items-center gap-2"><DollarSign size={18}/> Pagar con PayPal</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default function App() {
  const [inventory, setInventory] = useState([]);
  const [cart, setCart] = useState([]);
  const [activeCategory, setActiveCategory] = useState("Todos");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isCartOpen, setIsCartOpen] = useState(false);

  useEffect(() => {
    if (!document.getElementById('tailwind-script')) {
      const script = document.createElement('script'); script.id = 'tailwind-script'; script.src = "https://cdn.tailwindcss.com"; document.head.appendChild(script);
    }
  }, []);

  useEffect(() => {
    fetch('/inventory.json?t=' + Date.now()).then(res => res.json()).then(data => setInventory(Array.isArray(data) ? data : [])).catch(() => console.log("Cargando..."));
  }, []);

  const filteredItems = useMemo(() => {
    if (activeCategory === "Todos") return inventory;
    return inventory.filter(p => p.category === activeCategory);
  }, [activeCategory, inventory]);

  return (
    <div className="min-h-screen bg-white font-sans text-gray-900 selection:bg-[#006340] selection:text-white">
      <Navbar cartCount={cart.length} toggleCart={() => setIsCartOpen(true)} />
      <FilterBar activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
      <div className="max-w-[1600px] mx-auto px-4 py-8">
          <div className="flex justify-between items-end mb-8 border-b border-gray-100 pb-4"><div><h1 className="text-2xl font-black uppercase tracking-tight">{activeCategory}</h1></div><span className="text-xs font-bold bg-gray-100 px-3 py-1 rounded-full">{filteredItems.length} Pares</span></div>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-x-4 gap-y-10">{filteredItems.map(item => <ProductCard key={item.id} product={item} onClick={setSelectedProduct} />)}</div>
      </div>
      {selectedProduct && <ProductDetail product={selectedProduct} onClose={() => setSelectedProduct(null)} onAddToCart={(p) => { setCart([...cart, p]); setSelectedProduct(null); setIsCartOpen(true); }} />}
      <CartDrawer isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} cart={cart} setCart={setCart} />
    </div>
  );
}