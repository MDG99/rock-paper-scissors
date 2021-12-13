from datetime import datetime
import torchvision
import torch.utils.data
from torch import nn
from torchvision import models
from torchvision import transforms
from dataset import get_dataset
import numpy as np
import matplotlib.pyplot as plt


def fit():
    device = torch.device('cpu')
    classes = 5

    # Cargamos los datos
    root_images = 'dataset/'
    file = 'game.csv'
    batch_size = 10

    transform = transforms.Compose([
        transforms.Resize((227, 227)),  # Cambiamos el tamaño al que recibe el AlexNet
        transforms.ToTensor(),  # Lo pasamos a Tensor
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalizamos
    ])

    dataset = get_dataset(csv_file=file, root=root_images, transform=transform)

    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    train_dataloader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True,
                                                   num_workers=1)
    test_dataloader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True,
                                                  num_workers=1)

    # Definimos el modelo a usar
    alexnet = models.alexnet(pretrained=True)
    alexnet.classifier[6] = nn.Linear(4096, classes)

    # Hiperparámetros
    lr = 0.01
    epochs = 30
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(alexnet.parameters(), lr)


    for epoch in range(epochs):
        epoch_loss = 0

        for data, label in train_dataloader:
            inputs, labels = data, label
            inputs, labels = inputs.to(device), labels.to(device)

            # Forward step
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

    return test_dataloader


def evaluate(val_loader, batch):
    classes = ['Empezar', 'Terminar', 'Piedra', 'Papel', 'Tijera']
    file = '.pt'
    PATH = 'dataset/'

    # Evaluando la red neuronal
    dataiter = iter(val_loader)
    images, labels = dataiter.__next__()

    def imshow(img):
        img = img / 2.0 + 0.5
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    imshow(torchvision.utils.make_grid(images))
    print("Ground truth: ", " ".join('%s' % classes[labels[j]] for j in range(batch)))

    my_net = torch.load(PATH + file)

    outputs = my_net(images)
    _, predicted = torch.max(outputs, 1)
    print("Predicted: ", " ".join('%s' % classes[predicted[j]] for j in range(batch)))

    # Performance
    correct = 0
    total = 0
    with torch.no_grad():
        for data in val_loader:
            images, labels = data
            outputs = my_net(images)
            _, predicted = torch.max(outputs.data, 1)
            total = labels.size(0)
            correct = torch.eq(predicted, labels).sum()

    print('Accuracy of the network: %0.2f %%' % (100 * correct / total))

    class_correct = list(0. for i in range(5))
    class_total = list(0. for i in range(5))

    with torch.no_grad():
        for data in val_loader:
            images, labels = data
            outputs = my_net(images)
            _, predicted = torch.max(outputs, 1)
            c = np.squeeze((predicted == labels))
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    for i in range(5):
        print('Accuracy of %5s : %0.2f %%' % (
            classes[i], 100 * class_correct[i] / class_total[i]))




test_dataloader = fit()
#evaluate(test_dataloader, 10)
