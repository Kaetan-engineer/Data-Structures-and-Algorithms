from typing import Any

from LinkedList.Linked_list import LinkedList


class Queue:
    def __init__(self) -> None:
        self.data = LinkedList()

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return 'Front -> ' + ' -> '.join([str(i) for i in self.data]) + ' <- Rear'

    def __iter__(self):
        yield from self.data.__iter__()

    def enqueue(self, value: Any) -> None:
        self.data.append(value)

    def dequeue(self) -> Any:
        return self.data.remove(0)

    def peek(self) -> Any:
        return self.data[0]

    @property
    def is_empty(self) -> bool:
        return len(self.data) == 0


def main():
    q = Queue()
    values = ['A', 'B', 'C', 'D']

    for v in values:
        q.enqueue(v)

    for v in q:
        print(v)


if __name__ == "__main__":
    main()
