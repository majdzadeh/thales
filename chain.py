import streamlit as st
from pandas_datareader.yahoo.options import Options

ATTRS = ('Last', 'Bid', 'Ask', 'Chg', 'PctChg', 'Vol' ,'Open_Int', 'IV', 'Underlying_Price', 'Quote_Time', 'Last_Trade_Date', )
OPS = ['call', 'put']

def fetch_chain(ticker: str):
    if ticker is None or ticker == '':
        st.error('Symbol not provided')
        return

    for k in OPS:
        if k in st.session_state:
            st.session_state.pop(k)

    full_chain = Options(ticker)
    full_chain.headers = {'User-Agent': 'Firefox'}
    try:
        st.session_state['all_data'] = full_chain.get_all_data()
    except:
        st.error(f'Error fetching data from Yahoo')
        return
    else:
        st.session_state['expiry_dates'] = full_chain.expiry_dates

def refresh():
    if 'expiry_date' in st.session_state:
        for op in OPS:
            st.session_state[op] = st.session_state['all_data'].loc[:, st.session_state['expiry_date'], op, :].loc[:, ATTRS]

def main():
    st.title('Thales - Stock Options chain')

    with open('README.md', 'r') as readme:
        st.sidebar.markdown(readme.read())

    ticker = st.text_input('Ticker', 
                           help='Stock symbol')

    clicked = st.button('Submit', 
                        on_click=fetch_chain,
                        args=(ticker,),
                        help='Fetch Options chain')

    if 'expiry_dates' in st.session_state: 
        expiry = st.selectbox(label='Expiry date',
                              key='expiry_date',
                              options=[exp.isoformat() for exp in st.session_state['expiry_dates']],
                              on_change=refresh,
                              help='Select contract expiry date')
        
        for op in OPS:
            with st.expander('{}s'.format(op.upper()), expanded=True):
                if op not in st.session_state:
                    refresh()

                st.dataframe(st.session_state[op])

if __name__ == '__main__':
    st.set_page_config(page_title='Thales - Stock Options chain',
                       initial_sidebar_state='expanded',
                       menu_items={
                                   'Get Help': 'https://www.thales-mfi.ir/', 
                                   'Report a bug': 'https://www.thales-mfi.ir/', 
                                   'About': 'Thales - Stock Options chain'},
                       layout='wide')
    main()
