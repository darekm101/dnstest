# dnstest
Simple script which tests DNS config and reports stats

To get it locally run this... 
`git clone https://github.com/darekm101/dnstest.git`

Once you downloaded it, let's setup the dependencies. 

`cd dnstest`
`python3.6 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

#Run the test... 

Once installed, you can run it as: 
`python dnstest.py`


```(venv) [dmarkiew@katestats-db01 dnstest]$ python dnstest.py 
usage: dnstest.py [-h] [--net NET] [--debug DEBUG]

optional arguments:
  -h, --help     show this help message and exit
  --net NET      Provide class C subnet to reverse lookup i.e. --net
                 '10.10.10.0'
  --debug DEBUG  Turn on debugging. i.e. --debug True```
