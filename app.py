import streamlit as st
import pandas as pd
from buffett_calculator import get_all_ratios, check_ratio_pass

# Page configuration
st.set_page_config(
    page_title="Warren Buffett Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .ratio-pass {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 10px;
        margin: 10px 0;
    }
    .ratio-fail {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .stock-example {
        background-color: #e7f3ff;
        padding: 8px 12px;
        border-radius: 5px;
        margin: 5px 0;
        cursor: pointer;
        border: 1px solid #b3d9ff;
    }
    .stock-example:hover {
        background-color: #d0e8ff;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📈 Warren Buffett Stock Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Evaluate stocks using Warren Buffett\'s investment criteria</div>', unsafe_allow_html=True)

# Sidebar for stock input
with st.sidebar:
    st.header("🔍 Stock Selection")
    st.markdown("---")
    
    # Feature 1: Help text explaining stock symbols
    with st.expander("❓ What are stock symbols?"):
        st.markdown("""
        **Stock symbols** (or ticker symbols) are unique codes that identify publicly traded companies.
        
        **Examples:**
        - `AAPL` = Apple Inc.
        - `MSFT` = Microsoft Corporation
        - `GOOGL` = Google (Alphabet)
        - `TSLA` = Tesla, Inc.
        
        **How to find a symbol:**
        1. Google: "Company name + stock symbol"
        2. Visit: finance.yahoo.com
        3. Or use the examples below! 👇
        """)
    
    # Main stock input
    stock_symbol = st.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="Enter any publicly traded stock symbol (e.g., AAPL, MSFT, GOOGL, TSLA)",
        placeholder="e.g., AAPL"
    ).upper()
    
    analyze_button = st.button("🚀 Analyze Stock", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    # Feature 2: Quick Select - Popular Stocks
    st.markdown("### 🎯 Quick Select Popular Stocks")
    st.caption("Click any stock to analyze instantly:")
    
    # Dictionary of popular stocks
    popular_stocks = {
        "🍎 Apple": "AAPL",
        "🖥️ Microsoft": "MSFT",
        "🔍 Google": "GOOGL",
        "📦 Amazon": "AMZN",
        "⚡ Tesla": "TSLA",
        "🎬 Netflix": "NFLX",
        "💼 Berkshire Hathaway": "BRK.B",
        "🥤 Coca-Cola": "KO",
        "🏦 JPMorgan": "JPM",
        "💳 Visa": "V"
    }
    
    # Create clickable buttons for each stock
    cols = st.columns(2)
    for idx, (name, symbol) in enumerate(popular_stocks.items()):
        col = cols[idx % 2]
        if col.button(name, key=symbol, use_container_width=True):
            stock_symbol = symbol
            st.rerun()
    
    st.markdown("---")
    
    # Feature 3: Stock Categories
    st.markdown("### 📂 Browse by Category")
    
    stock_categories = {
        "🏢 Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"],
        "🚗 Auto & Transport": ["TSLA", "F", "GM", "UAL", "DAL"],
        "🏦 Finance": ["JPM", "BAC", "GS", "V", "MA", "BRK.B"],
        "🛒 Retail": ["WMT", "TGT", "HD", "COST", "NKE"],
        "🍔 Food & Beverage": ["KO", "PEP", "MCD", "SBUX", "CMG"],
        "💊 Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "LLY"],
        "🎮 Entertainment": ["DIS", "NFLX", "EA", "SONY"],
        "⚡ Energy": ["XOM", "CVX", "COP", "SLB"]
    }
    
    selected_category = st.selectbox(
        "Select a category:",
        options=list(stock_categories.keys()),
        index=0
    )
    
    st.caption(f"Stocks in {selected_category}:")
    category_cols = st.columns(3)
    for idx, symbol in enumerate(stock_categories[selected_category]):
        col = category_cols[idx % 3]
        if col.button(symbol, key=f"cat_{symbol}", use_container_width=True):
            stock_symbol = symbol
            st.rerun()
    
    st.markdown("---")
    
    # Feature 4: Symbol Lookup Helper
    st.markdown("### 🔎 Don't Know the Symbol?")
    company_name = st.text_input(
        "Search by company name:",
        placeholder="e.g., Apple, Microsoft, Tesla",
        help="Type a company name to get suggestions"
    )
    
    if company_name:
        # Simple company name to symbol mapping
        company_to_symbol = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "amazon": "AMZN",
            "tesla": "TSLA",
            "meta": "META",
            "facebook": "META",
            "netflix": "NFLX",
            "nvidia": "NVDA",
            "berkshire": "BRK.B",
            "berkshire hathaway": "BRK.B",
            "coca cola": "KO",
            "coca-cola": "KO",
            "pepsi": "PEP",
            "walmart": "WMT",
            "jpmorgan": "JPM",
            "jp morgan": "JPM",
            "visa": "V",
            "mastercard": "MA",
            "disney": "DIS",
            "mcdonald": "MCD",
            "mcdonalds": "MCD",
            "starbucks": "SBUX",
            "nike": "NKE",
            "johnson": "JNJ",
            "johnson & johnson": "JNJ",
            "pfizer": "PFE",
            "walmart": "WMT",
            "target": "TGT",
            "ford": "F",
            "general motors": "GM",
            "gm": "GM",
            "boeing": "BA",
            "procter": "PG",
            "procter & gamble": "PG"
        }
        
        search_lower = company_name.lower()
        found_symbols = []
        
        for company, symbol in company_to_symbol.items():
            if search_lower in company or company in search_lower:
                found_symbols.append((company.title(), symbol))
        
        if found_symbols:
            st.success(f"Found {len(found_symbols)} match(es):")
            for company, symbol in found_symbols:
                if st.button(f"✅ {company} ({symbol})", key=f"search_{symbol}", use_container_width=True):
                    stock_symbol = symbol
                    st.rerun()
        else:
            st.warning(f"No matches found for '{company_name}'. Try searching online or use examples above.")
            st.caption("💡 Tip: Search '[Company name] stock symbol' on Google")
    
    st.markdown("---")
    
    # About section
    st.markdown("### 📚 About Warren Buffett's Criteria")
    st.info("""
    This tool evaluates stocks using Warren Buffett's 14 key financial ratios:
    
    **Income Statement (8 ratios)**
    - Gross Margin
    - SG&A Expense Margin
    - R&D Expense Margin
    - Depreciation Margin
    - Interest Expense Margin
    - Tax Rate
    - Net Margin
    - EPS Growth
    
    **Balance Sheet (5 ratios)**
    - Cash vs Debt
    - Debt to Equity
    - Preferred Stock
    - Retained Earnings Growth
    - Treasury Stock
    
    **Cash Flow (1 ratio)**
    - CapEx Margin
    """)

# Main content area
if analyze_button or stock_symbol:
    with st.spinner(f"🔄 Analyzing {stock_symbol}..."):
        result = get_all_ratios(stock_symbol)
        
        if result is None:
            st.error(f"❌ Could not fetch data for **{stock_symbol}**. Please check the symbol and try again.")
            
            # Helpful suggestions
            st.markdown("### 💡 Suggestions:")
            col1, col2 = st.columns(2)
            with col1:
                st.info("""
                **Check if the symbol is correct:**
                - Stock symbols are usually 1-5 letters
                - Try searching "[Company name] stock symbol" on Google
                - Visit finance.yahoo.com to verify
                """)
            with col2:
                st.success("""
                **Try these popular stocks:**
                - Tech: AAPL, MSFT, GOOGL, TSLA
                - Finance: JPM, BAC, V, BRK.B
                - Retail: WMT, TGT, NKE, HD
                - Food: KO, PEP, MCD, SBUX
                """)
        else:
            ratios = result['ratios']
            data = result['data']
            
            # Company Information
            st.success(f"✅ Successfully loaded data for **{stock_symbol}**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                try:
                    st.metric("Company", data['info'].get('longName', stock_symbol))
                except:
                    st.metric("Company", stock_symbol)
            with col2:
                try:
                    st.metric("Sector", data['info'].get('sector', 'N/A'))
                except:
                    st.metric("Sector", "N/A")
            with col3:
                try:
                    st.metric("Industry", data['info'].get('industry', 'N/A'))
                except:
                    st.metric("Industry", "N/A")
            with col4:
                try:
                    current_price = data['info'].get('currentPrice', 'N/A')
                    if current_price != 'N/A':
                        st.metric("Current Price", f"${current_price:.2f}")
                    else:
                        st.metric("Current Price", "N/A")
                except:
                    st.metric("Current Price", "N/A")
            
            st.markdown("---")
            
            # Calculate overall score
            passed_count = sum(1 for ratio in ratios.values() if check_ratio_pass(ratio))
            total_count = len(ratios)
            pass_percentage = (passed_count / total_count) * 100 if total_count > 0 else 0
            
            # Overall Investment Score
            st.header("🎯 Buffett Investment Score")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: {'#28a745' if pass_percentage >= 70 else '#ffc107' if pass_percentage >= 50 else '#dc3545'};">
                        {pass_percentage:.1f}%
                    </h2>
                    <p>Overall Score</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #28a745;">{passed_count}</h2>
                    <p>Criteria Passed</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #dc3545;">{total_count - passed_count}</h2>
                    <p>Criteria Failed</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Investment Recommendation
            if pass_percentage >= 80:
                st.success("✅ **Strong Buy**: This stock meets most of Buffett's investment criteria!")
            elif pass_percentage >= 60:
                st.warning("⚠️ **Moderate**: This stock shows potential but has some concerns.")
            else:
                st.error("❌ **Caution**: This stock fails several key Buffett criteria.")
            
            st.markdown("---")
            
            # Tabs for different sections
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Buffett's Ratios", 
                "💰 Income Statement", 
                "🏦 Balance Sheet", 
                "💵 Cash Flow Statement",
                "🤖 Chat (Part 1 Integration)"
            ])
            
            # Tab 1: Buffett's Ratios
            with tab1:
                st.header("Warren Buffett's Key Financial Ratios")
                st.markdown("Each ratio is evaluated against Buffett's investment criteria with pass/fail indicators.")
                
                # Income Statement Ratios
                st.subheader("📄 Income Statement Metrics")
                income_ratios = [
                    'Gross Margin', 'SG&A Expense Margin', 'R&D Expense Margin',
                    'Depreciation Margin', 'Interest Expense Margin', 'Income Tax Rate',
                    'Net Margin', 'EPS Growth'
                ]
                
                for ratio_name in income_ratios:
                    if ratio_name in ratios:
                        ratio = ratios[ratio_name]
                        passed = check_ratio_pass(ratio)
                        
                        status_class = "ratio-pass" if passed else "ratio-fail"
                        status_icon = "✅" if passed else "❌"
                        
                        if ratio['rule'] in ['qualitative', 'qualitative_none', 'qualitative_exists']:
                            value_str = ratio['value']
                        else:
                            value_str = f"{ratio['value']:.2f}%"
                        
                        st.markdown(f"""
                        <div class="{status_class}">
                            <h4>{status_icon} {ratio_name}</h4>
                            <p><strong>Current Value:</strong> {value_str}</p>
                            <p><strong>Buffett's Rule:</strong> {ratio['reference']}</p>
                            <p><strong>Logic:</strong> {ratio['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Balance Sheet Ratios
                st.subheader("🏦 Balance Sheet Metrics")
                balance_ratios = ['Cash > Debt', 'Adjusted Debt to Equity', 'Preferred Stock', 'Retained Earnings Growth', 'Treasury Stock']
                
                for ratio_name in balance_ratios:
                    if ratio_name in ratios:
                        ratio = ratios[ratio_name]
                        passed = check_ratio_pass(ratio)
                        
                        status_class = "ratio-pass" if passed else "ratio-fail"
                        status_icon = "✅" if passed else "❌"
                        
                        if ratio['rule'] in ['qualitative', 'qualitative_none', 'qualitative_exists']:
                            value_str = ratio['value']
                        else:
                            value_str = f"{ratio['value']:.2f}"
                        
                        st.markdown(f"""
                        <div class="{status_class}">
                            <h4>{status_icon} {ratio_name}</h4>
                            <p><strong>Current Value:</strong> {value_str}</p>
                            <p><strong>Buffett's Rule:</strong> {ratio['reference']}</p>
                            <p><strong>Logic:</strong> {ratio['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Cash Flow Ratios
                st.subheader("💵 Cash Flow Metrics")
                cashflow_ratios = ['CapEx Margin']
                
                for ratio_name in cashflow_ratios:
                    if ratio_name in ratios:
                        ratio = ratios[ratio_name]
                        passed = check_ratio_pass(ratio)
                        
                        status_class = "ratio-pass" if passed else "ratio-fail"
                        status_icon = "✅" if passed else "❌"
                        
                        value_str = f"{ratio['value']:.2f}%"
                        
                        st.markdown(f"""
                        <div class="{status_class}">
                            <h4>{status_icon} {ratio_name}</h4>
                            <p><strong>Current Value:</strong> {value_str}</p>
                            <p><strong>Buffett's Rule:</strong> {ratio['reference']}</p>
                            <p><strong>Logic:</strong> {ratio['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Tab 2: Income Statement
            with tab2:
                st.header("Income Statement")
                st.markdown(f"*Most recent fiscal period for {stock_symbol}*")
                
                # Display the full income statement
                financials_df = data['financials']
                st.dataframe(financials_df, use_container_width=True)
                
                # Download option
                csv = financials_df.to_csv()
                st.download_button(
                    label="📥 Download Income Statement (CSV)",
                    data=csv,
                    file_name=f"{stock_symbol}_income_statement.csv",
                    mime="text/csv"
                )
            
            # Tab 3: Balance Sheet
            with tab3:
                st.header("Balance Sheet")
                st.markdown(f"*Most recent fiscal period for {stock_symbol}*")
                
                # Display the full balance sheet
                balance_sheet_df = data['balance_sheet']
                st.dataframe(balance_sheet_df, use_container_width=True)
                
                # Download option
                csv = balance_sheet_df.to_csv()
                st.download_button(
                    label="📥 Download Balance Sheet (CSV)",
                    data=csv,
                    file_name=f"{stock_symbol}_balance_sheet.csv",
                    mime="text/csv"
                )
            
            # Tab 4: Cash Flow Statement
            with tab4:
                st.header("Cash Flow Statement")
                st.markdown(f"*Most recent fiscal period for {stock_symbol}*")
                
                # Display the full cash flow statement
                cashflow_df = data['cashflow']
                st.dataframe(cashflow_df, use_container_width=True)
                
                # Download option
                csv = cashflow_df.to_csv()
                st.download_button(
                    label="📥 Download Cash Flow Statement (CSV)",
                    data=csv,
                    file_name=f"{stock_symbol}_cashflow.csv",
                    mime="text/csv"
                )
            
            # Tab 5: Chat Integration (Part 1)
            with tab5:
                st.header("🤖 AI Investment Advisor Chatbot")
                st.info(f"""
                **🔌 Integration Point for Part 1 (Person A's Chatbot)**
                
                This section is reserved for the AI chatbot that will provide investment insights and answer questions.
                
                **Data Available for Chatbot:**
                - Stock Symbol: `{stock_symbol}`
                - All Financial Ratios: Accessible via `ratios` dictionary
                - Financial Statements: Income, Balance Sheet, Cash Flow
                - Company Information: Sector, Industry, Price
                - Investment Score: Pass/Fail criteria
                
                **Example Integration:**
```python
                # Person A can access all this data:
                current_stock = "{stock_symbol}"
                current_ratios = ratios
                investment_score = {pass_percentage:.1f}
                
                # Pass to chatbot:
                chatbot_response = chat_model.generate(
                    user_query="Is {stock_symbol} a good investment?",
                    context={{
                        'symbol': current_stock,
                        'ratios': current_ratios,
                        'score': investment_score
                    }}
                )
```
                """)
                
                st.markdown("---")
                
                # Placeholder chatbot interface
                st.markdown("### 💬 Chat Interface (Coming Soon)")
                user_question = st.text_input(
                    "Ask a question about this stock:",
                    placeholder=f"e.g., Should I invest in {stock_symbol}?"
                )
                
                if st.button("Send"):
                    st.warning("🚧 Chatbot integration pending from Person A (Part 1)")
                    st.markdown(f"""
                    **When integrated, the chatbot will be able to answer:**
                    - "Is {stock_symbol} a good investment based on Buffett's criteria?"
                    - "What are the strengths and weaknesses of {stock_symbol}?"
                    - "How does {stock_symbol} compare to industry standards?"
                    - "What risks should I be aware of with {stock_symbol}?"
                    
                    **Context available to chatbot:**
                    - Investment Score: {pass_percentage:.1f}%
                    - Passed Criteria: {passed_count}/{total_count}
                    - All financial ratios and their pass/fail status
                    """)

else:
    # Welcome screen
    st.info("👈 Enter a stock symbol in the sidebar and click 'Analyze Stock' to get started!")
    st.markdown("**Or use the Quick Select buttons in the sidebar to try popular stocks!**")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 What This Tool Does")
        st.markdown("""
        This Warren Buffett Stock Analyzer evaluates any publicly traded stock using the legendary investor's proven criteria:
        
        1. **Fetches Real Financial Data** - Gets the latest financial statements
        2. **Calculates 14 Key Ratios** - Uses Buffett's exact formulas
        3. **Pass/Fail Evaluation** - Clear indicators for each criterion
        4. **Investment Score** - Overall rating based on all criteria
        5. **Detailed Explanations** - Understand why each ratio matters
        """)
    
    with col2:
        st.subheader("🎯 Warren Buffett's Investment Philosophy")
        st.markdown("""
        Warren Buffett looks for companies with:
        
        - **Strong Economic Moat** - Durable competitive advantages
        - **High Profit Margins** - Efficient operations (20%+ net margin)
        - **Low Debt** - Financial stability and flexibility
        - **Consistent Growth** - Increasing earnings year over year
        - **Capital Efficiency** - Low capital expenditure needs
        - **Shareholder Returns** - Growing retained earnings and buybacks
        """)
    
    st.markdown("---")
    
    st.subheader("💡 Popular Stocks to Try")
    example_col1, example_col2, example_col3, example_col4 = st.columns(4)
    
    with example_col1:
        st.code("AAPL", language="text")
        st.caption("Apple Inc.")
    with example_col2:
        st.code("MSFT", language="text")
        st.caption("Microsoft")
    with example_col3:
        st.code("GOOGL", language="text")
        st.caption("Alphabet (Google)")
    with example_col4:
        st.code("BRK.B", language="text")
        st.caption("Berkshire Hathaway")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. Not financial advice. 
    Always do your own research and consult with a financial advisor before making investment decisions.</p>
    <p>Built with ❤️ using Streamlit and yfinance | Data from Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)