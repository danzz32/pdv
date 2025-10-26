import React from "react";
import { MenuItemCard } from "./MenuItemCard";
import type { MenuItemProps } from "./MenuItemCard";
import { Separator } from "@/components/ui/separator"; // Importar separador

// --- 1. DADOS MOCK E LÓGICA FORAM REMOVIDOS ---
// (Eles agora estão no Home.tsx)

// --- 2. DEFINIR A INTERFACE DE PROPS ---
// O componente agora espera receber os itens agrupados
interface MenuItemListProps {
  groupedItems: Record<string, MenuItemProps[]>;
}

// --- 3. ATUALIZAR A ASSINATURA DO COMPONENTE ---
// Ele agora recebe 'groupedItems' das suas props
export const MenuItemList: React.FC<MenuItemListProps> = ({ groupedItems }) => {
  // Obter os nomes das categorias (para o separador condicional)
  const categoryNames = Object.keys(groupedItems);

  // Se não houver itens, mostrar uma mensagem
  if (categoryNames.length === 0) {
    return <p>Nenhum item encontrado no cardápio.</p>;
  }

  return (
    <section className="space-y-12">
      {Object.entries(groupedItems).map(([categoryName, items]) => (
        // --- 4. ATUALIZAR O DIV DA CATEGORIA ---
        <div
          key={categoryName}
          id={categoryName} // 'id' para o link âncora funcionar
          className="scroll-mt-32 pt-4" // Margem de scroll para não ficar atrás da navbar
        >
          {/* Título da Categoria */}
          <h2 className="text-3xl font-bold tracking-tight mb-6">
            {categoryName}
          </h2>

          {/* Grid de Itens da Categoria */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {items.map((item) => (
              <MenuItemCard key={item.id} item={item} />
            ))}
          </div>

          {/* 5. Separador condicional (não mostra no último item) */}
          {categoryNames[categoryNames.length - 1] !== categoryName && (
            <Separator className="mt-12" />
          )}
        </div>
      ))}
    </section>
  );
};
