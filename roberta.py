from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import torch

tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')

def get_emotion(text):
    output=model(torch.tensor([tokenizer.encode(text)]))
    probs = torch.nn.functional.softmax(output.logits,dim=-1)

    # 獲取正負向情緒
    negative_prob, positive_prob = probs[0].detach().numpy()

    if positive_prob > negative_prob:
        return "positive"
    else:
        return "negative"

a = get_emotion('和朋友們一起度過了一個美好的下午。')
print(a)