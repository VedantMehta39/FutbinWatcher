# FutbinWatcher
A Command Line Application to manage investments and create price alerts for particular players. Prices are sourced from www.futbin.com .

# SetUp:

## Investment Management
1)  I have provided the InvestmentManagement.txt file, keep it in the same directory as the .exe file, just edit it according to the format
2)  The file needs to be formatted in the following way: <playerurl> <costPrice> <playerQuantity> <console(ps,xbox,pc)> 

## Price Alerts
1)  To get the alert notifications, you need to download the IFTTT(IF This Then That) app on your device.
2)  Go to "My Applets" and press the "+" button to create a new applet.
3)  Press the "+" button next to "THEN" and add a webhook to it.
4)  Name the webhook (eg price_drop)
5)  Press the "+" button next to "THAT" and add notification(choose notification from the IFTTT app option not the rich notifications ) to     it.
6)  Copy Paste the following message to it "{{Value1}}'s lowest BIN is {{Value2}}"
7)  To use this service, you would also need to enter a key to my application. This key can be retrieved from the IFTTT application itself.
8)  To retrieve it, go to "My Applets" --> "Services" --> "Webhooks" --> "Settings"(Gear Icon) --> the key is the part after "/use/" in the     url
9)  When asked enter the name and the key into the FutbinWatcher application.
10) I have provided the PriceAlert.txt file, keep it in the same directory as the .exe file, just edit it according to the format
11) The file needs to be formatted in the following way: <playerurl> <console(ps,xbox,pc)> <targetPrice>
