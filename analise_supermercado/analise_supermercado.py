"""analise_supermercado.py

Script executável que carrega o dataset `supermarket_sales.csv` e realiza
as 6 análises descritas no projeto. Feito para rodar a partir da linha de
comando ou ser importado como módulo.

Uso:
    python analise_supermercado.py --file analise_supermercado/dados/supermarket_sales.csv

"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import pandas as pd


def analyze_supermarket_data(file_path: str) -> None:
    """Carrega o dataset e realiza as 6 análises solicitadas."""
    if not os.path.exists(file_path):
        print(f"Erro: arquivo não encontrado em '{file_path}'")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return


    # Converter Date para datetime
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        except Exception:
            try:
                df['Date'] = pd.to_datetime(df['Date'])
            except Exception:
                print("Aviso: não foi possível converter a coluna 'Date' para datetime.")
    else:
        print("Aviso: coluna 'Date' não encontrada no dataset.")

    # Garantir que 'Total' seja numérico
    if 'Total' in df.columns:
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    else:
        print("Aviso: coluna 'Total' não encontrada no dataset. Algumas análises podem falhar.")

    print('\n--- Análises de Vendas do Supermercado ---')

    # 1. Faturamento por filial
    print('\n--- 1. Faturamento por Filial ---')
    try:
        faturamento_filial = df.groupby('Branch')['Total'].sum().reset_index()
        faturamento_filial['Total'] = faturamento_filial['Total'].round(2)
        faturamento_filial.columns = ['Filial', 'Faturamento']
        print(faturamento_filial.to_string(index=False))
    except KeyError:
        print("Erro: Coluna 'Branch' ou 'Total' não encontrada.")
    except Exception as e:
        print(f"Erro na Análise 1: {e}")

    # 2. Percentual da receita por linha de produto
    print('\n--- 2. Percentual da Receita por Linha de Produto ---')
    try:
        total_receita = df['Total'].sum()
        if total_receita and total_receita > 0:
            receita_produto = df.groupby('Product line')['Total'].sum()
            percentual_produto = ((receita_produto / total_receita) * 100).sort_values(ascending=False).reset_index()
            percentual_produto.columns = ['Linha de Produto', 'Percentual (%)']
            percentual_produto['Percentual (%)'] = percentual_produto['Percentual (%)'].round(2)
            print(percentual_produto.to_string(index=False))
        else:
            print('Receita total é zero ou inválida.')
    except KeyError:
        print("Erro: Coluna 'Product line' ou 'Total' não encontrada.")
    except Exception as e:
        print(f"Erro na Análise 2: {e}")

    # 3. Distribuição de consumo (contagem) por gênero e linha de produto
    print('\n--- 3. Distribuição de Consumo (Contagem) por Gênero e Produto ---')
    try:
        consumo_genero_produto = pd.pivot_table(
            df,
            index='Product line',
            columns='Gender',
            aggfunc='size',
            fill_value=0,
        )
        print(consumo_genero_produto)
    except KeyError:
        print("Erro: Coluna 'Product line' ou 'Gender' não encontrada.")
    except Exception as e:
        print(f"Erro na Análise 3: {e}")

    # 4. Faturamento por mês
    print('\n--- 4. Faturamento por Mês ---')
    try:
        if 'Date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Mes_Ano'] = df['Date'].dt.to_period('M')
            faturamento_mes = df.groupby('Mes_Ano')['Total'].sum().reset_index()
            faturamento_mes = faturamento_mes.sort_values(by='Mes_Ano')
            faturamento_mes['Total'] = faturamento_mes['Total'].round(2)
            faturamento_mes['Mes_Ano'] = faturamento_mes['Mes_Ano'].astype(str)
            faturamento_mes.columns = ['Mes_Ano', 'Faturamento']
            print(faturamento_mes.to_string(index=False))
        else:
            print("Não foi possível calcular faturamento por mês: coluna 'Date' ausente ou inválida.")
    except Exception as e:
        print(f"Erro na Análise 4: {e}")

    # 5. Média de avaliação por filial em Janeiro de 2019
    print('\n--- 5. Média de Avaliação por Filial (Janeiro/2019) ---')
    try:
        if 'Date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Date']):
            df_jan_2019 = df[(df['Date'].dt.year == 2019) & (df['Date'].dt.month == 1)]
            if df_jan_2019.empty:
                print('Não há dados de vendas para Janeiro de 2019.')
            else:
                media_avaliacao_jan = df_jan_2019.groupby('Branch')['Rating'].mean().reset_index()
                media_avaliacao_jan['Rating'] = media_avaliacao_jan['Rating'].round(2)
                media_avaliacao_jan.columns = ['Filial', 'Média de Avaliação']
                print(media_avaliacao_jan.to_string(index=False))
        else:
            print("Não foi possível calcular média de avaliações: coluna 'Date' ausente ou inválida.")
    except KeyError:
        print("Erro: Coluna 'Branch' ou 'Rating' não encontrada.")
    except Exception as e:
        print(f"Erro na Análise 5: {e}")

    # 6. Gasto por tipo de consumidor em cada filial
    print('\n--- 6. Gasto por Tipo de Consumidor em cada Filial ---')
    try:
        gasto_pivot = df.pivot_table(
            index='Branch',
            columns='Customer type',
            values='Total',
            aggfunc='sum',
            fill_value=0,
        ).round(2)
        print(gasto_pivot)
    except KeyError:
        print("Erro: Coluna 'Branch', 'Customer type' ou 'Total' não encontrada.")
    except Exception as e:
        print(f"Erro na Análise 6: {e}")


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Análises de Vendas de Supermercado (supermarket_sales.csv)')
    parser.add_argument('--file', '-f', dest='file', type=str,
                        default=os.path.join(os.path.dirname(__file__), 'dados', 'supermarket_sales.csv'),
                        help='Caminho para o arquivo CSV (padrão: analise_supermercado/dados/supermarket_sales.csv)')
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    analyze_supermarket_data(args.file)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
