#ifndef LAB7_BINOMIAL_HEAP_HPP
#define LAB7_BINOMIAL_HEAP_HPP

#define SPACES 2
#define SEPARATORS 32

#include <cmath>
#include <vector>
#include <iostream>


namespace structures {

    template <typename T>
    class BinomialHeap {

        public:

            BinomialHeap() {
                head = nullptr;
            }

            void insert(T& t) {
                Node* to_insert = new Node(t);
                this->head = connectHeap(to_insert, head);
            }

            T extractMin() {
                Node* extract_min = head;
                Node* temp = head;

                Node* prev = nullptr;
                Node* next = temp->neighbor;

                while (next) {
                    if (next->value < extract_min->value) {
                        prev = temp;
                        extract_min = next;
                    }

                    temp = next;
                    next = next->neighbor;
                }

                if (prev) {
                    prev->neighbor = extract_min->neighbor;
                }
                else {
                    head = extract_min->neighbor;
                }

                Node* second_head = extract_min->child;

                prev = nullptr;

                while (second_head) {
                    second_head->parent = nullptr;

                    next = second_head->neighbor;
                    second_head->neighbor = prev;

                    prev = second_head;
                    second_head = next;
                }

                second_head = prev;

                if (head || second_head) {
                    head = connectHeap(second_head, head);
                }

                return extract_min->value;
            }

            void decreaseKey(int index, T value) {
                Node* decrease_key = findNodeByIndex(head, index, 0);

                if (decrease_key->value <= value) {
                    return;
                }

                decrease_key->value = value;

                T temp = decrease_key->value;

                while (decrease_key->parent && decrease_key->parent->value > decrease_key->value) {
                    decrease_key->value = decrease_key->parent->value;
                    decrease_key->parent->value = temp;
                    decrease_key = decrease_key->parent;
                }
            }

            void erase(int index) {
                decreaseKey(index, INT_MIN);
                extractMin();
            }

            void output() {
                std::cout << std::endl;

                if (head) {
                    output(head, 0);
                }
                else {
                    std::cout << "<empty>" << std::endl;
                }
            }

        private:

            class Node {

                public:

                    T value;

                    Node* parent;
                    Node* neighbor;
                    Node* child;

                    int degree;

                    explicit Node(T& value) {
                        this->value = value;

                        parent = nullptr;
                        neighbor = nullptr;
                        child = nullptr;

                        degree = 0;
                    }
            };

            Node* head;

            Node* merge(Node* first, Node* second) {
                Node* res;

                if (lessEquals(first, second)) {
                    res = first;
                    first = first->neighbor;
                }
                else {
                    res = second;
                    second = second->neighbor;
                }

                Node* toReturn = res;

                while (first || second) {
                    if (lessEquals(first, second)) {
                        res->neighbor = first;
                        res = first;
                        first = first->neighbor;
                    }
                    else {
                        res->neighbor = second;
                        res = second;
                        second = second->neighbor;
                    }
                }

                return toReturn;
            }

            bool lessEquals(Node* a, Node* b) {
                if (!a || !b) {
                    return a;
                }

                return a->degree <= b->degree;
            }

            Node* connectHeap(Node* first, Node* second) {
                Node* connected_heap = merge(first, second);

                Node* prev = nullptr;
                Node* temp = connected_heap;
                Node* next = connected_heap->neighbor;

                while (next) {
                    if ((temp->degree != next->degree) || (next->neighbor && next->degree == next->neighbor->degree)) {
                        prev = temp;
                        temp = next;
                    }
                    else if (temp->value <= next->value) {
                        temp->neighbor = next->neighbor;
                        link(next, temp);
                    }
                    else {
                        if (prev == nullptr) {
                            connected_heap = next;
                        }
                        else {
                            prev->neighbor = next;
                        }

                        link(temp, next);
                        temp = next;
                    }

                    next = temp->neighbor;
                }

                return connected_heap;
            }

            void link(Node* high_root, Node* low_root) {
                high_root->parent = low_root;
                high_root->neighbor = low_root->child;

                low_root->child = high_root;
                low_root->degree++;
            }

            Node* findNodeByIndex(Node* current_node, int index, int current_pos) {
                if (current_pos == index) {
                    return current_node;
                }

                int pos = current_pos + std::pow(2, current_node->degree) - 1;

                if (pos <= index) {
                    if (!current_node->parent) {
                        return findNodeByIndex(current_node->neighbor, index,
                                               pos + 1);
                    }
                    else {
                        return findNodeByIndex(current_node->child, index,
                                               current_pos + std::pow(2, current_node->degree - 1));
                    }
                }
                else {
                    if (!current_node->parent) {
                        return findNodeByIndex(current_node->child, index,
                                               current_pos + std::pow(2, current_node->degree - 1));
                    }
                    else {
                        return findNodeByIndex(current_node->neighbor, index,
                                               current_pos - std::pow(2, current_node->degree - 1));
                    }
                }
            }

            void output(Node* node, int depth) {
                if (!node) {
                    return;
                }

                for (int space = 0; space < depth * SPACES; space++) {
                    std::cout << " ";
                }

                std::cout<< node->value;

                if (node->parent) {
                    std::cout << " [Parent=" << node->parent->value << "]";
                }

                std::cout << std::endl;

                output(node->child, depth + 1);
                output(node->neighbor, depth);
            }

    };

} // namespace structures

#endif
