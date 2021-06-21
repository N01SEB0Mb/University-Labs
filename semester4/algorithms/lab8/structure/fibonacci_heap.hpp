#ifndef LAB8_FIBONACCI_HEAP_HPP
#define LAB8_FIBONACCI_HEAP_HPP

#define MAX 10e6
#define SPACES 6
#define SEPARATORS 32

#include <map>
#include <cmath>
#include <iostream>
#include <algorithm>


void print_separator(const std::string& text) {
    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl << text << std::endl;
}


namespace structures {

    template <class T>
    class FibonacciHeap;

    template <typename T>
    class Node {

        public:

            Node() {
                value = 0;

                parent = nullptr;
                child = nullptr;
                left = this;
                right = this;

                mark = false;
                degree = 0;
            }

            explicit Node(T new_value) {
                value = new_value;

                parent = nullptr;
                child = nullptr;
                left = this;
                right = this;

                mark = false;
                degree = 0;
            }

            ~Node() = default;

            friend FibonacciHeap<T>;

            void insertBetween(Node<T> *left, Node<T> *right) {
                left->right = right->left = this;

                this->right = right;
                this->left = left;
            }

            void extractBetween() {
                left->right = right;
                right->left = left;

                left = right = nullptr;
            }

            void clear(Node<T>* head) {
                if (this) {
                    if (child) {
                        child->clear(child);
                    }
                    if (left != head) {
                        left->clear(head);
                    }

                    delete this;
                }
            }

            void output(Node<T> *head, int depth) const {
                for (int space = 0; space < depth * SPACES; space++) {
                    std::cout << " ";
                }

                std::cout << value;
                std::cout << " (" << degree << ")";
                std::cout << " <" << mark << ">";
                std::cout << std::endl;

                if (child) {
                    child->output(child, depth + 1);
                }

                if (left != head) {
                    left->output(head, depth);
                }
            }

        private:
            T value;

            Node* parent;
            Node* left;
            Node* right;
            Node* child;

            bool mark{};
            int degree{};
    };

    template <typename T>
    class FibonacciHeap {

        public:

            FibonacciHeap() {
                min = nullptr;
                count_nodes = 0;
            }

            explicit FibonacciHeap(T value): FibonacciHeap() {
                min = new Node<T>(value);
            }

            ~FibonacciHeap() {
                if (min) {
                    min->clear(min);
                }
            }

            void output() const {
                print_separator("Number of nodes: " + std::to_string(count_nodes));

                if (min) {
                    std::cout << std::endl;

                    min->output(min, 0);
                }
            }

            void extractMin() {
                Node<T> *head = min;

                if (head) {
                    if (head->child) {
                        Node<T> *temp = head->child, *right_sibling;

                        do {
                            right_sibling = temp->right;

                            temp->parent = nullptr;

                            temp->extractBetween();
                            temp->insertBetween(min->left, min);

                            temp = right_sibling;
                        } while (temp->right != min);
                    }

                    if (head == head->right) {
                        min = nullptr;
                    }
                    else {
                        min = head->right;

                        head->extractBetween();
                        consolidate();
                    }

                    count_nodes--;
                }

                head->child = nullptr;
                head->clear(head);
            }

            void decreaseKey(Node<T> *node, T value) {
                if (value > node->value) {
                    return;
                }

                node->value = value;
                Node<T> *parent = node->parent;

                if (parent && node->value < parent->value) {
                    cut(node, parent);
                    cascadingCut(parent);
                }

                if (!min || node->value < min->value) {
                    min = node;
                }
            }

            void remove(Node<T> *node) {
                decreaseKey(node, -MAX);
                extractMin();
            }

            Node<T>* insert(Node<T> *node) {
                count_nodes++;

                if (!min) {
                    min = node;

                    return node;
                }

                if (min->left == min) {
                    min->left = node;
                    min->right = node;
                    node->right = min;
                    node->left = min;
                }
                else {
                    Node<T>* left_sibling = min->left;

                    left_sibling->right = node;
                    min->left = node;
                    node->right = min;
                    node->left = left_sibling;
                }

                if (node->value < min->value) {
                    min = node;
                }

                return node;
            }

            Node<T>* insert(T value) {
                auto node = new Node<T>(value);

                return insert(node);
            }

            bool isEmpty() {
                return min == nullptr;
            }

            Node<T>* getMin() {
                return min;
            }

        private:
            Node<T>* min;

            int count_nodes{};

            void cut(Node<T> *son, Node<T> *parent) {
                if (son == son->right) {
                    parent->child = nullptr;
                }
                else {
                    parent->child = son->right;
                }

                parent->degree--;

                son->parent = nullptr;
                son->extractBetween();
                son->insertBetween(min, min->right);
                son->mark = false;
            }

            void cascadingCut(Node<T> *node) {
                Node<T> *parent = node->parent;

                if (parent) {
                    if (node->mark) {
                        cut(node, parent);
                        cascadingCut(parent);
                    }
                    else {
                        node->mark = true;
                    }
                }
            }

            void consolidate() {
                int size = round(std::log(count_nodes)) + 2;
                auto array = new Node<T>*[size];

                for (int i = 0; i < size; i++) {
                    array[i] = nullptr;
                }

                std::map<Node<T>*, bool> dict;
                Node<T>* temp = min;
                Node<T>* right_sibling = nullptr;

                do {
                    dict[temp] = true;
                    right_sibling = temp->right;

                    Node<T> *x = temp;
                    int degree = x->degree;

                    while (array[degree] != nullptr) {
                        Node<T> *y = array[degree];

                        if (x->value > y->value) {
                            auto z = x;
                            x = y;
                            y = z;
                        }

                        link(y, x);

                        array[degree] = nullptr;
                        degree++;
                    }

                    array[degree] = x;
                    temp = right_sibling;
                } while (dict[temp] == false);

                for (int i = 0; i < size; i++) {
                    if (array[i] && min->value > array[i]->value) {
                        min = array[i];
                    }
                }
            }

            void link(Node<T> *lower, Node<T> *higher) {
                lower->extractBetween();

                if (!higher->child) {
                    higher->child = lower;
                    lower->right = lower->left = lower;
                }
                else {
                    lower->insertBetween(higher->child, higher->child->right);
                }

                lower->parent = higher;
                higher->degree++;
                lower->mark = false;
            }

            void connectHeaps(FibonacciHeap<T> *first, FibonacciHeap<T> *second) {
                if (first->min == nullptr && second->min == nullptr) {
                    return;
                }
                else if (first->min == nullptr) {
                    min = second->min;
                    count_nodes = second->count_nodes;

                    return;
                }
                else if (second->min == nullptr) {
                    min = first->min;
                    count_nodes = first->count_nodes;

                    return;
                }

                min = std::min(first->min, second->min);

                Node<T> *right_sibling_first = first->min->right;
                Node<T> *left_sibling_second = second->min->left;

                first->min->right = second->min;
                second->min->left = first->min;

                right_sibling_first->left = left_sibling_second;
                left_sibling_second->right = right_sibling_first;

                count_nodes = first->count_nodes + second->count_nodes;

                second->min = nullptr;
            }

    };

}  // namespace structures

#endif
