from typing import Any


class DynamicArray:
    def __init__(self) -> None:
        self.data: list[Any] = [None] * 4
        self.size: int = 0
        self.capacity: int = 4

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def _resize(self) -> None:
        new_array = [None] * (self.capacity * 2)
        self.capacity *= 2

        for i in range(self.size):
            new_array[i] = self.data[i]

        self.data = new_array

    def get(self, index: int) -> Any:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        if self.size == 0:
            raise IndexError('Cannot access element in empty list')

        return self.data[index]

    def append(self, value: Any) -> None:
        if self.size == self.capacity:
            self._resize()

        self.data[self.size] = value
        self.size += 1

    def insert(self, index: int, value: Any) -> None:
        if index < 0 or index > self.size:
            raise IndexError('Index is out of range')

        if self.size == self.capacity:
            self._resize()

        for i in range(self.size-1, index-1, -1):
            self.data[i+1] = self.data[i]

        self.data[index] = value
        self.size += 1

    def remove(self, index: int) -> Any:
        if index < 0 or index >= self.size:
            raise IndexError('Index out of range')

        for i in range(index + 1, self.size):
            self.data[i-1] = self.data[i]

        removed_data = self.data[self.size-1]
        self.data[self.size-1] = None
        self.size -= 1
        return removed_data

if __name__ == '__main__':
    arr = DynamicArray()

    arr.append(10)
    arr.append(20)
    arr.append(30)
    arr.append(True)
    arr.insert(2, 50)
    arr.remove(1)

    print(arr.get(1))
    print(arr.data)
