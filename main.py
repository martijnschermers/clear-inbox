import imaplib
import getpass
from pick import pick

def main(): 
  providers = ["Gmail", "Outlook"]
  title = "Please select the provider to remove emails from: "
  provider, index = pick(providers, title, indicator=">")

  print("Simple program to remove all emails from a selected mailbox. If you want to leave the program, you can press CTRL+C at any time.")
  email = input("Enter your email: ")

  print("The password is not visible due to security reasons. Please enter it manually. See the README.md for more information.")
  password = getpass.getpass(prompt="Enter your app password: ")

  imap = ""
  if provider == "Gmail":
    imap = "imap.gmail.com"
  else: 
    imap = "outlook.office365.com"

  box = imaplib.IMAP4_SSL(imap)
  try: 
    box.login(email, password)
  except:
    print("Invalid email or password.")
    exit()

  mailboxes = box.list()[1]
  for i in range(len(mailboxes)):
    mailbox = mailboxes[i].decode("utf-8").split(' "/" ')[1]
    mailboxes[i] = mailbox

  if provider == "Gmail":
    mailboxes.pop(1) # Remove the [Gmail] mailbox

  title = "Please select the mailbox to remove emails from: "
  mailbox, index = pick(mailboxes, title, indicator=">")

  box.select(mailbox)
  typ, data = box.search(None, "ALL")
  emails = data[0].split()

  amount = len(emails)
  print(f"Amount of emails in {mailbox}: ", amount)

  title = "Remove the emails instantly or move the emails to trash?"
  options = ["Remove Instantly", "Move to Trash"]
  remove_option, index = pick(options, title, indicator=">")

  def remove(): 
    if remove_option == "Remove Instantly":
      for email in emails:
        box.store(email, "+FLAGS", "\\Deleted")
      box.expunge() # Removes the emails that are marked as Deleted
      print("Emails removed.")
    else: 
      for email in emails:
        box.store(email, "+X-GM-LABELS", "\\Trash")  
      print("Emails moved to trash.")

    box.close()
    box.logout()

  confirm_text = ""
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
    print("Exiting...")
    exit()