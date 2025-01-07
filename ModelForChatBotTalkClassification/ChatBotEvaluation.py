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



# Model Tester Class
class ModelTester:
    def __init__(self, model_path, tokenizer, label_mapping, device='cpu'):
        self.model = DistillBERTClass()
        self.model.load_state_dict(torch.load(model_path))
        self.model.to(device)
        self.model.eval()

        self.tokenizer = tokenizer
        self.reverse_label_mapping = {v: k for k, v in label_mapping.items()}
        self.device = device

    def test_and_print_results(self, testing_loader):
        correct = 0
        total = 0

        with torch.no_grad():
            for idx, data in enumerate(testing_loader, 0):
                ids = data['ids'].to(self.device, dtype=torch.long)
                mask = data['mask'].to(self.device, dtype=torch.long)
                targets = data['targets'].to(self.device, dtype=torch.long)

                # Get model predictions
                outputs = self.model(ids, mask)
                _, predicted = torch.max(outputs.data, dim=1)

                # Convert prediction and target to labels
                predicted_label = self.reverse_label_mapping[predicted.item()]
                true_label = self.reverse_label_mapping[targets.item()]

                # Decode the input text
                input_text = self.tokenizer.decode(ids[0], skip_special_tokens=True)

                # Check if prediction is correct
                is_correct = predicted.item() == targets.item()
                status = "Correct :) " if is_correct else "Wrong :("

                # Print the results
                print(f"Text: {input_text}")
                print(f"Predicted Label: {predicted_label}")
                print(f"True Label: {true_label}")
                print(f"Result: {status}")
                print("-" * 50)

                total += 1
                correct += is_correct

        # Print overall accuracy
        accuracy = (correct / total) * 100
        print(f"\nOverall Testing Accuracy: {accuracy:.2f}%")

# Paths and Setup
data_dir = '/net/tscratch/people/plggabcza/RK/ModelForChatBotTalkClassification/testingData'
model_save_path = '/net/tscratch/people/plggabcza/RK/ModelForChatBotTalkClassification/classification_model.pth'

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Load dataset
test_dataset = CustomDataset(data_dir, tokenizer, max_len=512)

# Create DataLoader
test_params = {'batch_size': 1, 'shuffle': False, 'num_workers': 0}
testing_loader = DataLoader(test_dataset, **test_params)

# Initialize ModelTester and run tests
tester = ModelTester(model_save_path, tokenizer, label_mapping, device=device)
tester.test_and_print_results(testing_loader)