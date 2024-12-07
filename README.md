# asc0

This project is just to pass the time in Winters... I'm doing this project just because I can... 

Reverse Engineering ASC is not a horrendous task. Also, ASC being old as f*** doesn't have any firewall or rate limiter, except for the SSO landing page, which asks for non-IITB network users.  

## Setup

**Step 0:** Make sure you are connected to the IITB Network or use [OpenVPN](https://www.cc.iitb.ac.in/page/services-vpnssh), or you'll be bombarded with SSO Landing page captchas. You can dare if you're feeling lucky...

**Step 1:** Clone the repository onto your local machine.
```bash
git clone https://github.com/sudo-boo/asc0.git
cd asc0
```


**Step 2:** Run
```bash
python setup.py
```
This creates a `.env` file with your login credentials for ASC.

> [!IMPORTANT]   
> This does not share your credentials anywhere except your local machine. So, you're cool.!

**Step 3:** Run the main script.
```bash
python main.py
```
This creates various output directories, scrapes the ASC webpage, generates `logs`, and periodically sends emails on your mentioned email about the updates. 

### Yepp... That's it...!!
