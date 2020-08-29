# networking

In this project of mine I have created a program where you can chat anonymously with each other. 
For my program to work you first have to start the mainserver.py. This creates the server, that will manage all the message traffic. You only need one mainserver.py to run for the program to work. For the rest of the program you just need to start the clientgui.py, and connect to a channel, and youll be able to chat on the channel.

Anonymity was the main focus of this program. This doesnt only mean that you cant assign a username or a profile picture to your "account". But it also means that messages are not saved to your account. Every sent message isnt stored anywhere (only temporarily on your RAM). This means that once you turn off the program, all your message history will be gone. 

Another feature I want to add in the feature is end to end encryption. So all messages will be encrypted and it would be hard to perform a man in the middle attack to capture sent and received messages.

Another property this program has, is that there is complete anarchy. There isnt a user with the rights to kick people off the channels. 

To get into a channel you will have to give a channelcode for the channel you want to enter. A channelcode should consist only of numbers, and can be as long as you want it to be. This means if you want to speak with someone in private, you should consider choosing a very long channelcode no other user could guess. Thats another thing, all channels are public, so if someone knows your channelcode, he will be able to enter the channel at any time he wants. A message will be displayed to all users, when someone new entered a channel.
