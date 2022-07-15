import re

data = '24/06/2022 8:39 da manhã - +92 314 6971403: Anybody can tell me the easiest way to learn english'
#data = '26/02/2022 6:52 da tarde - Arruda adicionou +55 51 9835-1013'
#data = ''
#data = '21/09/2021 5:51 - +55 51 9135-5256: o SGM esta com problemas?'
#data = '21/09/2021, 5:51 - +55 51 9135-5256: o SGM esta com problemas?'
#pat = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#pat = '\d{1,2}/\d{1,2}/\d{2,4}\s\d{1,2}:\d{2}\s\w{2}\s\w{3,5}\s-\s'
#comma = re.sub ('\d{1,2}:\d{2}\s','\d{1,2):\d{2},\s',data)
comma = re.sub('\s',', ',data,count=1)
clear = re.sub ('\w{2}\s\w{5}\s','',comma,count=1)
pat = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

result = re.search(pat, clear)
messages = re.split(pat, clear)[1:]
dates = re.findall(pat, clear)
users = []
messages = []
entry = re.split('([\w\W]+?):\s', clear)
if entry[1:]:
    users.append(entry[1])
    messages.append(entry[2])
else:
    users.append('Group Notification')
    messages.append(entry[0])

print ( '#####################################################')
print ('Entrada : ',entry)
print ( '#####################################################')
print ('Usuarios : ', users)
print ('Menssagem: ',messages)
print ( '#####################################################')
print ('Original : ',data)
print ( '------------------')
print ('Padrao : ',result)
print ( '------------------')
print ('Limpo : ', clear)
print ( '------------------')
print ('C : ', comma)
print ( '------------------')
print ('Mensagem : ',messages)
print ( '------------------')
print ('Data : ',dates)
print ( '------------------')



# pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
##pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{1.2}\s\w[3,5]\s-\s'




#data = '20/09/2021 8:32 da noite - +55 51 8216-7367: Amanha eu vou ai'
#pat = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\W{2}\s\W{3,5}\s-\s'
#pat = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'