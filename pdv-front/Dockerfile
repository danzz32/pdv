# --- ESTÁGIO 1: Build ---
# Usamos uma imagem node "alpine" por ser leve
FROM node:20-alpine AS build

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de gerenciamento de pacotes
COPY package.json yarn.lock ./

# Instala as dependências
RUN yarn install

# Copia o resto do código-fonte
COPY . .

# Executa o build de produção (gera a pasta 'dist')
RUN yarn build

# --- ESTÁGIO 2: Serve ---
# Usamos uma imagem Nginx "alpine"
FROM nginx:1.25-alpine

# Copia os arquivos estáticos construídos do estágio anterior
COPY --from=build /app/dist /usr/share/nginx/html

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia nossa própria configuração do Nginx (que criaremos a seguir)
COPY nginx.conf /etc/nginx/conf.d/

# Expõe a porta 80 (padrão do Nginx)
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]