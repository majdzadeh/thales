import streamlit as st
from pandas_datareader.yahoo.options import Options

import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import pandas as pd

YAHOO_ATTRS = ('Last', 'Bid', 'Ask', 'Chg', 'PctChg', 'Vol' ,'Open_Int', 'IV', 'Underlying_Price', 'Quote_Time', 'Last_Trade_Date', )
OPS = ['call', 'put']

intrinio.ApiClient().configuration.api_key['api_key'] = 'OjFkOWRlYmVhYjU1ZGIyNmI4ZmM4NzFkZWVmMThhYzQ2'
intrinio.ApiClient().allow_retries(True)
intrinio_options = intrinio.OptionsApi()

@st.cache
def fetch_tickers():
    response = intrinio_options.get_all_options_tickers()
    return response.tickers

def fetch_chain(ticker: str, provider: str):
    if ticker is None or ticker == '':
        st.error('Symbol not provided')
        return

    for k in OPS:
        if k in st.session_state:
            st.session_state.pop(k)

    if provider.lower() == 'yahoo':
        full_chain = Options(ticker)
        full_chain.headers = {'User-Agent': 'Firefox'}
        try:
            st.session_state['all_data'] = full_chain.get_all_data()
        except:
            st.error(f'Error fetching data from Yahoo')
            return
        else:
            st.session_state['expiry_dates'] = full_chain.expiry_dates

    elif provider.lower() == 'intrinio':
        response = intrinio_options.get_options_expirations(ticker) 
        st.session_state['expiry_dates'] = response.expirations 

def refresh(ticker: str, provider: str):
    if 'expiry_date' in st.session_state:
        if provider.lower() == 'yahoo':
            for op in OPS:
                st.session_state[op] = st.session_state['all_data'].loc[:, st.session_state['expiry_date'], op, :].loc[:, YAHOO_ATTRS]
        elif provider.lower() == 'intrinio':
            response = intrinio_options.get_options_chain(ticker, st.session_state['expiry_date'])
            res = dict()
            res['call'] = [] 
            res['put'] = [] 
            for chain in response.chain:
                for op in OPS:
                    if chain.option.type.lower() == op: 
                        contract = dict()
                        contract['strike'] = chain.option.strike
                        contract['code'] = chain.option.code
                        contract.update(chain.price.to_dict())
                        res[op].append(contract)

            for op in OPS:
                st.session_state[op] = pd.DataFrame.from_dict(res[op])

def main():
    st.title('Thales - Stock Options chain')

    with open('README.md', 'r') as readme:
        st.sidebar.markdown(readme.read())

    ticker = st.selectbox(label='Ticker',
                          options=fetch_tickers())

    provider = st.selectbox(label='Provider', 
                            options=('Yahoo', 'Intrinio'))

    clicked = st.button('Submit', 
                        on_click=fetch_chain,
                        args=(ticker, provider,),
                        help='Fetch Options chain')

    if 'expiry_dates' in st.session_state: 
        expiry = st.selectbox(label='Expiry date',
                              key='expiry_date',
                              options=([exp.isoformat() for exp in st.session_state['expiry_dates']] if provider.lower() == 'yahoo' else st.session_state['expiry_dates']),
                              on_change=refresh,
                              args=(ticker, provider,),
                              help='Select contract expiry date')
        
        for op in OPS:
            with st.expander('{}s'.format(op.upper()), expanded=True):
                if op not in st.session_state:
                    refresh(ticker, provider)

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
