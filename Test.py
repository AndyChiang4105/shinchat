from soVITS_api import getVitsResponse

text = '曹操的勢力不及元紹'
output_bytesIO = getVitsResponse(text)
with open('output.wav', "wb") as f:
    f.write(output_bytesIO.read())