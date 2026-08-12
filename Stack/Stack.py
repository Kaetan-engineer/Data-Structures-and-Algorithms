from typing import Any
from Array.DynamicArray import DynamicArray


class Stack:
    def __init__(self) -> None:
        self.data: DynamicArray = DynamicArray()

    def __len__(self) -> int:
        return self.data.size

    def __str__(self) -> str:
        return 'Top\n|\n' + '\n'.join([str(i) for i in self.data.data])

    @property
    def is_empty(self) -> bool:
        return len(self) < 0

    def pop(self) -> Any:
        return self.data.remove(len(self) - 1)

    def push(self, value: Any) -> None:
        self.data.append(value)

    def peek(self) -> Any:
        return self.data[len(self) - 1]


S = Stack()
values = [10, 20, 30, 40, 50]

for v in values:
    S.push(v)

print(S)
