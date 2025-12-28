import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(symbol):
    """Fetch financial data for any stock symbol"""
    try:
        stock = yf.Ticker(symbol)
        return {
            'ticker': stock,
            'info': stock.info,
            'financials': stock.financials,
            'balance_sheet': stock.balancesheet,
            'cashflow': stock.cashflow
        }
    except Exception as e:
        return None

def calculate_income_statement_ratios(financials):
    """Calculate all 8 income statement ratios from your notebook"""
    try:
        ratios = {}
        
        # 1. Gross Margin
        try:
            ratios['Gross Margin'] = {
                'value': (financials.loc['Gross Profit'].iloc[0] / 
                         financials.loc['Total Revenue'].iloc[0]) * 100,
                'reference': '≥ 40%',
                'threshold': 40,
                'rule': 'higher',
                'description': "Signals the company isn't competing on price. High gross margins indicate pricing power and competitive advantage."
            }
        except Exception as e:
            print(f"Could not calculate Gross Margin: {e}")
        
        # 2. SG&A Expense Margin
        try:
            ratios['SG&A Expense Margin'] = {
                'value': (financials.loc['Selling General And Administration'].iloc[0] / 
                         financials.loc['Gross Profit'].iloc[0]) * 100,
                'reference': '≤ 30%',
                'threshold': 30,
                'rule': 'lower',
                'description': "Wide-moat companies don't need to spend a lot on overhead to operate. Low SG&A indicates operational efficiency."
            }
        except Exception as e:
            print(f"Could not calculate SG&A Expense Margin: {e}")
        
        # 3. R&D Expense Margin
        try:
            ratios['R&D Expense Margin'] = {
                'value': (financials.loc['Research And Development'].iloc[0] / 
                         financials.loc['Gross Profit'].iloc[0]) * 100,
                'reference': '≤ 30%',
                'threshold': 30,
                'rule': 'lower',
                'description': "R&D expenses don't always create value for shareholders. Buffett prefers businesses with sustainable advantages."
            }
        except Exception as e:
            print(f"Could not calculate R&D Expense Margin: {e}")
        
        # 4. Depreciation Margin
        try:
            ratios['Depreciation Margin'] = {
                'value': (financials.loc['Reconciled Depreciation'].iloc[0] / 
                         financials.loc['Gross Profit'].iloc[0]) * 100,
                'reference': '≤ 10%',
                'threshold': 10,
                'rule': 'lower',
                'description': "Buffett doesn't like businesses that need to invest in depreciating assets to maintain their competitive advantage."
            }
        except Exception as e:
            print(f"Could not calculate Depreciation Margin: {e}")
        
        # 5. Interest Expense Margin - FIXED VERSION
        try:
            # Try multiple field names for interest expense
            interest_expense = None
            possible_fields = [
                'Interest Expense',
                'Interest Expense Non Operating',
                'Net Non Operating Interest Income Expense'
            ]
            
            for field in possible_fields:
                if field in financials.index:
                    value = financials.loc[field].iloc[0]
                    # Take absolute value and ensure it's positive
                    if pd.notna(value) and value != 0:
                        interest_expense = abs(value)
                        break
            
            if interest_expense and interest_expense > 0:
                operating_income = financials.loc['Operating Income'].iloc[0]
                if operating_income > 0:
                    ratios['Interest Expense Margin'] = {
                        'value': (interest_expense / operating_income) * 100,
                        'reference': '≤ 15%',
                        'threshold': 15,
                        'rule': 'lower',
                        'description': "Great businesses don't need debt to finance themselves. Low interest expense indicates financial strength."
                    }
        except Exception as e:
            print(f"Could not calculate Interest Expense Margin: {e}")
        
        # 6. Income Tax Rate
        try:
            ratios['Income Tax Rate'] = {
                'value': (financials.loc['Tax Provision'].iloc[0] / 
                         financials.loc['Pretax Income'].iloc[0]) * 100,
                'reference': 'At corporate rate (~21%)',
                'threshold': 21,
                'rule': 'near',
                'description': "Great businesses are so profitable that they are forced to pay their full tax load."
            }
        except Exception as e:
            print(f"Could not calculate Income Tax Rate: {e}")
        
        # 7. Net Margin
        try:
            ratios['Net Margin'] = {
                'value': (financials.loc['Net Income'].iloc[0] / 
                         financials.loc['Total Revenue'].iloc[0]) * 100,
                'reference': '≥ 20%',
                'threshold': 20,
                'rule': 'higher',
                'description': "Great companies convert 20% or more of their revenue into net income, indicating strong profitability."
            }
        except Exception as e:
            print(f"Could not calculate Net Margin: {e}")
        
        # 8. EPS Growth
        try:
            current_eps = financials.loc['Basic EPS'].iloc[0]
            prior_eps = financials.loc['Basic EPS'].iloc[1]
            if prior_eps != 0:
                ratios['EPS Growth'] = {
                    'value': ((current_eps / prior_eps) - 1) * 100,
                    'reference': 'Positive & Growing',
                    'threshold': 0,
                    'rule': 'higher',
                    'description': "Great companies increase profits every year. Consistent EPS growth shows business quality."
                }
        except Exception as e:
            print(f"Could not calculate EPS Growth: {e}")
        
        return ratios
    except Exception as e:
        print(f"Error calculating income statement ratios: {e}")
        return {}

def calculate_balance_sheet_ratios(balance_sheet):
    """Calculate all 5 balance sheet ratios from your notebook"""
    try:
        ratios = {}
        
        # 1. Cash > Debt
        try:
            cash = balance_sheet.loc['Cash And Cash Equivalents'].iloc[0]
            current_debt = balance_sheet.loc['Current Debt'].iloc[0]
            if current_debt > 0:
                ratios['Cash > Debt'] = {
                    'value': cash / current_debt,
                    'reference': '> 1.0 (More cash than debt)',
                    'threshold': 1.0,
                    'rule': 'higher',
                    'description': "Great companies generate lots of cash without needing much debt. Cash exceeding debt provides financial flexibility."
                }
        except Exception as e:
            print(f"Could not calculate Cash > Debt: {e}")
        
        # 2. Adjusted Debt to Equity
        try:
            total_debt = balance_sheet.loc['Total Debt'].iloc[0]
            total_assets = balance_sheet.loc['Total Assets'].iloc[0]
            equity = total_assets - total_debt
            if equity > 0:
                ratios['Adjusted Debt to Equity'] = {
                    'value': total_debt / equity,
                    'reference': '< 0.80',
                    'threshold': 0.80,
                    'rule': 'lower',
                    'description': "Great companies finance themselves with equity rather than debt. Low leverage indicates financial stability."
                }
        except Exception as e:
            print(f"Could not calculate Adjusted Debt to Equity: {e}")
        
        # 3. Preferred Stock (NEW)
        try:
            has_preferred = False
            if 'Preferred Stock' in balance_sheet.index:
                preferred_value = balance_sheet.loc['Preferred Stock'].iloc[0]
                if pd.notna(preferred_value) and preferred_value != 0:
                    has_preferred = True
            
            ratios['Preferred Stock'] = {
                'value': 'Exists' if has_preferred else 'None',
                'reference': 'None',
                'threshold': None,
                'rule': 'qualitative_none',
                'description': "Great companies don't need to fund themselves with preferred stock. Absence of preferred stock indicates strong equity position."
            }
        except Exception as e:
            print(f"Could not calculate Preferred Stock: {e}")
        
        # 4. Retained Earnings Growth
        try:
            current_re = balance_sheet.loc['Retained Earnings'].iloc[0]
            prior_re = balance_sheet.loc['Retained Earnings'].iloc[1]
            
            ratios['Retained Earnings Growth'] = {
                'value': 'Growing' if current_re > prior_re else 'Declining',
                'reference': 'Consistent Growth',
                'threshold': None,
                'rule': 'qualitative',
                'description': "Great companies grow retained earnings each year, showing they reinvest profits successfully."
            }
        except Exception as e:
            print(f"Could not calculate Retained Earnings Growth: {e}")
        
        # 5. Treasury Stock (NEW)
        try:
            has_treasury = False
            # Look for treasury stock indicators
            possible_fields = ['Treasury Stock', 'Treasury Shares Number', 'Common Stock']
            
            for field in possible_fields:
                if field in balance_sheet.index:
                    treasury_value = balance_sheet.loc[field].iloc[0]
                    if pd.notna(treasury_value):
                        if field == 'Treasury Stock' and treasury_value < 0:
                            # Treasury stock is typically negative
                            has_treasury = True
                            break
                        elif field == 'Treasury Shares Number' and treasury_value > 0:
                            has_treasury = True
                            break
            
            # Alternative: Check if shares outstanding is decreasing (buybacks)
            if not has_treasury and 'Ordinary Shares Number' in balance_sheet.index:
                try:
                    current_shares = balance_sheet.loc['Ordinary Shares Number'].iloc[0]
                    prior_shares = balance_sheet.loc['Ordinary Shares Number'].iloc[1]
                    if current_shares < prior_shares:
                        has_treasury = True
                except:
                    pass
            
            ratios['Treasury Stock'] = {
                'value': 'Exists' if has_treasury else 'None',
                'reference': 'Exists (Share buybacks)',
                'threshold': None,
                'rule': 'qualitative_exists',
                'description': "Great companies repurchase their stock, showing confidence in their business and commitment to shareholder returns."
            }
        except Exception as e:
            print(f"Could not calculate Treasury Stock: {e}")
        
        return ratios
    except Exception as e:
        print(f"Error calculating balance sheet ratios: {e}")
        return {}

def calculate_cashflow_ratios(cashflow, financials):
    """Calculate cash flow ratios from your notebook"""
    try:
        ratios = {}
        
        # CapEx Margin
        try:
            capex = abs(cashflow.loc['Capital Expenditure'].iloc[0])
            net_income = financials.loc['Net Income'].iloc[0]
            if net_income > 0:
                ratios['CapEx Margin'] = {
                    'value': (capex / net_income) * 100,
                    'reference': '< 25%',
                    'threshold': 25,
                    'rule': 'lower',
                    'description': "Great companies don't need much equipment to generate profits. Low CapEx means capital-light business model."
                }
        except Exception as e:
            print(f"Could not calculate CapEx Margin: {e}")
        
        return ratios
    except Exception as e:
        print(f"Error calculating cashflow ratios: {e}")
        return {}

def check_ratio_pass(ratio):
    """Check if ratio passes Buffett's criteria"""
    if ratio['rule'] == 'qualitative':
        return ratio['value'] == 'Growing'
    elif ratio['rule'] == 'qualitative_none':
        return ratio['value'] == 'None'
    elif ratio['rule'] == 'qualitative_exists':
        return ratio['value'] == 'Exists'
    elif ratio['rule'] == 'higher':
        return ratio['value'] >= ratio['threshold']
    elif ratio['rule'] == 'lower':
        return ratio['value'] <= ratio['threshold']
    elif ratio['rule'] == 'near':
        return abs(ratio['value'] - ratio['threshold']) <= 5
    return False

def get_all_ratios(symbol):
    """Main function to get all ratios for a stock"""
    data = fetch_stock_data(symbol)
    if not data:
        return None
    
    all_ratios = {}
    
    # Income Statement Ratios (8 ratios)
    income_ratios = calculate_income_statement_ratios(data['financials'])
    all_ratios.update(income_ratios)
    
    # Balance Sheet Ratios (5 ratios)
    balance_ratios = calculate_balance_sheet_ratios(data['balance_sheet'])
    all_ratios.update(balance_ratios)
    
    # Cash Flow Ratios (1 ratio)
    cashflow_ratios = calculate_cashflow_ratios(data['cashflow'], data['financials'])
    all_ratios.update(cashflow_ratios)
    
    return {
        'ratios': all_ratios,
        'data': data
    }