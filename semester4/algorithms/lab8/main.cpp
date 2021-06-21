#include "structure/fibonacci_heap.hpp"


int main() {
    structures::FibonacciHeap<int> fib_heap;
    structures::Node<int> *temp;

    structures::Node<int> *test_node_1;
    structures::Node<int> *test_node_2;
    structures::Node<int> *test_node_3;
    structures::Node<int> *test_node_4;

    // Inserting nodes x20

    print_separator("Inserting 20 nodes");

    for (int value = 0; value < 20; value++) {
        temp = fib_heap.insert(value + 1);

        // Save test nodes
        switch (value) {
            case 8:
                test_node_1 = temp;
                break;

            case 11:
                test_node_2 = temp;
                break;

            case 13:
                test_node_3 = temp;
                break;

            case 19:
                test_node_4 = temp;
                break;

            default:
                break;
        }
    }

    fib_heap.output();

    // Extract min x8

    print_separator("Extracting min 8 times");

    for (int value = 0; value < 8; ++value){
        fib_heap.extractMin();
        fib_heap.output();
    }

    // Decrease x3

    print_separator("Decrease (9 -> 1)");
    fib_heap.decreaseKey(test_node_1, 1);
    fib_heap.output();

    print_separator("Decrease (12 -> 0)");
    fib_heap.decreaseKey(test_node_2, 0);
    fib_heap.output();

    print_separator("Decrease (17 -> -1)");
    fib_heap.decreaseKey(test_node_3, -1);
    fib_heap.output();

    // Delete

    print_separator("Delete (20)");
    fib_heap.remove(test_node_4);
    fib_heap.output();

    // Extract min

    print_separator("Extracting min");
    fib_heap.extractMin();
    fib_heap.output();

    return 0;
}
