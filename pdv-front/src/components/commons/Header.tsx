// src/components/layout/Header.tsx

import { Menu, ShoppingCart, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";

export function Header() {
  return (
    <header className="border-b sticky top-0 z-10 bg-background">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        {/* 1. Logo */}
        <div className="font-bold text-lg md:text-xl">PDV Delivery</div>

        {/* 2. Nav Desktop (Escondido no Mobile) */}
        <nav className="hidden md:flex items-center gap-4">
          <a
            href="#"
            className="text-sm font-medium text-muted-foreground hover:text-primary"
          >
            Cardápio
          </a>
          <a
            href="#"
            className="text-sm font-medium text-muted-foreground hover:text-primary"
          >
            Meus Pedidos
          </a>
        </nav>

        {/* 3. Ações Desktop (Escondido no Mobile) */}
        <div className="hidden md:flex items-center gap-3">
          <Button
            size="icon"
            aria-label="Carrinho"
            className="bg-yellow-500 hover:bg-yellow-600 border-yellow-500"
          >
            <ShoppingCart className="h-5 w-5 text-white" />
          </Button>
          <Button className="bg-yellow-500 hover:bg-yellow-600 border-yellow-500">
            <User className="h-5 w-5 mr-2" />
            Entrar
          </Button>
        </div>

        {/* 4. Menu Mobile (Apenas no Mobile) */}
        <div className="md:hidden">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" aria-label="Abrir menu">
                <Menu className="h-5 w-5 text-white" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="flex flex-col w-3/4">
              <SheetHeader>
                <SheetTitle>PDV Delivery</SheetTitle>
              </SheetHeader>

              {/* Links do Menu Mobile */}
              <nav className="flex flex-col gap-4 mt-6">
                <a href="#" className="text-lg font-medium hover:underline">
                  Cardápio
                </a>
                <a href="#" className="text-lg font-medium hover:underline">
                  Meus Pedidos
                </a>
              </nav>

              {/* Ações no fim do menu */}
              <div className="mt-auto flex flex-col gap-3">
                <Separator />
                <Button variant="outline" className="justify-start gap-2">
                  <ShoppingCart className="h-5 w-5" />
                  <span>Meu Carrinho</span>
                </Button>
                <Button className="justify-start gap-2">
                  <User className="h-5 w-5" />
                  <span>Entrar / Criar Conta</span>
                </Button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
