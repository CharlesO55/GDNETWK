from ollama import chat
print('Here')

res = chat(
    model='llava:7b',
    messages=[{
        'role' : 'user',
        'content' : 'Is there a dog in the image',
        'images' : ['./Client_submission.jpg']
    }]
)


print(res['message']['content'])
print('THere')
