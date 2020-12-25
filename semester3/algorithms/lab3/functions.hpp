#include <vector>

int n, d;
std::vector<int> heap;


void heapify(int node) {
	int maxP = node;
	int maxValue = heap[node];

	for (int k = 1; k <= d; k++) {
		int p = d * node + k;

		if (p >= n) {
			break;
		}

		if (heap[p] > maxValue) {
			maxValue = heap[p];
			maxP = p;
		}
	}

	if (maxP != node) {
		std::swap(heap[node], heap[maxP]);
		heapify(maxP);
	}
}


void buildHeap() {
	for (int i = n - 1; i >= 0; i--) {
		heapify(i);
	}
}


int extractMax() {
	int maxValue = heap[0];

	std::swap(heap[0], heap[n - 1]);
	heap.pop_back();
	n--;
	heapify(0);

	return maxValue;
}


void increaseKey(int i, int value) {
	if (i == 0) {
        heap[0] = value;
		return;
	}

	int p = (i - 1) / d;

	if (heap[p] < value) {
        heap[i] = heap[p];
		increaseKey(p, value);
	}
	else {
        heap[i] = value;
	}
}


void insert(int value) {
	n++;
	increaseKey(n - 1, value);
}


int height() {
    int power = 0;
    int number = 0;

    while (power < n) {
        power = (power + 1) * d;
        number++;
    }

    return number;
}


void writeHeap() {
    for (int node: heap) {
        std::cout << node << " ";
    }

	std::cout << std::endl;
}
