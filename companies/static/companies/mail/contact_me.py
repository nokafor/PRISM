import sendgrid

def index(request):
	postData = request.form
	email = str(postData['email'].value)

	sg = sendgrid.SendGridClient('princetonism', 'PRISMfounder16')

	message = sendgrid.Mail()
	message.add_to('nokafor@princeton.edu')
	message.set_subject('Example')
	message.set_text('Body')
	message.set_from(email)
	status, msg = sg.send(message)
