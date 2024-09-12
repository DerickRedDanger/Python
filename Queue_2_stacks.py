class queue_2s():
    def __init__(self, queue=None):
        """
        A queue made by using two stacks.

        A queue can be computationally costly as the list increase in size. This happens because
        poping a element that isn't the last from a list, forces python to reorganize the whole list,
        moving the elements after that element foward.

        That's why I am using two stacks instead. we will keep appending elements to the first stack, keeping them in order.
        But when we need to dequeue elements, if S2 is already empty, we will pop elements from the first list and append them in the second list,
        So that the first element in the first list become the last in the second one, allowing us to simply pop them in order.
        If s2 is not empty, then we can just continue to pop it's last element, only adding elements from S1 when it's empty again.
        """
        self.s1 = []
        self.s2 = []

        # if queue already exist, appens it's elements to S1, one at time
        # this is done to make sure S1 is still a list.
        # it might not be true if we did s1 = queue.

        if queue:
            for element in queue:
                self.s1.append(element)

    def enqueue(self, item):
        self.s1.append(item)

    def dequeue(self):

        # if both S1 and S2 are empty
        if not self.s1 and not self.s2:
            raise QueueEmptyError("Queue is empty")

        # If S2 is empty, but S1 isn't
        elif not self.s2 and self.s1:
            for _ in range(len(self.s1)):
                self.s2.append(self.s1.pop())

        return self.s2.pop()

    def check(self):
        # Return the number of elements in the queue
        return len(self.s1) + len(self.s2)

class QueueEmptyError(Exception):
    def __init__(self, message="Queue is empty"):
        super().__init__(message)