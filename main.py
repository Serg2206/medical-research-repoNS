# Импорт необходимых библиотек
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# Определение архитектуры модели


class MedicalNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MedicalNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(F.relu(self.fc2(x)))
        x = self.fc3(x)
        return x

# Функция для обучения модели


def train_model(
        data,
        labels,
        input_size,
        hidden_size,
        output_size,
        epochs=20,
        batch_size=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Создание датасета и загрузчика данных
    dataset = TensorDataset(
        torch.tensor(
            data, dtype=torch.float32), torch.tensor(
            labels, dtype=torch.long))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Инициализация модели
    model = MedicalNet(input_size, hidden_size, output_size).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()

    # Обучение модели
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

    # Сохранение модели
    torch.save(model.state_dict(), "medical_net.pth")
    print("Модель сохранена как 'medical_net.pth'")

# Функция для прогнозирования


def predict(
        data,
        input_size,
        hidden_size,
        output_size,
        model_path="medical_net.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Загрузка модели
    model = MedicalNet(input_size, hidden_size, output_size)
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    model.eval()

    # Прогноз
    data = torch.tensor(data, dtype=torch.float32).to(device)
    with torch.no_grad():
        outputs = model(data)
        predictions = torch.argmax(outputs, dim=1)
    return predictions.cpu().numpy()

# Основной код


def main():
    # Пример данных
    data = np.random.rand(100, 10)  # 100 образцов, 10 признаков
    labels = np.random.randint(0, 2, size=(100,))  # 2 класса

    input_size = 10
    hidden_size = 32
    output_size = 2

    # Обучение
    train_model(data, labels, input_size, hidden_size, output_size)

    # Прогнозирование
    test_data = np.random.rand(5, 10)  # 5 новых образцов
    predictions = predict(test_data, input_size, hidden_size, output_size)
    print("Predictions:", predictions)


if __name__ == "__main__":
    main()
