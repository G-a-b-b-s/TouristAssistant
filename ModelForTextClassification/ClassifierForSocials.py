import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertModel


# Customized model with DistilBERT and additional layers
class DistillBERTClass(torch.nn.Module):
    def __init__(self):
        super(DistillBERTClass, self).__init__()
        self.l1 = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(768, 3)

    def forward(self, input_ids, attention_mask):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = output_1.last_hidden_state
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output
label_mapping = {
    'sports': 0,
    'culture': 1,
    'enterntainment': 2
}

class TestDataSet(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, index):
        text = str(self.data.text[index])
        text = " ".join(text.split())  # Clean and format text
        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',  # Updated argument
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        label = label_mapping[self.data.label[index]]  # Convert label to integer

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'targets': torch.tensor(label, dtype=torch.long)
        }

    def __len__(self):
        return self.len

# Check device compatibility
from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'

# Load dataset
data = pd.read_csv('combined.csv')

MAX_LEN = 512
TRAIN_BATCH_SIZE = 4
VALID_BATCH_SIZE = 2
EPOCHS = 3
LEARNING_RATE = 1e-05
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Split dataset
train_size = 0.8
train_dataset = data.sample(frac=train_size, random_state=200)
test_dataset = data.drop(train_dataset.index).reset_index(drop=True)
train_dataset = train_dataset.reset_index(drop=True)

# Create Dataset objects
training_set = TestDataSet(train_dataset, tokenizer, MAX_LEN)
testing_set = TestDataSet(test_dataset, tokenizer, MAX_LEN)

# DataLoader parameters
train_params = {'batch_size': TRAIN_BATCH_SIZE, 'shuffle': True, 'num_workers': 0}
test_params = {'batch_size': VALID_BATCH_SIZE, 'shuffle': True, 'num_workers': 0}

training_loader = DataLoader(training_set, **train_params)
testing_loader = DataLoader(testing_set, **test_params)

# Model setup
model = DistillBERTClass()
model.to(device)
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)


# Helper function to calculate accuracy
def calcuate_accu(big_idx, targets):
    n_correct = (big_idx == targets).sum().item()
    return n_correct


# Training function
def train(epoch):
    tr_loss = 0
    n_correct = 0
    nb_tr_steps = 0
    nb_tr_examples = 0
    model.train()
    for _, data_loaded in enumerate(training_loader, 0):
        ids = data_loaded['ids'].to(device, dtype=torch.long)
        mask = data_loaded['mask'].to(device, dtype=torch.long)
        targets = data_loaded['targets'].to(device, dtype=torch.long)

        outputs = model(ids, mask)
        loss = loss_function(outputs, targets)
        tr_loss += loss.item()
        big_val, big_idx = torch.max(outputs.data, dim=1)
        n_correct += calcuate_accu(big_idx, targets)

        nb_tr_steps += 1
        nb_tr_examples += targets.size(0)

        if _ % 100 == 0 and nb_tr_examples > 0:
            loss_step = tr_loss / nb_tr_steps
            accu_step = (n_correct * 100) / nb_tr_examples

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    epoch_accu = (n_correct * 100) / nb_tr_examples
    return


# Validation function
def valid(model, testing_loader):
    model.eval()
    n_correct = 0
    tr_loss = 0
    nb_tr_steps = 0
    nb_tr_examples = 0
    with torch.no_grad():
        for _, data in enumerate(testing_loader, 0):
            ids = data['ids'].to(device, dtype=torch.long)
            mask = data['mask'].to(device, dtype=torch.long)
            targets = data['targets'].to(device, dtype=torch.long)
            outputs = model(ids, mask)
            loss = loss_function(outputs, targets)
            tr_loss += loss.item()
            big_val, big_idx = torch.max(outputs.data, dim=1)
            n_correct += calcuate_accu(big_idx, targets)

            nb_tr_steps += 1
            nb_tr_examples += targets.size(0)

    epoch_accu = (n_correct * 100) / nb_tr_examples
    return epoch_accu


# Training loop
for epoch in range(EPOCHS):
    train(epoch)

# Validation
accuracy = valid(model, testing_loader)

save_directory="."
model_save_path = os.path.join(save_directory, 'classification_model.pth')
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")
