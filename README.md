# PDF Splitter

Um aplicativo Python para dividir arquivos PDF grandes em partes menores.

## Features

- Interface gráfica moderna e intuitiva
- Split qualquer PDF em múltiplos volumes
- Calcula automaticamente quantas páginas vão em cada parte
- Sem limite de tamanho de arquivo — roda localmente na sua máquina
- Escolha da pasta de saída para os arquivos divididos
- Preview do número total de páginas do PDF
- Barra de progresso durante o processamento
- Informações detalhadas sobre a divisão

## Requisitos

- Python 3.7+
- `PyPDF2` library
- `ttkthemes` library

## Instruções de Instalação

### 1. Clone este repositório

```
git clone https://github.com/yourusername/pdf-splitter.git
cd pdf-splitter
```

### 2. Crie um ambiente virtual

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```
pip install -r requirements.txt
```

### 4. Execute o aplicativo

```
python gui.py
```

## Como Usar

1. Clique no botão "Procurar" para selecionar o arquivo PDF que deseja dividir
2. (Opcional) Clique em "Escolher" para selecionar uma pasta de saída diferente
3. Escolha o número de partes em que deseja dividir o PDF
4. Observe as informações do PDF (total de páginas e páginas por parte)
5. Clique em "Dividir PDF" para iniciar o processo
6. Acompanhe o progresso na barra de progresso
7. Os arquivos divididos serão salvos na pasta escolhida (ou na mesma pasta do arquivo original)

## Licença

Este projeto está licenciado sob a Licença MIT.