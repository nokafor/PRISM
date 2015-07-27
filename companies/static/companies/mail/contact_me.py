import sendgrid

sg = sendgrid.SendGridClient('princetonism', 'PRISMfounder16')

message = sendgrid.Mail()
message.add_to('nokafor@princeton.edu')
message.set_subject('Example')
message.set_text('Body')
message.set_from('sokafor15@gmail.com')
status, msg = sg.send(message)

return True