"""
Módulo de Análise Exploratória de Dados (EDA)
==============================================
Análise estatística e profiling de dados de churn.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EDAAnalyzer:
    """Classe para análise exploratória de dados de churn."""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = 'reports'):
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 11
        
    def get_basic_statistics(self) -> dict:
        """Retorna estatísticas básicas do dataset."""
        
        stats = {
            'total_customers': len(self.df),
            'churn_rate': self.df['Churn'].mean() * 100,
            'churn_count': self.df['Churn'].sum(),
            'avg_tenure': self.df['tenure'].mean(),
            'avg_monthly_charges': self.df['MonthlyCharges'].mean(),
            'avg_total_charges': self.df['TotalCharges'].mean(),
            'total_revenue': self.df['TotalCharges'].sum()
        }
        
        return stats
    
    def analyze_churn_by_category(self, column: str) -> pd.DataFrame:
        """Analisa taxa de churn por categoria."""
        
        churn_by_cat = self.df.groupby(column)['Churn'].agg([
            ('total', 'count'),
            ('churned', 'sum'),
            ('churn_rate', 'mean')
        ]).reset_index()
        
        churn_by_cat['churn_rate'] = churn_by_cat['churn_rate'] * 100
        churn_by_cat = churn_by_cat.sort_values('churn_rate', ascending=False)
        
        return churn_by_cat
    
    def plot_churn_distribution(self) -> None:
        """Plota distribuição geral do churn."""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        churn_counts = self.df['Churn'].value_counts()
        colors = ['#2ecc71', '#e74c3c']
        
        ax1.pie(churn_counts, labels=['No Churn', 'Churn'], autopct='%1.1f%%',
                colors=colors, explode=(0, 0.05), shadow=True, startangle=90)
        ax1.set_title('Distribuição de Churn', fontsize=14, fontweight='bold')
        
        bars = ax2.bar(['No Churn', 'Churn'], churn_counts.values, color=colors)
        ax2.set_ylabel('Número de Clientes')
        ax2.set_title('Contagem de Clientes por Churn', fontsize=14, fontweight='bold')
        
        for bar, count in zip(bars, churn_counts.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                    f'{count:,}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'churn_distribution.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de distribuição de churn salvo")
    
    def plot_churn_by_contract(self) -> None:
        """Plota taxa de churn por tipo de contrato."""
        
        churn_by_contract = self.analyze_churn_by_category('Contract')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(churn_by_contract['Contract'], churn_by_contract['churn_rate'],
                     color=['#e74c3c', '#f39c12', '#2ecc71'])
        
        ax.set_xlabel('Tipo de Contrato')
        ax.set_ylabel('Taxa de Churn (%)')
        ax.set_title('Taxa de Churn por Tipo de Contrato', fontsize=14, fontweight='bold')
        
        for bar, rate in zip(bars, churn_by_contract['churn_rate']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'churn_by_contract.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de churn por contrato salvo")
    
    def plot_churn_by_internet(self) -> None:
        """Plota taxa de churn por tipo de internet."""
        
        churn_by_internet = self.analyze_churn_by_category('InternetService')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#3498db', '#e74c3c', '#95a5a6']
        bars = ax.bar(churn_by_internet['InternetService'], churn_by_internet['churn_rate'],
                     color=colors)
        
        ax.set_xlabel('Tipo de Internet')
        ax.set_ylabel('Taxa de Churn (%)')
        ax.set_title('Taxa de Churn por Tipo de Internet', fontsize=14, fontweight='bold')
        
        for bar, rate in zip(bars, churn_by_internet['churn_rate']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'churn_by_internet.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de churn por internet salvo")
    
    def plot_tenure_distribution(self) -> None:
        """Plota distribuição de tenure com relação ao churn."""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        self.df[self.df['Churn'] == 0]['tenure'].hist(bins=30, ax=axes[0], 
                                                       color='#2ecc71', alpha=0.7, label='No Churn')
        self.df[self.df['Churn'] == 1]['tenure'].hist(bins=30, ax=axes[0], 
                                                       color='#e74c3c', alpha=0.7, label='Churn')
        axes[0].set_xlabel('Meses como Cliente')
        axes[0].set_ylabel('Frequência')
        axes[0].set_title('Distribuição de Tenure por Churn', fontsize=14, fontweight='bold')
        axes[0].legend()
        
        tenure_churn = self.df.groupby(pd.cut(self.df['tenure'], bins=6))['Churn'].mean() * 100
        tenure_churn.plot(kind='bar', ax=axes[1], color='#e74c3c')
        axes[1].set_xlabel('Grupo de Tenure (meses)')
        axes[1].set_ylabel('Taxa de Churn (%)')
        axes[1].set_title('Taxa de Churn por Grupo de Tenure', fontsize=14, fontweight='bold')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'tenure_distribution.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de distribuição de tenure salvo")
    
    def plot_churn_by_payment(self) -> None:
        """Plota taxa de churn por método de pagamento."""
        
        churn_by_payment = self.analyze_churn_by_category('PaymentMethod')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
        bars = ax.barh(churn_by_payment['PaymentMethod'], churn_by_payment['churn_rate'],
                      color=colors)
        
        ax.set_xlabel('Taxa de Churn (%)')
        ax.set_ylabel('Método de Pagamento')
        ax.set_title('Taxa de Churn por Método de Pagamento', fontsize=14, fontweight='bold')
        
        for bar, rate in zip(bars, churn_by_payment['churn_rate']):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{rate:.1f}%', va='center', fontweight='bold')
        
        ax.set_xlim(0, max(churn_by_payment['churn_rate']) * 1.15)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'churn_by_payment.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de churn por pagamento salvo")
    
    def plot_correlation_matrix(self) -> None:
        """Plota matriz de correlação."""
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='RdYlGn', center=0, ax=ax, 
                   square=True, linewidths=0.5)
        
        ax.set_title('Matriz de Correlação - Variáveis Numéricas', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'correlation_matrix.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Matriz de correlação salva")
    
    def plot_churn_by_services(self) -> None:
        """Plota taxa de churn por serviços adicionais."""
        
        services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                   'TechSupport', 'StreamingTV', 'StreamingMovies']
        
        service_churn = []
        for service in services:
            if service in self.df.columns:
                churn_rate = self.df[self.df[service] == 'Yes']['Churn'].mean() * 100
                service_churn.append({'Service': service, 'ChurnRate': churn_rate})
        
        service_df = pd.DataFrame(service_churn).sort_values('ChurnRate', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#e74c3c' if x > 30 else '#f39c12' if x > 20 else '#2ecc71' 
                  for x in service_df['ChurnRate']]
        bars = ax.bar(service_df['Service'], service_df['ChurnRate'], color=colors)
        
        ax.set_xlabel('Serviço Adicional')
        ax.set_ylabel('Taxa de Churn (%)')
        ax.set_title('Taxa de Churn por Serviços Adicionais (Clientes com o Serviço)', 
                    fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        for bar, rate in zip(bars, service_df['ChurnRate']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{rate:.1f}%', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'figures' / 'churn_by_services.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Gráfico de churn por serviços salvo")
    
    def generate_summary_report(self) -> str:
        """Gera relatório de insights em texto."""
        
        stats = self.get_basic_statistics()
        
        report = f"""
================================================================================
                    RELATÓRIO DE ANÁLISE EXPLORATÓRIA - CHURN TELECOM
================================================================================

MÉTRICAS GERAIS
---------------
Total de Clientes: {stats['total_customers']:,}
Taxa de Churn: {stats['churn_rate']:.2f}%
Clientes Perdidos: {stats['churn_count']:,}
Receita Total: ${stats['total_revenue']:,.2f}

MÉTRICAS FINANCEIRAS
-------------------
Ticket Médio Mensal: ${stats['avg_monthly_charges']:.2f}
Receita Média por Cliente: ${stats['avg_total_charges']:.2f}
Tempo Médio de Relacionamento: {stats['avg_tenure']:.1f} meses

ANÁLISE POR CONTRATO
--------------------
"""
        
        contract_analysis = self.analyze_churn_by_category('Contract')
        for _, row in contract_analysis.iterrows():
            report += f"  {row['Contract']}: {row['churn_rate']:.1f}% ({row['churned']:.0f}/{row['total']:.0f})\n"
        
        report += "\nANÁLISE POR INTERNET\n--------------------\n"
        internet_analysis = self.analyze_churn_by_category('InternetService')
        for _, row in internet_analysis.iterrows():
            report += f"  {row['InternetService']}: {row['churn_rate']:.1f}%\n"
        
        report += "\nANÁLISE POR PAGAMENTO\n---------------------\n"
        payment_analysis = self.analyze_churn_by_category('PaymentMethod')
        for _, row in payment_analysis.iterrows():
            report += f"  {row['PaymentMethod']}: {row['churn_rate']:.1f}%\n"
        
        report += "\n" + "="*80
        report += "\nPRINCIPAIS INSIGHTS\n"
        report += "="*80
        
        return report
    
    def run_full_eda(self) -> dict:
        """Executa análise EDA completa."""
        
        logger.info("Iniciando análise exploratória completa...")
        
        self.plot_churn_distribution()
        self.plot_churn_by_contract()
        self.plot_churn_by_internet()
        self.plot_tenure_distribution()
        self.plot_churn_by_payment()
        self.plot_correlation_matrix()
        self.plot_churn_by_services()
        
        stats = self.get_basic_statistics()
        report = self.generate_summary_report()
        
        logger.info("Análise EDA concluída")
        
        return {'stats': stats, 'report': report}


def main():
    """Função principal para execução do script."""
    
    df = pd.read_csv('data/processed/telco_churn_cleaned.csv')
    
    analyzer = EDAAnalyzer(df)
    results = analyzer.run_full_eda()
    
    print(results['report'])
    
    return results


if __name__ == "__main__":
    main()