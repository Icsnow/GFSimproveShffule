
from collections import deque

def DR_max_Search(shuffle):
    border_round = len(shuffle)
    max_round = -1

    for i in range(border_round):
        queue = deque([i])
        diffuse_round = 1
        temp_queue = deque()

        while len(queue) < border_round and diffuse_round < border_round:
            while queue:
                node = queue.popleft()
                if node % 2 == 0 and node+1 not in queue:
                    queue.append(node+1)
                temp_queue.append(shuffle[node])

            while temp_queue:
                queue.append(temp_queue.popleft())

            diffuse_round += 1

        max_round = max(max_round, diffuse_round)
    return max_round



if __name__ == '__main__':
    # the shuffles in 2010-FSE-[Improving the Generalized Feistel]
    A = [[9,0,1,2,3,4,5,6,7,8], [2,0,4,1,6,3,8,5,9,7], [5,0,7,2,9,6,3,8,1,4], [3,0,1,4,7,2,5,8,9,6], [3,0,7,4,1,6,5,8,9,2]]
    B = [[7,0,1,2,3,4,5,6], [2,0,4,1,6,3,7,5], [3,0,1,4,7,2,5,6], [3,0,7,4,5,6,1,2]]
    C = [[15,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14], [2,0,4,1,6,3,8,5,10,7,12,9,14,11,15,13], [1,2,9,4,15,6,5,8,13,10,7,14,11,12,3,0],
         [1,2,11,4,9,6,7,8,15,12,5,10,3,0,13,14], [1,2,11,4,9,6,15,8,5,12,7,10,3,0,13,14]]
    for a in A+B+C:
        print(DR_max_Search(a))
