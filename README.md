# PDF Splitter

Um aplicativo Python para dividir arquivos PDF grandes em partes menores.

## Features

- Interface gráfica moderna e intuitiva
- Split qualquer PDF em múltiplos volumes
- Calcula automaticamente quantas páginas vão em cada parte
- Sem limite de tamanho de arquivo — roda localmente na sua máquina

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
2. Escolha o número de partes em que deseja dividir o PDF
3. Clique em "Dividir PDF" para iniciar o processo
4. Os arquivos divididos serão salvos na mesma pasta do arquivo original

## Licença

Este projeto está licenciado sob a Licença MIT.