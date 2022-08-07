import imaplib
import getpass
from pick import pick
from progress.bar import Bar

def main(): 
  print("Simple program to remove all emails from a selected mailbox. If you want to leave the program, you can press CTRL+C at any time.")
  providers = ["Gmail", "Outlook"]
  title = "Please select the provider to remove emails from: "
  provider, index = pick(providers, title, indicator=">")

  if provider == "Gmail":
    imap = "imap.gmail.com"
  else: 
    imap = "outlook.office365.com"

  def login(): 
    email = input("Enter your email: ")

    print("The app password is not visible due to security reasons. Please enter it manually. See the README.md for more information.")
    password = getpass.getpass(prompt="Enter your app password: ")

    global box
    box = imaplib.IMAP4_SSL(imap)
    try: 
      box.login(email, password)
    except:
      print("Invalid email or password. Try again.")
      login()

  login()

  mailboxes = box.list()[1]
  for i in range(len(mailboxes)):
    decoded_mailbox = mailboxes[i].decode("utf-8").split(' "/" ')[1]
    mailboxes[i] = decoded_mailbox

  if provider == "Gmail":
    mailboxes.pop(1) # Remove the [Gmail] mailbox

  def select_mailbox():
    title = "Please select the mailbox to remove emails from: "
    global mailbox
    mailbox, index = pick(mailboxes, title, indicator=">")

    box.select(mailbox)
    typ, data = box.search(None, "ALL")
    global emails
    emails = data[0].split()

    global amount
    amount = len(emails)
    if amount == 0:
      print("There are no emails in this mailbox. Select another one.")
      select_mailbox()
    
    print(f"Amount of emails in {mailbox}: ", amount)

  select_mailbox()

  title = "Remove the emails instantly or move the emails to trash?"
  options = ["Remove Instantly", "Move to Trash"]
  remove_option, index = pick(options, title, indicator=">")

  def remove(): 
    bar = Bar('Removing', max=amount)

    if remove_option == "Remove Instantly":
      for email in emails:
        bar.next()
        box.store(email, "+FLAGS", "\\Deleted")
      box.expunge() # Removes the emails that are marked as Deleted
    else: 
      for email in emails:
        bar.next()
        box.store(email, "+X-GM-LABELS", "\\Trash")

    bar.finish()
    box.close()
    box.logout()

  if remove_option == "Remove Instantly":
    confirm_text = f"Are you sure you want to remove all emails from {mailbox}? (y/n) "
  else:
    confirm_text = f"Are you sure you want to move all emails from {mailbox} to trash? (y/n) "

  confirm = input(confirm_text)
  if confirm == "y":
    remove()
  else:
    print("Exiting...")
    exit()

if __name__ == "__main__":
  try: 
    main()
  except(KeyboardInterrupt): 
    print("\nExiting...")
    exit()