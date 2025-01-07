import os
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

class CustomDataset(Dataset):
    def __init__(self, data_dir, tokenizer, max_len):
        self.data = []
        self.labels = []
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.data_dir = data_dir
        self.load_data()

    def load_data(self):
        for label in label_mapping.keys():
            folder_path = os.path.join(self.data_dir, label)
            for filename in os.listdir(folder_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                        self.data.append(text)
                        self.labels.append(label_mapping[label])

    def __getitem__(self, index):
        text = str(self.data[index])
        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        label = self.labels[index]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'targets': torch.tensor(label, dtype=torch.long)
        }

    def __len__(self):
        return len(self.data)

# Check device compatibility
from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'

# Initialize tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Paths
data_dir = '/net/tscratch/people/plggabcza/RK/ModelForChatBotTalkClassification/trainingData'
model_save_path = '/net/tscratch/people/plggabcza/RK/ModelForChatBotTalkClassification/classification_model.pth'

full_dataset = CustomDataset(data_dir, tokenizer, max_len=512)
train_size = int(0.8 * len(full_dataset))
test_size = len(full_dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])

# DataLoader parameters
train_params = {'batch_size': 4, 'shuffle': True, 'num_workers': 0}
test_params = {'batch_size': 2, 'shuffle': True, 'num_workers': 0}

training_loader = DataLoader(train_dataset, **train_params)
testing_loader = DataLoader(test_dataset, **test_params)

# Model setup
model = DistillBERTClass()  # Your pre-defined model
model.to(device)
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=1e-5)

# Training function
def train(epoch):
    model.train()
    tr_loss = 0
    n_correct = 0
    nb_tr_steps = 0
    nb_tr_examples = 0
    for _, data_loaded in enumerate(training_loader, 0):
        ids = data_loaded['ids'].to(device, dtype=torch.long)
        mask = data_loaded['mask'].to(device, dtype=torch.long)
        targets = data_loaded['targets'].to(device, dtype=torch.long)

        outputs = model(ids, mask)
        loss = loss_function(outputs, targets)
        tr_loss += loss.item()

        big_val, big_idx = torch.max(outputs.data, dim=1)
        n_correct += (big_idx == targets).sum().item()

        nb_tr_steps += 1
        nb_tr_examples += targets.size(0)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    epoch_accu = (n_correct * 100) / nb_tr_examples
    print(f"Epoch {epoch}, Training Accuracy: {epoch_accu}%")

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
            n_correct += (big_idx == targets).sum().item()

            nb_tr_steps += 1
            nb_tr_examples += targets.size(0)

    epoch_accu = (n_correct * 100) / nb_tr_examples
    print(f"Validation Accuracy: {epoch_accu}%")
    return epoch_accu

# Training loop
EPOCHS = 20
for epoch in range(EPOCHS):
    train(epoch)

# Validation
accuracy = valid(model, testing_loader)

torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")