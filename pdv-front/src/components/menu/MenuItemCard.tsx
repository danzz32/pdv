// src/components/menu/MenuItemCard.tsx

import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Plus } from "lucide-react";

// Define a "forma" dos dados de um item
export interface MenuItemProps {
  id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  category: string; // <-- ADICIONADO AQUI
}

// Helper para formatar o preço
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
};

export const MenuItemCard: React.FC<{ item: MenuItemProps }> = ({ item }) => {
  return (
    <Card className="w-full flex flex-col">
      {/* Imagem */}
      <CardHeader className="p-0">
        <img
          src={item.imageUrl}
          alt={item.name}
          className="w-full h-48 object-cover rounded-t-lg"
        />
      </CardHeader>

      {/* Conteúdo */}
      <CardContent className="pt-4 flex-1">
        <CardTitle className="text-lg">{item.name}</CardTitle>
        <CardDescription className="mt-2 text-sm">
          {item.description}
        </CardDescription>
      </CardContent>

      {/* Footer com Preço e Botão */}
      <CardFooter className="flex justify-between items-center pt-4">
        <span className="text-lg font-bold">{formatCurrency(item.price)}</span>
        <Button
          size="icon"
          aria-label="Adicionar ao carrinho"
          className="bg-yellow-400 hover:bg-yellow-500"
        >
          <Plus className="h-4 w-4 " />
        </Button>
      </CardFooter>
    </Card>
  );
};
