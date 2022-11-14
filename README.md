## What is this?

This tool provides stock Options chain data using Yahoo Finance free Options data API service.

## How to

1. Enter stock ticker in ``Ticker``
2. Hit ``Submit``
3. Select an expiry date from the ``Expiry date`` list
4. Call and Put Options will be displayed for the given ticker and expiry date

## Dependencies

The following dependencies should be installed before running the script:

1. [pandas-datareader](https://pandas-datareader.readthedocs.io/en/latest/#)

2. [streamlit](https://streamlit.io/)

3. [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

## Execution

Run the following command to execute the script:

```bash
$ streamlit run chain.py --server.address 127.0.0.1
```

If you are using a graphical operating environment, the above command will open up system's default browser and displays the web-based user interface.

## Development

* Setup public key authentication for Github:
  
  ```bash
  ssh-keygen -t ed25519 -C "ali.majdzadeh@gmail.com"
  ssh-agent bash -c 'ssh-add /root/.ssh/id_ed25519_gmail'
  ```

* Clone the repository:
  
  ```bash
  git clone git@github.com:majdzadeh/thales.git
  ```

* Activate the environment:
  
  ```bash
  pipenv shell
  ```

* Install the dependencies (one-off task):
  
  ```bash
  pip install streamlit
  pip install pandas_datareader
  ```

## Deployment

[Heroku](https://www.heroku.com/) is used for deployment.
