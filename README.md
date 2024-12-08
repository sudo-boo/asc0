# asc0

This project is just to pass the time in Winters... I'm doing this project just because I can... 

Reverse Engineering ASC is not a horrendous task. Also, ASC being shit as f*** doesn't have any firewall or rate limiter, except for the SSO landing page, which is asked for non-IITB network users.  

## Setup

**Step 0:** Make sure you are connected to the IITB Network or use [OpenVPN](https://www.cc.iitb.ac.in/page/services-vpnssh), or you'll be bombarded with SSO Landing page captchas. You can dare if you're feeling lucky...

**Step 1:** Clone the repository onto your local machine, and install the dependencies.
```bash
git clone https://github.com/sudo-boo/asc0.git
cd asc0
pip install -r requirements.txt
```



**Step 2:** Run the `setup.py` script to configure your environment:

```bash
python setup.py [--user | --sender | --clean]
```

**Available options:**

- `--user`: Creates a `.env` file locally containing your login info for ASC.
- `--sender`: Creates a `.sender` file locally containing the sender email and login password.
- `--clean`: Cleans up any previously stored configurations or user data.


> [!IMPORTANT]   
> This does not share your credentials anywhere except your local machine. So, you're cool.!


**Step 3:** Run the `main.py` script.
```bash
python main.py
```
This creates various output directories, scrapes the ASC webpage, generates `logs`, and periodically sends emails on your mentioned email about the updates. 


### And yepp... That's it...!!
