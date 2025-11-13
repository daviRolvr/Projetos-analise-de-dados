# Análise de Vendas de Supermercado

Breve descrição
----------------

Este projeto contém a análise exploratória (EDA) do dataset `supermarket_sales.csv`. O objetivo é responder perguntas de negócio como:

- Qual o faturamento por filial?
- Quais os produtos mais rentáveis?
- Qual a avaliação média dos clientes por loja/segmento?
- Existem padrões sazonais nas vendas?

Estrutura do projeto
--------------------

```
analise_supermercado/
    README.md
    dados/                    # coloque aqui supermarket_sales.csv
    imagens/                  # gráficos e imagens geradas
    analise_supermercado.ipynb
    analise_supermercado.py   # script auxiliar (opcional)
```

Como usar
---------

1. Coloque `supermarket_sales.csv` em `dados/`.
2. Abra o notebook `analise_supermercado.ipynb` e execute as células (ou execute `analise_supermercado.py`).
3. Gere gráficos e salve em `imagens/`.

Dependências (exemplo)
----------------------

Recomendo criar um venv e instalar:

```
pip install pandas matplotlib seaborn jupyter
```

Observações
-----------

Este diretório serve como um template inicial — sinta-se à vontade para adaptar e enviar PRs com melhorias.