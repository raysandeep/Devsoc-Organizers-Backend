from pyfcm import FCMNotification


        
# OR initialize with proxies

push_service = FCMNotification(api_key="AIzaSyD8v3e4a3v-rcasU3Mh0KKkPaflm1dW1J4")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = ['ewcRwkjhMAs:APA91bGbJpD9CAS5ido1d_zLrmFlT7D__1GrkDCNYc8Cc4oFZsJyUmHJ7DGbToHkPXFKDr0EYR8HPZnS_FCuy9hu_f1GUTpTKQYOPN9r2w8gdZq33tXjyD0JwlG8L8h-EQnH7I-S1OeW']

message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id[0], message_title=message_title, message_body=message_body)
print(result)