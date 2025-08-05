#!/usr/bin/env python3
"""
Villa Los Jardines Property Data Analysis

This script analyzes the scraped property data from Villa Los Jardines,
creates a unit price feature (price/square_meters), and visualizes the distribution
with percentile regions highlighted.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VillaJardinesAnalyzer:
    """Analyzer for Villa Los Jardines property data."""
    
    def __init__(self, csv_file):
        """Initialize the analyzer with the CSV file."""
        self.csv_file = csv_file
        self.df = None
        self.unit_price_stats = {}
        
    def load_data(self):
        """Load and prepare the data."""
        print("Loading Villa Los Jardines property data...")
        
        # Load the CSV file
        self.df = pd.read_csv(self.csv_file)
        
        # Display basic info
        print(f"Dataset shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print(f"Data types:\n{self.df.dtypes}")
        
        # Show first few rows
        print("\nFirst 5 rows:")
        print(self.df.head())
        
        return self.df
    
    def create_unit_price_feature(self):
        """Create the unit_price feature (price per square meter)."""
        print("\n" + "="*50)
        print("CREATING UNIT PRICE FEATURE")
        print("="*50)
        
        # Calculate unit price (price per square meter)
        self.df['unit_price'] = self.df['price'] / self.df['square_meters']
        
        # Convert to thousands of CLP per m² for easier reading
        self.df['unit_price_k_clp_m2'] = self.df['unit_price'] / 1000
        
        # Calculate statistics
        self.unit_price_stats = {
            'mean': self.df['unit_price_k_clp_m2'].mean(),
            'median': self.df['unit_price_k_clp_m2'].median(),
            'std': self.df['unit_price_k_clp_m2'].std(),
            'min': self.df['unit_price_k_clp_m2'].min(),
            'max': self.df['unit_price_k_clp_m2'].max(),
            'q10': self.df['unit_price_k_clp_m2'].quantile(0.10),
            'q25': self.df['unit_price_k_clp_m2'].quantile(0.25),
            'q75': self.df['unit_price_k_clp_m2'].quantile(0.75),
            'q90': self.df['unit_price_k_clp_m2'].quantile(0.90)
        }
        
        print("Unit Price Statistics (thousands of CLP per m²):")
        for stat, value in self.unit_price_stats.items():
            print(f"  {stat.upper()}: {value:.2f}")
        
        print(f"\nUnit price range: {self.unit_price_stats['min']:.2f} - {self.unit_price_stats['max']:.2f} k CLP/m²")
        print(f"Average unit price: {self.unit_price_stats['mean']:.2f} k CLP/m²")
        
        return self.df
    
    def show_unit_price_distribution(self):
        """Display the distribution of unit prices."""
        print("\n" + "="*50)
        print("UNIT PRICE DISTRIBUTION ANALYSIS")
        print("="*50)
        
        # Basic statistics
        print("Distribution Statistics:")
        print(f"  Skewness: {stats.skew(self.df['unit_price_k_clp_m2']):.3f}")
        print(f"  Kurtosis: {stats.kurtosis(self.df['unit_price_k_clp_m2']):.3f}")
        
        # Percentile information
        print(f"\nPercentile Information:")
        print(f"  10th percentile: {self.unit_price_stats['q10']:.2f} k CLP/m²")
        print(f"  25th percentile: {self.unit_price_stats['q25']:.2f} k CLP/m²")
        print(f"  50th percentile (median): {self.unit_price_stats['median']:.2f} k CLP/m²")
        print(f"  75th percentile: {self.unit_price_stats['q75']:.2f} k CLP/m²")
        print(f"  90th percentile: {self.unit_price_stats['q90']:.2f} k CLP/m²")
        
        # Properties in extreme percentiles
        low_percentile = self.df[self.df['unit_price_k_clp_m2'] <= self.unit_price_stats['q10']]
        high_percentile = self.df[self.df['unit_price_k_clp_m2'] >= self.unit_price_stats['q90']]
        
        print(f"\nProperties in bottom 10% (≤{self.unit_price_stats['q10']:.2f} k CLP/m²): {len(low_percentile)}")
        print(f"Properties in top 10% (≥{self.unit_price_stats['q90']:.2f} k CLP/m²): {len(high_percentile)}")
        
        return low_percentile, high_percentile
    
    def plot_unit_price_distribution(self):
        """Create comprehensive plots of the unit price distribution."""
        print("\n" + "="*50)
        print("CREATING UNIT PRICE DISTRIBUTION PLOTS")
        print("="*50)
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Villa Los Jardines - Unit Price Distribution Analysis', fontsize=16, fontweight='bold')
        
        # 1. Histogram with percentile regions
        ax1 = axes[0, 0]
        self._plot_histogram_with_percentiles(ax1)
        
        # 2. Box plot
        ax2 = axes[0, 1]
        self._plot_boxplot(ax2)
        
        # 3. Density plot with percentile regions
        ax3 = axes[1, 0]
        self._plot_density_with_percentiles(ax3)
        
        # 4. Q-Q plot for normality check
        ax4 = axes[1, 1]
        self._plot_qq_plot(ax4)
        
        plt.tight_layout()
        plt.savefig('villa_jardines_unit_price_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create additional detailed plot
        self._create_detailed_distribution_plot()
    
    def _plot_histogram_with_percentiles(self, ax):
        """Plot histogram with percentile regions highlighted."""
        # Create histogram
        n, bins, patches = ax.hist(self.df['unit_price_k_clp_m2'], bins=30, alpha=0.7, 
                                 color='lightblue', edgecolor='black', density=True)
        
        # Highlight regions under 10th and over 90th percentile
        for i, (patch, bin_edge) in enumerate(zip(patches, bins)):
            if bin_edge <= self.unit_price_stats['q10'] or bin_edge >= self.unit_price_stats['q90']:
                patch.set_facecolor('blue')
                patch.set_alpha(0.8)
        
        # Add vertical lines for percentiles
        ax.axvline(self.unit_price_stats['q10'], color='red', linestyle='--', linewidth=2, 
                  label=f'10th percentile ({self.unit_price_stats["q10"]:.1f})')
        ax.axvline(self.unit_price_stats['median'], color='green', linestyle='--', linewidth=2, 
                  label=f'Median ({self.unit_price_stats["median"]:.1f})')
        ax.axvline(self.unit_price_stats['q90'], color='red', linestyle='--', linewidth=2, 
                  label=f'90th percentile ({self.unit_price_stats["q90"]:.1f})')
        
        ax.set_xlabel('Unit Price (k CLP/m²)')
        ax.set_ylabel('Density')
        ax.set_title('Unit Price Distribution with Percentile Regions')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_boxplot(self, ax):
        """Plot box plot of unit prices."""
        box_plot = ax.boxplot(self.df['unit_price_k_clp_m2'], patch_artist=True)
        box_plot['boxes'][0].set_facecolor('lightblue')
        box_plot['medians'][0].set_color('red')
        box_plot['medians'][0].set_linewidth(2)
        
        ax.set_ylabel('Unit Price (k CLP/m²)')
        ax.set_title('Unit Price Box Plot')
        ax.grid(True, alpha=0.3)
        
        # Add statistics as text
        stats_text = f'Mean: {self.unit_price_stats["mean"]:.1f}\n'
        stats_text += f'Median: {self.unit_price_stats["median"]:.1f}\n'
        stats_text += f'Std: {self.unit_price_stats["std"]:.1f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def _plot_density_with_percentiles(self, ax):
        """Plot density plot with percentile regions."""
        # Create density plot
        sns.kdeplot(data=self.df['unit_price_k_clp_m2'], ax=ax, color='blue', linewidth=2)
        
        # Shade regions under 10th and over 90th percentile
        x = np.linspace(self.df['unit_price_k_clp_m2'].min(), self.df['unit_price_k_clp_m2'].max(), 1000)
        y = stats.gaussian_kde(self.df['unit_price_k_clp_m2'])(x)
        
        # Shade bottom 10%
        mask_low = x <= self.unit_price_stats['q10']
        ax.fill_between(x[mask_low], y[mask_low], alpha=0.3, color='blue', label='Bottom 10%')
        
        # Shade top 10%
        mask_high = x >= self.unit_price_stats['q90']
        ax.fill_between(x[mask_high], y[mask_high], alpha=0.3, color='blue', label='Top 10%')
        
        # Add vertical lines
        ax.axvline(self.unit_price_stats['q10'], color='red', linestyle='--', linewidth=2)
        ax.axvline(self.unit_price_stats['q90'], color='red', linestyle='--', linewidth=2)
        
        ax.set_xlabel('Unit Price (k CLP/m²)')
        ax.set_ylabel('Density')
        ax.set_title('Unit Price Density with Percentile Regions')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_qq_plot(self, ax):
        """Plot Q-Q plot to check normality."""
        stats.probplot(self.df['unit_price_k_clp_m2'], dist="norm", plot=ax)
        ax.set_title('Q-Q Plot (Normality Check)')
        ax.grid(True, alpha=0.3)
    
    def _create_detailed_distribution_plot(self):
        """Create a detailed single plot focusing on the distribution."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create histogram with density overlay
        ax.hist(self.df['unit_price_k_clp_m2'], bins=25, alpha=0.6, color='lightblue', 
               edgecolor='black', density=True, label='Histogram')
        
        # Add density curve
        sns.kdeplot(data=self.df['unit_price_k_clp_m2'], ax=ax, color='red', linewidth=2, label='Density')
        
        # Shade extreme percentile regions in blue
        x = np.linspace(self.df['unit_price_k_clp_m2'].min(), self.df['unit_price_k_clp_m2'].max(), 1000)
        y = stats.gaussian_kde(self.df['unit_price_k_clp_m2'])(x)
        
        # Shade bottom 10%
        mask_low = x <= self.unit_price_stats['q10']
        ax.fill_between(x[mask_low], y[mask_low], alpha=0.4, color='blue', label='Bottom 10%')
        
        # Shade top 10%
        mask_high = x >= self.unit_price_stats['q90']
        ax.fill_between(x[mask_high], y[mask_high], alpha=0.4, color='blue', label='Top 10%')
        
        # Add vertical lines for key percentiles
        ax.axvline(self.unit_price_stats['q10'], color='darkblue', linestyle='--', linewidth=2, 
                  label=f'10th percentile ({self.unit_price_stats["q10"]:.1f})')
        ax.axvline(self.unit_price_stats['median'], color='green', linestyle='-', linewidth=2, 
                  label=f'Median ({self.unit_price_stats["median"]:.1f})')
        ax.axvline(self.unit_price_stats['q90'], color='darkblue', linestyle='--', linewidth=2, 
                  label=f'90th percentile ({self.unit_price_stats["q90"]:.1f})')
        
        ax.set_xlabel('Unit Price (k CLP/m²)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title('Villa Los Jardines - Unit Price Distribution\n(Blue regions: Bottom 10% and Top 10%)', 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add statistics text box
        stats_text = f'Mean: {self.unit_price_stats["mean"]:.1f} k CLP/m²\n'
        stats_text += f'Median: {self.unit_price_stats["median"]:.1f} k CLP/m²\n'
        stats_text += f'Std Dev: {self.unit_price_stats["std"]:.1f} k CLP/m²\n'
        stats_text += f'Range: {self.unit_price_stats["min"]:.1f} - {self.unit_price_stats["max"]:.1f} k CLP/m²'
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9), fontsize=10)
        
        plt.tight_layout()
        plt.savefig('villa_jardines_unit_price_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def show_extreme_properties(self, low_percentile, high_percentile):
        """Display properties in extreme percentiles."""
        print("\n" + "="*50)
        print("PROPERTIES IN EXTREME PERCENTILES")
        print("="*50)
        
        print("\nLOWEST UNIT PRICE PROPERTIES (Bottom 10%):")
        print(low_percentile[['title', 'price', 'square_meters', 'unit_price_k_clp_m2']].to_string(index=False))
        
        print("\n\nHIGHEST UNIT PRICE PROPERTIES (Top 10%):")
        print(high_percentile[['title', 'price', 'square_meters', 'unit_price_k_clp_m2']].to_string(index=False))
    
    def save_enhanced_data(self):
        """Save the enhanced dataset with unit price features."""
        output_file = 'villa_jardines_enhanced_data.csv'
        self.df.to_csv(output_file, index=False)
        print(f"\nEnhanced dataset saved to: {output_file}")
        return output_file
    
    def run_analysis(self):
        """Run the complete analysis."""
        print("VILLA LOS JARDINES PROPERTY DATA ANALYSIS")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Create unit price feature
        self.create_unit_price_feature()
        
        # Show distribution
        low_percentile, high_percentile = self.show_unit_price_distribution()
        
        # Create plots
        self.plot_unit_price_distribution()
        
        # Show extreme properties
        self.show_extreme_properties(low_percentile, high_percentile)
        
        # Save enhanced data
        self.save_enhanced_data()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)


def main():
    """Main function to run the analysis."""
    # File path
    csv_file = 'villa_jardines_properties_20250805_125939.csv'
    
    # Create analyzer and run analysis
    analyzer = VillaJardinesAnalyzer(csv_file)
    analyzer.run_analysis()


if __name__ == "__main__":
    main() 