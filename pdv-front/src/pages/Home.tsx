// src/pages/Home.tsx

import React from "react";
import { Header } from "@/components/commons/Header";
import { MenuItemList } from "@/components/menu/MenuItemList";
// Importamos o TIPO do item e o Botão
import type { MenuItemProps } from "@/components/menu/MenuItemCard";
import { Button } from "@/components/ui/button";

// --- DADOS MOCK (Agora moram aqui) ---
const MOCK_ITEMS: MenuItemProps[] = [
  {
    id: "1",
    name: "Hambúrguer Clássico",
    description: "Pão, carne (180g), queijo...",
    price: 25.5,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Hambúrguer",
    category: "Hambúrgueres",
  },
  {
    id: "4",
    name: "Hambúrguer Vegano",
    description: "Pão vegano, burger à base...",
    price: 28.0,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Hambúrguer+Vegano",
    category: "Hambúrgueres",
  },
  {
    id: "2",
    name: "Batata Frita Média",
    description: "Porção de 200g...",
    price: 12.0,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Batata+Frita",
    category: "Acompanhamentos",
  },
  {
    id: "3",
    name: "Refrigerante Lata",
    description: "Coca-Cola, Guaraná...",
    price: 6.0,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Refrigerante",
    category: "Bebidas",
  },
  {
    id: "5",
    name: "Água Mineral 500ml",
    description: "Água sem gás.",
    price: 4.0,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Água",
    category: "Bebidas",
  },
  {
    id: "6",
    name: "Milkshake Ovomaltine",
    description: "300ml.",
    price: 18.0,
    imageUrl: "https://via.placeholder.com/300x200.png?text=Milkshake",
    category: "Sobremesas",
  },
];
// --- FIM DOS DADOS MOCK ---

const Home: React.FC = () => {
  // --- LÓGICA DE AGRUPAMENTO (Agora mora aqui) ---
  const groupedItems = MOCK_ITEMS.reduce((acc, item) => {
    const category = item.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {} as Record<string, MenuItemProps[]>);

  // Obter apenas os nomes das categorias para a nav
  const categories = Object.keys(groupedItems);
  // --- FIM DA LÓGICA ---

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Navbar (vinda de 'commons') */}
      <Header />

      {/* Área principal */}
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold">Bem-vindo ao Cardápio Online!</h1>
        <p className="text-muted-foreground mt-2">Escolha seus itens abaixo.</p>

        {/* --- Lista de categorias do menu (A NAV HORIZONTAL) --- */}
        <nav className="sticky top-[65px] md:top-[73px] bg-background py-4 z-10 -mx-4 px-4 border-b">
          {/* 'flex' para horizontal, 'overflow-x-auto' para scrollar no mobile */}
          <div className="flex gap-3 overflow-x-auto pb-2">
            {categories.map((category) => (
              <Button
                asChild // Permite usar um 'a' (link) dentro do botão
                variant="outline"
                size="sm"
                key={category}
                className="shrink-0 text-white bg-yellow-400 hover:bg-yellow-500" // Evita que os botões encolham
              >
                {/* O 'href' com '#' faz o scroll para o 'id' correspondente */}
                <a href={`#${category}`} className="block py-2 px-4">{category}</a>
              </Button>
            ))}
          </div>
        </nav>

        {/* 2. Lista de itens (cardápio) agora recebe os dados */}
        <div className="mt-8">
          <MenuItemList groupedItems={groupedItems} />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t py-4">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} PDV Delivery. Todos os direitos
          reservados.
        </div>
      </footer>
    </div>
  );
};

export default Home;
