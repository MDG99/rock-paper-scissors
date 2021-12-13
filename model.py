from datetime import datetime
import torchvision
import torch.utils.data
from torch import nn
from torchvision import models
from torchvision import transforms
from dataset import get_dataset

device = torch.device('cpu')
classes = 5

#Cargamos los datos
root_images = 'dataset/'
file = 'game.csv'
batch_size = 10

transform = transforms.Compose([
    transforms.Resize((227, 227)), #Cambiamos el tamaño al que recibe el AlexNet
    transforms.ToTensor(), #Lo pasamos a Tensor
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) #Normalizamos
])

dataset = get_dataset(csv_file=file, root=root_images, transform=transform)

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_dataloader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
test_dataloader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True, num_workers=2)

#Definimos el modelo a usar
alexnet = models.alexnet(pretrained=True)
alexnet.classifier[6] = nn.Linear(4096, classes)

#Hiperparámetros
lr = 0.01
epochs = 30
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(alexnet.parameters(), lr)

for epoch in range(epochs):
    epoch_loss = 0

    for i, data in enumerate(train_dataloader, 0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)

        #Forward step
        optimizer.zero_grad()
        outputs = alexnet(inputs)
        loss = loss_fn(outputs, labels)
        loss.backward()
        epoch_loss += loss.item()

        print(f'Época: {epoch + 1} Loss: {epoch_loss}')

print("Entrenamiento terminado")
now = datetime.now()
dt_str = now.strftime("%Y%m%d_%H%M%S")
torch.save(alexnet, f"Modelo_{dt_str}.pt")