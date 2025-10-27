# PDV Front - Cardápio Online

Este é o repositório para o front-end do projeto PDV (Ponto de Venda), uma aplicação web moderna desenvolvida para atuar como um cardápio digital interativo.

## ✨ Principais Funcionalidades

- **Visualização de Cardápio:** Exibe os itens do cardápio de forma organizada e atraente.
- **Agrupamento por Categoria:** Os itens são agrupados por categorias (ex: Hambúrgueres, Bebidas, Sobremesas) para fácil navegação.
- **Navegação Rápida por Categorias:** Uma barra de navegação fixa permite ao usuário pular diretamente para a categoria desejada.
- **Design Responsivo:** Interface adaptável para uma boa experiência tanto em desktops quanto em dispositivos móveis.

## 🚀 Tecnologias Utilizadas

- **React:** Biblioteca para construção da interface de usuário.
- **TypeScript:** Superset de JavaScript que adiciona tipagem estática.
- **Vite:** Ferramenta de build moderna e rápida para desenvolvimento front-end.
- **Tailwind CSS:** Framework CSS utility-first para estilização rápida e customizável.
- **Radix UI:** Componentes de UI de baixo nível e acessíveis.
- **Lucide React:** Biblioteca de ícones.
- **React Router DOM:** Para gerenciamento de rotas na aplicação.

## 🏁 Começando

Siga os passos abaixo para configurar e executar o projeto em seu ambiente de desenvolvimento local.

### Pré-requisitos

- [Node.js](https://nodejs.org/en/) (versão 18 ou superior)
- [Yarn](https://yarnpkg.com/) (gerenciador de pacotes)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pdv-front.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd pdv-front
   ```
3. Instale as dependências:
   ```bash
   yarn install
   ```

### Executando o Projeto

Para iniciar o servidor de desenvolvimento, execute:

```bash
yarn dev
```

A aplicação estará disponível em `http://localhost:5173`.

## 📜 Scripts Disponíveis

- `yarn dev`: Inicia o servidor de desenvolvimento com Hot Reload.
- `yarn build`: Compila e otimiza a aplicação para produção.
- `yarn lint`: Executa o linter para analisar o código e encontrar problemas.
- `yarn preview`: Inicia um servidor local para visualizar a build de produção.

## 🐳 Deployment

O projeto está configurado para ser implantado utilizando Docker. O `Dockerfile` e o arquivo `nginx.conf` estão incluídos para criar uma imagem de produção e servi-la com Nginx.

Para construir a imagem Docker, execute:
```bash
docker build -t pdv-front .
```
