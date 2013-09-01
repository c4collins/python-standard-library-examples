## 14.5 getpass Secure Password Prompt
# Many programs that interact with the user via the terminal need to ask the user for password values 
# without showing what the user types on the screen.  getpass provides a portable way to securely handle password prompts.
import getpass, sys

## 14.5.1 Example
# The getpass() function prints a prompt and then reads input from the user until return is pressed
# The input is returned as a string to the caller

try:
    p = getpass.getpass()
except Exception, err:
    print 'Error:', err
else:
    print 'You entered:', p

# The prompt can be altered
p = getpass.getpass(prompt="Who's a good kitty?")
if p.lower() == 'meow':
    print "Yes you are!"
else:
    print "No, absolutely not"

# By default, getpass() used sys.stdout to print the prompt string.
# For a program that may produce useful output on sys.stdout it's better to used another stream, like sys.stderr
p = getpass.getpass(stream=sys.stderr)
print 'You entered:', p

## 14.5.2 Using getpass without a terminal
# Under UNIX, getpass always requires a tty
# python 2.6 and 2.7 try wehn redirecting sys.stdin, but it's still not very useful outside the cli