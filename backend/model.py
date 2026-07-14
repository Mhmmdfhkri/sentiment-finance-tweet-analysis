import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

MODEL_NAME = 'bert-base-uncased'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BERT_Arch(nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert = bert
        self.dropout = nn.Dropout(0.1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768, 512)
        self.fc2 = nn.Linear(512, 3) # Output 3 kelas (0: Bearish, 1: Bullish, 2: Neutral)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        outputs = self.bert(sent_id, attention_mask=mask)
        cls_hs = outputs[1] # CLS token representation
        
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

def get_bert_prediction_tools(model_path):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    bert_base = AutoModel.from_pretrained(MODEL_NAME)
    
    model = BERT_Arch(bert_base)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))
    model = model.to(device)
    model.eval()
    
    return tokenizer, model