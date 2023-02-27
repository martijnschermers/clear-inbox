# Clear Inbox
Simple CLI program that makes it possible to remove all the emails in a certain inbox. 
Currently Gmail and Outlook are supported.

## Important Note
Use this script at your own risk! I'm in no way liable for any direct, indirect, incidental, special, exemplary, or consequential damages,
arising in any way out of the use of this script, even if advised of the possibility of such damage.

## Run Locally
Tested on Ubuntu and Windows.

Clone the project

```bash
  git clone https://github.com/martijnschermers/remove-email.git
```

Go to the project directory

```bash
  cd remove-email
```

Install dependencies

```bash
  pip install pick progress
```

Run the program (Windows)

```bash
  python main.py
```

Run the program (Ubuntu)

```bash
  python3 main.py
```

## App Passwords
It is possible to remove emails from Gmail and from Outlook. 
For both providers it is neccesary to create an app password to access your account. 
Links to help on how to generate these passwords: 
- [Gmail](https://support.google.com/accounts/answer/185833)
- [Outlook](https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944)
