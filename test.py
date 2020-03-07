from pyfcm import FCMNotification


        
# OR initialize with proxies

push_service = FCMNotification(api_key="AIzaSyD8v3e4a3v-rcasU3Mh0KKkPaflm1dW1J4")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = ['eUFJY9T5bu4:APA91bHyxcISobHhemQwuNfqFSEHtd_RhKfUU0C1ObOF2G08nSKiakclua1VjsGku33xBtoGgSD8GmtW7TJgUMH8KjofRcCFUUFYwf-ok6kY1A4cZdGqUqi_3ym_rw7axjRFyMVEmOf-']

message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
print
result = push_service.notify_single_device(registration_id=registration_id[0], message_title=message_title, message_body=message_body)
print(result)